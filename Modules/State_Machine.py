###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from __future__ import annotations

import os
import sys
from time import time
from typing import TYPE_CHECKING, Tuple, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST

if TYPE_CHECKING:
    import numpy as np

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

state_timer = 0

###########################################################################################################################
###########################################################################################################################

def get_next_state(image: np.ndarray, state: str, encounter_type: str) -> str:

    """
    Determines the next state in the encounter state machine based on the current screen image and encounter type.

    Delegates to the appropriate encounter handler depending on the type:
        - WILD: Standard wild Pokémon encounter
        - STATIC: Static overworld Pokémon (e.g. legendaries)
        - STARTER: Starter selection encounter
        - SHAYMIN: Special Shaymin encounter
        - WILD_DOUBLES: Wild double encounters (Eterna Forest)

    Args:
        image (np.ndarray): Current game screen image.
        state (str): The current state in the state machine.
        encounter_type (str): The kind of encounter being processed.

    Returns:
        str: Next state in the encounter state machine.
    """

    if encounter_type == 'WILD': return search_wild_pokemon(image, state)
    elif encounter_type == 'STATIC': return static_encounter(image, state)
    elif encounter_type == 'STARTER': return starter_encounter(image, state)
    elif encounter_type == 'SHAYMIN': return shaymin_encounter(image, state)
    elif encounter_type == 'WILD_DOUBLES': return search_wild_pokemon_double_combat(image, state)

###########################################################################################################################
###########################################################################################################################

def search_wild_pokemon(image: np.ndarray, state: str) -> str:

    """
    This function analyzes the current screen image and uses it to determine the next state in wild encounters
    (grass/surf). It handles detection of various in-game screens, such as overworld, combat, escape sequences, and shiny
    encounter detection.

    Args:
        image (np.ndarray): Current game screen image.
        state (str): The current state in the state machine.

    Returns:
        str: Next state based on the detected game screen, or the same state if no transition applies.
    """

    global state_timer

    # Start of the execution
    if not state:
        return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image):
            return 'MOVE_PLAYER'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_4':
        # Look for the top-left load screen pixel
        if not is_bdsp_loading_screen_visible(image):
            return 'MOVE_PLAYER'

    # Game loaded, player in the overworld
    elif state == 'MOVE_PLAYER':
        # Look for the load combat white screen
        if is_white_screen_visible(image):
            state_timer = time()
            return 'ENTER_COMBAT_1'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Check the elapsed time. The shiny star animation combined with the trainer throwing the Pokémon takes over
        # CONST.WILD_SHINY_DETECTION_TIME seconds, so the shiny is confirmed
        if time() - state_timer >= CONST.WILD_SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

        # If the text box is detected before WILD_SHINY_DETECTION_TIME seconds, it means the shiny animation has not
        # occurred
        if is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_1'

        # If the life box is detected before WILD_SHINY_DETECTION_TIME seconds, it indicates that due to resource overload, 
        # the game skipped the animation of the trainer throwing the Pokéball. This causes the combat to load faster than 
        # expected, and if this condition is not checked, it would always trigger a false positive shiny detection. If the 
        # wild Pokémon was shiny, it would still be detected, as the time would exceed CONST.WILD_SHINY_DETECTION_TIME
        # seconds
        if is_life_box_visible(image):
            return 'ESCAPE_COMBAT_1'

    # Combat loaded (Both Pokémon in the field)
    elif state == 'ESCAPE_COMBAT_1':
        # Look for the life box
        if is_life_box_visible(image):
            return 'ESCAPE_COMBAT_2'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_2':
        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_3':
        # Check if the text box has disappeared
        if not is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_4'

    # Combat loaded (Escaped combat / Failed escaping)
    elif state == 'ESCAPE_COMBAT_4':
        # Look for the black screen
        if is_black_screen_visible(image):
            return 'ESCAPE_COMBAT_5'
        # Look for the life box (Escape has failed)
        elif is_life_box_visible(image):
            return 'ESCAPE_FAILED'

    # Escaped from combat (Full black screen)
    elif state == 'ESCAPE_COMBAT_5':
        # Check if the black screen has ended
        if not is_black_screen_visible(image):
            return 'MOVE_PLAYER'

    # Failed escaping (Escaping combat)
    elif state == 'ESCAPE_FAILED':
        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'
   
    else: return _check_common_states(image, state)

    return state

###########################################################################################################################
###########################################################################################################################

