###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import cv2
from time import time, sleep

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

def search_wild_pokemon(image, state):
    if not state: return 'WAIT_HOME_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        if all(pixel_value == CONST.PAIRING_MENU_COLOR for pixel_value in image.check_pixel_color()):
            return 'FAST_RESTART_GAME'

    # Nintendo Switch pairing controller menu
    elif state == 'FAST_RESTART_GAME':
        if not all(pixel_value == CONST.HOME_MENU_COLOR for pixel_value in image.check_pixel_color()):
            return 'MOVE_PLAYER'

    # Stuck screen (only used when the bot gets stuck in one state)
    elif state == 'RESTART_GAME_0':
        if all(pixel_value == CONST.HOME_MENU_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_1'

    # Nintendo Switch main menu
    elif state == 'RESTART_GAME_1':
        if all(pixel_value == CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_2'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_2':
        if all(pixel_value != CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_3'

    # Game main loadscreen (Dialga / Palkia)
    elif state == 'RESTART_GAME_3':
        if all(pixel_value == CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_4'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_4':
        if all(pixel_value != CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'MOVE_PLAYER'

    # Game loaded, player in the overworld
    elif state == 'MOVE_PLAYER':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ENTER_COMBAT_1'

    # Combat loadscreen (Full white screen)
    elif state == 'ENTER_COMBAT_1':
        # Check if the text box has disappeared
        if not image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ENTER_COMBAT_2'

    # Combat loadscreen (Grass/Rock/Water animation)
    elif state == 'ENTER_COMBAT_2':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ENTER_COMBAT_3'

    # Combat loaded (Wild Pokémon appeared)
    elif state == 'ENTER_COMBAT_3':
        # Check if the text box has disappeared
        if not image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ): 
            return 'CHECK_SHINY'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ESCAPE_COMBAT_1'

        # Check the elapsed time
        if image.shiny_detection_time and time() - image.shiny_detection_time >= CONST.SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

    # Combat loaded (Both Pokémon in the field)
    elif state == 'ESCAPE_COMBAT_1':
        # Look for the life box
        if image.check_multiple_pixel_colors(
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y1']],
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y2']], CONST.LIFE_BOX_LINE['color']
        ):
            return 'ESCAPE_COMBAT_2'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_2':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ESCAPE_COMBAT_3'

    # Combat loaded (Escaping combat)
    elif state == 'ESCAPE_COMBAT_3':
        # Check if the text box has disappeared
        if not image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ESCAPE_COMBAT_4'

    # Combat loaded (Escaped combat / Failed escaping)
    elif state == 'ESCAPE_COMBAT_4':
        # Look for the black screen
        if image.check_multiple_pixel_colors(
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y1']],
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y2']], CONST.ESCAPE_COMBAT_BLACK_COLOR
        ):
            return 'ESCAPE_COMBAT_5'
        # Look for the life box (Escape has failed)
        elif image.check_multiple_pixel_colors(
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y1']],
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y2']], CONST.LIFE_BOX_LINE['color']
        ):
            return 'ESCAPE_FAILED_1'

    # Escaped from combat (Full black screen)
    elif state == 'ESCAPE_COMBAT_5':
        # Check if the black screen has ended
        if not image.check_multiple_pixel_colors(
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y1']],
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y2']], CONST.ESCAPE_COMBAT_BLACK_COLOR
        ):
            return 'MOVE_PLAYER'

    # Failed escapping (Both Pokémon in the field)
    elif state == 'ESCAPE_FAILED_1':
        # Look for the life box
        if image.check_multiple_pixel_colors(
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y1']],
            [CONST.LIFE_BOX_LINE['x'], CONST.LIFE_BOX_LINE['y2']], CONST.LIFE_BOX_LINE['color']
        ):
            return 'ESCAPE_FAILED_2'

    # Failed escapping (Escaping combat)
    elif state == 'ESCAPE_FAILED_2':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ESCAPE_COMBAT_3'

    return state

###########################################################################################################################

def static_encounter(image, state):
    if not state: return 'WAIT_HOME_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        if all(pixel_value == CONST.PAIRING_MENU_COLOR for pixel_value in image.check_pixel_color()):
            return 'FAST_RESTART_GAME'

    # Nintendo Switch pairing controller menu
    elif state == 'FAST_RESTART_GAME':
        if not all(pixel_value == CONST.HOME_MENU_COLOR for pixel_value in image.check_pixel_color()):
            return 'ENTER_STATIC_COMBAT'

    # Stuck screen (only used when the bot gets stuck in one state)
    elif state == 'RESTART_GAME_0':
        if all(pixel_value == CONST.HOME_MENU_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_1'

    # Nintendo Switch main menu
    elif state == 'RESTART_GAME_1':
        if all(pixel_value == CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_2'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_2':
        if all(pixel_value != CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_3'

    # Game main loadscreen (Dialga / Palkia)
    elif state == 'RESTART_GAME_3':
        if all(pixel_value == CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_4'

    # Game main loadscreen (Full black screen)
    elif state == 'RESTART_GAME_4':
        if all(pixel_value != CONST.GAME_LOAD_SCREEN_BLACK_COLOR for pixel_value in image.check_pixel_color()):
            return 'ENTER_STATIC_COMBAT'

    # Game loaded, player in the overworld
    elif state == 'ENTER_STATIC_COMBAT':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ENTER_COMBAT_1'

    # Combat loadscreen (Full white screen)
    elif state == 'ENTER_COMBAT_1':
        # Check if the text box has disappeared
        if not image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ENTER_COMBAT_2'

    # Combat loadscreen (Grass/Rock/Water animation)
    elif state == 'ENTER_COMBAT_2':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'ENTER_COMBAT_3'

    # Combat loaded (Wild Pokémon appeared)
    elif state == 'ENTER_COMBAT_3':
        # Check if the text box has disappeared
        if not image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'CHECK_SHINY'

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        # Look for the text box
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']], CONST.TEXT_BOX_LINE['color']
        ):
            return 'RESTART_GAME_1'

        # Check the elapsed time
        if image.shiny_detection_time and time() - image.shiny_detection_time >= CONST.SHINY_DETECTION_TIME:
            return 'SHINY_FOUND'

    return state

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import numpy as np

    from Image_Processing import Image_Processing
    from Game_Capture import Game_Capture

    Game_Capture = Game_Capture()
    state = 'MOVE_PLAYER'

    while True:
        sleep(0.01)
        image = Image_Processing(Game_Capture.read_frame())
        image.resize_image()
        image.FPS_image = np.copy(image.resized_image)

        # print(image.check_pixel_color())
        state = search_wild_pokemon(image, state)
        print(state)

        if not isinstance(image.resized_image, type(None)): image.FPS_image = np.copy(image.resized_image)
        cv2.imshow(f'{CONST.BOT_NAME} - Image', image.FPS_image)

        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'): break

    Game_Capture.stop()