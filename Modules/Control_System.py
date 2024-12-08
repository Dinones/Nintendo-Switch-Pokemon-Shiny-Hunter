###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import cv2
from time import time

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

state_timer = 0

def search_wild_pokemon(image, state):
    global state_timer
    if not state: return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image):
            return 'MOVE_PLAYER'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_4':
        # Look for the top-left load screen pixel
        if not is_bdsp_loading_screen(image):
            return 'MOVE_PLAYER'

    # Game loaded, player in the overworld
    elif state == 'MOVE_PLAYER':
        # Look for the load combat white screen
        if is_white_screen_visible(image):
            state_timer = time()
            return 'ENTER_COMBAT_1'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Look for the text box
        if is_text_box_visible(image):
            return 'ESCAPE_COMBAT_1'

        # Check the elapsed time
        if image.shiny_detection_time and time() - image.shiny_detection_time >= CONST.SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

    # Combat loaded (Both Pokémon in the field)
    elif state == 'ESCAPE_COMBAT_1':
        # Look for the life box
        if is_life_box_visible(image):
            return 'ESCAPE_COMBAT_2'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_2':
        # Look for the text box
        if is_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_3':
        # Check if the text box has disappeared
        if not is_text_box_visible(image):
            return 'ESCAPE_COMBAT_4'

    # Combat loaded (Escaped combat / Failed escaping)
    elif state == 'ESCAPE_COMBAT_4':
        # Look for the black screen
        if is_black_screen_visible(image):
            return 'ESCAPE_COMBAT_5'
        # Look for the life box (Escape has failed)
        elif is_life_box_visible(image):
            return 'ESCAPE_FAILED_1'

    # Escaped from combat (Full black screen)
    elif state == 'ESCAPE_COMBAT_5':
        # Check if the black screen has ended
        if not is_black_screen_visible(image):
            return 'MOVE_PLAYER'

    # Failed escaping (Both Pokémon in the field)
    elif state == 'ESCAPE_FAILED_1':
        # Look for the life box
        if is_life_box_visible(image):
            return 'ESCAPE_FAILED_2'

    # Failed escaping (Escaping combat)
    elif state == 'ESCAPE_FAILED_2':
        # Look for the text box
        if is_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'
   
    else: return _check_common_states(image, state)

    return state

###########################################################################################################################
###########################################################################################################################

def static_encounter(image, state):
    global state_timer
    if not state: return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image):
            return 'ENTER_STATIC_COMBAT_1'

    # Game loading, full black screen
    elif state == 'RESTART_GAME_4':
        # Check if the black screen has ended
        if not is_bdsp_loading_screen(image):
            return 'ENTER_STATIC_COMBAT_1'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_1':
        # Look for the text box
        if is_overworld_visible(image):
            return 'ENTER_STATIC_COMBAT_2'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_2':
        # Look if the text box has disappeared
        if not is_overworld_visible(image):
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
        # Look for the text box
        if is_text_box_visible(image):
            return 'RESTART_GAME_1'

        # Check the elapsed time
        if image.shiny_detection_time and time() - image.shiny_detection_time >= CONST.SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

    else: return _check_common_states(image, state)

    return state

###########################################################################################################################
###########################################################################################################################

