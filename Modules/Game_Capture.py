###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass
    
import cv2
# Disable warning messages
cv2.setLogLevel(0)

import sys; sys.path.append('..')
import Colored_Strings as COLOR_str
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Game_Capture():
    def __init__(self, video_capture_index = CONST.VIDEO_CAPTURE_INDEX):
        self.video_capture = cv2.VideoCapture(video_capture_index)
        # Highly increase the FPS using the MJPEG codec
        self.video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        if not self.video_capture.isOpened():
            video_captures = self.find_available_video_captures()
            if not any(video_captures): return
            self.video_capture.release()
            first_available_capture_card = video_captures.index(True)
            self.video_capture = cv2.VideoCapture(first_available_capture_card)
            print(COLOR_str.USING_DIFFERENT_CAPTURE_CARD
                .replace('{old_video_capture}', str(video_capture_index))
                .replace('{new_video_capture}', str(first_available_capture_card))
            )

        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CONST.ORIGINAL_FRAME_SIZE[0])
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CONST.ORIGINAL_FRAME_SIZE[1])
        
        self.video_recorder = None
        self.frame = None
        self.skipped_frames = 0

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
        cv2.destroyAllWindows()

    #######################################################################################################################

    # Find all available capture cards
    @staticmethod
    def find_available_video_captures():
        video_captures = []
        for index in range(CONST.MAX_VIDEO_DEVICES_ANALIZED):
            video_capture = cv2.VideoCapture(index)
            video_captures.append(video_capture.isOpened())
            video_capture.release()
        return video_captures

    #######################################################################################################################

    # Record a video of each encounter
    def start_recording(self):
        if CONST.ENABLE_VIDEO_RECORDING:
            self.video_recorder = cv2.VideoWriter(f'./{CONST.OUTPUT_VIDEO_PATH}', cv2.VideoWriter_fourcc(*'XVID'),
                CONST.VIDEO_FPS, CONST.ORIGINAL_FRAME_SIZE)

    #######################################################################################################################

    # Save the current video and start recording the next one
    def save_video(self, special_name = ''):
        if CONST.ENABLE_VIDEO_RECORDING:
            self.video_recorder.release()
            try: 
                if special_name: os.rename(f'./{CONST.OUTPUT_VIDEO_PATH}', f'./Media/Videos/{special_name}.avi')
            except: pass
        
    #######################################################################################################################

    # Add a frame to the video
    def add_frame_to_video(self, image):
        if CONST.ENABLE_VIDEO_RECORDING:
            if isinstance(self.video_recorder, type(None)): self.start_recording()
            self.video_recorder.write(image.original_image)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    from time import time
    from FPS_Counter import FPS_Counter
    from Image_Processing import Image_Processing

    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Game Capture'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Print all available video devices'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Check current capture device'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Game Capture'))

        menu_options = {
            '1': print_video_captures,
            '2': check_video_capture,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Game Capture') + '\n')

    #######################################################################################################################

    def print_video_captures(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Game Capture')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Printing all available video devices...")
            .replace('{path}', f"")
        )

        video_captures = Game_Capture.find_available_video_captures()
        print(COLOR_str.AVAILABLE_CAPTURE_DEVICES)
        for index, video_capture in enumerate(video_captures):
            if video_capture: print(COLOR_str.CAPTURE_DEVICE_OK.replace('{index}', str(index)))
            else: print(COLOR_str.CAPTURE_DEVICE_NOT_OK.replace('{index}', str(index)))
        print()

    #######################################################################################################################
    #######################################################################################################################

    def check_video_capture(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Game Capture')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Activating capture device nº{CONST.VIDEO_CAPTURE_INDEX}...")
            .replace('{path}', f"")
        )

        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
        if not Video_Capture.video_capture.isOpened(): 
            Video_Capture.stop()
            print(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'") + '\n')
            return
        FPS = FPS_Counter()

        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'c'")
            .replace('{instruction}', 'take a screenshot')
        ); print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'q'")
            .replace('{instruction}', 'exit the program')
        )

        while True: 
            image = Image_Processing(Video_Capture.read_frame())
            if isinstance(image.original_image, type(None)): continue

            image.resize_image()
            FPS.get_FPS()
            image.draw_FPS(FPS.FPS)

            cv2.imshow(f'{CONST.BOT_NAME} - Device {CONST.VIDEO_CAPTURE_INDEX}', image.FPS_image)

            # Press 'q' to stop the program
            # Press 'c' to take a screenshot
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'): break
            elif key == ord('c') or key == ord('C'): 
                if not os.path.exists(f'../{CONST.SAVING_FRAMES_PATH}'):
                    print(COLOR_str.INVALID_PATH_WARNING
                        .replace('{module}', 'Game Capture')
                        .replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}'")
                    )
                    continue

                file_name = str(time())
                cv2.imwrite(f'../{CONST.SAVING_FRAMES_PATH}/{file_name}.png', image.original_image)
                print(COLOR_str.IMAGE_SAVED.replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}/{file_name}.png'"))

        # Release the capture card and close all windows
        Video_Capture.stop()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Game Capture')
            .replace('{reason}', 'Successfully activated video device!') + '\n'
        )

    #######################################################################################################################
    #######################################################################################################################

    main_menu()