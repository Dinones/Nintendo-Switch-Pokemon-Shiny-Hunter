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
        if image.check_pixel_color(CONST.HOME_MENU_COLOR):
            return 'MOVE_PLAYER'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_4':
        # Look for the top-left load screen pixel
        if image.check_pixel_color(CONST.LOAD_SCREEN_BLACK_COLOR):
            return 'MOVE_PLAYER'

    # Game loaded, player in the overworld
    elif state == 'MOVE_PLAYER':
        # Look for the load combat white screen
        if is_load_fight_white_screen(image):
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

    # Failed escapping (Both Pokémon in the field)
    elif state == 'ESCAPE_FAILED_1':
        # Look for the life box
        if is_life_box_visible(image):
            return 'ESCAPE_FAILED_2'

    # Failed escapping (Escaping combat)
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
        if image.check_pixel_color(CONST.HOME_MENU_COLOR):
            return 'ENTER_STATIC_COMBAT_1'

    # Game loading, full black screen
    elif state == 'RESTART_GAME_4':
        # Check if the black screen has ended
        if not is_black_screen_visible(image):
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
        if is_load_fight_white_screen(image):
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
        if image.check_pixel_color(CONST.HOME_MENU_COLOR):
            return 'ENTER_LAKE_1'

    elif state == 'RESTART_GAME_4':
        # Check if the black screen has ended
        if not is_black_screen_visible(image):
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
        if image.check_multiple_pixel_colors(
            [CONST.SELECTION_BOX_LINE['x'], CONST.SELECTION_BOX_LINE['y1']],
            [CONST.SELECTION_BOX_LINE['x'], CONST.SELECTION_BOX_LINE['y2']], CONST.SELECTION_BOX_LINE['color']
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

def _check_common_states(image, state):
    global state_timer

    # Nintendo Switch pairing controller menu
    if state == 'WAIT_PAIRING_SCREEN':
        # Look for the pairing controller screen
        if image.check_pixel_color(CONST.PAIRING_MENU_COLOR):
            return 'WAIT_HOME_SCREEN'

    # Stuck screen (only used when the bot gets stuck in one state)
    if state == 'RESTART_GAME_0':
        # Look for the top-left nintendo switch main menu pixel
        if image.check_pixel_color(CONST.HOME_MENU_COLOR):
            return 'RESTART_GAME_1'

    # Nintendo Switch main menu
    elif state == 'RESTART_GAME_1':
        if is_black_screen_visible(image):
            return 'RESTART_GAME_2'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_2':
        if not is_black_screen_visible(image):
            return 'RESTART_GAME_3'

    # Game main loadscreen (Dialga / Palkia)
    elif state == 'RESTART_GAME_3':
        if is_black_screen_visible(image):
            return 'RESTART_GAME_4'

    # Combat loadscreen (Full white screen)
    # Some wild encounters missdetect this state with the grass animation
    elif state == 'ENTER_COMBAT_1' and time() - state_timer >= 0.5:
        # Check if the white load screen has ended
        if not is_load_fight_white_screen(image):
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

def is_life_box_visible(image, color=CONST.LIFE_BOX_LINE['color']):
    """
    Checks if the life box is visible in the given image.
    Args:
        image: The image in which to check for the life box.
        color: The color of the life box.
    Returns:
        bool: True if the life box is visible, False otherwise.
    """
    return image.check_multiple_pixel_colors(
        [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y1']],
        [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y2']], color
    )

###########################################################################################################################

def is_black_screen_visible(image):
    """
    Checks if a black screen is visible in the given image.
    Args:
        image: The image in which to check for the black screen.
    Returns:
        bool: True if the black screen is visible, False otherwise.
    """
    return is_life_box_visible(image, CONST.LOAD_SCREEN_BLACK_COLOR)

###########################################################################################################################

def is_text_box_visible(image):
    """
    Checks if the text box is visible in the given image.
    Args:
        image: The image in which to check for the text box.
        x: The x coordinate of the text box.
    Returns:
        bool: True if the text box is visible, False otherwise.
    """
    text_box_left_visible = image.check_multiple_pixel_colors(
        [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
        [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']],
        CONST.TEXT_BOX_LINE['color'])

    text_box_right_visible = image.check_multiple_pixel_colors(
        [CONST.MAIN_FRAME_SIZE[0] - CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
        [CONST.MAIN_FRAME_SIZE[0] - CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']],
        CONST.TEXT_BOX_LINE['color'])

    return text_box_left_visible and text_box_right_visible

###########################################################################################################################

def is_overworld_visible(image):
    """
    Checks if the overworld is visible in the given image.
    Args:
        image: The image in which to check for the overworld.
    Returns:
        bool: True if the overworld is visible, False otherwise.
    """
    return image.check_multiple_pixel_colors(
        [CONST.TEXT_BOX_LINE['overworld_x'], CONST.TEXT_BOX_LINE['y1']],
        [CONST.TEXT_BOX_LINE['overworld_x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
    )

###########################################################################################################################

def is_load_fight_white_screen(image):
    """
    Checks if the white screen is visible in the given image.
    Args:
        image: The image in which to check for the white screen.
    Returns:
        bool: True if the white screen is visible, False otherwise.
    """
    is_bottom_left_white = image.check_multiple_pixel_colors(
        [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
        [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']],
        CONST.TEXT_BOX_LINE['color'])

    is_bottom_right_white = image.check_multiple_pixel_colors(
        [CONST.MAIN_FRAME_SIZE[0] - CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
        [CONST.MAIN_FRAME_SIZE[0] - CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']],
        CONST.TEXT_BOX_LINE['color'])

    is_top_left_white = image.check_multiple_pixel_colors(
        [CONST.TEXT_BOX_LINE['x'], CONST.MAIN_FRAME_SIZE[1] - CONST.TEXT_BOX_LINE['y2']],
        [CONST.TEXT_BOX_LINE['x'], CONST.MAIN_FRAME_SIZE[1] - CONST.TEXT_BOX_LINE['y1']],
        CONST.TEXT_BOX_LINE['color'])

    is_top_right_white = image.check_multiple_pixel_colors(
        [CONST.MAIN_FRAME_SIZE[0] - CONST.TEXT_BOX_LINE['x'], CONST.MAIN_FRAME_SIZE[1] - CONST.TEXT_BOX_LINE['y2']],
        [CONST.MAIN_FRAME_SIZE[0] - CONST.TEXT_BOX_LINE['x'], CONST.MAIN_FRAME_SIZE[1] - CONST.TEXT_BOX_LINE['y1']],
        CONST.TEXT_BOX_LINE['color'])

    return is_bottom_left_white and is_bottom_right_white and is_top_left_white and is_top_right_white

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
        state = 'ENTER_STATIC_COMBAT_1'
        pause = False
        shiny_detection_time = 0

        while True:
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'): break
            elif key == ord(' '): pause = not pause

            if pause: continue
            if option == '2': sleep(0.02)
           
            image = Image_Processing(Video_Capture.read_frame())
            if type(image.original_image) == type(None): break
            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            # Check if the pokemon is shiny
            if state == "CHECK_SHINY":
                # Only reset the first time it enters to the state
                if time() - shiny_detection_time >= 10: shiny_detection_time = time()
                image.shiny_detection_time = shiny_detection_time

            state = static_encounter(image, state)
            image.write_text(state, (0, CONST.TEXT_PARAMS['position'][1] + 5))

            cv2.imshow(f'{CONST.BOT_NAME} - Image', image.FPS_image)

        Video_Capture.stop()
        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Control System')
            .replace('{reason}', 'Successfully checked states!') + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
