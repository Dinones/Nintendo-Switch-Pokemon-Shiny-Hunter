###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os, logging
from typing import Union, List

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

# Go from "Change Grip/Order Menu" to the main menu and then go back to "Change Grip/Order Menu" 
def test_macro(controller):
    controller.current_event = "Test"
    start_macro(controller)
    sleep(2); controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    controller.current_button_pressed = ''
    sleep(1); stop_macro(controller)

###########################################################################################################################

# Go from "Change Grip/Order Menu" to the main menu
def start_macro(controller):
    if controller.previous_event == controller.current_event: return
    
    controller.current_button_pressed = 'B'; sleep(1)
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.B])
    sleep(1); controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])

###########################################################################################################################

# Go from "Change Grip/Order Menu" to the main menu and start the game
def fast_start_macro(controller):
    if controller.previous_event == controller.current_event: return
    
    controller.current_button_pressed = 'B'; sleep(1)
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.B])
    sleep(1); controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    controller.current_button_pressed = ''
    sleep(2); controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
    sleep(1)

###########################################################################################################################

# Pause the game and go to the "Change Grip/Order Menu"
def stop_macro(controller):
    if controller.previous_event == controller.current_event: return

    controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    controller.current_button_pressed = ''
    sleep(1.5); controller.current_button_pressed = 'DOWN'
    for _ in range(2): controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_DOWN])
    for _ in range(4): 
        controller.current_button_pressed = 'RIGHT'; sleep(0.1) 
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_RIGHT])
        controller.current_button_pressed = ''; sleep(0.1)
    sleep(0.5); controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
    controller.current_button_pressed = ''
    sleep(2); controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
    controller.current_button_pressed = ''; sleep(1)

###########################################################################################################################

# Fully restart the game (Hard reset)
def restart_game_macro(controller):
    if controller.previous_event == controller.current_event: return
    
    controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME], down=0.05, up=0)
    controller.current_button_pressed = ''

    # In case the sleep menu is open press the B button, this will avoid entering the sleep mode by mistake.
    sleep(0.2); controller.current_button_pressed = 'B'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.B])
    controller.current_button_pressed = ''

    sleep(1.3); controller.current_button_pressed = 'X'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.X])
    controller.current_button_pressed = ''
    sleep(1)

    # Confirm the restart, press the A button until the game is restarted
    # For Sword/Shield the game take longer to exit.
    # 10 'A' presses are enough for BDSP but 15 for SWSH
    for _ in range(15):
        controller.current_button_pressed = 'A'
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
        controller.current_button_pressed = ''
        sleep(0.3)

###########################################################################################################################

# The player moves Up/Down or Right/Left
def move_player_wild_macro(controller):
    global walking_direction

    if CONST.WILD_WALKING_DIRECTION == 'NS':
        if not walking_direction:
            controller.current_button_pressed = 'UP'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_UP, Buttons.B], down=CONST.WILD_WALKING_SECONDS)
        else: 
            controller.current_button_pressed = 'DOWN'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_DOWN, Buttons.B], down=CONST.WILD_WALKING_SECONDS)

    elif CONST.WILD_WALKING_DIRECTION == 'EW':
        if not walking_direction:
            controller.current_button_pressed = 'LEFT'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_LEFT, Buttons.B], down=CONST.WILD_WALKING_SECONDS)
        else: 
            controller.current_button_pressed = 'RIGHT'
            controller.nxbt_manager.press_buttons(
                controller.controller_index, [Buttons.DPAD_RIGHT, Buttons.B], down=CONST.WILD_WALKING_SECONDS)
    
    walking_direction = not walking_direction

###########################################################################################################################

# Escape from the combat
def escape_combat_macro(controller):
    if controller.previous_event != controller.current_event: 
        sleep(0.5)
        controller.current_button_pressed = 'UP'
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_UP], down=0.3)
    else:
        sleep(0.1)
        controller.current_button_pressed = 'A'
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A]); sleep(0.1)
    
###########################################################################################################################

# Go to home menu
def home_macro(controller):
    controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME], down=0.05, up=0)
    controller.current_button_pressed = ''; sleep(1)

