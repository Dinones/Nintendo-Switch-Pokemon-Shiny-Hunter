###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import copy
from time import sleep, time, perf_counter
from threading import Thread, Timer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
from Modules.Macros import *
from Modules.Database import *
from Modules.GUI import play_sound
from Modules.State_Machine import *
import Modules.Colored_Strings as STR
from Modules.Email.Email import Email_Sender
from Modules.Game_Capture import Game_Capture
from Modules.Telegram.Telegram import Telegram_Sender
from Modules.Image_Processing import Image_Processing, Debug_Image

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Control System'

SWITCH_CONTROLLER_IMAGE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', CONST.SWITCH_CONTROLLER_IMAGE_PATH)
)

stuck_timer = time()
shiny_timer = time()
initial_time = time()
encounter_playtime = time()
last_saved_image_path = ''

Email = Email_Sender()
Telegram = Telegram_Sender()

###########################################################################################################################
###########################################################################################################################

def _initialize_switch_controller_image():
    # Initialize the swith controller image where the pressed buttons are printed in real time
    switch_controller_image = Image_Processing(SWITCH_CONTROLLER_IMAGE_PATH)
    if switch_controller_image.original_image is None:
        print(STR.G_INVALID_PATH_ERROR.format(module=MODULE_NAME, path=SWITCH_CONTROLLER_IMAGE_PATH))
        return

    switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
    # No button is drawn, but ensures the FPS image exists
    switch_controller_image.draw_button()

    return switch_controller_image

###########################################################################################################################
###########################################################################################################################

def _get_database_components():
    # Ensure the database is created
    initialize_database()
    database_data = get_all_data()
    local_encounters = database_data['global_encounters']
    global_encounters = database_data['global_encounters']
    last_shiny_encounter = database_data['last_shiny_encounter']

    return local_encounters, global_encounters, last_shiny_encounter

###########################################################################################################################
###########################################################################################################################

def _draw_switch_controller_buttons(Controller, switch_controller_image):
    # Not blocking, don't care if any race condition
    if Controller.current_button_pressed != Controller.previous_button_pressed:
        switch_controller_image.draw_button(Controller.current_button_pressed)
        Controller.previous_button_pressed = Controller.current_button_pressed

###########################################################################################################################
###########################################################################################################################

