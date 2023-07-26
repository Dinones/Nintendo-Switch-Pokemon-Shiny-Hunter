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
from time import time
import cv2

import Constants as CONST

import sys; sys.path.append('Utils')
from Switch_Controller import Switch_Controller
from Image_Processing import Image_Processing
from Game_Capture import Game_Capture
from FPS_Counter import FPS_Counter
from GUI import GUI

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

with open('./Media/Attempts.txt', 'r') as txt_file:
    attempts = int(txt_file.read())
    print(f'Current attempts: {attempts}')

Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
if CONST.RECORD_VIDEO: 
    print('Recording video for each soft reset...')
    Game_Capture.start_recording()

Switch_Controller = Switch_Controller()
Thread(target = Switch_Controller.connect_controller, daemon = True).start()
Thread(target = Switch_Controller.run_event, daemon = True).start()

FPS_Counter = FPS_Counter()
Image_Queue = Queue()
GUI = GUI(Image_Queue)
GUI.start()

def queue_next_frame(image = None):
    if image is None: return
    Image_Queue.put(image)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

while True:
    if Switch_Controller.event_lock.acquire(blocking = False):
        if Switch_Controller.current_event == 'FINISH': exit()
        Switch_Controller.event_lock.release()

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
            if not all(pixel_value == 0 for pixel_value in image.check_corner_color()):
                Switch_Controller.current_event = 'COMBAT'
        # ↓↓ Wait for the white screen to load the combat
        elif Switch_Controller.current_event == 'WAIT_RESTART':
            if not all(pixel_value == 255 for pixel_value in image.check_corner_color()):
                Switch_Controller.current_event = 'WAIT_SHINY_CHECK'
                timer = time()
        elif Switch_Controller.current_event == 'WAIT_SHINY_CHECK':
                if time() - timer >= CONST.ENTER_COMBAT_WAIT_SECONDS:
                    cv2.imwrite(f'./Media/Results/{attempts}.png', image.original_image)
                    
                    if match: 
                        Switch_Controller.current_event = 'STOP'
                        Switch_Controller.event_lock.release()
                        continue
                    else: Switch_Controller.current_event = 'RESTART'

                    attempts += 1
                    with open('./Media/Attempts.txt', 'w') as txt_file:
                        txt_file.write(str(attempts))
                        print(f'Current attempts: {attempts}')

                    timer = time()
                    # ↓↓ Save the current video and start the new one
                    if CONST.RECORD_VIDEO and Switch_Controller.current_event == 'RESTART':
                        Game_Capture.save_video(image)
                        Game_Capture.start_recording(image)
        elif Switch_Controller.current_event == 'FINISH': 
            print('Shiny found!')
            Game_Capture.save_video(image)
            exit()
        Switch_Controller.event_lock.release()

    queue_next_frame(image)

    if not GUI.is_alive(): break

# ↓↓ Release the capture card and close all windows
Game_Capture.stop()
program_name = __file__.split('/')[-1]
os.system(f'sudo pkill -f "{program_name}"')