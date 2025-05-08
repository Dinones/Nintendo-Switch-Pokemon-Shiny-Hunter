###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
import pytesseract
import numpy as np
import PyQt5.QtGui as pyqt_g
from typing import Tuple, Union
from time import time, perf_counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Modules.Colored_Strings as COLOR_str
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Image_Processing():
    def __init__(self, image: Union[str, np.ndarray] = ''):
        self.original_image = None
        self.resized_image = None
        self.pyqt_image = None
        self.FPS_image = None
        self.shiny_detection_time = 0

        # File path used to store notification image
        self.saved_image_path = ''

        # Only used in the controller image to avoid redundant operations
        self.current_button_pressed = ''

        # Tracks changes in debug state to avoid redundant image updates
        self.debug_image_stats = {
            'event': '',
            'button': ''
        }

        # Load the image
        if isinstance(image, str):
            self.original_image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        else:
            self.original_image = image

        # If image loading failed
        if self.original_image is None:
            print(COLOR_str.COULD_NOT_PROCESS_IMAGE)

    #######################################################################################################################
    #######################################################################################################################

    def resize_image(self, desired_size = CONST.MAIN_FRAME_SIZE):
    
        """
        Resizes the original image to fit within a maximum bounding box while preserving the aspect ratio.

        Args:
            desired_size (Tuple[int, int]): Target bounding box size (width, height) for resizing

        Returns:
            None
        """

        # If there is no image to resize, exit early
        if self.original_image is None:
            return

        # Extract original size from image shape
        width, height = self.original_image.shape[1::-1]

        # Calculate aspect ratio
        aspect_ratio = width / height

        # Determine whether width or height is the constraining dimension
        max_size_index = np.argmax((width, height))

        # Compute new size maintaining aspect ratio
        if max_size_index == 0:  # Width is the limiting dimension
            new_size = [
                desired_size[max_size_index],
                int(desired_size[max_size_index] / aspect_ratio)
            ]
        else:  # Height is the limiting dimension
            new_size = [
                int(desired_size[max_size_index] * aspect_ratio),
                desired_size[max_size_index]
            ]

        # Resize the image using OpenCV
        self.resized_image = cv2.resize(self.original_image, new_size)  

    #######################################################################################################################
    #######################################################################################################################




    # Ensure FPS image is initialized
    def _ensure_fps_image(self, force = False):
        if self.FPS_image is None or force:
            # Without copy() method, images would be linked, meaning that modifying one image would also alter the other
            self.FPS_image = np.copy(self.resized_image)




    #######################################################################################################################
    #######################################################################################################################

    def draw_FPS(self, FPS: int = 0):

        """
        Wrapper for write_text to draw FPS at default position.

        Args:
            FPS (int): The current frames-per-second value to overlay.
        
        Returns:
            None
        """

        self.write_text(f'FPS: {FPS}')

    #######################################################################################################################
    #######################################################################################################################

    def write_text(self, text: str = '', position_offset: Tuple[int, int] = (0, 0)) -> None:

        """
        Writes arbitrary text onto the FPS image at a specified offset from the default position.

        Args:
            text (str): The text to display.
            position_offset (Tuple[int, int]): (x, y) offset added to the default position.

        Returns:
            None
        """

        # Ensure FPS image is available and synced with the resized image
        self._ensure_fps_image()

        # Compute the final position by offsetting the default
        position = tuple(a + b for a, b in zip(CONST.TEXT_PARAMS['position'], position_offset))

        # Draw the text on the FPS image
        cv2.putText(
            self.FPS_image,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            CONST.TEXT_PARAMS['font_scale'],
            CONST.TEXT_PARAMS['font_color'],
            CONST.TEXT_PARAMS['thickness'],
            cv2.LINE_AA
        )

    #######################################################################################################################
    #######################################################################################################################

    def get_pyqt_image(self, image: np.ndarray) -> None:
        
        """
        Converts an OpenCV image (NumPy array) to a QPixmap compatible with PyQt. Support both grayscale (2D) and color
        (3D) images.

        Args:
            image (np.ndarray): The image to convert, in BGR format (OpenCV).

        Returns:
            None
        """

        # Color image (3D)
        if len(image.shape) == 3:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            # Convert from BGR (OpenCV) to RGB (Qt expects RGB)
            aux_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qt_format = pyqt_g.QImage.Format_RGB888
        # Grayscale image (2D)
        else:
            height, width = image.shape
            bytes_per_line = width
            aux_image = image
            qt_format = pyqt_g.QImage.Format_Grayscale8

        # Create QImage from the raw image buffer
        qt_image = pyqt_g.QImage(aux_image.data, width, height, bytes_per_line, qt_format)

        # Convert QImage to QPixmap for display
        self.pyqt_image = pyqt_g.QPixmap.fromImage(qt_image)

    #######################################################################################################################
    #######################################################################################################################

    def draw_button(self, button: str = '') -> None:

        """
        Draws a filled circle on the FPS image to indicate the specified button press.

        Args:
            button (str): The name of the button to highlight ('A', 'B', 'HOME', ...).

        Returns:
            None
        """

        # Skip drawing if input is not a string or the same button is already drawn
        if not isinstance(button, str) or self.current_button_pressed == button:
            return

        # Start from a fresh copy of the resized image
        self._ensure_fps_image(force = True)

        # Map button names to fixed pixel coordinates on the controller overlay
        button_coordinates = {
            'A': (307, 80),
            'B': (288, 99),
            'Y': (269, 80),
            'X': (288, 61),
            'HOME': (275, 195),
            'UP': (62, 129),
            'DOWN': (61, 167),
            'RIGHT': (81, 148),
            'LEFT': (43, 148)
        }

        # If the button exists in the map, draw a filled circle on it
        if button in button_coordinates:
            cv2.circle(self.FPS_image, button_coordinates[button], 9, CONST.PRESSED_BUTTON_COLOR, -1)
            self.current_button_pressed = button

    #######################################################################################################################
    #######################################################################################################################

    def get_pixel_color(self, pixel: Tuple[int, int] = (20, 20)) -> Union[int, np.ndarray]:

        """
        Returns the color value of a specific pixel in the original image.

        Args:
            pixel (Tuple[int, int]): The (y, x) coordinates of the pixel to retrieve. Defaults to (20, 20).

        Returns:
            Union[int, np.ndarray]: The pixel color value. Returns:
                - int for grayscale images
                - np.ndarray of shape (3,) for color images (BGR order)
        """

        return self.original_image[pixel[0], pixel[1]]


    #######################################################################################################################

    # Return if the pixel is of the specified color
    def check_pixel_color(self, color, pixel = (20, 20)):
        # return all(self.original_image[pixel[0]][pixel[1]] == color)
        differences = [abs(self.original_image[pixel[0]][pixel[1]][color_index] - color[color_index])
            for color_index in range(3)]
        return all(difference <= CONST.PIXEL_COLOR_DIFF_THRESHOLD for difference in differences)

    #######################################################################################################################

    def check_column_pixel_colors(
        self,
        position: Tuple[int, int],
        column_height: int, 
        color: Tuple[int, int, int],
        threshold: int = CONST.PIXEL_COLOR_DIFF_THRESHOLD
    ) -> bool:

        """
        Check if all pixels in a specified column are of the specified color.

        Args:
            position (tuple): The starting bottom position (x, y) of the column.
            column_height (int): The height of the column to check.
            color (tuple): The color to check against.
            threshold (int): The maximum difference allowed between the pixel color and the specified color. (Default: 
                CONST.PIXEL_COLOR_DIFF_THRESHOLD)

        Returns:
            bool: True if all pixels match the specified color, False otherwise.
        """
        
        self._ensure_fps_image()

        match_pixels = True
        for row_index in range(position[1], position[1] + column_height):
            differences = [abs(self.resized_image[-row_index][position[0]][color_index] - color[color_index])
                for color_index in range(3)]

            # If one False is found, there is no need to check the other pixels
            if not all(difference <= threshold for difference in differences):
                match_pixels = False
                break

        self.draw_column(position, column_height)

        return match_pixels

    #######################################################################################################################

    def draw_column(self, position: Tuple[int, int], column_height: int) -> None:

        if CONST.TESTING:
            for row_index in range(position[1], position[1] + column_height):
                self.FPS_image[-row_index][position[0]] = CONST.TESTING_COLOR

    #######################################################################################################################

    # Read the pokémon name
    def recognize_pokemon(self):
        # Format: [y1:y2, x1:x2]
        # Wild Pokémon: [27:43, 535:650] | Player Pokémon: [y1:y2, x1:x2] | Text Box: [333:365, 50:670]
        name_image = self.resized_image[333:365, 50:670]
        name_image = cv2.cvtColor(name_image, cv2.COLOR_BGR2GRAY)

        # --oem 1: Faster and use less resources
        # --psm 6: Assume a single uniform block of text
        custom_config = '--oem 1 --psm 6'
        text = pytesseract.image_to_string(name_image, config=custom_config)

        # EN: Dialga appeared! | A wild Drifloon appeared! | Go! Chimchar!
        # FR: Dialga apparaît! | Un Baudrive sauvage apparaît! | Ouisticram! Go!
        # ES: ¡Es Dialga! | ¡Ha aparecido un Drifloon salvaje! | ¡Adelante, Chimchar!
        # IT: È apparso Dialga! | Ah! È apparso un Drifloon selvatico! | Avanti, Chimchar!
        # DE: Dialga erscheint! | Ein Driftlon (wild) erscheint! | Los, Panflam!
        # For the KO, ZH-CN and ZH-TW cases, it will return the whole text line
        if CONST.LANGUAGE in ('FR', 'ES', 'EN', 'DE', 'IT'):
            # Replace '¡' and "Go!" for the Spanish and French cases.
            pokemon_name = text
            for part in ['Go!', '¡', '!']: pokemon_name = pokemon_name.replace(part, '')
            pokemon_name = pokemon_name.split(' ')
            for word in pokemon_name[::-1]:
                # Empty spaces ['Ouisticram!', ''] will make it crash
                if word and word[0].isupper():
                    text = word; break
       
        text = text.strip()
        return text

    #######################################################################################################################

    # Save the image
    def save_image(self, pokemon_name = ''):
        file_name = f'{pokemon_name}_{str(int(time()))}' if pokemon_name else str(int(time()))
        self.saved_image_path = f'./{CONST.IMAGES_FOLDER_PATH}{file_name}.png'
        cv2.imwrite(self.saved_image_path, self.original_image)

    #######################################################################################################################

    # Color the specified pixel of the original image
    def replace_pixels(self, pixel_color):
        mask = np.all(self.original_image == pixel_color, axis=-1)
        self.original_image[mask] = CONST.TESTING_COLOR

    #######################################################################################################################

    def populate_debug_image(self, stats):
        # Only populates if something has changed to reduce workload
        for key in stats:
            if stats.get(key) != self.debug_image_stats.get(key):
                self.FPS_image = np.copy(self.original_image)
                cv2.putText(
                    self.FPS_image, f'Button: {stats.get("button")}',
                    CONST.DEBUG_IMAGE_TEXT_PARAMS['button_position'], cv2.FONT_HERSHEY_SIMPLEX, 
                    CONST.DEBUG_IMAGE_TEXT_PARAMS['font_scale'], CONST.DEBUG_IMAGE_TEXT_PARAMS['font_color'], 
                    CONST.DEBUG_IMAGE_TEXT_PARAMS['thickness'], cv2.LINE_AA
                )
                cv2.putText(
                    self.FPS_image, f'| State: {stats.get("event")}', 
                    CONST.DEBUG_IMAGE_TEXT_PARAMS['state_position'], cv2.FONT_HERSHEY_SIMPLEX, 
                    CONST.DEBUG_IMAGE_TEXT_PARAMS['font_scale'], CONST.DEBUG_IMAGE_TEXT_PARAMS['font_color'], 
                    CONST.DEBUG_IMAGE_TEXT_PARAMS['thickness'], cv2.LINE_AA
                )
                self.debug_image_stats = stats
                return

    #######################################################################################################################

    @staticmethod
    def stack_images(image_1, image_2):
        # Vertical stack. Image_1 Top - Image_2 - Bottom
        return np.vstack((image_1, image_2))

