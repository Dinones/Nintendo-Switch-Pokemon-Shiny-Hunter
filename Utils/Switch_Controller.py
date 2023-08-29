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

import nxbt
from time import sleep
from threading import Lock

from Macros import *
import Messages as MSG
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
        self.event_lock = Lock()
        self.current_event = None

    @staticmethod
    def __test_print(text): print(text) if CONST.TESTING else None

    @staticmethod
    def restart_bluetooth():
        print(MSG.RESTARTING_BLUETOOTH)
        # ↓↓ Turns off bluetooth systems
        os.system('sudo rfkill block bluetooth')
        sleep(1)
        # ↓↓ Turns on bluetooth systems
        os.system('sudo rfkill unblock bluetooth')
        sleep(CONST.RESTART_BLUETOOTH_SECONDS)
        print(MSG.BLUETOOTH_RESTARTED)

    def connect_controller(self, special_case = None):
        self.restart_bluetooth()
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
        print(MSG.CONNECTING_TO_SWITCH)
        # ↓↓ Connect to Nintendo Switch
        self.nxbt_manager.wait_for_connection(self.controller_index)
        print(MSG.CONTROLLER_CONNECTED)
        if type(special_case) == type(None): 
            with self.event_lock: self.current_event = 'SETUP'
        with self.event_lock: self.current_event = special_case

    def run_event(self):
        while True:
            if self.event_lock.acquire():
                ######################################     GENERAL     ####################################################

                if self.current_event == 'SETUP': 
                    setup_macro(self.nxbt_manager, self.controller_index)
                    self.__test_print(MSG.LOADING_GAME)
                    self.current_event = 'WAIT_COMBAT'
                elif self.current_event in ['HOME_STOP', 'HOME_RESTART']:
                    if self.current_event == 'HOME_STOP': sleep(CONST.SHINY_RECORDING_SECONDS)
                    home_macro(self.nxbt_manager, self.controller_index)
                    if self.current_event == 'HOME_STOP': self.current_event = 'WAIT_HOME_STOP'
                    elif self.current_event == 'HOME_RESTART': self.current_event = 'WAIT_HOME_RESTART'
                elif self.current_event == 'RESTART':
                    start_game_macro(self.nxbt_manager, self.controller_index)
                    self.current_event = 'WAIT_COMBAT'
                elif self.current_event == 'STOP':
                    stop_macro(self.nxbt_manager, self.controller_index)
                    self.current_event = 'FINISH'

                ######################################     STATIC     #####################################################

                elif self.current_event == 'COMBAT': 
                    start_combat_macro(self.nxbt_manager, self.controller_index)
                    self.current_event = 'WAIT_RESTART'

                #####################################     STARTERS     ####################################################

                elif self.current_event == 'MOVE_FORWARD':
                    move_forward(self.nxbt_manager, self.controller_index)
                    self__test_print(MSG.SKIPPING_DIALOGUE)
                    self.current_event = 'PRESS_A'
                elif self.current_event == 'PRESS_A':
                    press_A(self.nxbt_manager, self.controller_index)
                elif self.current_event == 'WAIT_STARTER_SELECTION':
                    select_starter(self.nxbt_manager, self.controller_index)
                    self.current_event = 'STARTER_SELECTED'
                elif self.current_event == 'WAIT_STARTER_POKEMON_FOREGROUND':
                    sleep(2.5); self.current_event = 'DETECT_STARTER_POKEMON'

                #######################################     WILD     ######################################################
                
                elif self.current_event == 'FAST_SETUP': 
                    fast_setup_macro(self.nxbt_manager, self.controller_index)
                    self.__test_print(MSG.STARTING_MACRO.replace('{macro}', 'move_straight'))
                    self.current_event = 'MOVE_STRAIGHT'
                elif self.current_event == 'MOVE_STRAIGHT': 
                    # ↓↓ Provide more accurate detection when entering the combat walking long distances
                    self.event_lock.release()
                    move_straight_macro(self.nxbt_manager, self.controller_index)
                    sleep(0.5); continue
                elif self.current_event == 'WAIT_WILD_POKEMON_FOREGROUND': 
                    sleep(1.5); self.current_event = 'DETECT_WILD_POKEMON'
                elif self.current_event == 'ESCAPE_COMBAT': 
                    escape_combat_macro(self.nxbt_manager, self.controller_index)
                    sleep(2)
                    self.__test_print(MSG.STARTING_MACRO.replace('{macro}', 'move_straight'))
                    self.current_event = 'MOVE_STRAIGHT'

                self.event_lock.release()
            # ↓↓ Provide the main thread some time to check the current event
            sleep(0.5)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    Switch_Controller = Switch_Controller()
    Switch_Controller.connect_controller()
    for _ in range(2):
        setup_macro(Switch_Controller.nxbt_manager, Switch_Controller.controller_index)
        sleep(10)
        start_combat_macro(Switch_Controller.nxbt_manager, Switch_Controller.controller_index, False)
        sleep(7)
    stop_macro(Switch_Controller.nxbt_manager, Switch_Controller.controller_index)