def _is_program_stuck(Controller, Video_Capture, shutdown_event):
    global stuck_timer, encounter_playtime


    # If stuck in the same state for STUCK_TIMER_SECONDS, restart the game
    skip_states = ("MOVE_PLAYER", "WAIT_PAIRING_SCREEN", "WAIT_HOME_SCREEN", "SHINY_FOUND", "ENTER_LAKE_4")
    if (
        Controller.current_event not in skip_states and
        Controller.current_event == Controller.previous_event and
        time() - stuck_timer > CONST.STUCK_TIMER_SECONDS
    ):
        stuck_timer = time()
        encounter_playtime = time()

        # If got stuck in "RESTART_GAME_1", it would be stuck forever
        Controller.previous_event = None
        Controller.current_event = "RESTART_GAME_1"

        print(STR.STUCK_FOR_TOO_LONG_WARN_1.format(
            module=MODULE_NAME,
            event=Controller.current_event,
            seconds=CONST.STUCK_TIMER_SECONDS
        ))

        # Save the error video
        if CONST.SAVE_ERROR_VIDEOS:
            Video_Capture.save_video(f'State Stuck Error - {time()}')
        return
    
    # If stuck in a loop where state changes, but no pokémon is found for FAILURE_DETECTION_SECONDS_WARN, restart the game
    skip_states = ("RESTART_GAME_1", "WAIT_PAIRING_SCREEN", "WAIT_HOME_SCREEN", "SHINY_FOUND", "ENTER_LAKE_4")
    if (
        Controller.current_event not in skip_states and
        time() - encounter_playtime > CONST.FAILURE_DETECTION_SECONDS_WARN
    ):
        stuck_timer = time()
        encounter_playtime = time()

        # If got stuck in "RESTART_GAME_1", it would be stuck forever
        Controller.previous_event = None
        Controller.current_event = "RESTART_GAME_1"

        print(STR.STUCK_FOR_TOO_LONG_WARN_2.format(module=MODULE_NAME, minutes=CONST.FAILURE_DETECTION_SECONDS_WARN//60))

        # Save the error video
        if CONST.SAVE_ERROR_VIDEOS:
            Video_Capture.save_video(f'Loop Stuck Error - {time()}')
        return

    # If no pokemon is found for FAILURE_DETECTION_SECONDS_ERROR, stop the program
    if (
        Controller.current_event != 'SHINY_FOUND' and
        time() - encounter_playtime > CONST.FAILURE_DETECTION_SECONDS_ERROR
    ):
        # Send Telegram and Email notifications
        Thread(target=lambda: Telegram.send_error_detected('STUCK'), daemon=False).start()
        Thread(target=lambda: Email.send_error_detected('STUCK'), daemon=False).start()

        print(STR.STUCK_FOR_TOO_LONG_ERROR.format(module=MODULE_NAME, minutes=CONST.FAILURE_DETECTION_SECONDS_ERROR//60))
        shutdown_event.set()
        return
    
    elif Controller.current_event != Controller.previous_event:
        stuck_timer = time()

###########################################################################################################################
###########################################################################################################################

def _record_new_video(Controller, Video_Capture):
    # Start recording a new video after a non-shiny pokémon is found. Ovewrites the older one
    if (
        Controller.current_event in ("ESCAPE_COMBAT_1", "RESTART_GAME_1") and
        Controller.current_event != Controller.previous_event
    ):
            Video_Capture.save_video()
            Video_Capture.start_recording()

###########################################################################################################################
###########################################################################################################################

def _update_database(FPS, Controller, Video_Capture, stop_event, pokemon_image, encounter_type, last_shiny_encounter):
    global shiny_timer

    # A new pokemon has been found. Don't know if shiny or not yet
    if Controller.current_event == "CHECK_SHINY" and pokemon_image is not None:
        # Extract the pokemon name from the image
        pokemon_name = pokemon_image.recognize_pokemon()

        # Save the image
        if CONST.SAVE_IMAGES: 
            pokemon_image.save_image(pokemon_name)
            # This path will be used to attach the image if the pokémon is shiny
            last_saved_image_path = pokemon_image.saved_image_path

            # Check if the computer is running out of space. If it is, disable the image saving
            system_space = FPS.get_system_available_space()
            if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE:
                CONST.SAVE_IMAGES = False
                CONST.SAVE_ERROR_VIDEOS = False

                print(STR.RUNNING_OUT_OF_SPACE.format(module=MODULE_NAME, available_space=system_space['available']))

        # Update the database with the new encounter (always non-shiny, if it results to be shiny, it's updated afterwards)
        global_encounters += 1
        pokemon = {'name': pokemon_name, 'shiny': False}
        add_or_update_encounter(pokemon, int(time() - encounter_playtime))

        encounter_playtime = time()
        # Start the timer so if the pokémon is shiny, the video records for SHINY_RECORDING_SECONDS before stopping
        shiny_timer = time()
        pokemon_image = None

        return last_saved_image_path

    elif Controller.current_event == "SHINY_FOUND":
        # It sometimes gets bugged and detects the Starly instead of the starter, which will raise always a false positive
        # due to the amount of time between the text boxes. It also restarts the game if no pokémon name is detected
        if (
            (encounter_type == 'STARTER' and pokemon_name in ['Starly', 'Étourmi', 'Staralili']) or
            (pokemon_name == '')
        ):
            Controller.current_event = "RESTART_GAME_1"
        
        # If a shiny has been found, wait SHINY_RECORDING_SECONDS to record the encounter video
        elif time() - shiny_timer > CONST.SHINY_RECORDING_SECONDS:
            # Add a shiny to the pokémon table in the database 
            pokemon = {'name': pokemon_name, 'shiny': True}
            add_or_update_encounter(pokemon, int(time() - encounter_playtime))

            # Save the video of the shiny encounter
            Video_Capture.save_video(f'Shiny {pokemon_name} - {time()}')

            # Play a sound so the user can hear a shiny has been found
            sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.CONST.SHINY_SOUND_PATH))
            Thread(target=lambda: play_sound(sound_path), daemon=True).start()
            
            # Send a notification to the user (does nothing if notifications are disabled)
            for notification in (Email, Telegram):
                Thread(target=lambda: 
                    notification.send_shiny_found(
                        pokemon_name, 
                        last_saved_image_path, 
                        global_encounters - last_shiny_encounter
                    ), daemon=False
                ).start()

            print(STR.SHINY_FOUND.format(
                module=MODULE_NAME,
                pokemon=pokemon_name,
                encounters=global_encounters - last_shiny_encounter
            ))

            stop_event.set()

###########################################################################################################################
###########################################################################################################################

def _stop_execution(Controller, Video_Capture, stop_event, shutdown_event):
    if stop_event.is_set() and Controller.current_event not in ("STOP_1", "STOP_2", "STOP_3"):
        Controller.current_event = "STOP_1"

    # Stop macro has been executed
    elif Controller.current_event == "STOP_2":

        def _shutdown(Video_Capture, shutdown_event):
            try: Video_Capture.save_video()
            except: pass
            shutdown_event.set()

        Timer(3, lambda: _shutdown(Video_Capture, shutdown_event)).start()
        Controller.current_event = "STOP_3"

###########################################################################################################################
###########################################################################################################################

def start_control_system(Encounter_Type, FPS, Controller, Image_Queue, shutdown_event, stop_event):

    Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
    # Could not connect to the capture card
    if not Video_Capture.video_capture.isOpened(): 
        Video_Capture.stop()
        print(STR.GC_INVALID_VIDEO_CAPTURE.format(video_capture=CONST.VIDEO_CAPTURE_INDEX))
        return
    Video_Capture.start_recording()

    # Initialize the swith controller image where the pressed buttons are printed in real time
    switch_controller_image = _initialize_switch_controller_image()
    if not switch_controller_image:
        return

    # Get the global stats of the database (create a new database if it doesn't exist)
    local_encounters, global_encounters, last_shiny_encounter = _get_database_components()
    pokemon_image = None

    if CONST.DEBUG_VIDEO:
        debug_image = Debug_Image()

    while not shutdown_event.is_set():

        # Start a perfect counter to force a maximum of 60 FPS
        iteration_start_time = perf_counter()   

        image = Image_Processing(Video_Capture.read_frame())
        image.resize_image()

        # Check the video capture is not disconnected
        if Video_Capture.previous_frame_skipped:
            if time() - Video_Capture.last_frame_time > CONST.STUCK_TIMER_SECONDS:
                print(STR.GC_INVALID_VIDEO_CAPTURE.format(video_capture=CONST.VIDEO_CAPTURE_INDEX))
                shutdown_event.set()
            # Force a maximum of 60 FPS
            sleep(max(0, 0.016 - (perf_counter() - iteration_start_time)))
            continue

        # Get the current FPS and draw them at the top-left corner of the image
        FPS.get_FPS()
        image.draw_FPS(FPS.FPS)

        _draw_switch_controller_buttons(Controller, switch_controller_image)

        # Blocking so no race condition occurs
        with Controller.event_lock: 
            # Get the next state
            Controller.current_event = get_next_state(image, Controller.current_event, Encounter_Type)

            # Check if the program is stuck. If it is, try to solve the issue by restarting the game. If cannot, stop the 
            # program execution and notify the user (if notifications are enabled)
            _is_program_stuck(Controller, Video_Capture, shutdown_event)

            # Start recording a new video after a non-shiny pokémon is found. Ovewrites the older one
            _record_new_video(Controller, Video_Capture)

            # Save the last frame where the name of the pokemon appears in the text box. This is the image that will be
            # attached to the notification if the pokémon is shiny
            if Controller.current_event in ('ENTER_COMBAT_3', 'ENTER_COMBAT_5'):
                pokemon_image = image

            _update_database(
                FPS, Controller, Video_Capture, stop_event, pokemon_image, Encounter_Type, last_shiny_encounter
            )

            # Stop program execution (shiny found or stop button pressed)
            _stop_execution(Controller, Video_Capture, stop_event, shutdown_event)
            
            # Items needed to update the GUI
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
    # Connect the controller
    try:
        controller.connect_controller()
    except:
        return

    while not shutdown_event.is_set(): 
        # Prevent the main execution from being blocked
        with controller.event_lock:
            aux_current_event = controller.current_event

        # Macros that require A button press
        # ENTER_STATIC_COMBAT_3 needs to press A to enter the combat for Regigigas, it has two dialog phases.
        press_A_states = (
            'RESTART_GAME_2', 'RESTART_GAME_3', 'ENTER_STATIC_COMBAT_2', 'ENTER_STATIC_COMBAT_3', 'ESCAPE_FAILED',
            'ENTER_LAKE_2', 'ENTER_LAKE_4'
        )

        if aux_current_event == 'WAIT_HOME_SCREEN': fast_start_macro(controller)
        elif aux_current_event == 'RESTART_GAME_1': restart_game_macro(controller)
        elif aux_current_event in press_A_states: press_single_button(controller, 'A')
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

    # Disconnect the controller
    try:
        controller.disconnect_controller()
    except:
        return

###########################################################################################################################
###########################################################################################################################

# Check if all threads are alive or if they have raised an error
def check_threads(threads, shutdown_event):
    while not shutdown_event.is_set():
        for thread in threads:
            if not thread['thread'].is_alive():
                
                # Play a sound so the user can hear an error has occurred
                sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.ERROR_SOUND_PATH))
                play_sound(sound_path)
            
                # Send a notification to the user (does nothing if notifications are disabled)
                for notification in (Email, Telegram):
                    Thread(
                        target=lambda: notification.send_error_detected('THREAD_DIED', thread['function']), daemon=False
                    ).start()

                print(STR.THREAD_DIED_ERROR.format(module=MODULE_NAME, thread=thread['function']))
                shutdown_event.set()

        # Wait 5s to check again
        sleep(5)