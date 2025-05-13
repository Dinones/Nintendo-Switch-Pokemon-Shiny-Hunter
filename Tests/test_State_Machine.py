###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import unittest
from time import sleep
from parameterized import parameterized_class

import sys
folders = ['../', '../Modules']
for folder in folders: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))

# Mock Qt modules to make them optional in the tests
from unittest.mock import MagicMock
sys.modules['PyQt5'] = MagicMock()
sys.modules['PyQt5.QtGui'] = MagicMock()

from Image_Processing import Image_Processing
import Constants as CONST
import Control_System

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Media/Images'))

###########################################################################################################################

@parameterized_class([{'state': 'WAIT_PAIRING_SCREEN'}])
class Test_Image_Processing(unittest.TestCase):
    def setUp(self):
        pass

    #######################################################################################################################

    def test_wild_encounter_shiny(self):
        # Test wild shiny encounter state machine path

        # Dialga_Animation_1080p.png is a generic image used for state transitions like checking if the white load screen
        # has disappeared of if the text box is not visible anymore
        necessary_images = [
            'Pairing_Screen_1080p.png', 'Home_Screen_1080p.png', 'Overworld_Cave_1080p.png', 'White_Load_Screen_1080p.png',
            'Geodude_Combat_1080p.png', 'Combat_Screen_1080p.png', 'Black_Load_Screen_1080p.png',
            'Dialga_Animation_1080p.png'
        ]

        # Load and resize all images
        for image_name in necessary_images: 
            attribute_name = image_name.split('.')[0]
            if not hasattr(self, attribute_name):
                image_path = os.path.join(IMAGE_DIR, image_name)
                self.assertTrue(os.path.exists(image_path), f'File not found: {image_path}')
                setattr(self, attribute_name, Image_Processing(image_path))
                getattr(self, attribute_name).resize_image()

        # Open Game
        self.state = Control_System.search_wild_pokemon(self.Pairing_Screen_1080p, self.state) # WAIT_HOME_SCREEN
        self.state = Control_System.search_wild_pokemon(self.Home_Screen_1080p, self.state) # MOVE_PLAYER
        self.state = Control_System.search_wild_pokemon(self.Overworld_Cave_1080p, self.state) # MOVE_PLAYER

        # Not Shiny - Case 1 (Normal)
        self.state = Control_System.search_wild_pokemon(self.White_Load_Screen_1080p, self.state) # ENTER_COMBAT_1
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ENTER_COMBAT_1
        Control_System.state_timer -= 0.5 # Simulate time has elapsed
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # ENTER_COMBAT_2
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ENTER_COMBAT_3
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # CHECK_SHINY
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ESCAPE_COMBAT_1
        self.state = Control_System.search_wild_pokemon(self.Combat_Screen_1080p, self.state) # ESCAPE_COMBAT_2
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ESCAPE_COMBAT_3
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # ESCAPE_COMBAT_4
        self.state = Control_System.search_wild_pokemon(self.Black_Load_Screen_1080p, self.state) # ESCAPE_COMBAT_5
        self.state = Control_System.search_wild_pokemon(self.Overworld_Cave_1080p, self.state) # MOVE_PLAYER

        # Not Shiny - Case 2 (Animation skipped due to resource overload)
        self.state = Control_System.search_wild_pokemon(self.White_Load_Screen_1080p, self.state) # ENTER_COMBAT_1
        Control_System.state_timer -= 0.5 # Simulate time has elapsed
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # ENTER_COMBAT_2
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ENTER_COMBAT_3
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # CHECK_SHINY
        self.state = Control_System.search_wild_pokemon(self.Combat_Screen_1080p, self.state) # ESCAPE_COMBAT_1
        self.state = Control_System.search_wild_pokemon(self.Combat_Screen_1080p, self.state) # ESCAPE_COMBAT_2
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ESCAPE_COMBAT_3
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # ESCAPE_COMBAT_4
        self.state = Control_System.search_wild_pokemon(self.Combat_Screen_1080p, self.state) # ESCAPE_FAILED
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ESCAPE_COMBAT_3
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # ESCAPE_COMBAT_4
        self.state = Control_System.search_wild_pokemon(self.Black_Load_Screen_1080p, self.state) # ESCAPE_COMBAT_5
        self.state = Control_System.search_wild_pokemon(self.Overworld_Cave_1080p, self.state) # MOVE_PLAYER

        # Shiny Found
        self.state = Control_System.search_wild_pokemon(self.White_Load_Screen_1080p, self.state) # ENTER_COMBAT_1
        Control_System.state_timer -= 0.5 # Simulate time has elapsed
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # ENTER_COMBAT_2
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # ENTER_COMBAT_3
        self.state = Control_System.search_wild_pokemon(self.Dialga_Animation_1080p, self.state) # CHECK_SHINY
        Control_System.state_timer -= CONST.WILD_SHINY_DETECTION_TIME # Simulate time has elapsed
        self.state = Control_System.search_wild_pokemon(self.Geodude_Combat_1080p, self.state) # SHINY_FOUND

        self.assertEqual(self.state, "SHINY_FOUND", 'Failed to find shiny in wild encounters')

    #######################################################################################################################

    def test_static_encounter_shiny(self):
        # Test static shiny encounter state machine path

        # Dialga_Animation_1080p.png is a generic image used for state transitions like checking if the white load screen
        # has disappeared of if the text box is not visible anymore
        necessary_images = [
            'Pairing_Screen_1080p.png', 'Home_Screen_1080p.png', 'Overworld_Cave_1080p.png', 'White_Load_Screen_1080p.png',
            'Geodude_Combat_1080p.png', 'Combat_Screen_1080p.png', 'BDSP_Load_Screen_1_1080p.png',
            'BDSP_Load_Screen_2_1080p.png', 'BDSP_Load_Screen_3_1080p.png', 'Overworld_Text_Box_1080p.png',
            'Dialga_Animation_1080p.png'
        ]

        # Load and resize all images
        for image_name in necessary_images: 
            attribute_name = image_name.split('.')[0]
            if not hasattr(self, attribute_name):
                image_path = os.path.join(IMAGE_DIR, image_name)
                self.assertTrue(os.path.exists(image_path), f'File not found: {image_path}')
                setattr(self, attribute_name, Image_Processing(image_path))
                getattr(self, attribute_name).resize_image()

        # Open Game
        self.state = Control_System.static_encounter(self.Pairing_Screen_1080p, self.state) # WAIT_HOME_SCREEN
        self.state = Control_System.static_encounter(self.Home_Screen_1080p, self.state) # ENTER_STATIC_COMBAT_1
        self.state = Control_System.static_encounter(self.Overworld_Cave_1080p, self.state) # ENTER_STATIC_COMBAT_1

        # Not Shiny
        self.state = Control_System.static_encounter(self.Overworld_Text_Box_1080p, self.state) # ENTER_STATIC_COMBAT_2
        self.state = Control_System.static_encounter(self.Dialga_Animation_1080p, self.state) # ENTER_STATIC_COMBAT_3
        self.state = Control_System.static_encounter(self.White_Load_Screen_1080p, self.state) # ENTER_STATIC_COMBAT_3
        Control_System.state_timer -= CONST.STATIC_ENCOUNTERS_DELAY # Simulate time has elapsed
        self.state = Control_System.static_encounter(self.White_Load_Screen_1080p, self.state) # ENTER_STATIC_COMBAT_3
        self.state = Control_System.static_encounter(self.White_Load_Screen_1080p, self.state) # ENTER_COMBAT_1
        Control_System.state_timer -= 0.5 # Simulate time has elapsed
        self.state = Control_System.static_encounter(self.Dialga_Animation_1080p, self.state) # ENTER_COMBAT_2
        self.state = Control_System.static_encounter(self.Geodude_Combat_1080p, self.state) # ENTER_COMBAT_3
        self.state = Control_System.static_encounter(self.Dialga_Animation_1080p, self.state) # CHECK_SHINY
        self.state = Control_System.static_encounter(self.Geodude_Combat_1080p, self.state) # RESTART_GAME_1
        self.state = Control_System.static_encounter(self.BDSP_Load_Screen_1_1080p, self.state) # RESTART_GAME_2
        self.state = Control_System.static_encounter(self.BDSP_Load_Screen_2_1080p, self.state) # RESTART_GAME_2
        self.state = Control_System.static_encounter(self.BDSP_Load_Screen_3_1080p, self.state) # RESTART_GAME_2
        self.state = Control_System.static_encounter(self.Dialga_Animation_1080p, self.state) # RESTART_GAME_3
        self.state = Control_System.static_encounter(self.BDSP_Load_Screen_2_1080p, self.state) # RESTART_GAME_4
        self.state = Control_System.static_encounter(self.Overworld_Cave_1080p, self.state) # ENTER_STATIC_COMBAT_1

        # Shiny Found
        self.state = Control_System.static_encounter(self.Overworld_Text_Box_1080p, self.state) # ENTER_STATIC_COMBAT_2
        self.state = Control_System.static_encounter(self.Dialga_Animation_1080p, self.state) # ENTER_STATIC_COMBAT_3
        Control_System.state_timer -= CONST.STATIC_ENCOUNTERS_DELAY # Simulate time has elapsed
        self.state = Control_System.static_encounter(self.White_Load_Screen_1080p, self.state) # ENTER_STATIC_COMBAT_3
        self.state = Control_System.static_encounter(self.White_Load_Screen_1080p, self.state) # ENTER_COMBAT_1
        Control_System.state_timer -= 0.5 # Simulate time has elapsed
        self.state = Control_System.static_encounter(self.Dialga_Animation_1080p, self.state) # ENTER_COMBAT_2
        self.state = Control_System.static_encounter(self.Geodude_Combat_1080p, self.state) # ENTER_COMBAT_3
        self.state = Control_System.static_encounter(self.Dialga_Animation_1080p, self.state) # CHECK_SHINY
        Control_System.state_timer -= 50 # Simulate time has elapsed
        self.state = Control_System.static_encounter(self.Geodude_Combat_1080p, self.state) # SHINY_FOUND
        
        self.assertEqual(self.state, "SHINY_FOUND", 'Failed to find shiny in wild encounters')

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    unittest.main()