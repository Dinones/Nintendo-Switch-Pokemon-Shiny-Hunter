###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
from queue import Queue
from time import time, sleep
from threading import Thread, Event

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
from Modules.GUI import GUI, App
import Modules.Colored_Strings as STR
from Modules.FPS_Counter import FPS_Counter
from Modules.Game_Capture import Game_Capture
from Modules.Image_Processing import Image_Processing

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'GUI'

SWITCH_CONTROLLER_IMAGE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', CONST.SWITCH_CONTROLLER_IMAGE_PATH)
)
TEMPLATE_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.TEMPLATE_IMAGE_PATH))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def main_menu():
    print('\n' + STR.M_MENU.format(module=MODULE_NAME))
    print(STR.M_MENU_OPTION.format(index='1', option='Open GUI using a template image'))
    print(STR.M_MENU_OPTION.format(index='2', option='Open GUI using capture card'))

    option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

    menu_options = {
        '1': test_GUI_template_image,
        '2': test_GUI_capture_card,
    }

    if option in menu_options: menu_options[option](option)
    else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME) + '\n')

###########################################################################################################################
###########################################################################################################################

def test_GUI_template_image(option):

    """
    Launches the full GUI using a static template image.

    Args:
        option (str): Menu option for display purposes (e.g., "3").
    """

    #######################################################################################################################
    #######################################################################################################################

    def test_GUI_control(shutdown_event: Event) -> None:

        """
        Simulates GUI updates by pushing test frames and stats to the GUI queue.

        Args:
            shutdown_event (Event): Signals when to stop pushing updates.

        Returns:
            None
        """

        while not shutdown_event.is_set():
            update_items = {
                'image': image,
                'current_state': 'TESTING',
                'shutdown_event': shutdown_event,
                'global_encounter_count': 0,
                'local_encounter_count': 0,
                'memory_usage': FPS.memory_usage,
                'cpu_usage': FPS.cpu_usage,
                'switch_controller_image': switch_controller_image,
                'clock': int(time() - initial_time),
            }

            Image_Queue.put(update_items)
            Image_Queue.put(update_items)

    #######################################################################################################################
    #######################################################################################################################

    print('\n' + STR.M_SELECTED_OPTION.format(
        module=MODULE_NAME,
        option=option,
        action=f"Testing GUI using a template image...",
        path=''
    ))

    # Initialize global data
    FPS = FPS_Counter()
    initial_time = time()
    Image_Queue = Queue()
    shutdown_event = Event()

    # Load and prepare Switch controller image
    switch_controller_image = Image_Processing(SWITCH_CONTROLLER_IMAGE_PATH)
    if switch_controller_image.original_image is None:
        print(STR.G_INVALID_PATH_ERROR.format(module=MODULE_NAME, path=SWITCH_CONTROLLER_IMAGE_PATH))
        return
    switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
    switch_controller_image.draw_button()

    # Load and prepare frame template image
    image = Image_Processing(TEMPLATE_IMAGE_PATH)
    if image.original_image is None:
        print(STR.G_INVALID_PATH_ERROR.format(module=MODULE_NAME, path=TEMPLATE_IMAGE_PATH))
        return
    image.resize_image()
    image.FPS_image = image.resized_image

    # Start background threads for GUI simulation and system metrics
    threads = [
        Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True),
        Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True)
    ]
    for thread in threads:
        thread.start()

    # Start GUI loop (blocking until the GUI is closed)
    GUI_App = App()
    gui = GUI(Image_Queue, shutdown_event, shutdown_event)
    GUI_App.exec_()

    shutdown_event.set()
    print(STR.G_RELEASING_THREADS.format(module=MODULE_NAME, threads=len(threads)) + '\n')

###########################################################################################################################
###########################################################################################################################

def test_GUI_capture_card(option):

    """
    Launches the full GUI using the game capture input images.

    Args:
        option (str): Menu option for display purposes (e.g., "3").
    """

    #######################################################################################################################
    #######################################################################################################################

    def test_GUI_control(shutdown_event: Event) -> None:

        """
        Continuously captures video frames from the game source, processes them, and pushes updates to the GUI queue
        while "shutdown_event" is not set.

        Args:
            shutdown_event (Event): Thread-safe signal to stop the capture loop.
        """

        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)

        if not Video_Capture.video_capture.isOpened():
            Video_Capture.stop()
            print(STR.GC_INVALID_VIDEO_CAPTURE.format(video_capture=f"'{CONST.VIDEO_CAPTURE_INDEX}'"))
            shutdown_event.set()
            return

        while not shutdown_event.is_set():
            image = Image_Processing(Video_Capture.read_frame())

            # Stop if capture card disconnected for more than CAPTURE_CARD_DISCONNECTED_MAX_SECONDS
            if (
                Video_Capture.previous_frame_skipped and
                time() - Video_Capture.last_frame_time > CONST.CAPTURE_CARD_DISCONNECTED_MAX_SECONDS
            ):
                Video_Capture.stop()
                print(STR.GC_INVALID_VIDEO_CAPTURE.format(video_capture=f"'{CONST.VIDEO_CAPTURE_INDEX}'"))
                shutdown_event.set()

            # Frame is valid
            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            update_items = {
                'image': image,
                'current_state': 'TESTING',
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

    print('\n' + STR.M_SELECTED_OPTION.format(
        module=MODULE_NAME,
        option=option,
        action=f"Testing GUI with the capture card...",
        path=''
    ))

    # Initialize global data
    FPS = FPS_Counter()
    initial_time = time()
    Image_Queue = Queue()
    shutdown_event = Event()

    # Load and prepare Switch controller image
    switch_controller_image = Image_Processing(SWITCH_CONTROLLER_IMAGE_PATH)
    if switch_controller_image.original_image is None:
        print(STR.G_INVALID_PATH_ERROR.format(module=MODULE_NAME, path=SWITCH_CONTROLLER_IMAGE_PATH))
        return
    switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
    switch_controller_image.draw_button()

    # Load and prepare frame template image
    image = Image_Processing(TEMPLATE_IMAGE_PATH)
    if image.original_image is None:
        print(STR.G_INVALID_PATH_ERROR.format(module=MODULE_NAME, path=TEMPLATE_IMAGE_PATH))
        return
    image.resize_image()
    image.FPS_image = image.resized_image

    # Start background threads for GUI simulation and system metrics
    threads = [
        Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True),
        Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True)
    ]
    for thread in threads:
        thread.start()

    # Start GUI loop (blocking until the GUI is closed)
    GUI_App = App()
    gui = GUI(Image_Queue, shutdown_event, shutdown_event)
    GUI_App.exec_()

    shutdown_event.set()
    print(STR.G_RELEASING_THREADS.format(module=MODULE_NAME, threads=len(threads)) + '\n')       

###########################################################################################################################
###########################################################################################################################

main_menu()