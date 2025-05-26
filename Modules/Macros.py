###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from __future__ import annotations

import os
import sys
from time import sleep
from nxbt import Buttons
from typing import TYPE_CHECKING

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST

if TYPE_CHECKING:
    import nxbt

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Used to toggle the direction when walking on the wild grass 
walking_direction = bool(0)

###########################################################################################################################
###########################################################################################################################

def press_single_button(controller: nxbt.Nxbt, button: str, down_time: float = 0) -> None:

    """
    Presses a single button once using the controller.

    Args:
        controller (nxbt.Nxbt): The controller instance managing input via nxbt.
        button (str): The name of the button to press (must match an attribute in Buttons).
        down_time (float): Seconds the controller will press the button.
    """

    controller.current_button_pressed = button

    if button in ('UP', 'DOWN', 'RIGHT', 'LEFT'):
        button = f'DPAD_{button}'

    if down_time:
        controller.nxbt_manager.press_buttons(controller.controller_index, [getattr(Buttons, button)])
    else:
        controller.nxbt_manager.press_buttons(controller.controller_index, [getattr(Buttons, button)], down=down_time)
    controller.current_button_pressed = ''

###########################################################################################################################
###########################################################################################################################

def wait_and_press_single_button(controller: nxbt.Nxbt, seconds: float, button: str, down_time: float = 0) -> None:

    """
    Waits a specified number of seconds, then presses a single button.

    Args:
        controller (nxbt.Nxbt): The controller instance managing input via nxbt.
        seconds (float): Time to wait before pressing the button.
        button (str): The name of the button to press (must exist in Buttons).
        down_time (float): Seconds the controller will press the button.
    """

    sleep(seconds)
    press_single_button(controller, button, down_time)

###########################################################################################################################
###########################################################################################################################

def test_macro(controller: nxbt.Nxbt) -> None:

    """
    Performs a macro to navigate from the "Change Grip/Order" menu to the game and back again.

    Args:
        controller (nxbt.Nxbt): The controller object managing macro execution and button presses.
    """

    controller.current_event = "Test"

    start_macro(controller)
    sleep(2)

    # Press 'HOME' to launch the game
    press_single_button(controller, 'HOME')
    
    sleep(1)
    stop_macro(controller)

###########################################################################################################################
###########################################################################################################################

def start_macro(controller: nxbt.Nxbt, force_execution: bool = False) -> None:

    """
    Executes the macro to return from the "Change Grip/Order" menu to the game. If the macro was already performed, it
    does nothing.

    Args:
        controller (nxbt.Nxbt): The controller instance handling macro events and input.
        force_execution (bool): Runs the macro regardless of whether it has already been run.
    """

    # Avoid re-running the same macro
    if controller.previous_event == controller.current_event and not force_execution:
        return

    # Press 'B' to exit the "Change Grip/Order" menu
    wait_and_press_single_button(controller, 1, 'B')

    # Press 'HOME' to go to the HOME menu
    wait_and_press_single_button(controller, 1, 'HOME')

###########################################################################################################################
###########################################################################################################################

def fast_start_macro(controller: nxbt.Nxbt, force_execution: bool = False) -> None:

    """
    Executes an extended macro that returns from the "Change Grip/Order" menu to the HOME menu, and then launches the
    selected game. If the macro was already performed, it does nothing.

    Args:
        controller (nxbt.Nxbt): The controller managing button input via nxbt.
        force_execution (bool): Runs the macro regardless of whether it has already been run.
    """

    # Avoid re-running the same macro
    if controller.previous_event == controller.current_event and not force_execution:
        return

    # Press 'B' to exit the "Change Grip/Order" menu
    wait_and_press_single_button(controller, 1, 'B')

    # Press 'HOME' to go to the HOME menu
    wait_and_press_single_button(controller, 1, 'HOME')

    sleep(2)

    # Press 'HOME' to launch the game
    press_single_button(controller, 'HOME')

    sleep(1)

###########################################################################################################################
###########################################################################################################################