def search_wild_pokemon_double_combat(image: np.ndarray, state: str) -> str:

    """
    This function analyzes the current screen image and uses it to determine the next state in double combat wild
    encounters. It handles detection of various in-game screens, such as overworld, combat, escape sequences, and shiny
    encounter detection.

    Args:
        image (np.ndarray): Current game screen image.
        state (str): The current state in the state machine.

    Returns:
        str: Next state based on the detected game screen, or the same state if no transition applies.
    """
    
    # Start of the execution
    if not state:
        return 'WAIT_PAIRING_SCREEN'

    # Combat loaded (Wild Pokémon stars)
    if state == 'CHECK_SHINY':
        # Check the elapsed time. The shiny star animation combined with the trainer throwing the Pokémon takes over
        # CONST.WILD_SHINY_DETECTION_TIME seconds, so the shiny is confirmed
        if time() - state_timer >= CONST.WILD_SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

        # If the text box is detected before WILD_SHINY_DETECTION_TIME seconds, it means the shiny animation has not
        # occurred
        if is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_1'

        # If the life box is detected before WILD_SHINY_DETECTION_TIME seconds, it indicates that due to resource overload, 
        # the game skipped the animation of the trainer throwing the Pokéball. This causes the combat to load faster than 
        # expected, and if this condition is not checked, it would always trigger a false positive shiny detection. If the 
        # wild Pokémon was shiny, it would still be detected, as the time would exceed CONST.WILD_SHINY_DETECTION_TIME
        # seconds
        if is_double_combat_life_box_visible(image):
            return 'ESCAPE_COMBAT_1'

    # Combat loaded (Both Pokémon in the field)
    elif state == 'ESCAPE_COMBAT_1':
        # Look for the life box
        if is_double_combat_life_box_visible(image):
            return 'ESCAPE_COMBAT_2'

    # Combat loaded (Escaped combat / Failed escaping)
    elif state == 'ESCAPE_COMBAT_4':
        # Look for the black screen
        if is_black_screen_visible(image):
            return 'ESCAPE_COMBAT_5'
        # Look for the life box (Escape has failed)
        elif is_double_combat_life_box_visible(image):
            return 'ESCAPE_FAILED'

    return search_wild_pokemon(image, state)

###########################################################################################################################
###########################################################################################################################

def static_encounter(image: np.ndarray, state: str) -> str:

    """
    This function analyzes the current screen image and uses it to determine the next state in static encounters. It
    handles detection of various in-game screens, such as overworld, combat, restart game sequences, and shiny encounter
    detection.

    Args:
        image (np.ndarray): Current game screen image.
        state (str): The current state in the state machine.

    Returns:
        str: Next state based on the detected game screen, or the same state if no transition applies.
    """

    global state_timer

    if not state:
        return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image):
            return 'ENTER_STATIC_COMBAT_1'

    # Game loading, full black screen
    elif state == 'RESTART_GAME_4':
        # Check if the black screen has ended
        if not is_bdsp_loading_screen_visible(image):
            return 'ENTER_STATIC_COMBAT_1'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_1':
        # Look for the text box
        if is_overworld_text_box_visible(image):
            return 'ENTER_STATIC_COMBAT_2'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_2':
        # Look if the text box has disappeared
        if not is_overworld_text_box_visible(image):
            state_timer = time()
            return 'ENTER_STATIC_COMBAT_3'

    # Game loaded, player in the overworld
    # Some static encounters make a white screen flash before entering the combat
    elif state == 'ENTER_STATIC_COMBAT_3' and time() - state_timer >= CONST.STATIC_ENCOUNTERS_DELAY:
        # Look for the load combat white screen
        if is_white_screen_visible(image):
            state_timer = time()
            return 'ENTER_COMBAT_1'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Check the elapsed time
        if time() - state_timer >= CONST.SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'RESTART_GAME_1'

    else: return _check_common_states(image, state)

    return state

###########################################################################################################################
###########################################################################################################################

