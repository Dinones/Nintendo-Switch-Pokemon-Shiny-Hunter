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

import copy
from time import sleep, time
from threading import Thread, Event

from Macros import *
from Database import *
import Constants as CONST
from Control_System import *
import Colored_Strings as COLOR_str
from FPS_Counter import FPS_Counter
from Game_Capture import Game_Capture
from GUI import GUI, DllistQueue, App
from Image_Processing import Image_Processing
from Switch_Controller import Switch_Controller

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def GUI_control(Encounter_Type, FPS, Controller, Image_Queue, shutdown_event, previous_button = None):
    Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
    if not Video_Capture.video_capture.isOpened(): 
        Video_Capture.stop()
        print(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'"))
        return
    Video_Capture.start_recording()

    switch_controller_image = Image_Processing(CONST.SWITCH_CONTROLLER_IMAGE_PATH)
    switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
    switch_controller_image.draw_button()

    stuck_timer = time()
    shiny_timer = time()
    initial_time = time()
    encounter_playtime = time()
    shiny_detection_time = 0

    database_data = get_all_data()
    local_encounters = database_data['global_encounters']
    global_encounters = database_data['global_encounters']
    last_shiny_encounter = database_data['last_shiny_encounter']

    while not shutdown_event.is_set():
        image = Image_Processing(Video_Capture.read_frame())
        if isinstance(image.original_image, type(None)): 
            if Video_Capture.skipped_frames < CONST.SKIPPED_FRAMES_TO_RECONNECT - 1: 
                Video_Capture.skipped_frames += 1
                sleep(0.1); continue
            Video_Capture.stop()
            Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
            if not Video_Capture.video_capture.isOpened(): 
                Video_Capture.stop()
                print(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'"))
                return
            continue

        image.resize_image()
        FPS.get_FPS()
        image.draw_FPS(FPS.FPS)

        Video_Capture.add_frame_to_video(image)

        # Don't care if any race condition
        if Controller.current_button_pressed != previous_button:
            switch_controller_image.draw_button(Controller.current_button_pressed)
            previous_button = Controller.current_button_pressed

        with Controller.event_lock: 
            # Check if the pokemon is shiny
            if Controller.current_event == "CHECK_SHINY":
                # Only reset the first time it enters to the state
                if time() - shiny_detection_time >= 10: shiny_detection_time = time()
                image.shiny_detection_time = shiny_detection_time

            # Refresh the event
            if Encounter_Type == 'WILD': Controller.current_event = search_wild_pokemon(image, Controller.current_event)
            elif Encounter_Type == 'STATIC': Controller.current_event = static_encounter(image, Controller.current_event)

            # Check if the program got stuck in some event
            if Controller.current_event not in ["MOVE_PLAYER", "WAIT_HOME_SCREEN", "SHINY_FOUND", "STOP"] and \
                Controller.current_event == Controller.previous_event and \
                time() - stuck_timer > CONST.STUCK_TIMER_SECONDS:
                    stuck_timer = time()
                    # If stuck in "RESTART_GAME_1", it would be stuck forever
                    Controller.previous_event = None
                    Controller.current_event = "RESTART_GAME_1"
                    if CONST.TESTING: Video_Capture.save_video(f'Error - {time()}')
            elif Controller.current_event != Controller.previous_event: stuck_timer = time()

            # Start recording a new video
            if Controller.current_event in ["ESCAPE_COMBAT_1", "RESTART_GAME_1"] \
                and Controller.current_event != Controller.previous_event:
                    Video_Capture.save_video()
                    Video_Capture.start_recording()

            # Update the database
            elif Controller.current_event == "ENTER_COMBAT_3": pokemon_image = image
            elif Controller.current_event == "CHECK_SHINY" and type(pokemon_image) != type(None): 
                pokemon_name = pokemon_image.recognize_pokemon()
                if CONST.SAVE_IMAGES: 
                    pokemon_image.save_image(pokemon_name)
                    # Check if the computer is running out of space
                    system_space = FPS.get_system_available_space()
                    if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE:
                        print(COLOR_str.RUNNING_OUT_OF_SPACE
                            .replace('{module}', 'Shiny Hunter')
                            .replace('{available_space}', system_space['available'])
                        )
                        # I'm changing the value of a constant. I know, I deserve to die!
                        CONST.SAVE_IMAGES = False
                pokemon_image = None
                pokemon = {'name': pokemon_name, 'shiny': False}
                add_or_update_encounter(pokemon, int(time() - encounter_playtime))
                global_encounters += 1
                encounter_playtime = time()

            # Wait some seconds to save the video of the shiny encounter
            elif Controller.current_event == "SHINY_FOUND":
                if time() - shiny_timer > CONST.SHINY_RECORDING_SECONDS:
                    pokemon = {'name': pokemon_name, 'shiny': True}
                    add_or_update_encounter(pokemon, int(time() - encounter_playtime))
                    Video_Capture.save_video(f'Shiny {pokemon_name} - {time()}')
                    Controller.current_event = "STOP"
            else: shiny_timer = time()

            update_items = {
                'image': image,
                'current_state': Controller.current_event,
                'shutdown_event': shutdown_event,
                'global_encounter_count': global_encounters - last_shiny_encounter,
                'local_encounter_count': global_encounters - local_encounters,
                'memory_usage': FPS.memory_usage,
                'switch_controller_image': switch_controller_image,
                'clock': int(time() - initial_time),
            }

            Image_Queue.put(update_items)

###########################################################################################################################

def controller_control(controller, shutdown_event):
    try: controller.connect_controller()
    except: return

    while not shutdown_event.is_set(): 
        # Prevent the main execution from being blocked
        with controller.event_lock: aux_current_event = controller.current_event

        if aux_current_event == 'WAIT_HOME_SCREEN': fast_start_macro(controller)
        elif aux_current_event == 'RESTART_GAME_1': restart_game_macro(controller)
        elif aux_current_event in ['RESTART_GAME_2', 'RESTART_GAME_3', 'ENTER_STATIC_COMBAT', 'ESCAPE_FAILED_2']: 
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

    try: controller.disconnect_controller()
    except: return

###########################################################################################################################

# Check if all threads are alive or if they have raised an error
def check_threads(threads, shutdown_event):
    while not shutdown_event.is_set():
        for thread in threads:
            if not thread['thread'].is_alive():
                print(COLOR_str.THREAD_DIED_ERROR
                    .replace('{module}', 'Shiny Hunter')
                    .replace('{thread}', thread['function'])
                )
                shutdown_event.set()
        sleep(5)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Shiny Hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Start wild shiny hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Start static shiny hunter'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Shiny Hunter'))

        menu_options = {
            '1': shiny_hunter,
            '2': shiny_hunter,
        }

        # Set XDG_RUNTIME_DIR environment variable (avoid unnecessary warnings)
        os.environ['XDG_RUNTIME_DIR'] = "/tmp/runtime-root"
        os.makedirs(os.environ['XDG_RUNTIME_DIR'], exist_ok=True)
        os.chmod(os.environ['XDG_RUNTIME_DIR'], 0o700)

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Shiny Hunter') + '\n')

    #######################################################################################################################

    def shiny_hunter(option):
        if option == '1': action = 'wild'
        elif option == '2': action = 'static'
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Shiny Hunter')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Starting {action} shiny hunter...")
            .replace('{path}', '')
        )

        FPS = FPS_Counter()
        # Constantly saving images can cause to run out of space
        images_folder_size = FPS.get_directory_size(CONST.IMAGES_FOLDER_PATH)
        if len(os.listdir(f'./{CONST.IMAGES_FOLDER_PATH}')) - 1 > CONST.IMAGES_COUNT_WARNING:
            print(COLOR_str.IMAGES_COUNT_WARNING
                .replace('{module}', 'Shiny Hunter')
                .replace('{images}', str(len(os.listdir(f'./{CONST.IMAGES_FOLDER_PATH}')) - 1))
                .replace('{path}', f'./{CONST.IMAGES_FOLDER_PATH}')
                .replace('{size}', images_folder_size)
            )
        system_space = FPS.get_system_available_space()
        if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE:
            print(COLOR_str.AVAILABLE_SPACE_ERROR
                .replace('{module}', 'Shiny Hunter')
                .replace('{available_space}',
                    f"{FPS.format_space_size(CONST.CRITICAL_AVAILABLE_SPACE)} ({system_space['available']})")
            )
            delete = input(COLOR_str.DELETE_IMAGES_QUESTION)
            if delete.lower().strip() in ('', 'y', 'yes'): 
                images = sorted([image for image in sorted(os.listdir(f'./{CONST.IMAGES_FOLDER_PATH}')) 
                    if image.lower().endswith(('.png', '.jpg', 'jpeg'))])
                print(COLOR_str.DELETING_IMAGES.replace('{images}', str(len(images))))
                for image in images: os.remove(f'./{CONST.IMAGES_FOLDER_PATH}/{image}')
                print(COLOR_str.SUCCESSFULLY_DELETED_IMAGES.replace('{images}', str(len(images))))

                system_space = FPS.get_system_available_space()
                if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE: 
                    print(COLOR_str.AVAILABLE_SPACE_ERROR
                        .replace('{module}', 'Shiny Hunter')
                        .replace('{available_space}',
                            f"{FPS.format_space_size(CONST.CRITICAL_AVAILABLE_SPACE)} ({system_space['available']})")
                    )
                    return
            else: return print()

        # Image_Queue = DllistQueue(maxsize = 2)
        from queue import Queue
        Image_Queue = Queue()
        Controller = Switch_Controller()
        initialize_database()

        shutdown_event = Event()
        stop_event = Event()

        threads = []
        if option == '1': encounter_type = 'WILD'
        if option == '2': encounter_type = 'STATIC'
        threads.append({
            'function': 'GUI_control',
            'thread': Thread(target=lambda: 
                GUI_control(encounter_type, FPS, Controller, Image_Queue, shutdown_event), daemon=True)
        })
        threads.append({
            'function': 'get_memory_usage',
            'thread': Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True)
        })
        threads.append({
            'function': 'controller_control',
            'thread': Thread(target=lambda: controller_control(Controller, shutdown_event), daemon=True)
        })
        threads.append({
            'function': 'check_threads',
            'thread': Thread(target=lambda: check_threads(threads, shutdown_event), daemon=True)
        })
        for thread in threads: thread['thread'].start()

        GUI_App = App()
        User_Interface = GUI(Image_Queue, shutdown_event, stop_event)
        # Blocking function until the GUI is closed
        GUI_App.exec_()
        shutdown_event.set()

        print(COLOR_str.RELEASING_THREADS
            .replace('{module}', 'Shiny Hunter')
            .replace('{threads}', str(len(threads))) + '\n'
        )

    #######################################################################################################################

    main_menu()