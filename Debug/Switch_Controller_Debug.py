###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
from time import time
from queue import Queue
from typing import Optional
from threading import Thread, Event

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
from Modules.GUI import GUI, App
from Modules.Macros import test_macro
import Modules.Colored_Strings as STR
from Modules.FPS_Counter import FPS_Counter
from Modules.Game_Capture import Game_Capture
from Modules.Image_Processing import Image_Processing
from Modules.Switch_Controller import Switch_Controller
from Modules.Control_System import _draw_switch_controller_buttons, _initialize_switch_controller_image

if __name__ == '__main__':
    # NXBT requires administrator permissions
    if 'SUDO_USER' not in os.environ:
        print(f'\n{STR.SC_NOT_SUDO}')
        program_name = os.path.abspath(os.path.join(os.path.dirname(__file__), __file__.split('/')[-1]))
        exit(os.system(f'sudo .venv/bin/python {program_name}'))

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Switch Controller'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def main_menu():
    print('\n' + STR.M_MENU.format(module=MODULE_NAME))
    print(STR.M_MENU_OPTION.format(index=1, option='Test Switch Controller'))

    option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

    menu_options = {
        '1': test_controller,
    }

    if option in menu_options: menu_options[option](option)
    else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME) + '\n')

###########################################################################################################################
###########################################################################################################################

def test_controller(option: str) -> None:

    """
    Launch a test sequence to validate the Switch controller input and GUI display.

    Args:
        option (str): Menu option for display purposes.

    Returns:
        None
    """

    print('\n' + STR.M_SELECTED_OPTION.format(
        module = MODULE_NAME,
        option = option,
        action = 'Testing Switch Controller...',
        path = ''
    ))

    # Set XDG_RUNTIME_DIR to avoid warnings in some environments
    os.environ['XDG_RUNTIME_DIR'] = "/tmp/runtime-root"
    os.makedirs(os.environ['XDG_RUNTIME_DIR'], exist_ok=True)
    os.chmod(os.environ['XDG_RUNTIME_DIR'], 0o700)

    FPS = FPS_Counter()
    initial_time = time()
    Image_Queue = Queue(maxsize = 2)
    Controller = Switch_Controller()
    shutdown_event = Event()
    Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)

    switch_controller_image = _initialize_switch_controller_image()

    #######################################################################################################################
    #######################################################################################################################

    def test_GUI_control(controller: Switch_Controller, shutdown_event: Optional[Event] = None) -> None:

        """
        Continuously updates the image queue with GUI and controller state until shutdown.

        Args:
            controller (Switch_Controller): The controller instance.
            shutdown_event (Event): Event used to signal shutdown.

        Returns:
            None
        """

        if shutdown_event is None:
            return

        while not shutdown_event.is_set():
            image = Image_Processing(Video_Capture.read_frame())
            if image.original_image is None:
                continue

            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            _draw_switch_controller_buttons(controller, switch_controller_image)

            update_items = {
                'image': image,
                'current_state': None,
                'shutdown_event': shutdown_event,
                'global_encounter_count': 0,
                'local_encounter_count': 0,
                'memory_usage': FPS.memory_usage,
                'cpu_usage': FPS.cpu_usage,
                'switch_controller_image': switch_controller_image,
                'clock': int(time() - initial_time),
            }

            Image_Queue.put(update_items)

    #######################################################################################################################
    #######################################################################################################################

    def run_test_controller(controller: Switch_Controller, shutdown_event: Event) -> None:

        """
        Run the controller macro test and disconnect once finished.

        Args:
            controller (Switch_Controller): The controller instance.
            shutdown_event (Event): Event used to signal shutdown.

        Returns:
            None
        """

        try: 
            controller.connect_controller()
            test_macro(controller)
            controller.disconnect_controller()
        except:
            pass

        shutdown_event.set()

    #######################################################################################################################
    #######################################################################################################################

    # Start background threads
    threads = [
        Thread(target=lambda: test_GUI_control(Controller, shutdown_event), daemon=True),
        Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True),
        Thread(target=lambda: run_test_controller(Controller, shutdown_event), daemon=True)
    ]

    for thread in threads:
        thread.start()

    # Launch the GUI
    GUI_App = App()
    gui = GUI(Image_Queue, shutdown_event, shutdown_event)
    # Blocking function until the GUI is closed
    GUI_App.exec_()
    
    # Signal shutdown to threads
    shutdown_event.set()

    print(STR.G_RELEASING_THREADS
        .replace('{module}', 'Switch Controller')
        .replace('{threads}', str(len(threads)))
    )

###########################################################################################################################
###########################################################################################################################

main_menu()
print()