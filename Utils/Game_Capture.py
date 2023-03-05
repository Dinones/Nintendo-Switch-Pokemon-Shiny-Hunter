###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import cv2

import sys; sys.path.append('./')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Game_Capture:
    def __init__(self, video_capture_index = 0):
        self.video_capture = cv2.VideoCapture(video_capture_index, cv2.CAP_DSHOW)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CONST.ORIGINAL_FRAME_SIZE[0])
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CONST.ORIGINAL_FRAME_SIZE[1])

        self.original_frame = None
        self.resized_frame = None

        self.read()
        if self.original_frame is None: exit(print(f'[χ] Could not access to the video capture nº{video_capture_index}'))

    # ↓↓ Take a frame
    def read(self): 
        ret, self.original_frame = self.video_capture.read()
        # ↓↓ Could not read the frame
        if not ret: self.original_frame = None; return
        # ↓↓ Resize the image so it does not fit the full screen when displaying
        self.resized_frame = cv2.resize(self.original_frame, CONST.BOT_WINDOW_SIZE)

    # ↓↓ Release the capture card and close all windows
    def stop(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
while True:
    Game_Capture.read()
    if Game_Capture.original_frame is None: continue
    
    # ↓↓ Display the frame
    cv2.imshow(CONST.BOT_NAME, Game_Capture.resized_frame)

    key = cv2.waitKey(1)
    if key == ord('q'): break

# ↓↓ Release the capture card and close all windows
Game_Capture.stop()