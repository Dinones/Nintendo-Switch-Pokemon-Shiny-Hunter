###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
from Modules.State_Machine import *
import Modules.Colored_Strings as STR
from Modules.FPS_Counter import FPS_Counter
from Modules.Game_Capture import Game_Capture
from Modules.Image_Processing import Image_Processing

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'State Machine'
INITIAL_STATE = 'MOVE_PLAYER'

LEFT_ARROW_KEY_VALUE = 65361
RIGHT_ARROW_KEY_VALUE = 65363

TESTING_VIDEO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.TESTING_VIDEO_PATH))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":

    def main_menu():
        print('\n' + STR.M_MENU.format(module=MODULE_NAME))
        print(STR.M_MENU_OPTION.format(index='1', option='Check states from capture card'))
        print(STR.M_MENU_OPTION.format(index='2', option='Check states from video'))

        option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

        menu_options = {
            '1': check_states,
            '2': check_states,
        }

        if option in menu_options: menu_options[option](option)
        else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME) + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def check_states(option):

        if option == '1':
            tool = 'capture card'
        elif option == '2':
            tool = 'video'

        print('\n' + STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action=f"Checking states using {tool}...",
            path=''
        ))

        if option == '1':
            Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
            if not Video_Capture.video_capture.isOpened():
                Video_Capture.stop()
                print(STR.GC_INVALID_VIDEO_CAPTURE.format(video_capture=CONST.VIDEO_CAPTURE_INDEX))
                return
    
        elif option == '2':
            if not os.path.exists(TESTING_VIDEO_PATH):
                print(STR.G_INVALID_PATH_ERROR.format(module='Image Processing', path=TESTING_VIDEO_PATH))
                return

            Video_Capture = Game_Capture(TESTING_VIDEO_PATH)

        FPS = FPS_Counter()
        state = INITIAL_STATE
        pause = False
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
            if image.original_image is None:
                break

            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            state = search_wild_pokemon(image, state)
            image.write_text(state, (0, CONST.TEXT_PARAMS['position'][1] + 5))

            current_frames += 1
            force_load_frame = False
            cv2.imshow(f'{CONST.BOT_NAME} - Image', image.FPS_image)

        Video_Capture.stop()
        print(STR.G_SUCCESS_EXIT_PROGRAM.format(module=MODULE_NAME, reason='Successfully checked states!'))

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
    print()
