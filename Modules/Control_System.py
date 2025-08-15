###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from __future__ import annotations

import os
import sys
from datetime import datetime
from threading import Thread, Timer
from time import sleep, time, perf_counter
from typing import Any, Optional, Literal, TYPE_CHECKING

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

if TYPE_CHECKING:
    from queue import Queue
    from threading import Event
    from Modules.FPS_Counter import FPS_Counter
    from Modules.Switch_Controller import Switch_Controller

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

def _initialize_switch_controller_image() -> Optional[Image_Processing]:

    """
    Initialize the image used to display the Nintendo Switch controller with real-time button updates.

    Args:
        None

    Returns:
        Optional[Image_Processing]: The initialized image object or None if loading fails.
    """

    # Load the base image for the controller overlay
    switch_controller_image = Image_Processing(SWITCH_CONTROLLER_IMAGE_PATH)

    # Return if the image could not be loaded
    if switch_controller_image.original_image is None:
        print(STR.G_INVALID_PATH_ERROR.format(module=MODULE_NAME, path=SWITCH_CONTROLLER_IMAGE_PATH))
        return

    # Resize the image
    switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)

    # No button is drawn, but ensures the FPS image exists
    switch_controller_image.draw_button()

    return switch_controller_image

###########################################################################################################################
###########################################################################################################################

def _get_database_components() -> Tuple[int, int, int]:

    """
    Retrieve encounter data from the database after ensuring it is initialized.

    Args:
        None

    Returns:
        int: Local encounter count
        int: Global encounter count
        int: Last shiny encounter number
    """

    # Ensure the database exists
    initialize_database()

    # Retrieve all stored data
    database_data = get_all_data()

    local_encounters = database_data['global_encounters']
    global_encounters = database_data['global_encounters']
    last_shiny_encounter = database_data['last_shiny_encounter']

    return local_encounters, global_encounters, last_shiny_encounter

###########################################################################################################################
###########################################################################################################################

def _draw_switch_controller_buttons(Controller: Switch_Controller, switch_controller_image: Image_Processing) -> None:

    """
    Update the controller image by drawing the button currently being pressed.

    Args:
        Controller (Switch_Controller): The controller object tracking button states.
        switch_controller_image (Image_Processing): The image object where buttons are drawn.

    Returns:
        None
    """

    # Not blocking, don't care if any race condition
    # Update the image only if the button has changed
    if Controller.current_button_pressed != Controller.previous_button_pressed:
        switch_controller_image.draw_button(Controller.current_button_pressed)
        Controller.previous_button_pressed = Controller.current_button_pressed

###########################################################################################################################
###########################################################################################################################

