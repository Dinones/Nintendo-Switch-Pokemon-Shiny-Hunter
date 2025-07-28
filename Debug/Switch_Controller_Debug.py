###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import time
from threading import Thread, Event

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
from Modules.Macros import test_macro
import Modules.Colored_Strings as STR
from Modules.FPS_Counter import FPS_Counter
from Modules.Game_Capture import Game_Capture
from Modules.GUI import GUI, DllistQueue, App
from Modules.Image_Processing import Image_Processing
from Modules.Switch_Controller import Switch_Controller

if __name__ == '__main__':
    # NXBT requires administrator permissions
    if 'SUDO_USER' not in os.environ: 
        print(f'\n{STR.SC_NOT_SUDO}')
        program_name = os.path.abspath(os.path.join(os.path.dirname(__file__), __file__.split('/')[-1]))
        exit(os.system(f'sudo python3 {program_name}'))

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Switch Controller'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':

    def main_menu():
        print('\n' + STR.M_MENU.format(module=MODULE_NAME))
        print(STR.M_MENU_OPTION.format(index=1, option='Test Switch Controller'))

        option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

        menu_options = {
            '1': test_controller,
        }

        if option in menu_options: menu_options[option](option)
        else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME) + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def test_controller(option):
        print('\n' + STR.SELECTED_OPTION.format(
            module = MODULE_NAME,
            option = option,
            action = 'Testing Switch Controller...',
            path = ''
        ))

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
        print(STR.RELEASING_THREADS
            .replace('{module}', 'Switch Controller')
            .replace('{threads}', str(len(threads))) + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    main_menu()