###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
from time import time

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

MODULE_NAME = 'Game Capture'
SCREENSHOTS_OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.SAVING_FRAMES_PATH))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":

    def main_menu():
        print('\n' + STR.M_MENU.format(module=MODULE_NAME).format(module=MODULE_NAME))
        print(STR.M_MENU_OPTION.format(index = '1', option = 'Print all available video devices'))
        print(STR.M_MENU_OPTION.format(index = '2', option = 'Check current capture device'))

        option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

        menu_options = {
            '1': _print_video_captures,
            '2': _check_video_capture,
        }

        if option in menu_options: menu_options[option](option)
        else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME) + '\n')

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
                print(STR.GC_CAPTURE_DEVICE_OK.format(index=index))
            else:
                print(STR.GC_CAPTURE_DEVICE_NOT_OK.format(index=index))

    #######################################################################################################################
    #######################################################################################################################

    def _check_video_capture(option: str) -> None:

        """
        Show the frames for a video capture device.

        Args:
            option (str): Menu option for display purposes (e.g., "3").
        """

        print('\n' + STR.M_SELECTED_OPTION.format(
            module = MODULE_NAME,
            option = option,
            action = f"Activating capture device nº{CONST.VIDEO_CAPTURE_INDEX}...",
            path = ''
        ))

        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)

        if not Video_Capture.video_capture.isOpened():
            Video_Capture.stop()
            print(STR.GC_INVALID_VIDEO_CAPTURE.format(video_capture=CONST.VIDEO_CAPTURE_INDEX) + '\n')
            return

        FPS = FPS_Counter()

        print(STR.G_PRESS_KEY_TO_INSTRUCTION.format(module=MODULE_NAME, key="'c'", instruction='take a screenshot'))
        print(STR.G_PRESS_KEY_TO_INSTRUCTION.format(module=MODULE_NAME, key="'q'", instruction='exit the program'))

        while True:
            image = Image_Processing(Video_Capture.read_frame())

            if image.original_image is None:
                continue

            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            cv2.imshow(f'{CONST.BOT_NAME} - Device {CONST.VIDEO_CAPTURE_INDEX}', image.FPS_image)

            key = cv2.waitKey(1)
            if key in (ord('q'), ord('Q')):
                break
            elif key in (ord('c'), ord('C')):
                if not os.path.exists(SCREENSHOTS_OUTPUT_PATH):
                    print(STR.G_INVALID_PATH_WARNING.format(module=MODULE_NAME, path=f"'{SCREENSHOTS_OUTPUT_PATH}'"))
                    continue

                output_file_path = os.path.join(SCREENSHOTS_OUTPUT_PATH, f"{int(time())}.png")
                cv2.imwrite(output_file_path, image.original_image)
                print(STR.GC_IMAGE_SAVED.replace('{path}', f"'{output_file_path}'"))

        Video_Capture.stop()

        print(STR.G_SUCCESS_EXIT_PROGRAM.format(module=MODULE_NAME, reason='Successfully activated video device!'))

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
    print()