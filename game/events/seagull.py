from game import event
from game.player import Player
from game.context import Context
import game.config as config
import game.display as display
import random

#Example non-combat event
class Seagull (Context, event.Event):
    '''Encounter with an annoying seagull. Uses the parser to decide what to do about it.'''
    def __init__ (self):
        super().__init__()
        self.name = "seagull visitor"
        self.seagulls = 1
        self.verbs['chase'] = self
        self.verbs['feed'] = self
        self.verbs['help'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "chase"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "the seagulls fly off."
                if (self.seagulls > 1):
                    self.seagulls = self.seagulls - 1
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "luckly, the seagulls fly off."
                else:
                    self.result["message"] = f"{c.get_name()} is attacked by the seagulls."
                    if (c.inflict_damage (self.seagulls, "Pecked to death by seagulls")):
                        self.result["message"] = f".. {c.get_name()} is pecked to death by the seagulls!"

        elif (verb == "feed"):
            if (config.the_player.ship.get_food() > 0):
                if(self.seagulls//10 > 0): #if there's more than 10 seagulls, this definitely costs at least 1 food
                    config.the_player.ship.take_food ((self.seagulls//10))
                if(self.seagulls%10 > 0): #if there's a remainder, there's a chance of losing a(n additional) food
                    if(random.randint(1,10) < (self.seagulls%10)):
                        config.the_player.ship.take_food (1)
                self.seagulls = self.seagulls + 1
                self.result["newevents"].append (Seagull())
                self.result["message"] = "the seagulls are happy"
                self.go = True
            else:
                display.announce("You have no food to feed the seagulls. This does not bode well for you.")
                self.go = False
        elif (verb == "help"):
            display.announce ("the seagulls will pester you until you feed them or chase them off", pause=False)
            self.go = False
        else:
            display.announce ("it seems the only options here are to feed or chase", pause=False)
            self.go = False



    def process (self, world):

        self.go = False
        self.result = {}
        self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            display.announce(f"{self.seagulls} seagulls have appeared. What do you want to do?", pause=False)
            Player.get_interaction ([self])

        return self.result
