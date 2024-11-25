###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
folders = ['Modules', 'Modules/Mail', 'Modules/Telegram']
for folder in folders: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))
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

import logging
from queue import Queue
from time import sleep, time
from threading import Thread, Event, Timer

from Macros import *
from Database import *
import Constants as CONST
from Control_System import *
from Mail import Email_Sender
from FPS_Counter import FPS_Counter
from Telegram import Telegram_Sender
from GUI import GUI, App, play_sound
from Game_Capture import Game_Capture
from Image_Processing import Image_Processing
from Switch_Controller import Switch_Controller

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

Email = Email_Sender()
Telegram = Telegram_Sender()

###########################################################################################################################

def GUI_control(Encounter_Type, FPS, Controller, Image_Queue, shutdown_event, stop_event):
    Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
    if not Video_Capture.video_capture.isOpened(): 
        Video_Capture.stop()
        print(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'"))
        return
    Video_Capture.start_recording()

    switch_controller_image = Image_Processing(CONST.SWITCH_CONTROLLER_IMAGE_PATH)
    if isinstance(switch_controller_image.original_image, type(None)):
        print(COLOR_str.INVALID_PATH_ERROR
            .replace('{module}', 'Shiny Hunter')
            .replace('{path}', f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}')
        )
        return
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

    last_saved_image_path = str()

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
        if Controller.current_button_pressed != Controller.previous_button_pressed:
            switch_controller_image.draw_button(Controller.current_button_pressed)
            Controller.previous_button_pressed = Controller.current_button_pressed

        with Controller.event_lock:
            # Check if the pokemon is shiny
            if Controller.current_event == "CHECK_SHINY":
                # Only reset the first time it enters to the state
                if time() - shiny_detection_time >= 10: shiny_detection_time = time()
                image.shiny_detection_time = shiny_detection_time

            # Refresh the event
            if Encounter_Type == 'WILD': Controller.current_event = search_wild_pokemon(image, Controller.current_event)
            elif Encounter_Type == 'STATIC': Controller.current_event = static_encounter(image, Controller.current_event)
            elif Encounter_Type == 'STARTER': Controller.current_event = starter_encounter(image, Controller.current_event)
            elif Encounter_Type == 'SHAYMIN': Controller.current_event = shaymin_encounter(image, Controller.current_event)
            elif Encounter_Type == 'SWSH_GIANTS': Controller.current_event = sword_shield_giants(image, Controller.current_event)

            # If stuck in the same state for STUCK_TIMER_SECONDS, restart the game
            if (Controller.current_event not in 
                ["MOVE_PLAYER", "WAIT_PAIRING_SCREEN", "WAIT_HOME_SCREEN", "SHINY_FOUND", "ENTER_LAKE_4"] and \
                Controller.current_event == Controller.previous_event and \
                time() - stuck_timer > CONST.STUCK_TIMER_SECONDS):
                    print(COLOR_str.STUCK_FOR_TOO_LONG_WARN_1
                        .replace('{module}', 'Shiny Hunter')
                        .replace('{event}', Controller.current_event)
                        .replace('{seconds}', str(CONST.STUCK_TIMER_SECONDS))
                    )
                    stuck_timer = time()
                    # If stuck in "RESTART_GAME_1", it would be stuck forever
                    Controller.previous_event = None
                    Controller.current_event = "RESTART_GAME_1"
                    if CONST.SAVE_ERROR_VIDEOS: Video_Capture.save_video(f'State Stuck Error - {time()}')
            # If stuck in a loop where state changes, but no pokémon is found, restart the game
            elif Controller.current_event not in \
                ["RESTART_GAME_1", "WAIT_PAIRING_SCREEN", "WAIT_HOME_SCREEN", "SHINY_FOUND", "ENTER_LAKE_4"] and \
                CONST.FAILURE_DETECTION_TIME_WARN < time() - encounter_playtime < CONST.FAILURE_DETECTION_TIME_WARN + 3:
                    print(COLOR_str.STUCK_FOR_TOO_LONG_WARN_2
                        .replace('{module}', 'Shiny Hunter')
                        .replace('{minutes}', str(CONST.FAILURE_DETECTION_TIME_WARN//60))
                    )
                    stuck_timer = time()
                    Controller.current_event = "RESTART_GAME_1"
                    if CONST.SAVE_ERROR_VIDEOS: Video_Capture.save_video(f'Loop Stuck Error - {time()}')
            # If no pokemon is found for FAILURE_DETECTION_TIME_ERROR, stop the program
            elif Controller.current_event != 'SHINY_FOUND' and \
                time() - encounter_playtime > CONST.FAILURE_DETECTION_TIME_ERROR:
                    Thread(target=lambda: Telegram.send_error_detected('STUCK'), daemon=False).start()
                    Thread(target=lambda: Email.send_error_detected('STUCK'), daemon=False).start()
                    print(COLOR_str.STUCK_FOR_TOO_LONG_ERROR
                        .replace('{module}', 'Shiny Hunter')
                        .replace('{minutes}', str(CONST.FAILURE_DETECTION_TIME_ERROR//60))
                    )
                    shutdown_event.set()
            elif Controller.current_event != Controller.previous_event: stuck_timer = time()

            # Start recording a new video
            if Controller.current_event in ["ESCAPE_COMBAT_1", "RESTART_GAME_1"] \
                and Controller.current_event != Controller.previous_event:
                    Video_Capture.save_video()
                    Video_Capture.start_recording()

            # Save the last frame where the name of the pokemon appears in the text box
            elif Controller.current_event in ['ENTER_COMBAT_3', 'ENTER_COMBAT_5', 'SWSH_ENTER_GIANTS_COMBAT_2']:
                pokemon_image = image

            # Update the database
            elif Controller.current_event == "CHECK_SHINY" and type(pokemon_image) != type(None):
                pokemon_name = pokemon_image.recognize_pokemon()
                if CONST.SAVE_IMAGES: 
                    pokemon_image.save_image(pokemon_name)
                    last_saved_image_path = pokemon_image.saved_image_path
                    # Check if the computer is running out of space
                    system_space = FPS.get_system_available_space()
                    if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE:
                        print(COLOR_str.RUNNING_OUT_OF_SPACE
                            .replace('{module}', 'Shiny Hunter')
                            .replace('{available_space}', system_space['available'])
                        )
                        # I'm editing the value of a constant. I know, I deserve to die!
                        CONST.SAVE_IMAGES = False; CONST.SAVE_ERROR_VIDEOS = False
                pokemon_image = None
                pokemon = {'name': pokemon_name, 'shiny': False}
                add_or_update_encounter(pokemon, int(time() - encounter_playtime))
                global_encounters += 1
                encounter_playtime = time()

            # Wait some seconds to save the video of the shiny encounter
            elif Controller.current_event == "SHINY_FOUND":
                # It sometimes gets bugged and detects the Starly instead of the starter, which will raise always 
                # a false positive due to the amount of time between the text boxes
                if (Encounter_Type == 'STARTER' and pokemon_name in ['Starly', 'Étourmi', 'Staralili']) or \
                    (pokemon_name == ''): 
                        Controller.current_event = "RESTART_GAME_1"
                elif time() - shiny_timer > CONST.SHINY_RECORDING_SECONDS:
                    pokemon = {'name': pokemon_name, 'shiny': True}
                    add_or_update_encounter(pokemon, int(time() - encounter_playtime))
                    Video_Capture.save_video(f'Shiny {pokemon_name} - {time()}')
                    Thread(target=lambda: play_sound(f'./{CONST.SHINY_SOUND_PATH}'), daemon=True).start()
                    Thread(target=lambda: 
                        Email.send_shiny_found(
                            pokemon_name,
                            last_saved_image_path,
                            global_encounters - last_shiny_encounter
                        ), daemon=False
                    ).start()
                    Thread(target=lambda: 
                        Telegram.send_shiny_found(
                            pokemon_name,
                            last_saved_image_path,
                            global_encounters - last_shiny_encounter
                        ), daemon=False
                    ).start()
                    print(COLOR_str.SHINY_FOUND
                        .replace('{module}', 'Shiny Hunter')
                        .replace('{pokemon}', pokemon_name)
                        .replace('{encounters}', str(global_encounters - last_shiny_encounter))
                    )
                    stop_event.set()
            else: shiny_timer = time()

            # Stop program execution (shiny found or stop button pressed)
            if stop_event.is_set() and Controller.current_event not in ["STOP_1", "STOP_2", "STOP_3"]:
                Controller.current_event = "STOP_1"
            elif Controller.current_event == "STOP_2":
                def _stop_execution(Video_Capture, shutdown_event):
                    try: Video_Capture.save_video()
                    except: pass
                    shutdown_event.set()
                Timer(3, lambda: _stop_execution(Video_Capture, shutdown_event)).start()
                Controller.current_event = "STOP_3"

            update_items = {
                'image': image,
                'current_state': Controller.current_event,
                'shutdown_event': shutdown_event,
                'global_encounter_count': global_encounters - last_shiny_encounter,
                'local_encounter_count': global_encounters - local_encounters,
                'memory_usage': FPS.memory_usage,
                'cpu_usage': FPS.cpu_usage,
                'switch_controller_image': switch_controller_image,
                'clock': int(time() - initial_time),
            }

            Image_Queue.put(update_items)

###########################################################################################################################
###########################################################################################################################

def controller_control(controller, shutdown_event):
    try: controller.connect_controller()
    except: return

    while not shutdown_event.is_set(): 
        # Prevent the main execution from being blocked
        with controller.event_lock: aux_current_event = controller.current_event

        # Macros that require A button press
        # ENTER_STATIC_COMBAT_3 needs to press A to enter the combat for Regigigas, it has two dialog phases.
        need_to_press_a_states = ['RESTART_GAME_2', 'RESTART_GAME_3', 'ENTER_STATIC_COMBAT_2', 'ENTER_STATIC_COMBAT_3',
                  'ESCAPE_FAILED_2', 'ENTER_LAKE_2', 'ENTER_LAKE_4']

        if aux_current_event == 'WAIT_HOME_SCREEN': fast_start_macro(controller)
        elif aux_current_event == 'RESTART_GAME_1': restart_game_macro(controller)
        elif aux_current_event in need_to_press_a_states: press_single_button(controller, 'A')
        elif aux_current_event == 'SWSH_ENTER_GIANTS_COMBAT_1': press_button(controller, 'A', 0.3)
        elif aux_current_event == 'ENTER_STATIC_COMBAT_1': enter_static_combat_macro(controller)
        elif aux_current_event == 'MOVE_PLAYER': move_player_wild_macro(controller)
        elif aux_current_event == 'ENTER_LAKE_1': enter_lake_macro(controller)
        elif aux_current_event == 'STARTER_SELECTION_2': select_starter_macro(controller)
        elif aux_current_event == 'STARTER_SELECTION_3': accept_selection_box_macro(controller)
        elif aux_current_event == 'ESCAPE_COMBAT_2': escape_combat_macro(controller)
        elif aux_current_event == 'STOP_1': stop_macro(controller)
        elif aux_current_event == 'RESPAWN_SHAYMIN': bdsp_respawn_shaymin(controller)

        # Don't care about race conditions here
        controller.previous_event = aux_current_event
        controller.current_button_pressed = ''
        sleep(0.1)

    try: controller.disconnect_controller()
    except: return

###########################################################################################################################
###########################################################################################################################

# Check if all threads are alive or if they have raised an error
def check_threads(threads, shutdown_event):
    while not shutdown_event.is_set():
        for thread in threads:
            if not thread['thread'].is_alive():
                play_sound(f'./{CONST.ERROR_SOUND_PATH}')
                print(COLOR_str.THREAD_DIED_ERROR
                    .replace('{module}', 'Shiny Hunter')
                    .replace('{thread}', thread['function'])
                )
                Thread(
                    target=lambda: Telegram.send_error_detected('THREAD_DIED', thread['function']), daemon=False
                ).start()
                Thread(target=lambda: Email.send_error_detected('THREAD_DIED', thread['function']), daemon=False).start()
                shutdown_event.set()
        sleep(5)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":

    logging.basicConfig(
        level=CONST.LOG_LEVEL,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Shiny Hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Start wild shiny hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Start static shiny hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '3').replace('{option}', 'Start starter shiny hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '4').replace('{option}', 'Start Shaymin shiny hunter'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '5').replace('{option}', 'Start Sword/Shield Giants shiny hunter'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Shiny Hunter'))

        menu_options = {
            '1': shiny_hunter,
            '2': shiny_hunter,
            '3': shiny_hunter,
            '4': shiny_hunter,
            '5': shiny_hunter,
        }

        # Set XDG_RUNTIME_DIR and ALSOFT_LOGLEVEL environment variable (avoid unnecessary warnings)
        os.environ['XDG_RUNTIME_DIR'] = "/tmp/runtime-root"
        os.makedirs(os.environ['XDG_RUNTIME_DIR'], exist_ok=True)
        os.chmod(os.environ['XDG_RUNTIME_DIR'], 0o700)
        os.environ['ALSOFT_LOGLEVEL'] = '0'

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Shiny Hunter') + '\n')

    
    #######################################################################################################################
    #######################################################################################################################

    def shiny_hunter(option):
        if option == '1': action = 'wild'
        elif option == '2': action = 'static'
        elif option == '3': action = 'starter'
        elif option == '4': action = 'Shaymin'
        elif option == '5': action = 'SWSH Giants'
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Shiny Hunter')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Starting {action} shiny hunter...")
            .replace('{path}', '')
        )

        ###################################################################################################################
        ###################################################################################################################
        
        # Check system's available space. Constantly saving images can cause to run out of space

        FPS = FPS_Counter()

        # Check the Media/Images/ folder
        media_folder_size = FPS.get_directory_size(CONST.IMAGES_FOLDER_PATH)
        if len(os.listdir(f'./{CONST.IMAGES_FOLDER_PATH}')) - 1 > CONST.IMAGES_COUNT_WARNING:
            print(COLOR_str.IMAGES_COUNT_WARNING
                .replace('{module}', 'Shiny Hunter')
                .replace('{images}', str(len(os.listdir(f'./{CONST.IMAGES_FOLDER_PATH}')) - 1))
                .replace('{path}', f'./{CONST.IMAGES_FOLDER_PATH}')
                .replace('{size}', media_folder_size)
            )

        # Check if the recycle bin size is greater than 1GB 
        recycle_bin_size = FPS.get_directory_size(os.path.expanduser('~/.local/share/Trash/files'))
        if recycle_bin_size[-2:] == 'GB':
            print(COLOR_str.USED_SPACE_WARNING
                .replace('{module}', 'Shiny Hunter')
                .replace('{path}', f"Recycle Bin")
                .replace('{used_space}', recycle_bin_size)
            )

        # Check whole system available space
        system_space = FPS.get_system_available_space()
        if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE:
            print(COLOR_str.AVAILABLE_SPACE_ERROR
                .replace('{module}', 'Shiny Hunter')
                .replace('{threshold}', FPS.format_space_size(CONST.CRITICAL_AVAILABLE_SPACE))
                .replace('{available_space}', f"{system_space['available']}")
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
                        .replace('{threshold}', FPS.format_space_size(CONST.CRITICAL_AVAILABLE_SPACE))
                        .replace('{available_space}', f"{system_space['available']}")
                    )
                    return
            else: return print()

        ###################################################################################################################
        ###################################################################################################################

        Image_Queue = Queue()
        Controller = Switch_Controller()
        initialize_database()

        shutdown_event = Event()
        stop_event = Event()

        if option == '1': encounter_type = 'WILD'
        elif option == '2': encounter_type = 'STATIC'
        elif option == '3': encounter_type = 'STARTER'
        elif option == '4': encounter_type = 'SHAYMIN'
        elif option == '5': encounter_type = 'SWSH_GIANTS'

        threads = []
        threads.append({
            'function': 'GUI_control',
            'thread': Thread(target=lambda: 
                GUI_control(encounter_type, FPS, Controller, Image_Queue, shutdown_event, stop_event), daemon=True)
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
    #######################################################################################################################

    main_menu()
