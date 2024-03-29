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

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def test_macro(controller):
    controller.current_button_pressed = 'B'; sleep(1)
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.B])
    sleep(1); controller.current_button_pressed = 'HOME'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.HOME])
    sleep(1); stop_macro(controller)

###########################################################################################################################

def stop_macro(controller):
    controller.current_button_pressed = 'DOWN'
    for _ in range(2): controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_DOWN])
    controller.current_button_pressed = 'RIGHT'
    for _ in range(4): sleep(0.3); controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.DPAD_RIGHT])
    sleep(0.5); controller.current_button_pressed = 'A'
    controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A])
    sleep(2); controller.nxbt_manager.press_buttons(controller.controller_index, [Buttons.A]); sleep(2)
    controller.current_button_pressed = ''

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

