###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
import json
import random
import unittest
import numpy as np
from parameterized import parameterized_class

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Modules.Image_Processing import *
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Define absolute paths to required resources
IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Media/Images'))
TESTS_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tests Data/Image_Processing_Data.json'))

# Load test case definitions from JSON
with open(TESTS_DATA_FILE, 'r') as file: 
    TEST_DATA = json.load(file)

# Prepend absolute path to each image_path in the test data
for item in TEST_DATA: 
    item['image_path'] = os.path.join(IMAGE_DIR, item['image_path'])

# Manually enable debug mode if CONST.TESTING is not active
if not CONST.TESTING:
    CONST.TESTING = True

###########################################################################################################################
###########################################################################################################################

@parameterized_class(TEST_DATA)
class Test_Image_Processing(unittest.TestCase):
    def setUp(self):
    
        """
        Prepares the test case by verifying image existence and initializing the image processor. This function will run
        before every test function.
        """

        # Check that the test image file exists
        self.assertTrue(os.path.exists(self.image_path), f'File not found: {self.image_path}')

        # Create the Image_Processing object with the image path
        self.image = Image_Processing(self.image_path)

        # Reset resized image to None before each test
        self.image.resized_image = None

    #######################################################################################################################
    #######################################################################################################################

    def test_load_image(self):
        
        """
        Tests whether the image is correctly loaded and has the expected dimensions.

        Asserts:
            - The image object is not None.
            - The image size matches the expected dimensions.
        """

        # Ensure the image was loaded
        self.assertIsNotNone(self.image.original_image, f'Failed to load image: {self.image_path}')

        # Check the loaded image size
        width, height = self.image.original_image.shape[1::-1]
        self.assertEqual((width, height), tuple(self.image_original_size), f'Image size mismatch for {self.image_path}')

    #######################################################################################################################
    #######################################################################################################################

    def test_resize_image(self):

        """
        Tests whether the image is resized correctly to fit within the target frame size, while maintaining aspect ratio.

        Asserts:
            - The resized image is not None.
            - The resized image fits within the desired bounding box (CONST.MAIN_FRAME_SIZE).
        """

        # Perform the resizing operation
        self.image.resize_image()

        # Ensure the resized image exists
        self.assertIsNotNone(self.image.resized_image, 'Failed to resize image')

        # Get width and height of the resized image
        width, height = self.image.resized_image.shape[1::-1]

        # Check that the resized dimensions fit within the desired bounding box
        self.assertLessEqual(width, CONST.MAIN_FRAME_SIZE[0], 'Resized width exceeds limit')
        self.assertLessEqual(height, CONST.MAIN_FRAME_SIZE[1], 'Resized height exceeds limit')

        # Assert aspect ratio is preserved within reasonable error of ±1 pixel
        original_ratio = self.image.original_image.shape[1] / self.image.original_image.shape[0]
        resized_ratio = width / height
        self.assertAlmostEqual(resized_ratio, original_ratio, places = 2, msg = 'Aspect ratio not preserved')

    #######################################################################################################################
    #######################################################################################################################

    def test_is_pokemon_name_recognized(self):

        """
        Tests whether the Pokémon name is correctly recognized from the image. Skips the test if the current test case does
        not include a Pokémon name.

        Asserts:
            - The recognized Pokémon name matches the expected one.
        """

        # Skip this test if the image doesn't contain a Pokémon name
        if not self.has_pokemon_name:
            self.skipTest("Skipping because image is not showing a pokémon name (has_pokemon_name = False)")

        # Resize the image to standard dimensions before recognition
        self.image.resize_image()

        # Attempt to recognize the Pokémon name from the image
        recognized_name = self.image.recognize_pokemon()

        # Assert that the recognized name matches the expected one
        self.assertEqual(self.pokemon_name, recognized_name, 'Failed to recognize Pokémon name')
  
    #######################################################################################################################
    #######################################################################################################################

    def test_draw_and_check_column(self):

        """
        Tests whether a column drawn using 'draw_column()' is correctly detected by 'check_column_pixel_colors()'.

        Asserts:
            - All pixels in the column match the expected color exactly.
        """

        # Resize the image to ensure dimensions and FPS_image are initialized
        self.image.resize_image()
        height, width = self.image.resized_image.shape[:2]

        # Random column position and height
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # Draw the test column on the FPS image
        self.image.draw_column(
            position = (x, y),
            column_height = CONST.COLOR_SCREEN_CHECK.get('column_height', ''),
            color = CONST.TESTING_COLOR
        )

        self.image.resized_image = np.copy(self.image.FPS_image)

        # Validate all pixels in the column match the color
        match = self.image.check_column_pixel_colors(
            position = (x, y),
            column_height = CONST.COLOR_SCREEN_CHECK.get('column_height', ''),
            color = CONST.TESTING_COLOR,
            threshold = CONST.PIXEL_COLOR_DIFF_THRESHOLD
        )

        self.assertTrue(match, f"Column pixels at ({x},{y}) do not all match the expected color {CONST.TESTING_COLOR}")
    
    #######################################################################################################################
    #######################################################################################################################

    def test_save_image(self):

        """
        Tests whether the save_image() function correctly writes the original image to disk. The file is deleted after test
        completion.

        Asserts:
            - The saved file exists.
            - The saved file can be opened as a valid image.
        """

        self.image.resize_image()
        self.image.save_image(self.pokemon_name)

        saved_path = self.image.saved_image_path

        # Assert the file exists
        self.assertTrue(os.path.exists(saved_path), f"Image was not saved at path: {saved_path}")

        # Assert the file is readable as an image
        loaded = cv2.imread(saved_path)
        self.assertIsNotNone(loaded, f"Saved image at {saved_path} could not be opened")

        # Remove the file after test
        os.remove(saved_path)
    
    #######################################################################################################################
    #######################################################################################################################

    def test_debug_image_stack(self):

        """
        Tests that a debug image is correctly populated and stacked with a processed test image.

        Asserts:
            - The stacked image is not None.
            - The height equals the sum of both images' heights.
            - The width matches the testing image's one.
        """

        # Prepare the resized test image
        self.image.resize_image()
        resized_shape = self.image.resized_image.shape

        # Create and populate a debug image
        debug_image = Debug_Image()
        stats = {
            'event': 'STATE_WITH_SUPER_LARGE_NAME',
            'button': 'HOME'
        }
        debug_image.populate_debug_image(stats)
        debug_shape = debug_image.FPS_image.shape

        # Stack the debug image (top) and test image (bottom)
        stacked = debug_image.stack_images(debug_image.FPS_image, self.image.resized_image)

        # Assert the result exists
        self.assertIsNotNone(stacked, 'Stacked image is None')

        # Expected dimensions
        expected_height = debug_shape[0] + resized_shape[0]
        expected_width = resized_shape[1]

        # Assert shape matches
        self.assertEqual(stacked.shape[0], expected_height, 'Stacked image height is incorrect')
        self.assertEqual(stacked.shape[1], expected_width, 'Stacked image width is incorrect')

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()