###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import Colored_Strings as COLOR_str

# NXBT is only compatible with Linux systems
if os.name != 'posix': exit(f'\n{COLOR_str.NOT_LINUX_SYSTEM}\n')

if __name__ == '__main__': 
    # Will raise an error when restarting execution using sudo
    try: os.chdir(os.path.dirname(__file__))
    except: pass
    # NXBT requires administrator permissions
    if 'SUDO_USER' not in os.environ: 
        print(f'\n{COLOR_str.NOT_SUDO}')
        program_name = __file__.split('/')[-1]
        exit(os.system(f'sudo python3 {program_name}'))

import nxbt
from time import sleep
from threading import Lock

import sys; sys.path.append('..')
import Constants as CONST
from Macros import *

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

    #######################################################################################################################

    @staticmethod
    def restart_bluetooth():
        print(COLOR_str.RESTARTING_BLUETOOTH)
        # Turn off bluetooth systems
        os.system('sudo rfkill block bluetooth')
        sleep(1)
        # Turn on bluetooth systems
        os.system('sudo rfkill unblock bluetooth')
        sleep(CONST.RESTART_BLUETOOTH_SECONDS)
        print(COLOR_str.BLUETOOTH_RESTARTED)

    #######################################################################################################################

    def connect_controller(self):
        self.restart_bluetooth()
        # Get a list of all available Bluetooth adapters
        adapters = self.nxbt_manager.get_available_adapters()
        controller_indexes = []
        # Loop over all bluetooth adapters and create a Switch Controller for each
        for index in range(len(adapters)):
            controller_index = self.nxbt_manager.create_controller(
                nxbt.PRO_CONTROLLER,
                adapter_path = adapters[index],
                colour_body = CONST.CONTROLLER_BODY_COLOR,
                colour_buttons = CONST.CONTROLLER_BUTTONS_COLOR
            )
            controller_indexes.append(controller_index)

        self.controller_index = controller_indexes[-1]
        print(COLOR_str.CONNECTING_TO_SWITCH)
        # Connect to Nintendo Switch
        self.nxbt_manager.wait_for_connection(self.controller_index)
        print(COLOR_str.CONTROLLER_CONNECTED)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    from queue import Queue
    from threading import Thread, Event

    from GUI import GUI
    import Colored_Strings as COLOR_str
    from FPS_Counter import FPS_Counter
    from Game_Capture import Game_Capture
    from Image_Processing import Image_Processing

    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Switch Controller'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Test Switch Controller'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Switch Controller'))

        menu_options = {
            '1': test_controller,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Switch Controller') + '\n')

    #######################################################################################################################

    def test_controller(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Switch Controller')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Testing Switch Controller...")
            .replace('{path}', '')
        )

        Image_Queue = Queue()
        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
        FPS = FPS_Counter()
        shutdown_event = Event()
        switch_controller_image = Image_Processing(f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}')
        switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
        Controller = Switch_Controller()
        
        def test_GUI_control(shutdown_event = None, previous_button = None):
            if isinstance(shutdown_event, type(None)): return

            while not shutdown_event.is_set():
                image = Image_Processing(Video_Capture.read_frame())
                if isinstance(image.original_image, type(None)): continue

                image.resize_image()
                FPS.get_FPS()
                image.draw_FPS(FPS.FPS)
                image.get_mask()
                n_contours = image.get_rectangles()

                if Controller.current_button_pressed != previous_button:
                    switch_controller_image.draw_button(Controller.current_button_pressed)
                    previous_button = Controller.current_button_pressed

                Image_Queue.put([image, FPS.memory_usage, switch_controller_image, None])

        def test_controller():
            Controller.connect_controller()
            test_macro(Controller)

        threads = []
        threads.append(Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True))
        threads.append(Thread(target=test_controller, daemon=True))
        for thread in threads: thread.start()

        user_interface = GUI(Image_Queue)
        shutdown_event.set()

        print(COLOR_str.RELEASING_THREADS
            .replace('{module}', 'Switch Controller')
            .replace('{threads}', str(len(threads))) + '\n'
        ) 

    #######################################################################################################################

    main_menu()