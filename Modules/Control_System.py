###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################



###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def search_wild_pokemon(image, state):
    if not state: return 'WAIT_HOME_SCREEN'

    # Nintendo Switch pairing controller menu
    elif state == 'WAIT_HOME_SCREEN':
        if all(pixel_value == 240 for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_1'
        # Wait

    # Nintendo Switch main menu
    elif state == 'RESTART_GAME_1':
        if all(pixel_value == 8 for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_2'
        # Press A

    # Game main loadscreen (Full black)
    elif state == 'RESTART_GAME_2':
        if all(pixel_value != 8 for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_3'
        # Press A

    # Game main loadscreen (Dialga / Palkia)
    elif state == 'RESTART_GAME_3':
        if all(pixel_value == 8 for pixel_value in image.check_pixel_color()):
            return 'RESTART_GAME_4'
        # Press A

    # Game main loadscreen (Full black)
    elif state == 'RESTART_GAME_4':
        if all(pixel_value != 8 for pixel_value in image.check_pixel_color()):
            return 'MOVE_PLAYER'
        # Wait

    # Game loaded, player in the overworld
    elif state == 'MOVE_PLAYER':
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']]
        ):
            return 'ENTER_COMBAT_1'
        # Up-Down / Right-Left

    # Combat loadscreen (Full white)
    elif state == 'ENTER_COMBAT_1':
        if not image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']]
        ):
            return 'ENTER_COMBAT_2'
        # wait

    # Combat loadscreen (Grass/Rock/Water animation)
    elif state == 'ENTER_COMBAT_2':
        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']]
        ):
            return 'ENTER_COMBAT_3'
        # wait

    # Combat loaded (Wild Pokémon appeared)
    elif state == 'ENTER_COMBAT_3':
        if not image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']]
        ):
            return 'CHECK_SHINY'
        # wait

    # Combat loaded (Wild Pokémon stars)
    elif state == 'CHECK_SHINY':
        n_contours = image.get_rectangles()
        image.draw_star(n_contours)
        
        if n_contours >= CONST.MIN_DETECTED_CONTOURS:
            return 'SHINY_FOUND'

        if image.check_multiple_pixel_colors(
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y1']],
            [CONST.TEXT_BOX_LINE['x'], CONST.TEXT_BOX_LINE['y2']]
        ):
            return 'ESCAPE_COMBAT'
        # wait

    

    return state

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import cv2
    import numpy as np
    from time import sleep

    from Image_Processing import Image_Processing
    from Game_Capture import Game_Capture

    Game_Capture = Game_Capture()
    state = 'MOVE_PLAYER'

    while True:
        sleep(0.01)
        image = Image_Processing(Game_Capture.read_frame())
        image.resize_image()
        image.get_mask()
        image.FPS_image = np.copy(image.resized_image)

        # print(image.check_pixel_color())
        state = search_wild_pokemon(image, state)
        print(state)

        if not isinstance(image.contours_image, type(None)): image.FPS_image = np.copy(image.contours_image)
        cv2.imshow('Image', image.FPS_image)

        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'): break

    Game_Capture.stop()