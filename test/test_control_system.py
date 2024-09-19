import unittest
import os
from parameterized import parameterized_class

from Modules import Image_Processing
from Modules import Control_System


@parameterized_class([
    {
        'image_path': 'test/resources/Regice_720p.png',
        'has_text_box': True,
        'has_black_screen': False,
        'has_life_box': False,
        'overworld_visible': False,
        'has_white_screen': True # TODO @dinones should be False?
    },
    {
        'image_path': 'test/resources/Regice_1080p.png',
        'has_text_box': True,
        'has_black_screen': False,
        'has_life_box': False,
        'overworld_visible': False,
        'has_white_screen': True # TODO @dinones should be False?
    },
])
class TestControlSystem(unittest.TestCase):

    def setUp(self):
        # Initialize the ImageProcessor object
        self.image = Image_Processing(self.image_path)

    def test_text_box_visibility(self):
        # Test if the text box is visible
        text_box_visible = Control_System.is_text_box_visible(self.image)
        self.assertEqual(self.has_text_box, text_box_visible, 'Failed to recognize text box')

    def test_is_overworld_box_visible(self):
        # Test if overworld is visible
        overworld_visible = Control_System.is_overworld_visible(self.image)
        self.assertEqual(self.overworld_visible, overworld_visible, 'Failed to recognize overworld box')

    def test_is_black_screen_visible(self):
        # Test if black screen is visible
        black_screen_visible = Control_System.is_black_screen_visible(self.image)
        self.assertEqual(self.has_black_screen, black_screen_visible, 'Failed to recognize black screen')

    def test_is_life_box_visible(self):
        # Test if life box is visible
        life_box_visible = Control_System.is_life_box_visible(self.image)
        self.assertEqual(self.has_life_box, life_box_visible, 'Failed to recognize life box')

    def test_is_load_fight_white_screen(self):
        # Test if the white screen is visible
        white_screen_visible = Control_System.is_load_fight_white_screen(self.image)
        self.assertEqual(self.has_white_screen, white_screen_visible, 'Failed to recognize white screen')

    def tearDown(self):
        # Clean up any resources if needed
        pass


if __name__ == '__main__':
    unittest.main()
