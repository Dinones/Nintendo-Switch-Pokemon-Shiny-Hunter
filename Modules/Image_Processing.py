###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
import numpy as np
import pytesseract
from time import time
import PyQt5.QtGui as pyqt_g
from typing import Tuple, Union, Dict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Modules.Colored_Strings as STR
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

    #######################################################################################################################
    #######################################################################################################################

    def resize_image(self, desired_size = CONST.MAIN_FRAME_SIZE):
    
        """
        Resizes the original image to fit within a maximum bounding box while preserving the aspect ratio.

        Args:
            desired_size (Tuple[int, int]): Target bounding box size (width, height) for resizing.

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
            self._ensure_fps_image()
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
            threshold (int): The maximum difference allowed between the pixel color and the specified color.

        Returns:
            bool: True if all pixels in the column match the target color within the threshold, False otherwise.
        """
        
        x, start_y = position
        height, width = self.resized_image.shape[:2]

        # Validate x or all y within bounds
        if not (0 <= x < width) or not (0 <= start_y < height or 0 <= start_y + column_height < height):
            return False

        for offset in range(column_height):
            y = start_y + offset
            # Skip out-of-bounds pixel
            if not (0 <= y < height):
                continue

            pixel = self.resized_image[-y, x]

            # Compare each BGR channel
            differences = [abs(int(pixel[c]) - color[c]) for c in range(3)]
            if any(d > threshold for d in differences):
                return False

        # Draw the column for debugging
        self.draw_column(position, column_height)

        return True

    #######################################################################################################################
    #######################################################################################################################

    def draw_column(
        self,
        position: Tuple[int, int],
        column_height: int,
        color: Tuple[int, int, int] = CONST.TESTING_COLOR
    ) -> None:

        """
        Draws a vertical column of pixels on the FPS image for debugging purposes.

        Args:
            position (Tuple[int, int]): The (x, y) starting position of the column (bottom-left origin).
            column_height (int): Height of the column in pixels.
            color (Tuple[int, int, int]): Color to draw (BGR tuple).

        Returns:
            None
        """

        self._ensure_fps_image()

        if not CONST.TESTING:
            return

        x, start_y = position

        # Draw each pixel in the vertical column upwards from the starting position
        for offset in range(column_height):
            y = start_y + offset
            # Prevents from drawing outside the image
            if 0 <= y < self.FPS_image.shape[0] and 0 <= x < self.FPS_image.shape[1]:
                self.FPS_image[-y, x] = color

    #######################################################################################################################
    #######################################################################################################################

    def recognize_pokemon(self) -> str:

        """
        Extracts the Pokémon name from the battle text box in the resized image using OCR.

        EN: Dialga appeared! | A wild Drifloon appeared! | Go! Chimchar!
        FR: Dialga apparaît! | Un Baudrive sauvage apparaît! | Ouisticram! Go!
        ES: ¡Es Dialga! | ¡Ha aparecido un Drifloon salvaje! | ¡Adelante, Chimchar!
        IT: È apparso Dialga! | Ah! È apparso un Drifloon selvatico! | Avanti, Chimchar!
        DE: Dialga erscheint! | Ein Driftlon (wild) erscheint! | Los, Panflam!
        For the KO, ZH-CN and ZH-TW cases, it will return the whole text line

        Returns:
            str: The recognized Pokémon name. Returns a cleaned version or the raw OCR result if parsing fails.
        """

        # Crop the text box region where the Pokémon name is shown
        name_image = self.resized_image[333:365, 50:670]

        # Convert the cropped region to grayscale for better recognition
        name_image = cv2.cvtColor(name_image, cv2.COLOR_BGR2GRAY)

        # Configure Tesseract: --oem 1 (fast mode), --psm 6 (assume a single block of text)
        custom_config = '--oem 1 --psm 6'
        text = pytesseract.image_to_string(name_image, config=custom_config)

        # Handle language-specific noise cleaning (for supported languages)
        if CONST.LANGUAGE in ('FR', 'ES', 'EN', 'DE', 'IT'):
            pokemon_name = text
            # Remove known noise words or punctuation
            for part in ['Go!', '¡', '!']:
                pokemon_name = pokemon_name.replace(part, '')

            # Extract the last capitalized word (the Pokémon name)
            words = pokemon_name.split(' ')
            for word in reversed(words):
                if word and word[0].isupper():
                    text = word
                    break

        return text.strip()

    #######################################################################################################################
    #######################################################################################################################

    def save_image(self, pokemon_name: str = '') -> None:

        """
        Saves the original image with the Pokémon name + timestamp in the filename.

        Args:
            pokemon_name (str): Optional name to include in the filename.

        Returns:
            None
        """

        file_name = f'{pokemon_name}_{int(time())}' if pokemon_name else str(int(time()))
        self.saved_image_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f'../{CONST.IMAGES_FOLDER_PATH}{file_name}.png')
        )

        # Save the original image
        cv2.imwrite(self.saved_image_path, self.original_image)

    #######################################################################################################################
    #######################################################################################################################

    def _ensure_fps_image(self, force: bool = False) -> None:

        """
        Ensures that FPS_image is initialized by copying the current resized_image.

        Args:
            force (bool): If True, forces reinitialization even if FPS_image already exists.

        Returns:
            None
        """

        # If a frame is corrupted (None), generate a black frame to prevent an error
        # This is likely to happen when the capture card is reconnected after it's been disconnected
        if self.resized_image is None:
            self.resized_image = np.zeros((CONST.MAIN_FRAME_SIZE[1], CONST.MAIN_FRAME_SIZE[0], 3), dtype=np.uint8)

        # If FPS_image is not initialized or force is True, create a fresh copy
        if self.FPS_image is None or force:
            # Use copy to avoid linking images preventing unintended modifications
            self.FPS_image = np.copy(self.resized_image)

    #######################################################################################################################
    #######################################################################################################################

    def _replace_pixels(
        self,
        original_pixel_color: Tuple[int, int, int],
        target_color: Tuple[int, int, int] = CONST.TESTING_COLOR
    ) -> None:
    
        """
        Replaces all pixels in the original image that exactly match the given color with a target color. Only used for
        debugging purposes.

        Args:
            original_pixel_color (Tuple[int, int, int]): The BGR color to replace.

        Returns:
            None
        """

        if self.original_image is None:
            return

        # Create a boolean mask where all channels match the given color
        mask = np.all(self.original_image == original_pixel_color, axis=-1)

        # Replace matching pixels with the testing color
        self.original_image[mask] = target_color

    #######################################################################################################################
    #######################################################################################################################

    def _check_pixel_color_original_image(
        self,
        color: Tuple[int, int, int],
        pixel: Tuple[int, int] = (20, 20),
        threshold: int = CONST.PIXEL_COLOR_DIFF_THRESHOLD
    ) -> bool:

        """
        Checks whether the pixel at a given position matches the specified color within the tolerance threshold. Only used
        for debugging purposes.

        Args:
            color (Tuple[int, int, int]): The BGR color to compare against.
            pixel (Tuple[int, int]): The (y, x) coordinates of the pixel to check.
            threshold (int): The maximum difference allowed between the pixel color and the specified color.

        Returns:
            bool: True if the pixel matches the color within the defined threshold, False otherwise.
        """

        if self.original_image is None:
            return

        # Ensure pixel is inside image bounds
        y, x = pixel
        h, w = self.original_image.shape[:2]
        if not (0 <= y < h and 0 <= x < w):
            return False

        # Compare each color channel (BGR) with threshold
        differences = [abs(int(self.original_image[y, x][i]) - color[i]) for i in range(3)]

        return all(d <= threshold for d in differences)

