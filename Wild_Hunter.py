###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os

# ↓↓ NXBT is only compatible with Linux systems
if os.name != 'posix': exit('NXBT is only available on Linux systems.')

if __name__ == '__main__': 
    # ↓↓ Will raise an error when restarting execution using sudo
    try: os.chdir(os.path.dirname(__file__))
    except: pass
    # ↓↓ NXBT requires administrator permissions
    if 'SUDO_USER' not in os.environ: 
        print('NXBT must be executed using administrator permission: Restarting using sudo...')
        program_name = __file__.split('/')[-1]
        exit(os.system(f'sudo python3 {program_name}'))
        
from threading import Thread
from queue import Queue
import numpy as np
import cv2

import Constants as CONST

import sys; sys.path.append('Utils')
from Switch_Controller import Switch_Controller
from Image_Processing import Image_Processing
from Game_Capture import Game_Capture
from FPS_Counter import FPS_Counter
import Pokemon_Database as Pokemon_DB
from GUI import GUI
import Messages as MSG

import pyautogui, random; random.seed(6)

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# ↓↓ Read the total attempts
with open('./Media/Attempts.txt', 'r') as txt_file:
    attempts = int(txt_file.read())
    print(MSG.CURRENT_ATTEMPTS.replace('{attempts}', str(attempts)))

# ↓↓ Start all Capture card relatef stuff
Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
if CONST.RECORD_VIDEO: 
    print(MSG.RECORDING_VIDEO)
    Game_Capture.start_recording()

# ↓↓ Emulate the controller
Switch_Controller = Switch_Controller()
Thread(target = Switch_Controller.connect_controller, daemon = True, args = ('FAST_SETUP',)).start()
Thread(target = Switch_Controller.run_event, daemon = True).start()

FPS_Counter = FPS_Counter()
# ↓↓ Create and start the GUI
Image_Queue = Queue()
GUI = GUI(Image_Queue)
GUI.start()

# ↓↓ Send the GUI the captured image
def queue_next_frame(image = None):
    if image is None: return
    Image_Queue.put(image)

def __test_print(text): print(text) if CONST.TESTING else None

# ↓↓ Used to save the image of the pokemon in the foreground some extra time
wild_pokemon_foreground_image = Image_Processing('Don\'t worry, this is not an error!')
wild_pokemon_name_detection_image = None
# ↓↓ Images used to detect which pokemon has appeared in the wild encounter
pokemon_name_images = {}
for pokemon in CONST.TARGET_WILD_POKEMON:
    name_image = cv2.imread(f'./Media/Pokemon Names/{pokemon}.png', cv2.IMREAD_GRAYSCALE)
    if type(name_image) == type(None):
        print(MSG.COULD_NOT_LOAD_POKEMON_NAME_IMAGE.replace("{pokemon}", pokemon))
        continue
    pokemon_name_images[pokemon] = name_image
print(MSG.IMAGES_SUCCESSFULLY_LOADED.replace('{loaded}', str(len(pokemon_name_images)))
    .replace('{total}', str(len(CONST.TARGET_WILD_POKEMON))))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

