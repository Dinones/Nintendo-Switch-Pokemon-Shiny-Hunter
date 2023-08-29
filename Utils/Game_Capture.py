###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass
    
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
        
        self.video_recorder = None
        self.video_recorder_contours = None

        self.frame = None
        self.resized_frame = None

        self.read()
        if self.frame is None: exit(print(f'Could not access to the video capture nº{video_capture_index}'))

    # ↓↓ Take a frame
    def read(self): 
        ret, self.frame = self.video_capture.read()
        # ↓↓ Could not read the frame
        if not ret: self.frame = None; return
        # ↓↓ Resize the image so it does not fit the full screen when displaying
        self.resized_frame = cv2.resize(self.frame, CONST.BOT_WINDOW_SIZE)
        return self.frame

    # ↓↓ Release the capture card and close all windows
    def stop(self):
        self.video_capture.release()
        if CONST.RECORD_VIDEO and type(self.video_recorder) is not type(None):
            self.video_recorder.release()
            if CONST.RECORD_MULTIPLE_WINDOWS and type(self.video_recorder_contours) is not type(None):
                self.video_recorder_contours.release()
        cv2.destroyAllWindows()

    # ↓↓ Records a video of each soft reset
    def start_recording(self, image = None):
        self.video_recorder = cv2.VideoWriter(f'./Media/{CONST.OUTPUT_VIDEO_NAME}', cv2.VideoWriter_fourcc(*'XVID'),
            CONST.VIDEO_FPS, CONST.ORIGINAL_FRAME_SIZE)
            
        if CONST.RECORD_MULTIPLE_WINDOWS and type(image) is not type(None):
            self.video_recorder_contours = cv2.VideoWriter(f'./Media/{CONST.OUTPUT_CONTOURS_VIDEO_NAME}',
                cv2.VideoWriter_fourcc(*'XVID'), CONST.VIDEO_FPS, image.resized_image.shape[1::-1])

    # ↓↓ Save the current video and start recording the next one
    def save_video(self, image = None):
        self.video_recorder.release()
        if CONST.RECORD_MULTIPLE_WINDOWS and type(image) is not type(None):
            if type(self.video_recorder_contours) is not type(None): 
                self.video_recorder_contours.release()
                
    def add_frame_to_video(self, image):
        if CONST.RECORD_VIDEO: 
            self.video_recorder.write(image.original_image)
            if CONST.RECORD_MULTIPLE_WINDOWS and type(self.video_recorder_contours) is not type(None):
                    self.video_recorder_contours.write(image.contours_image)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    from FPS_Counter import FPS_Counter

    Game_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
    FPS_Counter = FPS_Counter()
    
    while True:
        Game_Capture.read()
        if Game_Capture.frame is None: continue

        if CONST.TESTING:
            # ↓↓ Middle dot
            # print(f'Middle Dot Color: {Game_Capture.frame[len(Game_Capture.frame)//2, len(Game_Capture.frame[0])//2]}')
            Game_Capture.resized_frame[len(Game_Capture.resized_frame)//2, 
                len(Game_Capture.resized_frame[0])//2] = [255, 0, 255]

            # ↓↓ Starter backpack
            x = int(len(Game_Capture.resized_frame[0]) // 8 * 5.3)
            y1 = int(len(Game_Capture.resized_frame) // 8 * 4)
            y2 = int(len(Game_Capture.resized_frame) // 8 * 5)
            # [x, y1], [x, y2]
            for index in range(y1, y2): 
                # print(all(pixel_value == 255 for pixel_value in Game_Capture.resized_frame[-index][x]))
                Game_Capture.resized_frame[-index][x] = [255, 0, 255]

            # ↓↓ Text box
            x = int(len(Game_Capture.resized_frame[0]) // 16 * 1.2)
            y1 = int(len(Game_Capture.resized_frame) // 15 * 1)
            y2 = int(len(Game_Capture.resized_frame) // 15 * 2)
            # [x, y1], [x, y2]
            for index in range(y1, y2): 
                # print(all(pixel_value == 255 for pixel_value in Game_Capture.resized_frame[-index][x]))
                Game_Capture.resized_frame[-index][x] = [255, 0, 255]

            # ↓↓ Wild pokemon life box
            x = int(len(Game_Capture.resized_frame[0]) // 8 * 7.9)
            y1 = int(len(Game_Capture.resized_frame) // 16 * 14.3)
            y2 = int(len(Game_Capture.resized_frame) // 16 * 15.2)
            # [x, y1], [x, y2]
            for index in range(y1, y2): 
                # print(all(pixel_value == 255 for pixel_value in Game_Capture.resized_frame[-index][x]))
                Game_Capture.resized_frame[-index][x] = [255, 0, 255]

            # ↓↓ Wild pokemon life box
            x1 = int(len(Game_Capture.resized_frame[0]) // 8 * 0.65)
            x2 = int(len(Game_Capture.resized_frame[0]) // 8 * 7.5)
            y1 = int(len(Game_Capture.resized_frame) // 16 * 13.2)
            y2 = int(len(Game_Capture.resized_frame) // 16 * 14.7)
            Game_Capture.resized_frame = cv2.rectangle(Game_Capture.resized_frame, [x1, y1], [x2, y2], [255, 0, 255])

        FPS_Counter.get_FPS()
        cv2.putText(Game_Capture.resized_frame, f'FPS: {FPS_Counter.FPS}', CONST.TEXT_PARAMS['position'], 
            cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'], 
            CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

        # ↓↓ Display the frame
        cv2.imshow(CONST.BOT_NAME, Game_Capture.resized_frame)
        # ↓↓ Press 'q' to stop the program
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'): break

    # ↓↓ Release the capture card and close all windows
    Game_Capture.stop()