###########################################################################################################################

def create_debug_image(frame_size = CONST.DEBUG_FRAME_SIZE):
    black_image = np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)

    # Same color as for the GUI borders (#aaa)
    border_color = [170, 170, 170] 
    border_thickness = 1
    black_image[:border_thickness, :] = border_color  # Top
    black_image[-border_thickness:, :] = border_color  # Bottom
    black_image[:, :border_thickness] = border_color  # Left
    black_image[:, -border_thickness:] = border_color  # Right

    debug_image = Image_Processing(black_image)

    return debug_image

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import logging
    from time import sleep
    from Control_System import *
    from Game_Capture import Game_Capture

    #######################################################################################################################

    LEFT_ARROW_KEY_VALUE = 65361
    RIGHT_ARROW_KEY_VALUE = 65363
   
    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Image Processing'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Process image'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Process video'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '3').replace('{option}', 'Extract frames from video'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '4').replace('{option}', 'Check lost shiny'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '5').replace('{option}', 'Test debug video frame'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Image Processing'))

        menu_options = {
            '1': process_image,
            '2': process_video,
            '3': extract_frames_from_video,
            '4': check_lost_shiny,
            '5': check_debug_video_frames,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Image Processing') + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def process_image(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Processing image")
            .replace('{path}', f"'../{CONST.TESTING_IMAGE_PATH}'")
        )

        if not os.path.exists(f'../{CONST.TESTING_IMAGE_PATH}'):
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_IMAGE_PATH}'") + '\n'
            )

        image = Image_Processing(f'../{CONST.TESTING_IMAGE_PATH}')
        if isinstance(image.original_image, type(None)): return
        image.resize_image()
        # Linked images: If one image is edited, the other one is too
        image.FPS_image = image.resized_image

        # image.replace_pixels([141, 140, 130])
        # print(image.check_pixel_color())
        # cv2.circle(image.original_image, (20, 20), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        # cv2.rectangle(image.resized_image, (50, 333), (670, 365), (255, 255, 0), 1)
        # print(image.recognize_pokemon())
        # print(image.check_column_pixel_colors(
        #     (int(CONST.MAIN_FRAME_SIZE[0] // 16 * 13), int(CONST.MAIN_FRAME_SIZE[1] // 16 * 4)),
        #     CONST.COLOR_SCREEN_CHECK['column_height'],
        #     CONST.COLOR_SCREEN_CHECK['white_color']
        # ))
        
        print(is_life_box_visible(image))

        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', 'any key')
            .replace('{instruction}', 'exit the program')
        )

        # cv2.imshow(f'{CONST.BOT_NAME} - Resized', image.original_image[0:500])
        cv2.imshow(f'{CONST.BOT_NAME} - Resized', image.FPS_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the image!') + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    def extract_frames_from_video(option):
        print(COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f'Extracting frames into')
            .replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}'")
        )

        if not os.path.exists(f'../{CONST.TESTING_VIDEO_PATH}') or not os.path.exists(f'../{CONST.SAVING_FRAMES_PATH}'):
            return print(COLOR_str.INVALID_PATH_ERROR
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

            # Inefficient? Maybe, but looks cool and doesn't affect the main code
            print(COLOR_str.CURRENT_EXTRACTED_FRAMES
                .replace('{extracted_frame}', str(frame_index + 1))
                .replace('{total_frames}', str(total_frames))
                .replace('{percentage}', str(int((frame_index + 1)/total_frames*100))), end='\r', flush=True
            )        

            frame_index += 1

        Video_Capture.stop()
        print(COLOR_str.SUCCESSFULLY_EXTRACTED_FRAMES.replace('{frames}', str(frame_index)) + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def process_video(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Processing video")
            .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}'")
        )

        if not os.path.exists(f'../{CONST.TESTING_VIDEO_PATH}'):
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}'") + '\n'
            )

        Video_Capture = Game_Capture(f'../{CONST.TESTING_VIDEO_PATH}')
        image = Image_Processing(Video_Capture.frame)

        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'Q'")
            .replace('{instruction}', 'exit the program')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'SPACE'")
            .replace('{instruction}', 'pause/resume the execution')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'A'")
            .replace('{instruction}', 'move a frame backwards')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'D'")
            .replace('{instruction}', 'move a frame forward')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'C'")
            .replace('{instruction}', 'take a screenshot')
        )

        frame_index = 0
        pause = False
        total_video_frames = int(Video_Capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        def process_single_frame(image, frame = None):
            if not isinstance(frame, type(None)): Video_Capture.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

            image.original_image = Video_Capture.read_frame()
            # No more frames in the video
            if isinstance(image.original_image, type(None)): return

            image.resize_image()

            cv2.imshow(f'{CONST.BOT_NAME} - Resized', image.resized_image)

        while True:
            if pause:
                # Press 'SPACE' to resume the execution
                # Press 'a' or '<' and 'd' or '>' to move between frames
                # Press 'c' to take a sceenshot
                # Press 'q' to stop the program
                key = cv2.waitKeyEx(1)
                if key in [ord('q'), ord('Q')]: break
                elif key == ord(' '): pause = not pause
                elif key in [ord('a'), ord('A'), LEFT_ARROW_KEY_VALUE]:
                    if frame_index > 0:
                        frame_index = frame_index - 1
                        process_single_frame(image, frame_index)
                        continue
                elif key in [ord('d'), ord('D'), RIGHT_ARROW_KEY_VALUE]:
                    if frame_index < total_video_frames:
                        frame_index = frame_index + 1
                        process_single_frame(image, frame_index)
                        continue
                elif key in [ord('c'), ord('C')]:
                    cv2.imwrite(f'../{CONST.SAVING_FRAMES_PATH}/{frame_index}.png', image.original_image)
                    print(COLOR_str.IMAGE_SAVED.replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}/{frame_index}.png'"))

                # Reduce workload
                sleep(0.05)
                continue

            process_single_frame(image)
            # No more frames in the video
            if isinstance(image.original_image, type(None)): break

            # Press 'SPACE' to pause the execution
            # Press 'q' to stop the program
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'): break
            if key == ord(' '): pause = not pause

            frame_index += 1
            sleep(0.016)

        Video_Capture.stop()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the video!') + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    def check_lost_shiny(option):
        """
        Display images one by one.
        The user can pause/resume the processing using the space bar.
        While paused, the user can navigate between images using the 'a' (previous) and 'd' (next) keys.
        The user can quit the process using the 'q' key.

        Key Presses:
            - 'q' or 'Q': Quit the image processing loop.
            - ' ' (space): Pause or resume the image processing.
            - 'a', 'A' or '<' (left arrow): Move to the previous image (while paused).
            - 'd', 'D' or '>' (right arrow): Move to the next image (while paused).
            - If not paused, images will automatically progress.
        """

        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', "Checking lost shiny")
            .replace('{path}', "")
        )

        if not os.path.exists(f'../{CONST.IMAGES_FOLDER_PATH}'):
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.IMAGES_FOLDER_PATH}'") + '\n'
            )
       
        images = sorted([image for image in sorted(os.listdir(f'../{CONST.IMAGES_FOLDER_PATH}'))
            if image.lower().endswith(('.png', '.jpg', 'jpeg'))])

        if not len(images):
            print(COLOR_str.COULD_NOT_LOAD_IMAGES.replace('{path}', f"'../{CONST.IMAGES_FOLDER_PATH}'") + '\n')
            return

        # Instructions
        print(COLOR_str.SUCCESSFULLY_LOADED_IMAGES.replace('{images}', str(len(images))))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION.replace('{key}', "'SPACE'")
            .replace('{module}', 'Image Processing')
            .replace('{instruction}', 'pause the program'))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION.replace('{key}', "'A' or '<' and 'D' or '>'")
            .replace('{module}', 'Image Processing')
            .replace('{instruction}', 'go back / forward while in pause'))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION.replace('{key}', "'Q'")
            .replace('{module}', 'Image Processing')
            .replace('{instruction}', 'stop the program'))

        index = 0
        cached_index = -1
        # Start paused; if not, when the dialog shows up, multiple images will have already been processed
        pause = True
        second_text_position = [CONST.TEXT_PARAMS['position'][0], CONST.TEXT_PARAMS['position'][1] + 20]

        while index < len(images):
            # Start measuring the iteration time
            iteration_start = perf_counter()

            # Process only if the index has changed
            if index != cached_index:
                try:
                    # Load and process the image
                    image = Image_Processing(f'../{CONST.IMAGES_FOLDER_PATH}/{images[index]}')
                    image.resize_image()

                    # Prepare text for overlay
                    count_text = f'Count: {index + 1}/{len(images)}'
                    image_name = images[index]

                    # Add text to the image
                    cv2.putText(image.resized_image, count_text, CONST.TEXT_PARAMS['position'],
                                cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'],
                                CONST.TEXT_PARAMS['font_color'], CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)
                    cv2.putText(image.resized_image, image_name, second_text_position,
                                cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'],
                                CONST.TEXT_PARAMS['font_color'], CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

                    # Display the updated image
                    cv2.imshow(f'{CONST.BOT_NAME} - Lost Shiny Checker', image.resized_image)

                    # Update cached index
                    cached_index = index
                except Exception as e:
                    logging.error(f"Error processing image %s: %s", images[index], e)
                    # Automatically move to the next image on error
                    index = min(index + 1, len(images) - 1)
                    continue

            # Calculate the remaining time for the iteration
            iteration_duration = perf_counter() - iteration_start
            remaining_time_ms = int(max(0.001, CONST.CHECK_LOST_SHINY_TIME - iteration_duration) * 1000)

            # Handle keyboard inputs and wait
            key = cv2.waitKeyEx(remaining_time_ms)
            if key in [ord('q'), ord('Q')]:  # Quit
                break
            elif key == ord(' '):  # Pause or resume
                pause = not pause
            elif pause and key in [ord('a'), ord('A'), LEFT_ARROW_KEY_VALUE]:  # Previous image
                index = max(0, index - 1)  # Ensure index is not negative
            elif pause and key in [ord('d'), ord('D'), RIGHT_ARROW_KEY_VALUE]:  # Next image
                index = min(len(images) - 1, index + 1)  # Ensure index stays in range
            elif not pause:  # Automatically move to the next image
                index += 1

        sleep(1)
        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', f'Successfully checked {index}/{len(images)} images!')
        )

        cv2.destroyAllWindows()
        delete = input(COLOR_str.DELETE_IMAGES_QUESTION)
        if delete.lower().strip() in ('', 'y', 'yes'):
            print(COLOR_str.DELETING_IMAGES.replace('{images}', str(len(images))))
            for image in images: os.remove(f'../{CONST.IMAGES_FOLDER_PATH}/{image}')
            print(COLOR_str.SUCCESSFULLY_DELETED_IMAGES.replace('{images}', str(len(images))) + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def check_debug_video_frames(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', "Testing debug video frame")
            .replace('{path}', "")
        )

        if not os.path.exists(f'../{CONST.TESTING_IMAGE_PATH}'):
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_IMAGE_PATH}'") + '\n'
            )

        image = Image_Processing(f'../{CONST.TESTING_IMAGE_PATH}')
        # Ensures images has 3 channels instead of 4
        image.original_image = cv2.cvtColor(image.original_image, cv2.COLOR_BGRA2BGR)
        image.resize_image()

        debug_image = create_debug_image()
        stats = {
            'event': 'STATE_WITH_SUPER_LARGE_NAME',
            'button': 'HOME'
        }
        debug_image.populate_debug_image(stats)

        combined_image = debug_image.stack_images(debug_image.FPS_image, image.resized_image)

        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', 'any key')
            .replace('{instruction}', 'exit the program')
        )

        cv2.imshow(f'{CONST.BOT_NAME} - Debug Frame', combined_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the image!') + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    main_menu()