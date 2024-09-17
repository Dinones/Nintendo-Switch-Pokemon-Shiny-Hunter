import unittest
import os
from parameterized import parameterized_class

from Modules import Image_Processing

@parameterized_class([
   { 'image_path': 'test/resources/Regice_720p.png', 'image_size': (1280, 720) },
   { 'image_path': 'test/resources/Regice_1080p.png', 'image_size': (1920, 1080) },
])
class TestImageProcessor(unittest.TestCase):

    def setUp(self):
        # Ensure the file exists
        self.assertIsNotNone(self.image_path, "File not found")
        self.assertTrue(os.path.exists(self.image_path), "File not found")

        # Initialize the ImageProcessor object
        self.image = Image_Processing(self.image_path)

    def test_load_image(self):
        # Test loading an image
        self.assertIsNotNone(self.image.original_image, "Failed to load image")

        size = self.image.original_image.shape[1::-1]
        self.assertEqual(size, self.image_size, 'Failed to load image')

    def test_resize_image(self):
        # Test resizing an image
        self.assertIsNone(self.image.resized_image, "Failed to load image")
        self.image.resize_image()
        self.assertIsNotNone(self.image.resized_image, "Failed to load image")

        size = self.image.resized_image.shape[1::-1]
        self.assertEqual(size, (720, 405), 'Failed to resize image')

    def test_extract_text_from_image(self):
        # Test applying a filter to an image
        pokemon_name = self.image._extract_text_from_image()
        self.assertEquals(pokemon_name, 'Regice apparait !\n', 'Failed to recognize pokemon')

    def tearDown(self):
        # Clean up any resources if needed
        pass

if __name__ == '__main__':
    unittest.main()