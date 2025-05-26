###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
from time import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Modules.Image_Processing import Image_Processing
from Modules.Game_Capture import Game_Capture
from Modules.FPS_Counter import FPS_Counter
import Modules.Colored_Strings as STR
from Modules.Control_System import *
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Game Capture'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":

    def main_menu():
        print('\n' + STR.M_MENU.replace('{module}', 'Game Capture'))
        print(STR.M_MENU_OPTION.format(index = '1', option = 'Print all available video devices'))
        print(STR.M_MENU_OPTION.format(index = '2', option = 'Check current capture device'))

        option = input('\n' + STR.M_OPTION_SELECTION.replace('{module}', 'Game Capture'))

        menu_options = {
            '1': _print_video_captures,
            '2': _check_video_capture,
        }

        if option in menu_options: menu_options[option](option)
        else: print(STR.M_INVALID_OPTION.replace('{module}', 'Game Capture') + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def _print_video_captures(option: str) -> None:

        """
        Prints all available video capture devices to the console, along with formatted status messages.

        Args:
            option (str): Menu option for display purposes (e.g., "3").
        """

        print('\n' + STR.M_SELECTED_OPTION.format(
            module = MODULE_NAME,
            option = option,
            action = 'Printing all available video devices...',
            path = ''
        ))

        video_captures = Game_Capture.find_available_video_captures()
        print(STR.GC_AVAILABLE_CAPTURE_DEVICES)

        for index, is_available in enumerate(video_captures):
            if is_available:
                print(STR.GC_CAPTURE_DEVICE_OK.replace('{index}', str(index)))
            else:
                print(STR.GC_CAPTURE_DEVICE_NOT_OK.replace('{index}', str(index)))

    #######################################################################################################################
    #######################################################################################################################

    def _check_video_capture(option):
        print('\n' + STR.M_SELECTED_OPTION
            .replace('{module}', 'Game Capture')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Activating capture device nº{CONST.VIDEO_CAPTURE_INDEX}...")
            .replace('{path}', f"")
        )

        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
        if not Video_Capture.video_capture.isOpened(): 
            Video_Capture.stop()
            print(STR.GC_INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'") + '\n')
            return
        FPS = FPS_Counter()

        print(STR.G_PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'c'")
            .replace('{instruction}', 'take a screenshot')
        ); print(STR.G_PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'q'")
            .replace('{instruction}', 'exit the program')
        )

        while True: 
            image = Image_Processing(Video_Capture.read_frame())
            if isinstance(image.original_image, type(None)): continue

            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            cv2.imshow(f'{CONST.BOT_NAME} - Device {CONST.VIDEO_CAPTURE_INDEX}', image.FPS_image)

            # Press 'q' to stop the program
            # Press 'c' to take a screenshot
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'): break
            elif key == ord('c') or key == ord('C'): 
                if not os.path.exists(f'../{CONST.SAVING_FRAMES_PATH}'):
                    print(STR.G_INVALID_PATH_WARNING
                        .replace('{module}', 'Game Capture')
                        .replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}'")
                    )
                    continue

                file_name = str(time())
                cv2.imwrite(f'../{CONST.SAVING_FRAMES_PATH}/{file_name}.png', image.original_image)
                print(STR.GC_IMAGE_SAVED.replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}/{file_name}.png'"))
            
        # Release the capture card and close all windows
        Video_Capture.stop()

        print(STR.G_SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Game Capture')
            .replace('{reason}', 'Successfully activated video device!')
        )

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
    print()