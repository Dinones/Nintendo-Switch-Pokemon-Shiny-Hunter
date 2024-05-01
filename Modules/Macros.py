###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

from nxbt import Buttons, Sticks
from time import sleep

import sys; sys.path.append('..')
import Constants as CONST

# Used to toggle the direction when walking on the wild grass 
walking_direction = bool(0)

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def test_macro(controller):
    controller.current_event = "Test"
    start_macro(controller)
    sleep(2); controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    sleep(1); stop_macro(controller)

###########################################################################################################################

def start_macro(controller):
    if controller.previous_event == controller.current_event: return
    
    controller.current_button_pressed = 'B'; sleep(1)
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.B])
    sleep(1); controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])

###########################################################################################################################

def fast_start_macro(controller):
    if controller.previous_event == controller.current_event: return
    
    controller.current_button_pressed = 'B'; sleep(1)
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.B])
    sleep(1); controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    sleep(2); controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])

###########################################################################################################################

def stop_macro(controller):
    if controller.previous_event == controller.current_event: return

    controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    sleep(2); controller.current_button_pressed = 'DOWN'
    for _ in range(2): controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_DOWN])
    for _ in range(4): 
        controller.current_button_pressed = 'RIGHT'; sleep(0.2) 
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_RIGHT])
        controller.current_button_pressed = ''; sleep(0.1)
    sleep(0.5); controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
    sleep(3); controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A]); sleep(2)
    controller.current_button_pressed = ''

###########################################################################################################################

def restart_game_macro(controller):
    if controller.previous_event == controller.current_event: return
    
    controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    sleep(2); controller.current_button_pressed = 'X'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.X]); sleep(0.5)
    for _ in range(10): 
        controller.current_button_pressed = 'A'; sleep(0.2)
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
        controller.current_button_pressed = ''; sleep(0.1)

###########################################################################################################################

def move_player_wild_macro(controller):
    global walking_direction

    if CONST.WILD_WALKING_DIRECTION == 'NS':
        if not walking_direction:
            controller.current_button_pressed = 'UP'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_UP], down=CONST.WILD_WALKING_SECONDS)
        else: 
            controller.current_button_pressed = 'DOWN'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_DOWN], down=CONST.WILD_WALKING_SECONDS)

    elif CONST.WILD_WALKING_DIRECTION == 'EW':
        if not walking_direction:
            controller.current_button_pressed = 'LEFT'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_LEFT], down=CONST.WILD_WALKING_SECONDS)
        else: 
            controller.current_button_pressed = 'RIGHT'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_RIGHT], down=CONST.WILD_WALKING_SECONDS)
    
    walking_direction = not walking_direction

###########################################################################################################################

def escape_combat_macro(controller):
    if controller.previous_event == controller.current_event: return
    
    controller.current_button_pressed = 'UP'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_UP]); sleep(0.5)
    controller.current_button_pressed = 'A'
    for _ in range(5): controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A]); sleep(0.1)
    

###########################################################################################################################

def home_macro(controller):
    controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME]); sleep(1)

###########################################################################################################################

def press_single_button(controller, button):
    controller.current_button_pressed = button
    controller.nxbt_manager.press_buttons(controller.controller_index, [getattr(Buttons, button)])

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