###########################################################################################################################
###########################################################################################################################

class Debug_Image(Image_Processing):

    """
    Creates a debug image (blank with border) and inherits all functionality from Image_Processing.
    """

    def __init__(self, frame_size: Tuple[int, int] = CONST.DEBUG_FRAME_SIZE):

        """
        Initializes the debug image with a black background and a border.

        Args:
            frame_size (Tuple[int, int]): The (width, height) of the debug image. Default: CONST.DEBUG_FRAME_SIZE.

        Returns:
            None
        """

        # Create a black image
        black_image = np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)

        # Add gray borders (#AAA)
        border_color = [170, 170, 170]
        border_thickness = 1
        black_image[:border_thickness, :] = border_color   # Top
        black_image[-border_thickness:, :] = border_color  # Bottom
        black_image[:, :border_thickness] = border_color   # Left
        black_image[:, -border_thickness:] = border_color  # Right

        # Initialize the parent class with the debug image
        super().__init__(black_image)
    
    #######################################################################################################################
    #######################################################################################################################

    def populate_debug_image(self, stats: Dict[str, str]) -> None:

        """
        Populates the debug FPS image with button and event state text, but only if the content has changed since the last
        render.

        Args:
            stats (Dict[str, str]): A dictionary with keys like 'button' and 'event' describing current debug state.

        Returns:
            None
        """

        # Skip rendering if nothing has changed to avoid unnecessary processing
        if all(stats.get(key) == self.debug_image_stats.get(key) for key in stats):
            return

        # Make a fresh copy of the original image (the black rectangle with gray borders)
        self.FPS_image = np.copy(self.original_image)

        # Write the button label
        cv2.putText(
            self.FPS_image,
            f'Button: {stats.get("button")}',
            CONST.DEBUG_IMAGE_TEXT_PARAMS['button_position'],
            cv2.FONT_HERSHEY_SIMPLEX,
            CONST.DEBUG_IMAGE_TEXT_PARAMS['font_scale'],
            CONST.DEBUG_IMAGE_TEXT_PARAMS['font_color'],
            CONST.DEBUG_IMAGE_TEXT_PARAMS['thickness'],
            cv2.LINE_AA
        )

        # Write the state label
        cv2.putText(
            self.FPS_image,
            f'| State: {stats.get("event")}',
            CONST.DEBUG_IMAGE_TEXT_PARAMS['state_position'],
            cv2.FONT_HERSHEY_SIMPLEX,
            CONST.DEBUG_IMAGE_TEXT_PARAMS['font_scale'],
            CONST.DEBUG_IMAGE_TEXT_PARAMS['font_color'],
            CONST.DEBUG_IMAGE_TEXT_PARAMS['thickness'],
            cv2.LINE_AA
        )

        # Cache the current stats to avoid redundant redraws
        self.debug_image_stats = stats.copy()
    
    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def stack_images(image_1: np.ndarray, image_2: np.ndarray) -> np.ndarray:

        """
        Vertically stacks two images: image_1 on top, image_2 on bottom.

        Args:
            image_1 (np.ndarray): The top image.
            image_2 (np.ndarray): The bottom image.

        Returns:
            np.ndarray: The vertically stacked image.
        """

        return np.vstack((image_1, image_2))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    import Debug.Image_Processing_Debug