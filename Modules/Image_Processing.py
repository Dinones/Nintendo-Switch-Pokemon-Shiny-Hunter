###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import cv2
import numpy as np

import sys; sys.path.append('..')
import Colored_Strings as COLOR_str
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Image_Processing():
    def __init__(self, image = ''):
        self.original_image = None
        self.grayscale_image = None
        self.resized_image = None
        self.tkinter_image = None
        self.masked_image = None
        self.contours_image = None
        self.FPS_image = None

        # Load the image
        if isinstance(image, str): self.original_image = cv2.imread(image)
        else: self.original_image = image
        if isinstance(self.original_image, type(None)): return print(COLOR_str.COULD_NOT_PROCESS_IMAGE + '\n')

    #######################################################################################################################

    def resize_image(self, desired_size = CONST.BOT_WINDOW_SIZE):
        if isinstance(self.original_image, type(None)): return

        # Get the desired aspect ratio and size
        aspect_ratio = CONST.ORIGINAL_FRAME_SIZE[0]/CONST.ORIGINAL_FRAME_SIZE[1]
        # (width, height)
        original_size = self.original_image.shape[1::-1]
        max_size_index = np.argmax(original_size)
        if not max_size_index: new_size = [desired_size[max_size_index], int(desired_size[max_size_index]/aspect_ratio)]
        else: new_size = [int(desired_size[max_size_index]*aspect_ratio), desired_size[max_size_index]]

        # Resize the image
        self.resized_image = cv2.resize(self.original_image, new_size)

    #######################################################################################################################

    def get_mask(self):
        if isinstance(self.resized_image, type(None)): return

        self.grayscale_image = cv2.cvtColor(self.resized_image, cv2.COLOR_BGR2GRAY)
        _, self.masked_image = cv2.threshold(self.grayscale_image, CONST.LOWER_COLOR, CONST.UPPER_COLOR, cv2.THRESH_BINARY)

    #######################################################################################################################

    def get_rectangles(self):
        if isinstance(self.masked_image, type(None)): return
        self.contours_image = np.copy(self.resized_image)

        contours, hierarchy = cv2.findContours(self.masked_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = []

        import random
        for contour in contours:
            # Minimum object size to detect as a match
            if cv2.contourArea(contour) > CONST.MIN_DETECT_SIZE:
                filtered_contours.append(contour)
                # Draw the rectangles
                x, y, w, h = cv2.boundingRect(contour)
                # The "-1" parameter indicates that all contours should be drawn
                cv2.drawContours(self.contours_image, filtered_contours, -1, CONST.RECTANGLES_PARAMS['color'], 
                    CONST.RECTANGLES_PARAMS['thickness'])

        return len(filtered_contours)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import time
    from Game_Capture import Game_Capture
    
    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU
            .replace('{module}', 'Image Processing')
            .replace('{options}', '[1] Process video\n    [2] Process image\n    [3] Extract frames from video')
        )
        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Image Processing'))
        # option = '1'

        menu_options = {
            '1': process_video,
            '2': process_image,
            '3': extract_frames_from_video,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Image Processing') + '\n')

    #######################################################################################################################

    def process_video(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Processing video '../{CONST.TESTING_VIDEO_PATH}'")
        )

        if not os.path.exists(f'../{CONST.TESTING_VIDEO_PATH}'): 
            return print(COLOR_str.INVALID_PATH
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}'") + '\n'
            )

        Video_Capture = Game_Capture(f'../{CONST.TESTING_VIDEO_PATH}')
        image = Image_Processing(Video_Capture.frame)

        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'q'")
            .replace('{instruction}', 'exit the program')
        )

        while True:
            image.original_image = Video_Capture.read_frame()
            # No more frames in the video
            if isinstance(image.original_image, type(None)): break

            image.resize_image()
            image.get_mask()
            contours = image.get_rectangles()

            cv2.imshow(f'{CONST.BOT_NAME} - Contours', image.contours_image)
            cv2.imshow(f'{CONST.BOT_NAME} - Mask', image.masked_image)

            # Press 'q' to stop the program
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'): break

            time.sleep(0.1)

        Video_Capture.stop()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the video!') + '\n'
        )

    #######################################################################################################################

    def process_image(option): 
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Processing image '../{CONST.TESTING_IMAGE_PATH}'")
        )

        image = Image_Processing(f'../{CONST.TESTING_IMAGE_PATH}' )
        if isinstance(image.original_image, type(None)): return

        image.resize_image()
        image.get_mask()
        contours = image.get_rectangles()

        print(COLOR_str.CONTOURS_FOUND.replace('{contours}', str(contours)))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'q'")
            .replace('{instruction}', 'exit the program')
        )

        # cv2.imshow(f'{CONST.BOT_NAME} - Original', image.resized_image)
        # cv2.imshow(f'{CONST.BOT_NAME} - Grayscale', image.grayscale_image)
        cv2.imshow(f'{CONST.BOT_NAME} - Mask', image.masked_image)
        cv2.imshow(f'{CONST.BOT_NAME} - Contours', image.contours_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the image!') + '\n'
        )

    #######################################################################################################################

    def extract_frames_from_video(option): 
        print(COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f'Extracting frames to \'{CONST.SAVING_FRAMES_PATH}\'...')
        )

        if not os.path.exists(f'../{CONST.TESTING_VIDEO_PATH}') or not os.path.exists(f'../{CONST.SAVING_FRAMES_PATH}'): 
            return print(COLOR_str.INVALID_PATH
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}' or '../{CONST.SAVING_FRAMES_PATH}'") + '\n'
            )

        Video_Capture = Game_Capture(f'../{CONST.TESTING_VIDEO_PATH}')
        image = Image_Processing(Video_Capture.frame)

        total_frames = int(Video_Capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_index = 1
        
        print(COLOR_str.CURRENT_EXTRACTED_FRAMES
            .replace('{extracted_frame}', str(frame_index))
            .replace('{total_frames}', str(total_frames))
            .replace('{percentage}', '0'), end='\r', flush=True
        )

        while True:
            image.original_image = Video_Capture.read_frame()
            # No more frames in the video
            if isinstance(image.original_image, type(None)): print(); break

            cv2.imwrite(f'../{CONST.SAVING_FRAMES_PATH}/{frame_index}.png', image.original_image)

            # Inefficient? Maybe, but looks cool and does not affect the main code
            print(COLOR_str.CURRENT_EXTRACTED_FRAMES
                .replace('{extracted_frame}', str(frame_index + 1))
                .replace('{total_frames}', str(total_frames))
                .replace('{percentage}', str(int((frame_index + 1)/total_frames*100))), end='\r', flush=True
            )         

            frame_index += 1

        Video_Capture.stop()
        print(COLOR_str.SUCCESSFULLY_EXTRACTED_FRAMES.replace('{frames}', str(frame_index)) + '\n')

    #######################################################################################################################

    main_menu()