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

    #######################################################################################################################

    def disconnect_controller(self):
        os.system('sudo rfkill block bluetooth')

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    import time
    from threading import Thread, Event
    import PyQt5.QtWidgets as pyqt_w
    
    import Colored_Strings as COLOR_str
    from FPS_Counter import FPS_Counter
    from Game_Capture import Game_Capture
    from GUI import GUI, DllistQueue, App
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
    #######################################################################################################################

    def test_controller(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Switch Controller')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Testing Switch Controller...")
            .replace('{path}', '')
        )

        # Set XDG_RUNTIME_DIR environment variable (avoid unnecessary warnings)
        os.environ['XDG_RUNTIME_DIR'] = "/tmp/runtime-root"
        os.makedirs(os.environ['XDG_RUNTIME_DIR'], exist_ok=True)
        os.chmod(os.environ['XDG_RUNTIME_DIR'], 0o700)

        FPS = FPS_Counter()
        initial_time = time.time()
        Image_Queue = DllistQueue(maxsize = 2)
        Controller = Switch_Controller()
        shutdown_event = Event()
        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)

        switch_controller_image = Image_Processing(f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}')
        switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
        switch_controller_image.draw_button()

        def test_GUI_control(shutdown_event = None):
            if isinstance(shutdown_event, type(None)): return

            while not shutdown_event.is_set():
                image = Image_Processing(Video_Capture.read_frame())
                if isinstance(image.original_image, type(None)): continue

                image.resize_image()
                FPS.get_FPS()
                image.draw_FPS(FPS.FPS)

                update_items = {
                    'image': image,
                    'current_state': None,
                    'shutdown_event': shutdown_event,
                    'global_encounter_count': 0,
                    'local_encounter_count': 0,
                    'memory_usage': FPS.memory_usage,
                    'cpu_usage': FPS.cpu_usage,
                    'switch_controller_image': switch_controller_image,
                    'clock': int(time.time() - initial_time),
                }

                Image_Queue.put(update_items)

        def run_test_controller(controller, shutdown_event):
            try: 
                controller.connect_controller()
                test_macro(controller)
                controller.disconnect_controller()
            except: pass
            shutdown_event.set()

        threads = []
        threads.append(Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: run_test_controller(Controller, shutdown_event), daemon=True))
        for thread in threads: thread.start()

        GUI_App = App()
        gui = GUI(Image_Queue, shutdown_event, shutdown_event)
        # Blocking function until the GUI is closed
        GUI_App.exec_()
        
        # Kill all secondary threads
        shutdown_event.set()
        print(COLOR_str.RELEASING_THREADS
            .replace('{module}', 'Switch Controller')
            .replace('{threads}', str(len(threads))) + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    main_menu()