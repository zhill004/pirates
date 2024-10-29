#import pygame
import game.config as config

WINDOW_HEIGHT = 500
WINDOW_WIDTH = 1000

class Display ():
    def __init__(self):
        # pygame.init()
        # surface = pygame.display.set_mode(size=(WINDOW_WIDTH,WINDOW_HEIGHT))
        config.the_display = self
        self.updater = []
    def push_updater(self, updater):
        self.updater.append(updater)

    def pop_updater(self):
        #Never pop the last updater
        if(len(self.updater) > 1):
            self.updater.pop()

    def do_updater(self):
        #Do the top updater
        self.updater[-1]()

    def begin_loop(self):
        while (config.the_player.notdone() and len(self.updater)):
            self.do_updater()


def announce(announcement, end='\n', pause = True):
    #if(the_display != None):
    #   display stuff
    #else:
    if(pause):
        input (announcement)
    else:
        print (announcement, end=end)

def menu(options):
    #if(the_display != None):
    #   display stuff
    #else:
    chosen = -1
    while chosen < 0 or chosen >= len(options):
        menuletters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(len(options)):
            if i >= len(menuletters):
                print ("too many options :(")
                break
            print (menuletters[i] + " - " + str(options[i]))
        #Bad :(
        o = input("Choose: ")
        chosen = menuletters.find(o)
    return chosen

def get_text_input(prompt):
    return input(prompt)
