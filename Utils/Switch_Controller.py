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

import nxbt
from time import sleep

from Macros import *
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

    @staticmethod
    def restart_bluetooth():
        print('Restarting bluetooth systems...')
        # ↓↓ Turns off bluetooth systems
        os.system('sudo rfkill block bluetooth')
        sleep(1)
        # ↓↓ Turns on bluetooth systems
        os.system('sudo rfkill unblock bluetooth')
        sleep(CONST.RESTART_BLUETOOTH_SECONDS)
        print('Bluetooth restarted successfully!')

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

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    Switch_Controller = Switch_Controller()
    Switch_Controller.restart_bluetooth()
    Switch_Controller.connect_controller()
    for _ in range(2):
        setup_macro(Switch_Controller.nxbt_manager, Switch_Controller.controller_index)
        sleep(10)
        start_combat(Switch_Controller.nxbt_manager, Switch_Controller.controller_index, False)
        sleep(7)
    stop_macro(Switch_Controller.nxbt_manager, Switch_Controller.controller_index)