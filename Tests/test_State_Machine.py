###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import json
import unittest
from parameterized import parameterized_class

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Modules.State_Machine import *
from Modules.Image_Processing import Image_Processing

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Define absolute paths to required resources
IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Media/Images'))
TESTS_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tests Data/State_Machine_Data.json'))

# Load test case definitions from JSON
with open(TESTS_DATA_FILE, 'r') as file: 
    TEST_DATA = json.load(file)

# Prepend absolute path to each image_path in the test data
for item in TEST_DATA: 
    item['image_path'] = os.path.join(IMAGE_DIR, item['image_path'])

###########################################################################################################################
###########################################################################################################################

@parameterized_class(TEST_DATA)
class Test_State_Machine(unittest.TestCase): 
    def setUp(self):

        """
        Prepares the test case by verifying image existence and initializing the image processor. This function will run
        before every test function.
        """

        # Ensure the file exists
        self.assertTrue(os.path.exists(self.image_path), f'File not found: {self.image_path}')

        # Initialize the image processor object
        self.image = Image_Processing(self.image_path)
        self.image.resize_image()

    #######################################################################################################################
    #######################################################################################################################

    def test_is_pairing_screen_visible(self):

        """
        Unit test for the 'is_pairing_screen_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        pairing_screen_visible = is_pairing_screen_visible(self.image)
        self.assertEqual(self.is_pairing_screen_visible, pairing_screen_visible, 'Failed to recognize pairing screen') 
    
    #######################################################################################################################
    #######################################################################################################################

    def test_is_home_screen_visible(self):

        """
        Unit test for the 'is_home_screen_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        home_screen_visible = is_home_screen_visible(self.image)
        self.assertEqual(self.is_home_screen_visible, home_screen_visible, 'Failed to recognize home screen') 

    #######################################################################################################################
    #######################################################################################################################

    def test_is_bdsp_load_screen_visible(self):

        """
        Unit test for the 'is_bdsp_loading_screen_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        bdsp_load_screen_visible = is_bdsp_loading_screen_visible(self.image)
        self.assertEqual(
            self.is_bdsp_load_white_screen_visible, bdsp_load_screen_visible, 'Failed to recognize BDSP load screen'
        ) 

    #######################################################################################################################
    #######################################################################################################################

    def test_is_load_black_screen_visible(self):

        """
        Unit test for the 'is_black_screen_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        black_screen_visible = is_black_screen_visible(self.image)
        self.assertEqual(self.is_load_black_screen_visible, black_screen_visible, 'Failed to recognize black load screen')  

    #######################################################################################################################
    #######################################################################################################################

    def test_is_load_white_screen_visible(self):

        """
        Unit test for the 'is_white_screen_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        white_screen_visible = is_white_screen_visible(self.image)
        self.assertEqual(self.is_load_white_screen_visible, white_screen_visible, 'Failed to recognize white load screen')

    #######################################################################################################################
    #######################################################################################################################

    def test_is_overworld_text_box_visible(self):

        """
        Unit test for the 'is_overworld_text_box_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        overworld_text_box_visible = is_overworld_text_box_visible(self.image)
        self.assertEqual(
            self.is_overworld_text_box_visible, overworld_text_box_visible, 'Failed to recognize overworld text box'
        )

    #######################################################################################################################
    #######################################################################################################################

    def test_is_combat_text_box_visible(self):

        """
        Unit test for the 'is_combat_text_box_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        combat_text_box_visible = is_combat_text_box_visible(self.image)
        self.assertEqual(self.is_combat_text_box_visible, combat_text_box_visible, 'Failed to recognize combat text box')

    #######################################################################################################################
    #######################################################################################################################

    def test_is_life_box_visible(self):

        """
        Unit test for the 'is_life_box_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        life_box_visible = is_life_box_visible(self.image)
        self.assertEqual(self.is_life_box_visible, life_box_visible, 'Failed to recognize life box')

    #######################################################################################################################
    #######################################################################################################################

    def test_is_double_combat_life_box_visible(self):

        """
        Unit test for the 'is_double_combat_life_box_visible' function.

        Asserts:
            - That the detection result matches the expected outcome.
        """

        double_combat_life_box_visible = is_double_combat_life_box_visible(self.image)
        self.assertEqual(
            self.is_double_combat_life_box_visible,
            double_combat_life_box_visible,
            'Failed to recognize life box in double combat'
        )

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()
