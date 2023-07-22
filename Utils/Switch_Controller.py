###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__': os.chdir(os.path.dirname(__file__))

import nxbt
from nxbt import Buttons, Sticks
from time import sleep

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Switch_Controller():
    def __init__(self):
        # ↓↓ Init NXBT
        self.nxbt_manager = nxbt.Nxbt()
        self.controller_index = None

    def connect_controller(self):
        # ↓↓ Get a list of all available Bluetooth adapters
        adapters = self.nxbt_manager.get_available_adapters()
        controller_indexes = []
        # ↓↓ Loop over all bluetooth adapters and create a Switch Controller for each
        for index in range(len(adapters)):
            controller_index = self.nxbt_manager.create_controller(
                nxbt.PRO_CONTROLLER,
                adapter_path = adapters[index],
                colour_body = CONST.CONTROLLER_BODY_COLOR,
                colour_buttons = CONST.CONTROLLER_BUTTONS_COLOR
            )
            controller_indexes.append(controller_index)

        self.controller_index = controller_indexes[-1]
        print('Connecting to Nintendo Switch...')
        # ↓↓ Connect to Nintendo Switch
        self.nxbt_manager.wait_for_connection(self.controller_index)
        print('Controller connected!')

    def start_macro(self):
        sleep(0.01)
        self.nxbt_manager.press_buttons(self.controller_index, [Buttons.HOME])
        sleep(1)
        self.nxbt_manager.press_buttons(self.controller_index, [Buttons.A])

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    Switch_Controller = Switch_Controller()
    Switch_Controller.connect_controller()
    Switch_Controller.start_macro()