def _is_program_stuck(Controller: Switch_Controller, Video_Capture: Game_Capture, shutdown_event: Event) -> None:

    """
    Detect whether the program is stuck in an invalid state or endless loop, and take action accordingly.

    Args:
        Controller (Switch_Controller): Controller tracking the current and previous state.
        Video_Capture (Game_Capture): Object used to save the video when an error occurs.
        shutdown_event (Event): Event to signal shutdown if an unrecoverable error is detected.

    Returns:
        None
    """

    global stuck_timer, encounter_playtime

    # Stuck in the same state for STUCK_TIMER_SECONDS -> Restart the game
    skip_states = (
        "MOVE_PLAYER", "WAIT_PAIRING_SCREEN", "WAIT_HOME_SCREEN", "SHINY_FOUND", "ENTER_LAKE_4", "STOP_1", "STOP_2",
        "STOP_3"
    )
    if (
        Controller.current_event not in skip_states and
        Controller.current_event == Controller.previous_event and
        time() - stuck_timer > CONST.STUCK_TIMER_SECONDS
    ):
        # If got stuck in "RESTART_GAME_1", it would be stuck forever
        Controller.previous_event = None
        Controller.current_event = "RESTART_GAME_1"

        print(STR.STUCK_FOR_TOO_LONG_WARN_1.format(
            time=datetime.now().strftime("%H:%M:%S"),
            module=MODULE_NAME,
            event=Controller.current_event,
            seconds=CONST.STUCK_TIMER_SECONDS
        ))

        stuck_timer = time()
        encounter_playtime = time()

        # Save the video of the error
        if CONST.SAVE_ERROR_VIDEOS:
            Video_Capture.save_video(f'State Stuck Error - {time()}')

        return

    # Stuck in a loop where states change, but no pokemon is found for FAILURE_DETECTION_SECONDS_WARN -> Restart the game
    skip_states = (
        "RESTART_GAME_1", "WAIT_PAIRING_SCREEN", "WAIT_HOME_SCREEN", "SHINY_FOUND", "ENTER_LAKE_4", "STOP_1", "STOP_2",
        "STOP_3"
    )
    if (
        Controller.current_event not in skip_states and
        time() - encounter_playtime > CONST.FAILURE_DETECTION_SECONDS_WARN
    ):
        stuck_timer = time()
        encounter_playtime = time()

        # If got stuck in "RESTART_GAME_1", it would be stuck forever
        Controller.previous_event = None
        Controller.current_event = "RESTART_GAME_1"

        print(STR.STUCK_FOR_TOO_LONG_WARN_2.format(
            time=datetime.now().strftime("%H:%M:%S"),
            module=MODULE_NAME,
            minutes=CONST.FAILURE_DETECTION_SECONDS_WARN//60)
        )

        # Save the error video
        if CONST.SAVE_ERROR_VIDEOS:
            Video_Capture.save_video(f'Loop Stuck Error - {time()}')

        return

    # No pokemon is found for FAILURE_DETECTION_SECONDS_ERROR -> stop the program
    if (
        Controller.current_event != 'SHINY_FOUND' and
        time() - encounter_playtime > CONST.FAILURE_DETECTION_SECONDS_ERROR
    ):
        # Send Telegram and/or Email notifications
        Thread(target=lambda: Telegram.send_error_detected('STUCK'), daemon=False).start()
        Thread(target=lambda: Email.send_error_detected('STUCK'), daemon=False).start()

        print(STR.STUCK_FOR_TOO_LONG_ERROR.format(
            time=datetime.now().strftime("%H:%M:%S"),
            module=MODULE_NAME,
            minutes=CONST.FAILURE_DETECTION_SECONDS_ERROR//60)
        )

        shutdown_event.set()
        return

    # Reset the stuck timer if the state changed normally
    elif Controller.current_event != Controller.previous_event:
        stuck_timer = time()

    # Reset the encounter timer when a pokemon is found
    elif Controller.current_event == 'CHECK_SHINY':
        encounter_playtime = time()

###########################################################################################################################
###########################################################################################################################

def _record_new_video(Controller: Switch_Controller, Video_Capture: Game_Capture) -> None:

    """
    Start recording a new video after a non-shiny Pokemon encounter ends, overwriting the previous one.

    Args:
        Controller (Switch_Controller): Object containing current and previous game events.
        Video_Capture (Game_Capture): Object that manages video recording and saving.

    Returns:
        None
    """

    # If entering ESCAPE_COMBAT_1 or RESTART_GAME_1, start recording a new video
    if (
        Controller.current_event in ("ESCAPE_COMBAT_1", "RESTART_GAME_1") and
        Controller.current_event != Controller.previous_event
    ):
        Video_Capture.save_video()
        Video_Capture.start_recording()

###########################################################################################################################
###########################################################################################################################

def _add_frame_to_video(
    Controller: Switch_Controller,
    Video_Capture: Game_Capture,
    image: Image_Processing,
    debug_image: Union[Debug_Image, None]
) -> None:

    """
    Add a video frame to the current recording, optionally stacking it with debug data.

    Args:
        Controller (Switch_Controller): Provides the current macro state and pressed button.
        Video_Capture (Game_Capture): Video object to record the current frame.
        image (Image_Processing): Processed frame from the capture card or video.
        debug_image (Union[Debug_Image, None]): Image used to visualize debugging information.

    Returns:
        None
    """

    if CONST.DEBUG_VIDEO:
        # Include event and button state in the debug image
        stats = {
            'event': Controller.current_event,
            'button': Controller.current_button_pressed
        }
        debug_image.populate_debug_image(stats)

        # Combine debug and gameplay images for recording
        combined_image = debug_image.stack_images(debug_image.FPS_image, image.FPS_image)
        Video_Capture.add_frame_to_video(combined_image)

    else:
        Video_Capture.add_frame_to_video(image.original_image)

###########################################################################################################################
###########################################################################################################################

def _update_database(
    FPS: FPS_Counter,
    Controller: Switch_Controller,
    Video_Capture: Game_Capture,
    stop_event: Event,
    pokemon_image: Image_Processing,
    encounter_type: str,
    last_shiny_encounter: int,
    encounter_playtime: float,
    global_encounters: int,
    last_saved_image_path: str
) -> Tuple[int, float, str, Optional[Image_Processing]]:

    """
    Update the encounter database and handle image/video saving and notifications for both normal and shiny pokemon
    encounters.

    Args:
        FPS (FPS_Counter): Utility to track performance and available disk space.
        Controller (Switch_Controller): Tracks the current game event.
        Video_Capture (Game_Capture): Handles video recording and saving.
        stop_event (Event): Signals the main loop to stop after shiny detection.
        pokemon_image (Image_Processing): Image object with pokemon data.
        encounter_type (str): Either 'STARTER' or 'WILD' to describe the encounter.
        last_shiny_encounter (int): Last shiny encounter number.
        encounter_playtime (float): Time passed since last encounter.
        global_encounters (int): Global encounter count.
        last_saved_image_path (str): Path of last saved image.

    Returns:
        int: Updated global encounter count
        float: Updated encounter playtime
        str: Updated path to last saved image
        Optional[Image_Processing]: Reset or updated pokemon image object
    """

    global shiny_timer

    # A new pokemon has appeared, but not confirmed shiny yet
    if Controller.current_event == "CHECK_SHINY" and pokemon_image is not None:
        # Extract the pokemon name from the image
        pokemon_name = pokemon_image.recognize_pokemon()

        # Save the pokemon image
        if CONST.SAVE_IMAGES:

            pokemon_image.save_image(pokemon_name)
            # This path will be used to attach the image to the notifications if the pokemon results to be shiny
            last_saved_image_path = pokemon_image.saved_image_path

            # Disable saving if running out of space
            system_space = FPS.get_system_available_space()
            if system_space['available_no_format'] < CONST.CRITICAL_AVAILABLE_SPACE:
                CONST.SAVE_IMAGES = False
                CONST.SAVE_ERROR_VIDEOS = False

                print(STR.RUNNING_OUT_OF_SPACE.format(module=MODULE_NAME, available_space=system_space['available']))

        # Log encounter in the database (initially always as non-shiny)
        global_encounters += 1
        pokemon = {'name': pokemon_name, 'shiny': False}
        add_or_update_encounter(pokemon, int(time() - encounter_playtime))

        encounter_playtime = time()
        # Start a timer so if the pokemon is shiny, the video records for SHINY_RECORDING_SECONDS before stopping
        shiny_timer = time()
        pokemon_image = None

    # A shiny pokemon has appeared
    elif Controller.current_event == "SHINY_FOUND":
        pokemon_name = last_saved_image_path.split('/')[-1].split('\\')[-1].split('_')[0]

        # It sometimes gets bugged and detects the Starly instead of the starter, which will raise always a false positive
        # due to the amount of time between the text boxes. It also restarts the game if no pokemon name is detected
        if (
            (encounter_type == 'STARTER' and pokemon_name in ['Starly', 'Étourmi', 'Staralili']) or
            (pokemon_name == '')
        ):
            Controller.current_event = "RESTART_GAME_1"

        # If a shiny has been found, wait SHINY_RECORDING_SECONDS to record the encounter video
        elif time() - shiny_timer > CONST.SHINY_RECORDING_SECONDS:
            # Add a shiny to the pokemon table in the database 
            pokemon = {'name': pokemon_name, 'shiny': True}
            add_or_update_encounter(pokemon, int(time() - encounter_playtime))

            # Save the video of the shiny encounter
            Video_Capture.save_video(f'Shiny {pokemon_name} - {time()}')

            # Play a sound so the user can hear a shiny has been found
            sound_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.SHINY_SOUND_PATH))
            Thread(target=lambda: play_sound(sound_path), daemon=True).start()
            
            # Send a shiny notification to Telegram and/or Email (does nothing if notifications are disabled)
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

            # Stops the program execution
            stop_event.set()

    return global_encounters, encounter_playtime, last_saved_image_path, pokemon_image