def starter_encounter(image: np.ndarray, state: str) -> str:

    """
    This function analyzes the current screen image and uses it to determine the next state in starter encounters. It
    handles detection of various in-game screens, such as overworld, combat, restart game sequences, and shiny encounter
    detection.

    Args:
        image (np.ndarray): Current game screen image.
        state (str): The current state in the state machine.

    Returns:
        str: Next state based on the detected game screen, or the same state if no transition applies.
    """

    global state_timer

    if not state:
        return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image):
            return 'ENTER_LAKE_1'

    elif state == 'RESTART_GAME_4':
        # Check if the black screen has ended
        if not is_bdsp_loading_screen_visible(image):
            return 'ENTER_LAKE_1'

    # In front of the lake entrance
    elif state == 'ENTER_LAKE_1':
        # Look for the text box
        if is_overworld_text_box_visible(image):
            return 'ENTER_LAKE_2'

    # In front of the lake entrance
    elif state == 'ENTER_LAKE_2':
        # Look if the text box has disappeared
        if not is_overworld_text_box_visible(image):
            return 'ENTER_LAKE_3'

    # Inside the lake
    elif state == 'ENTER_LAKE_3':
        # Look for the text box
        if is_overworld_text_box_visible(image):
            return 'ENTER_LAKE_4'

    # Inside the lake
    elif state == 'ENTER_LAKE_4':
        # Look for the black screen
        if is_black_screen_visible(image):
            return 'STARTER_SELECTION_1'

    # Opening briefcase
    elif state == 'STARTER_SELECTION_1':
        # Look for the text box
        if is_overworld_text_box_visible(image):
            return 'STARTER_SELECTION_2'

    # Briefcase is opened
    elif state == 'STARTER_SELECTION_2':
        # Look for the selection box: (Yes/No)
        if image.check_column_pixel_colors(
            CONST.SELECTION_BOX_LINE['position'],
            CONST.COLOR_SCREEN_CHECK['column_height'], CONST.COLOR_SCREEN_CHECK['white_color']
        ):
            return 'STARTER_SELECTION_3'

    # Starter has been selected
    elif state == 'STARTER_SELECTION_3':
        # Look for the text box
        if not is_overworld_text_box_visible(image):
            state_timer = time()
            return 'STARTER_SELECTION_4'

    # Starter has been selected
    # A white screen flashes before entering the combat
    elif state == 'STARTER_SELECTION_4' and time() - state_timer >= 3.5:
        # Look for the white load screen
        if is_white_screen_visible(image):
            state_timer = time()
            return 'ENTER_COMBAT_1'

    # Combat loaded (Wild Pokémon appeared)
    elif state == 'ENTER_COMBAT_3B':
        # Check if the text box has disappeared
        if not is_combat_text_box_visible(image):
            return 'ENTER_COMBAT_4'

    # Combat loaded (Starter Pokémon appeared)
    elif state == 'ENTER_COMBAT_4':
        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'ENTER_COMBAT_5'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Look for the text box
        if is_life_box_visible(image):
            if time() - state_timer >= CONST.SHINY_DETECTION_TIME:
                return 'SHINY_FOUND'
            else: return 'RESTART_GAME_1'

    else:
        state = _check_common_states(image, state)
        # We need to check the starter Pokémon, not the wild one
        if state == 'ENTER_COMBAT_3': state = 'ENTER_COMBAT_3B'

    return state

###########################################################################################################################
###########################################################################################################################

def shaymin_encounter(image: np.ndarray, state: str) -> str:

    """
    This function analyzes the current screen image and uses it to determine the next state in Sahymin encounters. It
    handles detection of various in-game screens, such as overworld, combat, escape combat sequences, and shiny encounter
    detection.

    This is a faster loop for static shaymin on BDSP as it does not close and open the game on each try.

    Args:
        image (np.ndarray): Current game screen image.
        state (str): The current state in the state machine.

    Returns:
        str: Next state based on the detected game screen, or the same state if no transition applies.
    """

    global state_timer

    if not state:
        return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image): 
            return 'ENTER_STATIC_COMBAT_1'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_1':
        # Look for the text box
        if is_overworld_text_box_visible(image):
            return 'ENTER_STATIC_COMBAT_2'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_2':
        # Look if the text box has disappeared
        if not is_overworld_text_box_visible(image):
            state_timer = time()
            return 'ENTER_STATIC_COMBAT_3'

    # Game loaded, player in the overworld
    # Some static encounters make a white screen flash before entering the combat
    elif state == 'ENTER_STATIC_COMBAT_3' and time() - state_timer >= CONST.STATIC_ENCOUNTERS_DELAY:
        # Look for the load combat white screen
        if is_white_screen_visible(image):
            state_timer = time()
            return 'ENTER_COMBAT_1'
    
    # Game loading, full black screen
    elif state == 'RESTART_GAME_4':
        # Check if the black screen has ended
        if not is_bdsp_loading_screen_visible(image):
            return 'ENTER_STATIC_COMBAT_1'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Check the elapsed time
        if time() - state_timer >= CONST.SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_1'
    
    # Combat loaded (Both Pokémon in the field)
    elif state == 'ESCAPE_COMBAT_1':
        # Look for the life box
        if is_life_box_visible(image):
            return 'ESCAPE_COMBAT_2'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_2':
        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_3':
        # Check if the text box has disappeared
        if not is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_4'

    # Combat loaded (Escaped combat / Failed escaping)
    elif state == 'ESCAPE_COMBAT_4':
        # Look for the black screen
        if is_black_screen_visible(image):
            return 'ESCAPE_COMBAT_5'
        # Look for the life box (Escape has failed)
        elif is_life_box_visible(image):
            return 'ESCAPE_FAILED_1'

    elif state == 'ESCAPE_COMBAT_5':
        # Check if the black screen has ended
        if not is_black_screen_visible(image):
            return 'RESPAWN_SHAYMIN'

    elif state == 'ESCAPE_FAILED_1':
        # Look for the life box
        if is_life_box_visible(image):
            return 'ESCAPE_FAILED_2'

    # Failed escaping (Escaping combat)
    elif state == 'ESCAPE_FAILED_2':
        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'

    elif state == 'RESPAWN_SHAYMIN':
        #After returning to the original position we begin the event again
        if is_combat_text_box_visible(image):
            return 'ENTER_STATIC_COMBAT_1'

    else: return _check_common_states(image, state)

    return state

