from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random


class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)
        self.locations["Forest_with_Treasure"] = Forest_with_Treasure(self)
        self.locations["Maze"] = Maze(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an island", pause=False)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Forest_with_Treasure"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Maze"]
        elif(verb == 'west'):
            config.the_player.next_loc = self.main_location.locations["Deserted_Town"]


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
        self.events.append(Rabid_Pirates())

    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Forest_with_Treasure"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Maze"]
        else:
            display.announce("You walk around the island.")

class Zombies(combat.Monster):
    def __init__ (self, name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(60,80), (10,25)]
        attacks["slash"] = ["slash", random.randrange(25,50), (15,20)]
        super().__init__(name, random.randrange(20,45), attacks, 120 + random.randrange(-20,21))
        self.type_name = "Zombies"

class Rabid_Pirates(event.Event):
    def __init__ (self):
        self.name = "Rabid Pirate attack"
    def process (self, world):
        result = {}
        result["message"] = "the Pirates are defeated! ...They dropped FOOD!"
        monsters = []
        n_appearing = random.randrange(1,3)
        n = 1
        while n <= n_appearing:
            monsters.append(Zombies("Zombies"+str(n)))
            n += 1
        display.announce ("The crew is attacked by a troop of Zombies!")
        combat.Combat(monsters).combat()
        if random.randrange(2) == 0:
            result["newevents"] = [ self ]
        else:
            result["newevents"] = [ ]
        config.the_player.ship.food += n_appearing*7

        return result

class Diamond_Sword(item.Item):
 def __init__(self):
    super().__init__("Diamond Sword", 200)
    self.damage = (15,85)
    self.skill = "swords"
    self.verb = "cut"
    self.verb2 = "cuts"

class Dagger(item.Item):
    def __init__(self):
        super().__init__("Small Dagger", 12)
        self.damage = (5,35)
        self.skill = "swords"
        self.verb = "stab"
        self.verb2 = "slashes"
    
class Maze(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Maze"
        self.maze_state_options = ['sick', 'treasure', 'continue', "exit"]
        self.maze_state = "continue"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.verbs['take'] = self
        self.verbs['give'] = self

    def exit(self):
        display.announce("Congratulations, you have explored the maze!")
        
    def sick_man(self):
        name = 'Paul'
        display.announce(f"{name} is sick, if you give him medicine he will reward you.")

    def continue_maze(self):
        display.announce("Nothing happened, continue exploring the maze.")
        pass

    def treasure(self):
        display.announce("You found a treasure!! It feels kind of lucky.")
        self.lucky = True

    def enter (self):
        display.announce ("arrive at a branch in a maze. You can go north east south or west.")
        
    def process_verb(self, verb, cmd_list, nouns):
        while(self.maze_state != exit):
            if(verb == 'north'):
                self.maze_state = random.choice(self.maze_state_options)
                display.announce("Due to your choice, the maze is now ", self.maze_state)
                if (self.maze_state == 'continue'):
                    self.continue_maze()
                elif(self.maze_state == 'treasure'):
                    self.treasure()
                elif(self.maze_state == 'sick'):
                    self.sick_man()
            elif(verb == 'south'):
                self.maze_state = random.choice(self.maze_state_options)
                display.announce(f"Due to your choice, the maze is now {self.maze_state}")
                if (self.maze_state == 'continue'):
                    self.continue_maze()
                elif(self.maze_state == 'treasure'):
                    self.treasure()
                elif(self.maze_state == 'sick'):
                    self.sick_man()
            elif(verb == 'west'):
                self.maze_state = random.choice(self.maze_state_options)
                display.announce(f"Due to your choice, the maze is now {self.maze_state}")
                if (self.maze_state == 'continue'):
                    self.continue_maze()
                elif(self.maze_state == 'treasure'):
                    self.treasure()
                elif(self.maze_state == 'sick'):
                    self.sick_man()
            elif(verb == 'east'):
                self.maze_state = random.choice(self.maze_state_options)
                display.announce(f"Due to your choice, the maze is now {self.maze_state}")
                if (self.maze_state == 'continue'):
                    self.continue_maze()
                elif(self.maze_state == 'treasure'):
                    self.treasure()
                elif(self.maze_state == 'sick'):
                    self.sick_man()
            elif(verb == 'take'):
                config.the_player.add_to_inventory([item])
            elif(verb == "give" and self.maze_state == "sick"):
                if (len(cmd_list) > 3):
                    if ((cmd_list[1] == "medicine") and (cmd_list[3] in nouns.keys())):
                        if (config.the_player.ship.medicine.medicine > 0):
                            nouns[cmd_list[3]].receive_medicine(1)
                            config.the_player.ship.medicine += config.the_player.ship.medicine - 1
                        else:
                            display.announce ("no more medicine to give")
                else:
                    display.announce ("Give medicine to who?")

class Forest_with_Treasure(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Forest with Treasure"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.verbs['take'] = self
        self.item_in_box = Diamond_Sword()
        self.item_in_corpse = Dagger()

        self.events_chance = 33
        self.events.append(Rabid_Pirates())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, Rabid_Pirates):
                edibles = True
        description = "You walk into the large forest on the island."
        if edibles == False:
             description = description + " Nothing around here looks very edible."

        if self.item_in_box != None:
            description = description + f" You see a box, open to find {self.item_in_box.name}."
        if self.item_in_corpse != None:
            description = description + f" You see a {self.item_in_corpse.name} in a half eaten corpse on the forest floor."
        display.announce (description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        if verb == "take":
            if self.item_in_box == None and self.item_in_corpse == None:
                display.announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False
                item = self.item_in_box
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You take the {item.name} from the box.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_box = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_corpse
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    display.announce(f"You pick up the {item.name} out of the corpse. ...It looks like someone was killed here recently.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_corpse = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    display.announce ("You don't see one of those around.")