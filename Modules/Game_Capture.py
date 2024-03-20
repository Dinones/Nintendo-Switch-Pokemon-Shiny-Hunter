###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass
    
import cv2

import sys; sys.path.append('..')
import Colored_Strings as COLOR_str
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Game_Capture():
    def __init__(self, video_capture_index = 0):
        self.video_capture = cv2.VideoCapture(video_capture_index)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CONST.ORIGINAL_FRAME_SIZE[0])
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CONST.ORIGINAL_FRAME_SIZE[1])
        
        self.video_recorder = None
        self.video_recorder_contours = None

        self.frame = None

        # Check if the capture card is working properly
        self.read_frame()
        if isinstance(self.frame, type(None)): 
            self.stop()
            exit(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{video_capture_index}'"))

    #######################################################################################################################

    # Take a frame
    def read_frame(self): 
        success, self.frame = self.video_capture.read()
        # Could not read the frame
        if not success: self.frame = None; return
        return self.frame

    #######################################################################################################################

    # Release the capture card
    def stop(self):
        self.video_capture.release()
        # if CONST.RECORD_VIDEO and type(self.video_recorder) is not type(None):
        #     self.video_recorder.release()
        #     if CONST.RECORD_MULTIPLE_WINDOWS and type(self.video_recorder_contours) is not type(None):
        #         self.video_recorder_contours.release()
        cv2.destroyAllWindows()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

