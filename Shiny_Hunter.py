###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__': os.chdir(os.path.dirname(__file__))

from threading import Thread
from queue import Queue
import cv2

import Constants as CONST

import sys; sys.path.append('Utils')
from Image_Processing import Image_Processing
from Game_Capture import Game_Capture
from FPS_Counter import FPS_Counter
from GUI import GUI

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
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
    image = Image_Processing(Game_Capture.read())
    if image.original_image is None: continue

    image.resize_image()
    FPS_Counter.get_FPS()
    image.draw_FPS(FPS_Counter.FPS)
    image.detect_color()
    match = image.get_rectangles()

    queue_next_frame(image)

    if not GUI.is_alive(): break

# ↓↓ Release the capture card and close all windows
Game_Capture.stop()