def starter_encounter(image, state):
    global state_timer
    if not state: return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image):
            return 'ENTER_LAKE_1'

    elif state == 'RESTART_GAME_4':
        # Check if the black screen has ended
        if not is_bdsp_loading_screen(image):
            return 'ENTER_LAKE_1'

    # In front of the lake entrance
    elif state == 'ENTER_LAKE_1':
        # Look for the text box
        if is_overworld_visible(image):
            return 'ENTER_LAKE_2'

    # In front of the lake entrance
    elif state == 'ENTER_LAKE_2':
        # Look if the text box has disappeared
        if not is_overworld_visible(image):
            return 'ENTER_LAKE_3'

    # Inside the lake
    elif state == 'ENTER_LAKE_3':
        # Look for the text box
        if is_overworld_visible(image):
            return 'ENTER_LAKE_4'

    # Inside the lake
    elif state == 'ENTER_LAKE_4':
        # Look for the black screen
        if is_black_screen_visible(image):
            return 'STARTER_SELECTION_1'

    # Opening briefcase
    elif state == 'STARTER_SELECTION_1':
        # Look for the text box
        if is_overworld_visible(image):
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
        if not is_overworld_visible(image):
            state_timer = time()
            return 'STARTER_SELECTION_4'

    # Starter has been selected
    # A white screen flashes before entering the combat
    elif state == 'STARTER_SELECTION_4' and time() - state_timer >= 3.5:
        # Look for the white load screen
        if is_overworld_visible(image):
            state_timer = time()
            return 'ENTER_COMBAT_1'

    # Combat loaded (Wild Pokémon appeared)
    elif state == 'ENTER_COMBAT_3B':
        # Check if the text box has disappeared
        if not is_text_box_visible(image):
            return 'ENTER_COMBAT_4'

    # Combat loaded (Starter Pokémon appeared)
    elif state == 'ENTER_COMBAT_4':
        # Look for the text box
        if is_text_box_visible(image):
            return 'ENTER_COMBAT_5'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Look for the text box
        if is_life_box_visible(image):
            if image.shiny_detection_time and time() - image.shiny_detection_time >= CONST.SHINY_DETECTION_TIME:
                return 'SHINY_FOUND'
            else: return 'RESTART_GAME_1'

    else:
        state = _check_common_states(image, state)
        # We need to check the starter pokémon, not the wild one
        if state == 'ENTER_COMBAT_3': state = 'ENTER_COMBAT_3B'

    return state

###########################################################################################################################
###########################################################################################################################

# This is a faster loop for static shaymin on BDSP as it does not close and open the game on each try
def shaymin_encounter(image, state):
    global state_timer
    if not state: return 'WAIT_PAIRING_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        # Look for the top-left nintendo switch main menu pixel
        if is_home_screen_visible(image): 
            return 'ENTER_STATIC_COMBAT_1'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_1':
        # Look for the text box
        if is_overworld_visible(image):
            return 'ENTER_STATIC_COMBAT_2'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT_2':
        # Look if the text box has disappeared
        if not is_overworld_visible(image):
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
        if not is_bdsp_loading_screen(image):
            return 'ENTER_STATIC_COMBAT_1'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Look for the text box
        if is_text_box_visible(image):
            return 'ESCAPE_COMBAT_1'

        # Check the elapsed time
        if image.shiny_detection_time and time() - image.shiny_detection_time >= CONST.SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'
    
    # Combat loaded (Both Pokémon in the field)
    elif state == 'ESCAPE_COMBAT_1':
        # Look for the life box
        if is_life_box_visible(image):
            return 'ESCAPE_COMBAT_2'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_2':
        # Look for the text box
        if is_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_3':
        # Check if the text box has disappeared
        if not is_text_box_visible(image):
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
        if is_text_box_visible(image):
            return 'ESCAPE_COMBAT_3'

    elif state == 'RESPAWN_SHAYMIN':
        #After returning to the original position we begin the event again
        if is_text_box_visible(image):
            return 'ENTER_STATIC_COMBAT_1'

    else: return _check_common_states(image, state)

    return state

###########################################################################################################################
###########################################################################################################################

def _check_common_states(image, state):
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
        if is_bdsp_loading_screen(image):
            return 'RESTART_GAME_2'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_2':
        if not is_bdsp_loading_screen(image):
            return 'RESTART_GAME_3'

    # Game main loadscreen (Dialga / Palkia)
    elif state == 'RESTART_GAME_3':
        if is_bdsp_loading_screen(image):
            return 'RESTART_GAME_4'

    # Combat loadscreen (Full white screen)
    # Some wild encounters missdetect this state with the grass animation
    elif state == 'ENTER_COMBAT_1' and time() - state_timer >= 0.5:
        # Check if the white load screen has ended
        if not is_white_screen_visible(image):
            return 'ENTER_COMBAT_2'

    # Combat loadscreen (Grass/Rock/Water animation, wild pokémon appearing)
    elif state == 'ENTER_COMBAT_2':
        # Look for the text box
        if is_text_box_visible(image):
            return 'ENTER_COMBAT_3'

    # Combat loaded (Wild Pokémon appeared)
    elif state in ['ENTER_COMBAT_3', 'ENTER_COMBAT_5']:
        # Check if the text box has disappeared
        if not is_text_box_visible(image):
            return 'CHECK_SHINY'

    # Stopping program
    elif state == 'STOP_1':
        # Look for the pairing controller screen
        if image.check_pixel_color(CONST.PAIRING_MENU_COLOR):
            return 'STOP_2'

    return state