###########################################################################################################################

# Selects the desired starter pokémon
def select_starter_macro(controller):
    if controller.previous_event == controller.current_event: return

    wait_and_press_single_button(controller, 1, 'A'); sleep(1)
    if CONST.STARTER == 'C': 
        controller.current_button_pressed = 'RIGHT'
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_RIGHT]); sleep(0.2)
    elif CONST.STARTER == 'R': 
        controller.current_button_pressed = 'LEFT'
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_LEFT]); sleep(0.2)
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])

###########################################################################################################################

# Selects the desired starter pokémon
def accept_selection_box_macro(controller):
    if controller.previous_event == controller.current_event: return

    controller.current_button_pressed = 'UP'
    for _ in range(2): controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_UP])
    for _ in range(2): 
        controller.current_button_pressed = 'A'; sleep(0.2)
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
        controller.current_button_pressed = ''; sleep(0.1)

###########################################################################################################################

# Enter the lake
def enter_lake_macro(controller):
    controller.current_button_pressed = 'UP'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_UP], down=0.5)
    controller.current_button_pressed = 'A'; sleep(0.2)
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
    controller.current_button_pressed = ''; sleep(0.1)

###########################################################################################################################

def enter_static_combat_macro(controller):
    if CONST.MOVE_FORWARD_STATIC_ENCOUNTER:
        controller.current_button_pressed = 'UP'
        controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_UP], down=0.5)
    press_single_button(controller, 'A')

###########################################################################################################################

# Press the specified button a single time
def press_single_button(controller, button):
    controller.current_button_pressed = button
    controller.nxbt_manager.press_buttons(controller.controller_index, [getattr(Buttons, button)])
    controller.current_button_pressed = ''

###########################################################################################################################

# Wait the specified time and press the button a single time
def wait_and_press_single_button(controller, seconds, button):
    sleep(seconds)
    press_single_button(controller, button)


# This macro is for static shaymin on bdsp. Walking down and then up reload the zone
# and shaymin respawns. This is faster than closing and opening the game by about 20 seconds
def walk_down_and_up_for_shaymin_respawn(controller):
    # Wait 1.5 seconds for the escape from combat animation to end
    sleep(1.5)
    # Press button A to close aftercombat textbox just in case
    controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A], down=0.5)
    # Get on the bike, Player must have enabled the fast gear beforehand
    controller.current_button_pressed = 'PLUS'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.PLUS], down=0.75)
    # Bike down and up to respawn shaymin, interact with it & close its textbox
    controller.current_button_pressed = 'DOWN'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_DOWN], down=3.0)
    controller.current_button_pressed = 'UP'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_UP], down=3.5)
    controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A], down=0.5)
    # This short break allows shaymin textbox to appear as there is a short animation for the player to get off their bike
    sleep(2.0)
    controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A], down=0.5)


def press_button(controller, buttons: Union[str, List[str]], wait_after_action=0.0, down=0.1, up=0.1, block=True):
    """
    Press the specified button(s) and wait the specified time after the action
    :param controller: The controller object
    :param buttons: The button(s) to press, can be a single string or a list of strings
    :param wait_after_action: The time to wait after the action

    :param down: How long to hold the buttons down for in seconds, defaults to 0.1
    :type down: float, optional

    :param up: How long to release the button for in seconds, defaults to 0.1
    :type up: float, optional

    :param block: A boolean variable indicating whether or not to block until the macro completes,
        defaults to True
    :type block: bool, optional
    """

    if isinstance(buttons, str):
        buttons = [buttons]

    # TODO add support for multiple buttons
    controller.current_button_pressed = buttons[0]

    try:
        controller.nxbt_manager.press_buttons(
            controller.controller_index,
            # Convert the button string(s) to the corresponding button object(s)
            list(map(lambda btn: getattr(Buttons, btn), buttons)),
            down=down,
            up=up,
            block=block
        )
    except Exception as e:
        logging.error(f"Error while pressing button(s): {buttons}, {e}")

    controller.current_button_pressed = ''

    if wait_after_action > 0:
        sleep(wait_after_action)


###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################