while True:
    image = Image_Processing(Game_Capture.read())
    if image.original_image is None: continue

    image.resize_image()
    FPS_Counter.get_FPS()
    image.draw_FPS(FPS_Counter.FPS)
    image.masked_image = np.zeros_like(image.resized_image)
    image.contours_image = np.zeros_like(image.resized_image)

    Game_Capture.add_frame_to_video(image)

    if Switch_Controller.event_lock.acquire(blocking = False):
        # ↓↓ Wait for the game to enter a combat
        if Switch_Controller.current_event == 'MOVE_STRAIGHT':
            # ↓↓ Check the white load screen when entering the combat
            x = int(len(image.resized_image[0]) // 16 * 1.2)
            y1 = int(len(image.resized_image) // 15 * 1)
            y2 = int(len(image.resized_image) // 15 * 2)
            if image.check_multiple_pixel_colors([x, y1], [x, y2]):
                __test_print(MSG.WILD_POKEMON_SEARCHING)
                Switch_Controller.current_event = 'WAIT_WILD_POKEMON_FOREGROUND'

        # ↓↓ Wait for the wild pokemon to appear in the foreground
        elif Switch_Controller.current_event == 'DETECT_WILD_POKEMON':
            # ↓↓ Check the text box "A wild [...] appeared!"
            x = int(len(image.resized_image[0]) // 16 * 1.2)
            y1 = int(len(image.resized_image) // 15 * 1)
            y2 = int(len(image.resized_image) // 15 * 2)
            if image.check_multiple_pixel_colors([x, y1], [x, y2]):
                if CONST.SAVE_SCREENSHOTS: cv2.imwrite(f'./Media/Results/{attempts}.png', image.original_image)
                # ↓↓ Save the foreground image to use later
                wild_pokemon_foreground_image.resized_image = np.copy(image.resized_image)

                Switch_Controller.current_event = 'CHECK_SHINY'

        # ↓↓ Wait until the pokemon name is written in the text box
        elif Switch_Controller.current_event == 'CHECK_SHINY':
            x = int(len(image.resized_image[0]) // 16 * 1.2)
            y1 = int(len(image.resized_image) // 15 * 1)
            y2 = int(len(image.resized_image) // 15 * 2)
            if not image.check_multiple_pixel_colors([x, y1], [x, y2]):
                # cv2.imwrite(f'./Media/Results/{attempts}_getname.png', wild_pokemon_name_detection_image)

                x1 = int(len(image.resized_image[0]) // 8 * 0.65)
                x2 = int(len(image.resized_image[0]) // 8 * 7.5)
                y1 = int(len(image.resized_image) // 16 * 13.2)
                y2 = int(len(image.resized_image) // 16 * 14.7)
                # ↓↓ Images must be grayscale in the matchTemplate()
                wild_pokemon_name_detection_image = \
                    cv2.cvtColor(np.copy(wild_pokemon_name_detection_image[y1:y2, x1:x2]), cv2.COLOR_RGB2GRAY)
                all_matches = {}
                for name_image in pokemon_name_images.keys():
                    # ↓↓ cv2.TM_CCORR provides faster response but with less accuracy
                    name_match = cv2.matchTemplate(wild_pokemon_name_detection_image, pokemon_name_images[name_image], 
                        cv2.TM_CCORR_NORMED)
                    all_matches[name_image] = np.max(name_match)
                    # print(f'{name_image}: {all_matches[name_image]}')

                __test_print(MSG.WILD_POKEMON_FOUND.replace('{pokemon}', max(all_matches, key=all_matches.get)))

                wild_pokemon_foreground_image.detect_pokemon_color(getattr(Pokemon_DB, max(all_matches, key=all_matches.get)))
                match = wild_pokemon_foreground_image.get_rectangles()
                if not getattr(Pokemon_DB, max(all_matches, key=all_matches.get))['shiny_color']: match = not match
                __test_print(MSG.SHINY_DETECTION.replace('{match}', str(match)))

                # ↓↓ Move mouse to prevent system from entering in rest mode
                try:
                    if CONST.INACTIVITY_AVOIDER:
                        random_number = random.randint(100, 1000)
                        pyautogui.moveTo(random_number, random_number)
                except: pass

                attempts += 1
                with open('./Media/Attempts.txt', 'w') as txt_file:
                    txt_file.write(str(attempts))
                    print(MSG.CURRENT_ATTEMPTS.replace('{attempts}', str(attempts)))

                if match: 
                    cv2.imwrite(f'./Media/Results/{attempts}_mask.png', wild_pokemon_foreground_image.masked_image)
                    cv2.imwrite(f'./Media/Results/{attempts}_contours.png', wild_pokemon_foreground_image.contours_image)
                    Switch_Controller.current_event = 'HOME_STOP'
                    Switch_Controller.event_lock.release()
                    continue
                else: Switch_Controller.current_event = 'WAIT_ESCAPE_COMBAT'

                # ↓↓ Save the current video and start the new one
                if CONST.RECORD_VIDEO:
                    Game_Capture.save_video(image)
                    Game_Capture.start_recording(image)

            wild_pokemon_name_detection_image = np.copy(image.resized_image)

        # ↓↓ Wait for the combat to fully load
        elif Switch_Controller.current_event == 'WAIT_ESCAPE_COMBAT':
            # ↓↓ Check the life box of the wild pokemon
            x = int(len(image.resized_image[0]) // 8 * 7.9)
            y1 = int(len(image.resized_image) // 16 * 14.3)
            y2 = int(len(image.resized_image) // 16 * 15.2)
            if image.check_multiple_pixel_colors([x, y1], [x, y2]):
                Switch_Controller.current_event = 'ESCAPE_COMBAT'

        # ↓↓ Check if it's in the HOME page. Sometimes it fails to press the HOME button
        elif Switch_Controller.current_event == 'WAIT_HOME_STOP':
            if all(pixel_value == 255 for pixel_value in image.check_pixel_color([0, 0])):
                Switch_Controller.current_event = 'STOP'
            else: Switch_Controller.current_event = 'HOME_STOP'

        # ↓↓ Stop the program
        elif Switch_Controller.current_event == 'FINISH':
            print(MSG.SHINY_FOUND)
            Game_Capture.save_video(image)
            exit()

        Switch_Controller.event_lock.release()

    queue_next_frame(image)

    if not GUI.is_alive(): break

# ↓↓ Release the capture card and close all windows
Game_Capture.stop()
program_name = __file__.split('/')[-1]