###########################################################################################################################
###########################################################################################################################

def _check_common_states(image: np.ndarray, state: str) -> str:

    """
    Handles common state transitions shared across multiple Pokémon encounter flows.

    Args:
        image (np.ndarray): Current game screen image.
        state (str): The current state in the state machine.

    Returns:
        str: Next state based on the detected game screen, or the same state if no transition applies.
    """

    global state_timer

    # Nintendo Switch pairing controller menu
    if state == 'WAIT_PAIRING_SCREEN':
        # Look for the pairing controller screen
        if is_pairing_screen_visible(image):
            return 'WAIT_HOME_SCREEN'

    # Stuck screen (only used when the bot gets stuck in one state)
    if state == 'RESTART_GAME_0':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image):
            return 'RESTART_GAME_1'

    # Nintendo Switch main menu
    elif state == 'RESTART_GAME_1':
        if is_bdsp_loading_screen_visible(image):
            return 'RESTART_GAME_2'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_2':
        if not is_bdsp_loading_screen_visible(image):
            return 'RESTART_GAME_3'

    # Game main loadscreen (Dialga / Palkia)
    elif state == 'RESTART_GAME_3':
        if is_bdsp_loading_screen_visible(image):
            return 'RESTART_GAME_4'

    # Combat loadscreen (Full white screen)
    # Some wild encounters missdetect this state with the grass animation
    elif state == 'ENTER_COMBAT_1' and time() - state_timer >= 0.5:
        # Check if the white load screen has ended
        if not is_white_screen_visible(image):
            state_timer = time()
            return 'ENTER_COMBAT_2'

    # Combat loadscreen (Grass/Rock/Water animation, wild Pokémon appearing)
    elif state == 'ENTER_COMBAT_2' and time() - state_timer >= 0.5:
        # Look for the text box
        if is_combat_text_box_visible(image):
            return 'ENTER_COMBAT_3'

    # Combat loaded (Wild Pokémon appeared)
    elif state in ['ENTER_COMBAT_3', 'ENTER_COMBAT_5']:
        # Check if the text box has disappeared
        if not is_combat_text_box_visible(image):
            state_timer = time()
            return 'CHECK_SHINY'

    # Stopping program
    elif state == 'STOP_1':
        # Look for the pairing controller screen
        if is_pairing_screen_visible(image):
            return 'STOP_2'

    return state

###########################################################################################################################
###########################################################################################################################

def check_image_position_colors(image: np.ndarray, color: Tuple[int, int, int], positions: List[Tuple[int, int]]):

    """
    Checks if the specified color is present at the given positions in the image.

    Args:
        image (np.ndarray): The image to check.
        color (Tuple[int, int, int]): The color to check for at the specified positions.
        positions (List[Tuple[int, int]]): A list of (x, y) positions to check columns from.

    Returns:
        bool: True if the specified color is present at all given positions, False otherwise.
    """

    match_pixels = True
    for position in positions:
        # If any column fails, it stops checking further but draws all columns for debugging purposes.
        if match_pixels:
            match_pixels = image.check_column_pixel_colors(position, CONST.COLOR_SCREEN_CHECK['column_height'], color)
        else:
            image.draw_column(position, CONST.COLOR_SCREEN_CHECK['column_height'])

    return match_pixels

