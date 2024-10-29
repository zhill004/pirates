#!/usr/bin/env python3

# player - controlling a ship
#    ship is lost at sea, trying to return home
#         - dangers and opportunities
#         - crew, crew's health

import game.ship as ship
import game.world as world
import game.player as player
import game.config as config
import game.display as display

ship_v     = ship.Ship()
world_v    = world.World (ship_v)
start_loc  = world_v.get_startloc()
ship_v.set_loc (start_loc)

player.Player(world_v, ship_v)
display.Display()

def sea_state_update():
    config.the_player.get_world().start_day ()
    config.the_player.process_day()
    config.the_player.get_world().end_day ()

config.the_display.push_updater(sea_state_update)

config.the_display.begin_loop()

# world_v.print()
