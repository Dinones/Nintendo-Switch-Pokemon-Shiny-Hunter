###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys; sys.path.append('Modules')
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

from queue import Queue
from time import sleep, time
from threading import Thread, Event

from GUI import GUI
from Macros import *
import Constants as CONST
from Control_System import *
import Colored_Strings as COLOR_str
from FPS_Counter import FPS_Counter
from Game_Capture import Game_Capture
from Image_Processing import Image_Processing
from Switch_Controller import Switch_Controller

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def GUI_control(FPS, Controller, Image_Queue, shutdown_event, previous_button = None):
    Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
    Video_Capture.start_recording()

    switch_controller_image = Image_Processing(CONST.SWITCH_CONTROLLER_IMAGE_PATH)
    switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
    switch_controller_image.draw_button()
    
    with open(f'./{CONST.ENCOUNTERS_TXT_PATH}', 'r') as file: encounter_counter = int(file.read())

    stuck_timer = time()

    while not shutdown_event.is_set():
        image = Image_Processing(Video_Capture.read_frame())
        if isinstance(image.original_image, type(None)): sleep(0.1); continue

        image.resize_image()
        FPS.get_FPS()
        image.draw_FPS(FPS.FPS)
        image.get_mask()
        image.n_contours = image.get_rectangles()
        image.draw_star()

        Video_Capture.add_frame_to_video(image)

        # Don't care if any race condition
        if Controller.current_button_pressed != previous_button:
            switch_controller_image.draw_button(Controller.current_button_pressed)
            previous_button = Controller.current_button_pressed

        with Controller.event_lock: 
            Controller.current_event = search_wild_pokemon(image, Controller.current_event)
            if Controller.current_event not in ["MOVE_PLAYER", "WAIT_HOME_SCREEN", "SHINY_FOUND"] and \
                Controller.current_event == Controller.previous_event and \
                time() - stuck_timer > CONST.STUCK_TIMER_SECONDS:
                    stuck_timer = time()
                    # If stuck in "RESTART_GAME_1", it will stuck forever
                    Controller.previous_event = None
                    Controller.current_event = "RESTART_GAME_1"
            elif Controller.current_event != Controller.previous_event: stuck_timer = time()

            # Take a screenshot of the wild pokémon
            if Controller.current_event == "ENTER_COMBAT_1" and Controller.current_event != Controller.previous_event:
                Controller.previous_event = Controller.current_event
                encounter_counter += 1 
                with open(f'./{CONST.ENCOUNTERS_TXT_PATH}', 'w') as file: file.write(str(encounter_counter))
                Video_Capture.save_video()
                Video_Capture.start_recording()

            elif Controller.current_event == "SHINY_FOUND":
                if time() - stuck_timer > CONST.SHINY_RECORDING_SECONDS:
                    Video_Capture.save_video()

            Image_Queue.put([
                image, FPS.memory_usage, 
                switch_controller_image, 
                Controller.current_event, 
                shutdown_event, 
                encounter_counter
            ])

###########################################################################################################################

def controller_control(controller, shutdown_event):
    controller.connect_controller()

    while not shutdown_event.is_set(): 
        # Prevent the main execution from being blocked
        with controller.event_lock: aux_current_event = controller.current_event

        if aux_current_event == 'WAIT_HOME_SCREEN': fast_start_macro(controller)
        elif aux_current_event == 'RESTART_GAME_1': restart_game_macro(controller)
        elif aux_current_event in ['RESTART_GAME_2', 'RESTART_GAME_3']: 
            press_single_button(controller, 'A')
        elif aux_current_event == 'MOVE_PLAYER': move_player_wild_macro(controller)
        elif aux_current_event == 'ESCAPE_COMBAT_2': escape_combat_macro(controller)
        elif aux_current_event == 'SHINY_FOUND': 
            # Give some time to save the video before killing the bot
            sleep(CONST.SHINY_RECORDING_SECONDS + 15)
            stop_macro(controller)
            shutdown_event.set()

        # Don't care about race conditions here
        controller.previous_event = controller.current_event
        controller.current_button_pressed = ''
        sleep(0.1)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Shiny Hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Start wild shiny hunter'))

        # option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Shiny Hunter'))
        option = str(1)

        menu_options = {
            '1': wild_shiny_hunter,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Shiny Hunter') + '\n')

    #######################################################################################################################

    def wild_shiny_hunter(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Shiny Hunter')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Starting wild shiny hunter...")
            .replace('{path}', '')
        )

        # Saving images constantly can cause to run out of memory
        if len(os.listdir(f'./{CONST.IMAGES_FOLDER_PATH}')) - 1 > CONST.IMAGES_COUNT_WARNING:
            print(COLOR_str.IMAGES_COUNT_WARNING
                .replace('{module}', 'Shiny Hunter')
                .replace('{images}', str(len(os.listdir(f'./{CONST.IMAGES_FOLDER_PATH}')) - 1))
                .replace('{path}', f'./{CONST.IMAGES_FOLDER_PATH}')
            )

        FPS = FPS_Counter()
        Image_Queue = Queue()
        Controller = Switch_Controller()

        shutdown_event = Event()

        threads = []
        threads.append(Thread(target=lambda: GUI_control(FPS, Controller, Image_Queue, shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: controller_control(Controller, shutdown_event), daemon=True))
        for thread in threads: thread.start()

        # Blocking function until the GUI is closed
        User_Interface = GUI(Image_Queue)
        shutdown_event.set()

        print(COLOR_str.RELEASING_THREADS.replace('{module}', 'Shiny Hunter').replace('{threads}',
            str(len(threads))) + '\n')

        Controller.disconnect_controller()
        sleep(5)
        os.system('sudo pkill -9 python')

    #######################################################################################################################

    main_menu()