###########################################################################################################################
###########################################################################################################################

def _stop_execution(
    Controller: Switch_Controller,
    Video_Capture: Game_Capture,
    stop_event: Event,
    shutdown_event: Event
) -> None:

    """
    Handle the shutdown of the program after a stop is requested or completed.

    Args:
        Controller (Switch_Controller): Tracks the current macro/game state.
        Video_Capture (Game_Capture): Used to save the final video before stopping.
        stop_event (Event): Event that signals when a stop is requested (e.g. shiny found).
        shutdown_event (Event): Event used to signal final program termination.

    Returns:
        None
    """

    if stop_event.is_set() and Controller.current_event not in ("STOP_1", "STOP_2", "STOP_3"):
        Controller.current_event = "STOP_1"

    # Stop macro has been executed
    elif Controller.current_event == "STOP_2":

        def _shutdown(Video_Capture, shutdown_event):
            try:
                Video_Capture.save_video()
            except:
                pass

            shutdown_event.set()

        # Schedule shutdown after 3 seconds (non-blocking)
        Timer(3, lambda: _shutdown(Video_Capture, shutdown_event)).start()
        Controller.current_event = "STOP_3"

###########################################################################################################################
###########################################################################################################################

def start_control_system(
    Encounter_Type: Literal["WILD", "STARTER"],
    FPS: FPS_Counter,
    Controller: Switch_Controller,
    Image_Queue: Queue,
    shutdown_event: Event,
    stop_event: Event
) -> None:

    """
    Main control loop for real-time detection, video capture, image processing, controller state management, and GUI
    updating.

    Args:
        Encounter_Type (Literal): The type of Pokémon encounter, either 'WILD' or 'STARTER'.
        FPS (FPS_Counter): Object that tracks FPS, CPU and memory usage.
        Controller (Switch_Controller): The controller tracking macro states.
        Image_Queue (Queue): Queue used to send frames and state to the GUI.
        shutdown_event (Event): Event used to gracefully stop the program.
        stop_event (Event): Event triggered when a shiny is found or user interrupts.

    Returns:
        None
    """

    Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)

    # Abort if the capture card is not available
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
    last_saved_image_path = ''
    encounter_playtime = time()

    debug_image = Debug_Image() if CONST.DEBUG_VIDEO else None
    
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

        # Overlay the current FPS at the top-left corner of the image
        FPS.get_FPS()
        image.draw_FPS(FPS.FPS)

        # Draw controller input button in the switch_controller_image image shown in the GUI
        _draw_switch_controller_buttons(Controller, switch_controller_image)

        # Prevent race conditions during state update
        with Controller.event_lock:
            # Get the next state
            Controller.current_event = get_next_state(image, Controller.current_event, Encounter_Type)

            # Check if the program is stuck. If it is, try to solve the issue by restarting the game. If cannot, stop the 
            # program execution and notify the user (if notifications are enabled)
            _is_program_stuck(Controller, Video_Capture, shutdown_event)

            # Start recording a new video after a non-shiny pokemon is found. Ovewrites the older one
            _record_new_video(Controller, Video_Capture)

            _add_frame_to_video(Controller, Video_Capture, image, debug_image)

            # Save the last frame where the name of the pokemon appears in the text box. This is the image that will be
            # attached to the notification if the pokemon is shiny
            if Controller.current_event in ('ENTER_COMBAT_3', 'ENTER_COMBAT_5'):
                pokemon_image = image

            global_encounters, encounter_playtime, last_saved_image_path, pokemon_image = _update_database(
                FPS,
                Controller,
                Video_Capture,
                stop_event,
                pokemon_image,
                Encounter_Type,
                last_shiny_encounter,
                encounter_playtime,
                global_encounters,
                last_saved_image_path
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

def controller_control(controller: Switch_Controller, shutdown_event: Event) -> None:

    """
    Main loop to control the Switch macros depending on the current event.

    Args:
        controller (Switch_Controller): Controller instance with macro logic and event tracking.
        shutdown_event (Event): Event to terminate the control loop when set.

    Returns:
        None
    """

    # Connect the controller
    try:
        controller.connect_controller()
    except:
        return

    while not shutdown_event.is_set(): 
        # Read current state safely without blocking main thread
        with controller.event_lock:
            aux_current_event = controller.current_event

        # States that require pressing the A button
        # ENTER_STATIC_COMBAT_3 needs to press A for some pokemon that have two dialog phases
        press_A_states = (
            'RESTART_GAME_2', 'RESTART_GAME_3', 'ENTER_STATIC_COMBAT_2', 'ENTER_STATIC_COMBAT_3', 'ESCAPE_FAILED',
            'ENTER_LAKE_2', 'ENTER_LAKE_4', 'RESPAWN_SHAYMIN_1', 'RESPAWN_SHAYMIN_2'
        )

        if aux_current_event == 'WAIT_HOME_SCREEN':
            fast_start_macro(controller)
        elif aux_current_event == 'RESTART_GAME_1':
            restart_game_macro(controller)
        elif aux_current_event in press_A_states:
            press_single_button(controller, 'A')
        elif aux_current_event == 'ENTER_STATIC_COMBAT_1':
            enter_static_combat_macro(controller)
        elif aux_current_event == 'MOVE_PLAYER':
            move_player_wild_macro(controller)
        elif aux_current_event == 'ENTER_LAKE_1':
            enter_lake_macro(controller)
        elif aux_current_event == 'STARTER_SELECTION_2':
            select_starter_macro(controller)
        elif aux_current_event == 'STARTER_SELECTION_3':
            accept_selection_box_macro(controller)
        elif aux_current_event == 'ESCAPE_COMBAT_2':
            escape_combat_macro(controller)
        elif aux_current_event == 'STOP_1':
            stop_macro(controller)
        elif aux_current_event == 'RESPAWN_SHAYMIN_3':
            bdsp_respawn_shaymin(controller)

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

def check_threads(threads: List[Dict[str, Any]], shutdown_event: Event) -> None:

    """
    Monitor a list of threads and trigger shutdown if any thread unexpectedly stops.

    Args:
        threads (List[Dict[str, any]]): List of threads with metadata. Each item must contain:
            - 'thread': Thread object
            - 'function': str with thread name or purpose
        shutdown_event (Event): Used to stop the program if a thread crashes.

    Returns:
        None
    """

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

        # Wait 5s before checking again
        sleep(5)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################