###########################################################################################################################
###########################################################################################################################

def is_screen_of_single_color(image: np.ndarray, color: Tuple[int, int, int]) -> bool:

    """
    Checks if image is of a single color. The image is considered to be of a single color if specific positions in the
    image are of the given color. The checked positions are the top-left, top-right, center, bottom-left, and bottom-right.

    Args:
        image (np.ndarray): The image to be checked.
        color (Tuple[int, int, int]): The color to check for.

    Returns:
        bool: True if all specified positions in the image are of the given color, False otherwise.
    """

    return check_image_position_colors(
        image,
        color,
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['top_right'],
            CONST.COLOR_SCREEN_CHECK['center'],
            CONST.COLOR_SCREEN_CHECK['bottom_left'],
            CONST.COLOR_SCREEN_CHECK['bottom_right']
        ]
    )

###########################################################################################################################
###########################################################################################################################

def is_bdsp_loading_screen_visible(image: np.ndarray):

    """
    Checks if the given image matches the BDSP loading screen by verifying specific color positions.

    BDSP loading screen has a black background.
    The top-left corner may have the Nintendo logo.
    The bottom-right may have the Nintendo Switch logo or the Pokémon starters icons.
    The center may have the Nintendo copyright texts.

    Args:
        image (np.ndarray): The image to be checked.

    Returns:
        bool: True if the image matches the BDSP loading screen, False otherwise.
    """

    return check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['black_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_right'],
            CONST.COLOR_SCREEN_CHECK['center_left'],
            CONST.COLOR_SCREEN_CHECK['center_right'],
            CONST.COLOR_SCREEN_CHECK['bottom_left']
        ]
    )

###########################################################################################################################
###########################################################################################################################

def is_pairing_screen_visible(image: np.ndarray) -> bool:

    """
    Checks if the Nintendo Switch pairing screen is visible.

    Args:
        image (np.ndarray): The image to be checked.

    Returns:
        bool: True if the pairing screen is visible, False otherwise.
    """

    return check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['pairing_menu_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['top_right']
        ]
    )

###########################################################################################################################
###########################################################################################################################

def is_home_screen_visible(image: np.ndarray) -> bool:

    """
    Checks if the Nintendo Switch HOME screen is visible.

    Args:
        image (np.ndarray): The image to be checked.

    Returns:
        bool: True if the HOME screen is visible, False otherwise.
    """

    # Check if the top-left part is of the HOME menu color
    return image.check_column_pixel_colors(
        CONST.COLOR_SCREEN_CHECK['home_menu'],
        CONST.COLOR_SCREEN_CHECK['column_height'],
        CONST.COLOR_SCREEN_CHECK['home_menu_color']
    )

###########################################################################################################################
###########################################################################################################################

def is_life_box_visible(image: np.ndarray) -> bool:

    """
    Checks if the life box is visible in the given image. The life box is considered visible if the life box content is
    white and the area outside the life box content is not white. This is made to avoid false positives during white load
    screens.
    
    Args:
        image (np.ndarray): The image to be checked.
    Returns:
        bool: True if the life box is visible, False otherwise.
    """

    # Check if life box content area is white
    is_life_box_content_white = image.check_column_pixel_colors(
        CONST.COLOR_SCREEN_CHECK['life_box'],
        CONST.COLOR_SCREEN_CHECK['small_column_height'],
        CONST.COLOR_SCREEN_CHECK['white_color']
    )

    if not is_life_box_content_white:
        # If any column fails, it stops checking further but draws all columns for debugging purposes.
        for column in ('top_left', 'center_left', 'center', 'bottom_right'):
            image.draw_column(CONST.COLOR_SCREEN_CHECK[column], CONST.COLOR_SCREEN_CHECK['column_height'])
        return False

    # Ensure surrounding regions are not white (to avoid matching a white load screen)
    is_outside_life_box_not_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['center_left'],
            CONST.COLOR_SCREEN_CHECK['center'],
            CONST.COLOR_SCREEN_CHECK['bottom_right'],
        ]
    )

    return not is_outside_life_box_not_white

###########################################################################################################################
###########################################################################################################################