###########################################################################################################################
###########################################################################################################################

def is_bdsp_loading_screen(image):
    """
    Checks if the given image matches the BDSP loading screen by verifying specific color positions.

    BDSP loading screen has a black background.
    The top-left may have the Nintendo logo.
    The bottom-right may have the Nintendo Switch logo or the Pokémon starters icons.
    The center may have the Nintendo copyright texts.

    Args:
        image: The image to be checked.

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

def is_screen_of_single_color(image, color):
    """
    Checks if image is of a single color.

    The image is considered to be of a single color if
    specific positions in the image are of the given color.
    The checked positions are the top-left, top-right, center, bottom-left, and bottom-right.

    Args:
        image (Image): The image to be checked.
        color (tuple): The color to check for.

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

def check_image_position_colors(image, color, positions):

    """
    Checks if the specified color is present at the given positions in the image.

    Args:
        image: The image to check.
        color: The color to check for at the specified positions.
        positions: A list of positions (coordinates) to check in the image.

    Returns:
        bool: True if the specified color is present at all given positions, False otherwise.
    """

    match_pixels = True
    for position in positions:
        # If a detection has failed, there is no need to check the other columns. Nevertheless, they are printed to 
        # show they are being checked
        if match_pixels:
            match_pixels = image.check_column_pixel_colors(position, CONST.COLOR_SCREEN_CHECK['column_height'], color)
        else: image.draw_column(position, CONST.COLOR_SCREEN_CHECK['column_height'])

    return match_pixels

###########################################################################################################################

def is_pairing_screen_visible(image):
    return check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['pairing_menu_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['top_right']
        ]
    )

###########################################################################################################################

def is_home_screen_visible(image):

    # Check if the top-left part is of the HOME menu color
    return image.check_column_pixel_colors(
        CONST.COLOR_SCREEN_CHECK['home_menu'],
        CONST.COLOR_SCREEN_CHECK['column_height'],
        CONST.COLOR_SCREEN_CHECK['home_menu_color']
    )

###########################################################################################################################

def is_life_box_visible(image):
    """
    Checks if the life box is visible in the given image.
    The life box is considered visible if the life box content is white
    and the area outside the life box content is not white.
    
    Args:
        image: The image in which to check for the life box.
        color: The color of the life box.
    Returns:
        bool: True if the life box is visible, False otherwise.
    """

    is_life_box_content_white = image.check_column_pixel_colors(
        CONST.COLOR_SCREEN_CHECK['life_box'],
        CONST.COLOR_SCREEN_CHECK['small_column_height'],
        CONST.COLOR_SCREEN_CHECK['white_color']
    )

    if not is_life_box_content_white:
        # Stop testing if the text box content is not white, but still drawing the other columns
        for column in ('top_left', 'center_left', 'center', 'bottom_right'):
            image.draw_column(CONST.COLOR_SCREEN_CHECK[column], CONST.COLOR_SCREEN_CHECK['column_height'])
        return False

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

def is_black_screen_visible(image):
    """
    Checks if a black screen is visible in the given image.
    Args:
        image: The image in which to check for the black screen.
    Returns:
        bool: True if the black screen is visible, False otherwise.
    """
    return is_screen_of_single_color(image, CONST.COLOR_SCREEN_CHECK['black_color'])

###########################################################################################################################

def is_text_box_visible(image):
    """
    Checks if the text box is visible in the given image.
    The text box is considered visible if the text box content is white
    and the area outside the text box content is not white.

    Args:
        image: The image in which to check for the text box.
    Returns:
        bool: True if the text box is visible, False otherwise.
    """

    is_text_box_content_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.TEXT_BOX_LINE['left_white'],
            CONST.TEXT_BOX_LINE['right_white']
        ]
    )

    if not is_text_box_content_white:
        # Stop testing if the text box content is not white, but still drawing the other columns
        for column in ('top_left', 'top_right', 'center'):
            image.draw_column(CONST.COLOR_SCREEN_CHECK[column], CONST.COLOR_SCREEN_CHECK['column_height'])
        return False

    is_outside_text_box_not_white = check_image_position_colors(
        image,
        CONST.COLOR_SCREEN_CHECK['white_color'],
        [
            CONST.COLOR_SCREEN_CHECK['top_left'],
            CONST.COLOR_SCREEN_CHECK['top_right'],
            CONST.COLOR_SCREEN_CHECK['center'],
        ]
    )

    return not is_outside_text_box_not_white

