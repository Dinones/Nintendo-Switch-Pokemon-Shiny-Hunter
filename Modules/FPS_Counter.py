###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

from time import time, sleep

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class FPS_Counter():
    def __init__(self):
        self.previous_time = time()
        self.frame_count = 0
        self.FPS = 0
    
    def get_FPS(self):
        if not CONST.FPS_COUNTER: return
        if time() - self.previous_time < CONST.REFRESH_FPS_TIME: self.frame_count += 1; return

        self.FPS = self.frame_count // CONST.REFRESH_FPS_TIME
        self.previous_time = time()
        self.frame_count = 0

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    FPS_Counter = FPS_Counter()
    FPS_aux = 0
    while True:
        FPS_Counter.get_FPS()
        if FPS_aux != FPS_Counter.FPS:
            print(f"FPS: {FPS_Counter.FPS}")
            FPS_aux = FPS_Counter.FPS