def stop_macro(controller: nxbt.Nxbtt, force_execution: bool = False) -> None:

    """
    Executes a macro to pause the game and navigate to the "Change Grip/Order" menu on Nintendo Switch.  If the macro was
    already performed, it does nothing.

    Args:
        controller (nxbt.Nxbt): The controller managing input and macro state.
        force_execution (bool): Runs the macro regardless of whether it has already been run.
    """

    # Avoid re-running the same macro
    if controller.previous_event == controller.current_event and not force_execution:
        return

    # Press 'HOME' to pause the game
    press_single_button(controller, 'HOME')

    # Navigate to "Controllers" section
    sleep(1.5)
    for _ in range(2):
        press_single_button(controller, 'DOWN')

    # Navigate to "Change Grip/Order"
    for _ in range(5):
        wait_and_press_single_button(controller, 0.1, 'RIGHT')
        sleep(0.1)

    # Press 'A' to enter the menu
    wait_and_press_single_button(controller, 0.5, 'A')

    # Press 'A' to enter the final menu
    wait_and_press_single_button(controller, 2, 'RIGHT')

    sleep(1)

###########################################################################################################################
###########################################################################################################################

def restart_game_macro(controller: nxbt.Nxbt, force_execution: bool = False) -> None:

    """
    Executes a macro to fully restart the game (hard reset).

    Args:
        controller (nxbt.Nxbt): The controller object managing macro input via nxbt.
        force_execution (bool): Runs the macro regardless of whether it has already been run.
    """

    # Avoid re-running the same macro
    if controller.previous_event == controller.current_event and not force_execution:
        return

    # Press 'HOME' to go to HOME menu
    press_single_button(controller, 'HOME', 0.05)

    # Press 'B'
    wait_and_press_single_button(controller, 0.2, 'B')

    # Press 'X' to close the game
    wait_and_press_single_button(controller, 1.3, 'X')
    sleep(0.5)

    # WARN: connection can fail and update the game
    # Handle "Skip update" dialog if enabled
    if CONST.SKIP_UPDATING_GAME:
        sleep(0.5)
        # Press 'A' to start the game
        for _ in range(2):
            wait_and_press_single_button(controller, 0.2, 'A')
            sleep(0.8)

        # Press 'Up' to move cursor to "Start Software" manually
        for _ in range(3):
            wait_and_press_single_button(controller, 0.1, 'UP')

    # Spam 'A' to launch the game
    for _ in range(10):
        wait_and_press_single_button(controller, 0.3, 'A')

###########################################################################################################################
###########################################################################################################################

def move_player_wild_macro(controller: nxbt.Nxbt) -> None:

    """
    Simulates the player moving back and forth in the overworld to trigger wild encounters. The movement direction
    alternates every call, using a global 'walking_direction' flag.

    Args:
        controller (nxbt.Nxbt): The controller instance handling button presses.
    """

    global walking_direction

    if CONST.WILD_WALKING_DIRECTION == 'NS':
        if not walking_direction:
            press_single_button(controller, 'UP', CONST.WILD_WALKING_SECONDS)
        else:
            press_single_button(controller, 'DOWN', CONST.WILD_WALKING_SECONDS)

    elif CONST.WILD_WALKING_DIRECTION == 'EW':
        if not walking_direction:
            press_single_button(controller, 'LEFT', CONST.WILD_WALKING_SECONDS)
        else:
            press_single_button(controller, 'RIGHT', CONST.WILD_WALKING_SECONDS)

    # Flip direction for next call
    walking_direction = not walking_direction

###########################################################################################################################
###########################################################################################################################

def escape_combat_macro(controller: nxbt.Nxbt, force_execution: bool = False) -> None:

    """
    Escape from a wild Pokémon combat.

    Args:
        controller (nxbt.Nxbt): The controller instance handling input via nxbt.
        force_execution (bool): Runs the macro regardless of whether it has already been run.
    """

    if controller.previous_event != controller.current_event or force_execution:
        # Press 'Up' to move to "Run" button
        wait_and_press_single_button(controller, 0.5, 'UP', 0.2)
    else:
        # Press 'A' to escape the combat
        wait_and_press_single_button(controller, 0.1, 'A')
        sleep(0.1)

###########################################################################################################################
###########################################################################################################################

