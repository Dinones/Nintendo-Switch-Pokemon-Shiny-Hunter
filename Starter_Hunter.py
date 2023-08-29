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
import cv2

import Constants as CONST

import sys; sys.path.append('Utils')
from Switch_Controller import Switch_Controller
from Image_Processing import Image_Processing
from Game_Capture import Game_Capture
from FPS_Counter import FPS_Counter
from Pokemon_Database import Starly, Turtwig
from GUI import GUI
import Messages as MSG

import pyautogui, random; random.seed(6)

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

with open('./Media/Attempts.txt', 'r') as txt_file:
    attempts = int(txt_file.read())
    initial_attempts = attempts
    print(MSG.CURRENT_ATTEMPTS.replace('{attempts}', str(attempts)))

Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
if CONST.RECORD_VIDEO: 
    print(MSG.RECORDING_VIDEO)
    Game_Capture.start_recording()

Switch_Controller = Switch_Controller()
Thread(target = Switch_Controller.connect_controller, daemon = True).start()
Thread(target = Switch_Controller.run_event, daemon = True).start()

FPS_Counter = FPS_Counter()
Image_Queue = Queue()
GUI = GUI(Image_Queue)
GUI.start()

wild_pokemon = Starly
starter_pokemon = Turtwig

def queue_next_frame(image = None):
    if image is None: return
    Image_Queue.put(image)

def __test_print(text): print(text) if CONST.TESTING else None

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

while True:
    image = Image_Processing(Game_Capture.read())
    if image.original_image is None: continue

    image.resize_image()
    FPS_Counter.get_FPS()
    image.draw_FPS(FPS_Counter.FPS)
    image.detect_color()
    match = image.get_rectangles()

    Game_Capture.add_frame_to_video(image)

    if Switch_Controller.event_lock.acquire(blocking = False):
        # ↓↓ Wait for the black screen to load the game
        if Switch_Controller.current_event == 'WAIT_COMBAT':
            if not all(pixel_value == 0 for pixel_value in image.check_pixel_color()):
                Switch_Controller.current_event = 'MOVE_FORWARD'

        # ↓↓ Constantly press A to pass all the dialogues until it detects the starter selection menu
        elif Switch_Controller.current_event == 'PRESS_A':
            x = int(len(image.resized_image[0]) // 8 * 5.3)
            y1 = int(len(image.resized_image) // 8 * 4)
            y2 = int(len(image.resized_image) // 8 * 5)
            if image.check_multiple_pixel_colors([x, y1], [x, y2]): 
                __test_print(MSG.STARTER_DETECTED)
                Switch_Controller.current_event = 'WAIT_STARTER_SELECTION'

        # ↓↓ Wait for the white screen to load the combat
        elif Switch_Controller.current_event == 'STARTER_SELECTED':
            if not all(pixel_value == 255 for pixel_value in image.check_pixel_color()):
                Switch_Controller.current_event = 'WAIT_WILD_POKEMON_FOREGROUND'
                __test_print(MSG.WILD_POKEMON_SEARCHING)

        # ↓↓ Wait for the wild pokemon to appear in the foreground
        elif Switch_Controller.current_event == 'WAIT_WILD_POKEMON_FOREGROUND':
            x = int(len(image.resized_image[0]) // 16 * 1.2)
            y1 = int(len(image.resized_image) // 15 * 1)
            y2 = int(len(image.resized_image) // 15 * 2)
            if image.check_multiple_pixel_colors([x, y1], [x, y2]):
                __test_print(MSG.WILD_POKEMON_DETECTED)

                image.detect_pokemon_color(wild_pokemon)
                match = image.get_rectangles()
                if not wild_pokemon['shiny_color']: match = not match

                __test_print(MSG.SHINY_DETECTION.replace('{match}', str(match)))
                # ↓↓ Check whether the wild pokemon is shiny or not
                if match: 
                    Switch_Controller.current_event = 'HOME_STOP'
                    Switch_Controller.event_lock.release()
                    continue
                else: 
                    __test_print(MSG.TOGGLE_POKEMON_DETECTION)
                    Switch_Controller.current_event = 'WAIT_CHANGE_POKEMON'

        # ↓↓ Wait for the text box of the wild pokemon to disappear
        elif Switch_Controller.current_event == 'WAIT_CHANGE_POKEMON':
            x = int(len(image.resized_image[0]) // 16 * 1.2)
            y1 = int(len(image.resized_image) // 15 * 1)
            y2 = int(len(image.resized_image) // 15 * 2)
            if not image.check_multiple_pixel_colors([x, y1], [x, y2]): 
                Switch_Controller.current_event = 'WAIT_STARTER_POKEMON_FOREGROUND'
                __test_print('Toggling Pokemon Detection...')

        # ↓↓ Wait for the starter pokemon to appear in the foreground
        elif Switch_Controller.current_event == 'DETECT_STARTER_POKEMON':
            x = int(len(image.resized_image[0]) // 16 * 1.2)
            y1 = int(len(image.resized_image) // 15 * 1)
            y2 = int(len(image.resized_image) // 15 * 2)
            if image.check_multiple_pixel_colors([x, y1], [x, y2]):
                __test_print(f'Starter Pokemon Detected!')
                if CONST.SAVE_SCREENSHOTS: cv2.imwrite(f'./Media/Results/{attempts}.png', image.original_image)

                image.detect_pokemon_color(starter_pokemon)
                match = image.get_rectangles()
                if not starter_pokemon['shiny_color']: match = not match

                __test_print(f'Shiny Detection: {match}')
                # ↓↓ Check whether the wild pokemon is shiny or not
                if match: 
                    Switch_Controller.current_event = 'HOME_STOP'
                    Switch_Controller.event_lock.release()
                    continue
                else: print(); Switch_Controller.current_event = 'HOME_RESTART'

                try:
                    if CONST.INACTIVITY_AVOIDER:
                        random_number = random.randint(100, 1000)
                        pyautogui.moveTo(random_number, random_number)
                except: pass

                attempts += 1
                with open('./Media/Attempts.txt', 'w') as txt_file:
                    txt_file.write(str(attempts))
                    print(MSG.CURRENT_ATTEMPTS.replace('{attempts}', str(attempts)))

                # ↓↓ Save the current video and start the new one
                if CONST.RECORD_VIDEO:
                    Game_Capture.save_video(image)
                    Game_Capture.start_recording(image)

        # ↓↓ Check if it's in the HOME page. Sometimes it fails to press the HOME button
        elif Switch_Controller.current_event in ['WAIT_HOME_STOP', 'WAIT_HOME_RESTART']:
            if all(pixel_value == 255 for pixel_value in image.check_pixel_color([0, 0])):
                if Switch_Controller.current_event == 'WAIT_HOME_STOP': Switch_Controller.current_event = 'STOP'
                elif Switch_Controller.current_event == 'WAIT_HOME_RESTART': 
                    Switch_Controller.current_event = 'RESTART'
            else: 
                if Switch_Controller.current_event == 'WAIT_HOME_STOP': Switch_Controller.current_event = 'HOME_STOP'
                elif Switch_Controller.current_event == 'WAIT_HOME_RESTART': 
                    Switch_Controller.current_event = 'HOME_RESTART'

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