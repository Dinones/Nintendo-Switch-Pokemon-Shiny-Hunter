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
        exit(os.system('sudo python3 Switch_Controller.py'))

from nxbt import Buttons, Sticks
from time import sleep

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def setup_macro(nxbt_manager, controller_index):
    sleep(1); nxbt_manager.press_buttons(controller_index, [Buttons.B])
    sleep(1); nxbt_manager.press_buttons(controller_index, [Buttons.HOME])
    start_game(nxbt_manager, controller_index)

def stop_macro(nxbt_manager, controller_index):
    nxbt_manager.press_buttons(controller_index, [Buttons.HOME])
    sleep(1); nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_DOWN])
    for _ in range(4): 
        sleep(0.1)
        nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_RIGHT])
    sleep(0.1); nxbt_manager.press_buttons(controller_index, [Buttons.A])
    sleep(2); nxbt_manager.press_buttons(controller_index, [Buttons.A])

def start_game(nxbt_manager, controller_index):
    sleep(1); nxbt_manager.press_buttons(controller_index, [Buttons.X])
    for _ in range(5): 
        sleep(0.5)
        nxbt_manager.press_buttons(controller_index, [Buttons.A])
    sleep(CONST.BLACK_SCREEN_LOAD_SECONDS)
    for _ in range(15): 
        sleep(0.5)
        nxbt_manager.press_buttons(controller_index, [Buttons.A])

def start_combat(nxbt_manager, controller_index, movement = False):
    if movement: nxbt_manager.press_buttons(controller_index, [Buttons.DPAD_UP], down=CONST.WALKING_SECONDS)
    for _ in range(10): 
        sleep(0.5)
        nxbt_manager.press_buttons(controller_index, [Buttons.A])