def home_macro(controller: nxbt.Nxbt) -> None:

    """
    Go to the Nintendo Switch HOME menu.

    Args:
        controller (nxbt.Nxbt): The controller managing button inputs via nxbt.
    """

    # Press 'HOME' to go to the HOME menu
    press_single_button(controller, 'HOME', 0.05)
    sleep(1)

###########################################################################################################################
###########################################################################################################################

def select_starter_macro(controller: nxbt.Nxbt, force_execution: bool = False) -> None:

    """
    Select a starter Pokémon during the briefcase sequence.

    Args:
        controller (nxbt.Nxbt): The controller managing the button presses.
        force_execution (bool): Runs the macro regardless of whether it has already been run.
    """

    # Avoid re-running the same macro
    if controller.previous_event == controller.current_event and not force_execution:
        return

    wait_and_press_single_button(controller, 1, 'A')
    sleep(1)

    # Cursor starts on the left pokémon
    # Center pokémon: move cursor to the right
    if CONST.STARTER == 'C':
        press_single_button(controller, 'RIGHT')
        sleep(0.2)
    # Right pokémon: move cursor to the left
    elif CONST.STARTER == 'R':
        press_single_button(controller, 'LEFT')
        sleep(0.2)
    # Left pokémon: no mevement needed
    elif CONST.STARTER == 'L':
        pass

    # Press 'A' to select the pokémon
    press_single_button(controller, 'A')

###########################################################################################################################
###########################################################################################################################

def accept_selection_box_macro(controller: nxbt.Nxbt, force_execution: bool = False) -> None:

    """
    Confirms the starter Pokémon selection by navigating the confirmation dialog.

    Args:
        controller (nxbt.Nxbt): The controller managing button inputs via nxbt.
        force_execution (bool): Runs the macro regardless of whether it has already been run.
    """

    # Avoid re-running the same macro
    if controller.previous_event == controller.current_event and not force_execution:
        return

    # Press 'Up' to move the cursor up to highlight "Yes"
    for _ in range(2):
        press_single_button(controller, 'UP')

    # Press 'A' to confirm selection
    for _ in range(2):
        wait_and_press_single_button(controller, 0.2, 'A')
        sleep(0.1)

###########################################################################################################################
###########################################################################################################################

def enter_lake_macro(controller: nxbt.Nxbt) -> None:

    """
    Simulates the player entering the lake by walking forward and interacting.

    Args:
        controller (nxbt.Nxbt): The controller handling input via nxbt.
    """

    # Press 'Up' to enter the lake
    press_single_button(controller, 'UP', 0.5)

    # Press 'A' to skip the text dialog
    wait_and_press_single_button(controller, 0.2, 'A')
    sleep(0.1)

###########################################################################################################################
###########################################################################################################################

def enter_static_combat_macro(controller: nxbt.Nxbt) -> None:

    """
    Starts a static Pokémon combat.

    Args:
        controller (nxbt.Nxbt): The controller handling input via nxbt.
    """

    # Press 'Up' to move forward if necessary
    if CONST.MOVE_FORWARD_STATIC_ENCOUNTER:
        press_single_button(controller, 'UP', 0.5)

    # Press 'A' to enter the static combat
    press_single_button(controller, 'A')

###########################################################################################################################
###########################################################################################################################

def bdsp_respawn_shaymin(controller: nxbt.Nxbt) -> None:

    """
    Reloads the Shaymin static encounter in Pokémon BDSP by moving down and up with the bike, which resets the overworld
    state without needing a full game restart.

    Args:
        controller (nxbt.Nxbt): The controller managing button presses via nxbt.
    """

    # Wait for the escape animation to end
    sleep(1.5)

    # Press 'A' to close combat textboxes
    press_single_button(controller, 'A', 0.5)

    # Mount the bike (must have fast gear enabled and bike on bottom option)
    press_single_button(controller, 'PLUS', 0.75)

    # Move down to unload Shaymin
    press_single_button(controller, 'DOWN', 3)

    # Move back up to reload Shaymin
    press_single_button(controller, 'UP', 3.5)

    # Interact with Shaymin
    press_single_button(controller, 'A', 0.5)

    # Wait for the dismount animation before the textbox appears
    sleep(2)

    # Close Shaymin's intro textbox
    press_single_button(controller, 'A', 0.5)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################
