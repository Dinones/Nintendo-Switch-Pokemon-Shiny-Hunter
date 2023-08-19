###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os

# ↓↓ NXBT is only compatible with Linux systems
if os.name != 'posix': exit('NXBT is only available on Linux systems.')

if __name__ == '__main__':
    # ↓↓ Will raise an error when restarting execution using sudo
    try: os.chdir(os.path.dirname(__file__))
    except: pass
    # ↓↓ NXBT requires administrator permissions
    if 'SUDO_USER' not in os.environ: 
        print('NXBT must be executed using administrator permission: Restarting using sudo...')
        program_name = __file__.split('/')[-1]
        exit(os.system(f'sudo python3 {program_name}'))

from nxbt import Buttons, Sticks
from time import sleep

import sys; sys.path.append('..')
import Constants as CONST
import Messages as MSG

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def __test_print(text): print(text) if CONST.TESTING else None
def __test_print_command(text): print(text) if CONST.TESTING and CONST.PRINT_CONTROLS else None

def setup_macro(nxbt_manager, controller_index):
    __test_print(MSG.STARTING_MACRO.replace('{macro}', 'setup'))
    sleep(1); nxbt_manager.press_buttons(controller_index, [Buttons.B]); 
    __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'B'))
    sleep(1); nxbt_manager.press_buttons(controller_index, [Buttons.HOME])
    __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'HOME'))
    __test_print(MSG.FINISHED_MACRO.replace('{macro}', 'setup'))
    sleep(1); start_game_macro(nxbt_manager, controller_index)

def start_game_macro(nxbt_manager, controller_index):
    __test_print(MSG.STARTING_MACRO.replace('{macro}', 'start_game'))
    for _ in range(3): 
        nxbt_manager.press_buttons(controller_index, [Buttons.X])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'X'))
    for _ in range(5): 
        sleep(0.5); nxbt_manager.press_buttons(controller_index, [Buttons.A])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'A'))
    __test_print_command(MSG.WAITING_SECONDS.replace('{seconds}', str(CONST.BLACK_SCREEN_LOAD_SECONDS)))
    sleep(CONST.BLACK_SCREEN_LOAD_SECONDS)
    for _ in range(15): 
        sleep(0.5); nxbt_manager.press_buttons(controller_index, [Buttons.A])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'A'))
    __test_print(MSG.FINISHED_MACRO.replace('{macro}', 'start_game'))

def start_combat_macro(nxbt_manager, controller_index, movement = False):
    __test_print(MSG.STARTING_MACRO.replace('{macro}', 'start_combat'))
    if CONST.WALK_FORWARD_BEFORE_COMBAT: 
        __test_print_command(MSG.BUTTON_LARGE_PRESSED.replace('{button}', 'DPAD_UP')
            .replace('{seconds}', str(CONST.WALKING_SECONDS)))
        nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_UP], down = CONST.WALKING_SECONDS)
    for _ in range(10): 
        sleep(0.5); nxbt_manager.press_buttons(controller_index, [Buttons.A])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'A'))
    __test_print_command(MSG.WAITING_SECONDS.replace('{seconds}', str(CONST.OVERWORLD_ENTER_COMBAT_WAIT_SECONDS)))
    sleep(CONST.OVERWORLD_ENTER_COMBAT_WAIT_SECONDS)
    __test_print(MSG.FINISHED_MACRO.replace('{macro}', 'start_combat'))

def home_macro(nxbt_manager, controller_index):
    __test_print(MSG.STARTING_MACRO.replace('{macro}', 'home'))
    nxbt_manager.press_buttons(controller_index, [Buttons.HOME])
    __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'HOME'))
    __test_print_command(MSG.WAITING_SECONDS.replace('{seconds}', str(1))); sleep(1)
    __test_print(MSG.FINISHED_MACRO.replace('{macro}', 'home'))

def stop_macro(nxbt_manager, controller_index):
    __test_print(MSG.STARTING_MACRO.replace('{macro}', 'stop'))
    for _ in range(2): 
        nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_DOWN])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'DPAD_DOWN'))
    for _ in range(4): 
        sleep(0.3); nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_RIGHT])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'DPAD_RIGHT'))
    sleep(0.5); nxbt_manager.press_buttons(controller_index, [Buttons.A])
    __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'A'))
    sleep(2); nxbt_manager.press_buttons(controller_index, [Buttons.A])
    __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'A'))
    sleep(3)
    __test_print(MSG.FINISHED_MACRO.replace('{macro}', 'stop'))

###########################################################################################################################

def move_forward(nxbt_manager, controller_index):
    __test_print(MSG.STARTING_MACRO.replace('{macro}', 'move_forward'))
    __test_print_command(MSG.BUTTON_LARGE_PRESSED.replace('{button}', 'DPAD_UP')
            .replace('{seconds}', str(CONST.WALKING_SECONDS)))
    nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_UP], down = CONST.WALKING_SECONDS)
    __test_print(MSG.FINISHED_MACRO.replace('{macro}', 'move_forward'))

def press_A(nxbt_manager, controller_index): nxbt_manager.press_buttons(controller_index, [Buttons.A])

def select_starter(nxbt_manager, controller_index):
    __test_print(MSG.STARTING_MACRO.replace('{macro}', 'select_starter'))
    for _ in range(2): 
        sleep(0.5); nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_UP])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'DPAD_UP'))
    for _ in range(2): 
        nxbt_manager.press_buttons(controller_index, [Buttons.A])
        __test_print_command(MSG.BUTTON_PRESSED.replace('{button}', 'A'))
    __test_print_command(MSG.WAITING_SECONDS.replace('{seconds}', str(CONST.STARTER_OVERWORLD_ENTER_COMBAT_WAIT_SECONDS)))
    sleep(CONST.STARTER_OVERWORLD_ENTER_COMBAT_WAIT_SECONDS)
    __test_print(MSG.FINISHED_MACRO.replace('{macro}', 'select_starter'))