def is_double_combat_life_box_visible(image: np.ndarray) -> bool:

    """
    Checks if the enemy life box is visible in the given image. The life box is considered visible if the life box content
    is white and the area outside the life box content is not white. This is made to avoid false positives during white
    load screens.
    
    Double combats can be found in Eterna Forest during the main story.

    Args:
        image (np.ndarray): The image to be checked.
    Returns:
        bool: True if the life box is visible, False otherwise.
    """

    # Check if life box content area is white
    is_life_box_content_white = image.check_column_pixel_colors(
        CONST.COLOR_SCREEN_CHECK['double_combat_life_box'],
        CONST.COLOR_SCREEN_CHECK['small_column_height'],
        CONST.COLOR_SCREEN_CHECK['white_color']
    )

    if not is_life_box_content_white:
        # If any column fails, it stops checking further but draws all columns for debugging purposes.
        for column in ('top_left', 'center_left', 'center', 'bottom_right'):
            image.draw_column(CONST.COLOR_SCREEN_CHECK[column], CONST.COLOR_SCREEN_CHECK['column_height'])
        return False

    # Ensure surrounding regions are not white (to avoid matching a white load screen)
    is_outside_life_box_not_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['center_left'],
            CONST.COLOR_SCREEN_CHECK['center'],
            CONST.COLOR_SCREEN_CHECK['bottom_right'],
        ]
    )

    return not is_outside_life_box_not_white

###########################################################################################################################
###########################################################################################################################

def is_combat_text_box_visible(image: np.ndarray) -> bool:

    """
    Checks if the text box is visible in the given image. The text box is considered visible if the text box content is
    white and the area outside the text box content is not white. This is made to avoid false positives during white load
    screens.

    Combat text boxes are slightly smaller than overworld text boxes, that's why there are two different methods.

    Args:
        image (np.ndarray): The image to be checked.

    Returns:
        bool: True if the text box is visible, False otherwise.
    """

    # Check if the textbox area is white
    is_text_box_content_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.TEXT_BOX_LINE['left_white'],
            CONST.TEXT_BOX_LINE['right_white']
        ]
    )

    if not is_text_box_content_white:
        # If any column fails, it stops checking further but draws all columns for debugging purposes.
        for column in ('top_left', 'top_right', 'center'):
            image.draw_column(CONST.COLOR_SCREEN_CHECK[column], CONST.COLOR_SCREEN_CHECK['column_height'])
        return False

    # Ensure surrounding regions are not white (to avoid matching a white load screen)
    is_outside_text_box_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['top_right'],
            CONST.COLOR_SCREEN_CHECK['center'],
        ]
    )

    return not is_outside_text_box_white

###########################################################################################################################

def is_overworld_text_box_visible(image: np.ndarray) -> bool:

    """
    Checks if the overworld text box is visible in the given image.

    Overworld text boxes are slightly bigger than combat text boxes, that's why there are two different methods.

    Args:
        image (np.ndarray): The image to be checked.

    Returns:
        bool: True if the overworld text box is visible, False otherwise.
    """

    # Check if the textbox area is white
    is_text_box_content_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.COLOR_SCREEN_CHECK['overworld_text_box_left'],
            CONST.COLOR_SCREEN_CHECK['overworld_text_box_right']
        ]
    )
    
    if not is_text_box_content_white:
        # If any column fails, it stops checking further but draws all columns for debugging purposes.
        for column in ('top_left', 'top_right', 'center'):
            image.draw_column(CONST.COLOR_SCREEN_CHECK[column], CONST.COLOR_SCREEN_CHECK['column_height'])
        return False

    # Ensure surrounding regions are not white (to avoid matching a white load screen)
    is_outside_text_box_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['top_right'],
            CONST.COLOR_SCREEN_CHECK['center'],
        ]
    )

    return not is_outside_text_box_white

###########################################################################################################################
###########################################################################################################################

def is_white_screen_visible(image: np.ndarray) -> bool:

    """
    Checks if the white screen is visible in the given image.

    Args:
        image (np.ndarray): The image to be checked.

    Returns:
        bool: True if the white screen is visible, False otherwise.
    """

    return is_screen_of_single_color(image, CONST.COLOR_SCREEN_CHECK['white_color'])

###########################################################################################################################
###########################################################################################################################

def is_black_screen_visible(image: np.ndarray) -> bool:

    """
    Checks if a black screen is visible in the given image.

    Args:
        image (np.ndarray): The image to be checked.

    Returns:
        bool: True if the black screen is visible, False otherwise.
    """

    return is_screen_of_single_color(image, CONST.COLOR_SCREEN_CHECK['black_color'])

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################
