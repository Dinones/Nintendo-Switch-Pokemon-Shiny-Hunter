###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__': os.chdir(os.path.dirname(__file__))

import cv2

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Game_Capture:
    def __init__(self, video_capture_index = 0):
        self.video_capture = cv2.VideoCapture(video_capture_index)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CONST.ORIGINAL_FRAME_SIZE[0])
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CONST.ORIGINAL_FRAME_SIZE[1])

        self.frame = None
        self.resized_frame = None
        self.masked_frame = None

        self.read()
        if self.frame is None: exit(print(f'[χ] Could not access to the video capture nº{video_capture_index}'))

    # ↓↓ Take a frame
    def read(self): 

        '''
        ################################# TRANSFORMAR A GRAYSCALE Y MIRAR SI TODO SON ZEROS, SI ES ASÍ, RETURN None TAMBIÉN
        #################### PONER EN OTRA FUNCIÓN, SOLO QUEREMOS QUE SE COMPRUEBE CUANDO SE ENCIENDE LA CÁMARA POR PRIMERA VEZ (PUEDE HABER FRAMES NEGROS EN EL JUEGO)
        # print(self.frame)
        # array = [x for x in self.frame if x]
        # print(array)
        #############################################################
        '''

        ret, self.frame = self.video_capture.read()
        # ↓↓ Could not read the frame
        if not ret: self.frame = None; return
        # ↓↓ Resize the image so it does not fit the full screen when displaying
        self.resized_frame = cv2.resize(self.frame, CONST.BOT_WINDOW_SIZE)
        return self.frame

    # ↓↓ Release the capture card and close all windows
    def stop(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
    while True:
        Game_Capture.read()
        if Game_Capture.frame is None: continue
        
        # ↓↓ Display the frame
        cv2.imshow(CONST.BOT_NAME, Game_Capture.resized_frame)
        # ↓↓ Press 'q' to stop the program
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'): break

    # ↓↓ Release the capture card and close all windows
    Game_Capture.stop()