###########################################################################################################################

def is_overworld_visible(image):
    """
    Checks if the overworld is visible in the given image.
    Args:
        image: The image in which to check for the overworld.
    Returns:
        bool: True if the overworld is visible, False otherwise.
    """
    return image.check_column_pixel_colors(
        CONST.TEXT_BOX_LINE['overworld'],
        CONST.COLOR_SCREEN_CHECK['column_height'],
        CONST.COLOR_SCREEN_CHECK['white_color']
    )

###########################################################################################################################

def is_white_screen_visible(image):
    """
    Checks if the white screen is visible in the given image.
    Args:
        image: The image in which to check for the white screen.
    Returns:
        bool: True if the white screen is visible, False otherwise.
    """
    return is_screen_of_single_color(image, CONST.COLOR_SCREEN_CHECK['white_color'])

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import numpy as np
    from time import sleep

    from FPS_Counter import FPS_Counter
    import Colored_Strings as COLOR_str
    from Game_Capture import Game_Capture
    from Image_Processing import Image_Processing

    #######################################################################################################################

    LEFT_ARROW_KEY_VALUE = 65361
    RIGHT_ARROW_KEY_VALUE = 65363

    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Control System'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Check states from capture card'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Check states from video'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Control System'))

        menu_options = {
            '1': check_states,
            '2': check_states,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Control System') + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def check_states(option):
        if option == '1': tool = 'capture card'
        elif option == '2': tool = 'video'
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Control System')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Checking states using {tool}...")
            .replace('{path}', '')
        )

        if option == '1':
            Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
            if not Video_Capture.video_capture.isOpened():
                Video_Capture.stop()
                print(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'") + '\n')
                return
        elif option == '2':
            if not os.path.exists(f'../{CONST.TESTING_VIDEO_PATH}'):
                return print(COLOR_str.INVALID_PATH_ERROR
                    .replace('{module}', 'Image Processing')
                    .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}' or '../{CONST.SAVING_FRAMES_PATH}'") + '\n'
                )
            Video_Capture = Game_Capture(f'../{CONST.TESTING_VIDEO_PATH}')

        FPS = FPS_Counter()
        state = 'MOVE_PLAYER'
        pause = False
        shiny_detection_time = 0
        total_frames = int(Video_Capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        current_frames = 0
        force_load_frame = False

        while True:
            # Function waitKeyEx() detect more keys than waitKey()
            key = cv2.waitKeyEx(1)
            if key in [ord('q'), ord('Q')]: break
            elif key == ord(' '): pause = not pause
            elif pause and key in [ord('a'), ord('A'), LEFT_ARROW_KEY_VALUE]:
                current_frames = max(0, current_frames - 2)
                force_load_frame = True
            elif pause and key in [ord('d'), ord('D'), RIGHT_ARROW_KEY_VALUE]:
                force_load_frame = True

            if pause and not force_load_frame: continue
            if force_load_frame:
                Video_Capture.video_capture.set(cv2.CAP_PROP_POS_FRAMES, current_frames)

            # Adjust to match the FPS of the video 0.05s ~ 20 FPS
            if option == '2' and not force_load_frame: sleep(0.05)
           
            image = Image_Processing(Video_Capture.read_frame())
            if type(image.original_image) == type(None): break
            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            # Needs to be here because this is controlled in the Shiny Hunter loop
            if state == "CHECK_SHINY":
                # Only reset the first time it enters to the state
                if time() - shiny_detection_time >= 10: shiny_detection_time = time()
                image.shiny_detection_time = shiny_detection_time

            state = search_wild_pokemon(image, state)
            image.write_text(state, (0, CONST.TEXT_PARAMS['position'][1] + 5))

            current_frames += 1
            force_load_frame = False
            cv2.imshow(f'{CONST.BOT_NAME} - Image', image.FPS_image)

        Video_Capture.stop()
        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Control System')
            .replace('{reason}', 'Successfully checked states!') + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
