###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import nxbt
from time import sleep
from threading import Lock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Modules.Colored_Strings as STR

# NXBT is only compatible with Linux systems
if os.name != 'posix':
    exit(f'\n{STR.SC_NOT_LINUX_SYSTEM}\n')

if __name__ == '__main__':
    # NXBT requires administrator permissions
    if 'SUDO_USER' not in os.environ: 
        print(f'\n{STR.SC_NOT_SUDO}')
        program_name = os.path.abspath(os.path.join(os.path.dirname(__file__), __file__.split('/')[-1]))
        exit(os.system(f'sudo python3 {program_name}'))

import Constants as CONST
from Modules.Macros import *

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Switch_Controller():
    def __init__(self):
        self.nxbt_manager = nxbt.Nxbt()
        self.controller_index = None
        self.event_lock = Lock()
        self.current_event = None
        self.previous_event = None
        self.current_button_pressed = ''
        self.previous_button_pressed = ''

    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def restart_bluetooth() -> None:
    
        """
        Restarts the Bluetooth system using system-level rfkill commands.
        """

        print(STR.SC_RESTARTING_BLUETOOTH)

        # Disable Bluetooth hardware
        os.system('sudo rfkill block bluetooth')
        sleep(1)

        # Enable Bluetooth hardware
        os.system('sudo rfkill unblock bluetooth')
        sleep(CONST.RESTART_BLUETOOTH_SECONDS)

        print(STR.SC_BLUETOOTH_RESTARTED)

    #######################################################################################################################
    #######################################################################################################################

    def connect_controller(self) -> None:

        """
        Connects a virtual Nintendo Switch controller using available Bluetooth adapters.
        """

        # Restart Bluetooth to ensure a clean connection state
        self.restart_bluetooth()

        # Get all available Bluetooth adapters
        adapters: list[str] = self.nxbt_manager.get_available_adapters()
        controller_indexes: list[int] = []

        # Create one controller per adapter
        for index in range(len(adapters)):
            controller_index = self.nxbt_manager.create_controller(
                nxbt.PRO_CONTROLLER,
                adapter_path=adapters[index],
                colour_body=CONST.CONTROLLER_BODY_COLOR,
                colour_buttons=CONST.CONTROLLER_BUTTONS_COLOR
            )
            controller_indexes.append(controller_index)

        # Store the last created controller (connected to the last adapter)
        self.controller_index = controller_indexes[-1]

        print(STR.SC_CONNECTING_TO_SWITCH)

        # Wait until the controller is connected to the Switch
        self.nxbt_manager.wait_for_connection(self.controller_index)

        print(STR.SC_CONTROLLER_CONNECTED)

    #######################################################################################################################
    #######################################################################################################################

    def disconnect_controller(self) -> None:
    
        """
        Disconnects the controller by disabling the Bluetooth interface.
        """

        os.system('sudo rfkill block bluetooth')

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################
