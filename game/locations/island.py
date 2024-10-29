####################################################################################################
# Imports
####################################################################################################

from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random

####################################################################################################
# Events and supporting classes
####################################################################################################

#########################
# Zombie marooned pirates
#########################

class Maroonee(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(35,51), (5,15)]
        attacks["punch 1"] = ["punches",random.randrange(35,51), (1,10)]
        attacks["punch 2"] = ["punches",random.randrange(35,51), (1,10)]
        #7 to 19 hp, bite attack, 65 to 85 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 75 + random.randrange(-10,11))
        self.type_name = "Mummified Maroonee"

class ShorePirates (event.Event):
    petemade = False
    '''
    A combat encounter with a crew of marooned pirate zombies.
    When the event is drawn, creates a combat encounter with 2 to 6 marooned pirates, kicks control over to the combat code to resolve the fight, then adds itself and a simple success message to the result
    '''

    def __init__ (self):
        self.name = " marooned pirate attack"

    def process (self, world):
        '''Process the event. Populates a combat with Maroonee monsters. The first Maroonee may be modified into a "Pirate captain" by buffing its speed and health.'''
        result = {}
        result["message"] = "the marooned pirates are defeated!"
        monsters = []
        min = 2
        uplim = 6
        if not ShorePirates.petemade:
            ShorePirates.petemade = True
            min = 1
            uplim = 5
            monsters.append(Maroonee("Partially-eaten Pete"))
            self.type_name = "Partially-eaten Pete"
            monsters[0].health = 3*monsters[0].health
        elif random.randrange(2) == 0:
            min = 1
            uplim = 5
            monsters.append(Maroonee("Pirate captain"))
            self.type_name = "Marooned Pirate Captain"
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(Maroonee("Mumified maroonee "+str(n)))
            n += 1
        display.announce ("You are attacked by a crew of marooned pirates!")
        combat.Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result

#########################
# Man-eating macaques
#########################

class Macaque(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        #7 to 19 hp, bite attack, 160 to 200 speed (100 is "normal")
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))
        self.type_name = "Man-eating Macacque"


class ManEatingMonkeys (event.Event):
    '''
    A combat encounter with a troop of man eating monkies.
    When the event is drawn, creates a combat encounter with 4 to 8 monkies, kicks control over to the combat code to resolve the fight.
    The monkies are "edible", which is modeled by increasing the ship's food by 5 per monkey appearing and adding an apropriate message to the result.
        Since food is good, the event only has a 50% chance to add itself to the result.
    '''

    def __init__ (self):
        self.name = " monkey attack"

    def process (self, world):
        result = {}
        result["message"] = "the macaques are defeated! ...Those look pretty tasty!"
        monsters = []
        n_appearing = random.randrange(4,8)
        n = 1
        while n <= n_appearing:
            monsters.append(Macaque("Man-eating Macaque "+str(n)))
            n += 1
        display.announce ("The crew is attacked by a troop of man-eating macaques!")
        combat.Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += n_appearing*5

        return result

####################################################################################################
# Treasure
####################################################################################################

class JeweledCutlass(item.Item):
    def __init__(self):
        super().__init__("jeweled-sword", 185) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "cut"
        self.verb2 = "cuts"

####################################################################################################
# Island definition
####################################################################################################

class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)
        self.locations["trees"] = Trees(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)


class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(ShorePirates())

    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        elif (verb == "east" or verb == "west"):
            display.announce ("You walk all the way around the island on the beach. It's not very interesting.")


class Trees (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = JeweledCutlass() #Treasure from this island
        self.item_in_clothes = items.Flintlock() #Flintlock from the general item list

        self.event_chance = 50
        self.events.append(ManEatingMonkeys())
        self.events.append(ShorePirates())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into the small forest on the island."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + f" You see a {self.item_in_tree.name} stuck in a tree."
        if self.item_in_clothes != None:
            description = description + f" You see a {self.item_in_clothes.name} in a pile of shredded clothes on the forest floor."
        display.announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You pick up the {item.name} out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")
