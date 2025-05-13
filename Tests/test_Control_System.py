###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import json
import unittest
from parameterized import parameterized_class

import sys
folders = ['../', '../Modules']
for folder in folders: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))

# Mock Qt modules to make them optional in the tests
from unittest.mock import MagicMock
sys.modules['PyQt5'] = MagicMock()
sys.modules['PyQt5.QtGui'] = MagicMock()

from Image_Processing import Image_Processing
import Control_System

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Media/Images'))
TESTS_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Tests Data/Control_System_Data.json'))

# Load test data, where tests are defined
with open(TESTS_DATA_FILE, 'r') as file: 
    TEST_DATA = json.load(file)

for item in TEST_DATA: 
    item['image_path'] = os.path.join(IMAGE_DIR, item['image_path'])

###########################################################################################################################

@parameterized_class(TEST_DATA)
class Test_Control_System(unittest.TestCase): 
    def setUp(self):
        # Ensure the file exists
        self.assertTrue(os.path.exists(self.image_path), f'File not found: {self.image_path}')

        # Initialize the ImageProcessor object
        self.image = Image_Processing(self.image_path)
        self.image.resize_image()

    #######################################################################################################################

    def test_is_pairing_screen_visible(self):
        # Test if black screen is visible
        pairing_screen_visible = Control_System.is_pairing_screen_visible(self.image)
        self.assertEqual(self.is_pairing_screen_visible, pairing_screen_visible, 'Failed to recognize pairing screen') 
    
    #######################################################################################################################

    def test_is_home_screen_visible(self):
        # Test if black screen is visible
        home_screen_visible = Control_System.is_home_screen_visible(self.image)
        self.assertEqual(self.is_home_screen_visible, home_screen_visible, 'Failed to recognize home screen') 

    #######################################################################################################################

    def test_is_bdsp_load_screen_visible(self):
        # Test if black screen is visible
        bdsp_load_screen_visible = Control_System.is_bdsp_loading_screen_visible(self.image)
        self.assertEqual(
            self.is_bdsp_load_white_screen_visible, bdsp_load_screen_visible, 'Failed to recognize BDSP load screen'
        ) 

    #######################################################################################################################

    def test_is_load_black_screen_visible(self):
        # Test if black screen is visible
        black_screen_visible = Control_System.is_black_screen_visible(self.image)
        self.assertEqual(self.is_load_black_screen_visible, black_screen_visible, 'Failed to recognize black load screen')  

    #######################################################################################################################

    def test_is_load_white_screen_visible(self):
        # Test if the white screen is visible
        white_screen_visible = Control_System.is_white_screen_visible(self.image)
        self.assertEqual(self.is_load_white_screen_visible, white_screen_visible, 'Failed to recognize white load screen')

    #######################################################################################################################

    def test_is_overworld_text_box_visible(self):
        # Test if the overworld text box is visible
        overworld_text_box_visible = Control_System.is_overworld_text_box_visible(self.image)
        self.assertEqual(
            self.is_overworld_text_box_visible, overworld_text_box_visible, 'Failed to recognize overworld text box'
        )

    #######################################################################################################################

    def test_is_combat_text_box_visible(self):
        # Test if the combat text box is visible
        combat_text_box_visible = Control_System.is_combat_text_box_visible(self.image)
        self.assertEqual(self.is_combat_text_box_visible, combat_text_box_visible, 'Failed to recognize combat text box')

    #######################################################################################################################

    def test_is_life_box_visible(self):
        # Test if life box is visible
        life_box_visible = Control_System.is_life_box_visible(self.image)
        self.assertEqual(self.is_life_box_visible, life_box_visible, 'Failed to recognize life box')

    #######################################################################################################################

    def test_is_double_combat_life_box_visible(self):
        # Test if life box is visible
        double_combat_life_box_visible = Control_System.is_double_combat_life_box_visible(self.image)
        self.assertEqual(
            self.is_double_combat_life_box_visible,
            double_combat_life_box_visible,
            'Failed to recognize life box in double combat'
        )

    #######################################################################################################################

    def tearDown(self):
        # Clean up any resources if needed
        pass

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()
