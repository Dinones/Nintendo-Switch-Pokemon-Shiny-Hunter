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

Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)

Switch_Controller = Switch_Controller()
Thread(target = Switch_Controller.connect_controller, daemon = True).start()
Thread(target = Switch_Controller.run_event, daemon = True).start()

FPS_Counter = FPS_Counter()
Image_Queue = Queue()
GUI = GUI(Image_Queue)
GUI.start()

def queue_next_frame(image=None):
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
                    cv2.imwrite(f'./Media/{time()}.png', image.original_image)
                    Switch_Controller.current_event = 'RESTART'
        elif Switch_Controller.current_event == 'FINISH': exit()
        Switch_Controller.event_lock.release()

    queue_next_frame(image)

    if not GUI.is_alive(): break

# ↓↓ Release the capture card and close all windows
Game_Capture.stop()