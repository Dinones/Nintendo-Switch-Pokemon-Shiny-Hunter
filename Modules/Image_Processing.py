###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import cv2
import numpy as np
from PIL import Image, ImageTk

import sys; sys.path.append('..')
import Colored_Strings as COLOR_str
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Image_Processing():
    def __init__(self, image = ''):
        self.original_image = None
        self.grayscale_image = None
        self.resized_image = None
        self.tkinter_images = {}
        self.masked_image = None
        self.contours_image = None
        self.FPS_image = None

        # Load the image
        if isinstance(image, str): self.original_image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        else: self.original_image = image
        if isinstance(self.original_image, type(None)): return print(COLOR_str.COULD_NOT_PROCESS_IMAGE)

    #######################################################################################################################

    def resize_image(self, desired_size = CONST.MAIN_FRAME_SIZE):
        if isinstance(self.original_image, type(None)): return

        # (width, height)
        original_size = self.original_image.shape[1::-1]
        # Get the desired aspect ratio and size
        aspect_ratio = original_size[0]/original_size[1]
        max_size_index = np.argmax(original_size)
        if not max_size_index: new_size = [desired_size[max_size_index], int(desired_size[max_size_index]/aspect_ratio)]
        else: new_size = [int(desired_size[max_size_index]*aspect_ratio), desired_size[max_size_index]]

        # Resize the image
        self.resized_image = cv2.resize(self.original_image, new_size)

    #######################################################################################################################

    def get_mask(self):
        if isinstance(self.resized_image, type(None)): return

        self.grayscale_image = cv2.cvtColor(self.resized_image, cv2.COLOR_BGR2GRAY)
        _, self.masked_image = cv2.threshold(self.grayscale_image, CONST.LOWER_COLOR, CONST.UPPER_COLOR, cv2.THRESH_BINARY)

    #######################################################################################################################

    def get_rectangles(self):
        if isinstance(self.masked_image, type(None)): return
        self.contours_image = np.copy(self.resized_image)

        contours, hierarchy = cv2.findContours(self.masked_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        filtered_contours = []

        import random
        for contour in contours:
            # Minimum object size to detect as a match
            if cv2.contourArea(contour) > CONST.MIN_DETECT_SIZE:
                filtered_contours.append(contour)
                # Draw the rectangles
                x, y, w, h = cv2.boundingRect(contour)
                # The "-1" parameter indicates that all contours should be drawn
                cv2.drawContours(self.contours_image, filtered_contours, -1, CONST.RECTANGLES_PARAMS['color'], 
                    CONST.RECTANGLES_PARAMS['thickness'])

        return len(filtered_contours)

    #######################################################################################################################

    def draw_FPS(self, FPS = 0):
        self.FPS_image = np.copy(self.resized_image)
        cv2.putText(self.FPS_image, f'FPS: {FPS}', CONST.TEXT_PARAMS['position'], cv2.FONT_HERSHEY_SIMPLEX, 
            CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'], CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

    #######################################################################################################################

    def draw_star(self, n_contours = 0):
        image_height, image_width = self.contours_image.shape[:2]
        inner_radius = 13
        outer_radius = 26
        border_margin = 10
        n_points = 8
        star_center_x = image_width - outer_radius - border_margin
        star_center_y = outer_radius + border_margin

        angle = np.pi / n_points
        star_points = []
        for i in range(n_points * 2):
            r = outer_radius if i % 2 == 0 else inner_radius
            # Adjust starting angle
            theta = i * angle - np.pi/2  
            x = star_center_x + int(r * np.cos(theta))
            y = star_center_y + int(r * np.sin(theta))
            star_points.append((x, y))

        star_points = np.array([star_points], dtype=np.int32)
        cv2.fillPoly(self.contours_image, [star_points], color=(0, 255, 255))

        cv2.putText(self.contours_image, str(n_contours), (star_center_x - 5*len(str(n_contours)), star_center_y + 5),
            cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['star_num_color'],
            CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

    #######################################################################################################################

    # Convert the image to tkinter compatible format
    # Will raise an error if used before creating a GUI (root = Tk())
    def get_tkinter_image(self, image):
        try: return ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        except: return None

    #######################################################################################################################

    def get_tkinter_images(self, images = []):
        if not isinstance(images, list): return

        self.tkinter_images['FPS_image'] = self.get_tkinter_image(self.FPS_image)
        for image_name in ['contours_image', 'masked_image']:
            self.tkinter_images[image_name] = cv2.resize(getattr(self, image_name), CONST.SECONDARY_FRAME_SIZE)
            self.tkinter_images[image_name] = self.get_tkinter_image(self.tkinter_images[image_name])

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import time
    from Game_Capture import Game_Capture
    
    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Image Processing'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Process video'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Process image'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '3').replace('{option}', 'Extract frames from video'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Image Processing'))

        menu_options = {
            '1': process_video,
            '2': process_image,
            '3': extract_frames_from_video,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Image Processing') + '\n')

    #######################################################################################################################

    def process_image(option): 
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Processing image")
            .replace('{path}', f"'../{CONST.TESTING_IMAGE_PATH}'")
        )

        image = Image_Processing(f'../{CONST.TESTING_IMAGE_PATH}' )
        if isinstance(image.original_image, type(None)): return

        image.resize_image()
        image.get_mask()
        contours = image.get_rectangles()

        print(COLOR_str.CONTOURS_FOUND.replace('{contours}', str(contours)))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'q'")
            .replace('{instruction}', 'exit the program')
        )

        cv2.imshow(f'{CONST.BOT_NAME} - Original', image.original_image)
        # cv2.imshow(f'{CONST.BOT_NAME} - Grayscale', image.grayscale_image)
        cv2.imshow(f'{CONST.BOT_NAME} - Mask', image.masked_image)
        cv2.imshow(f'{CONST.BOT_NAME} - Contours', image.contours_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the image!') + '\n'
        )

    #######################################################################################################################

    def extract_frames_from_video(option): 
        print(COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f'Extracting frames into')
            .replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}'")
        )

        if not os.path.exists(f'../{CONST.TESTING_VIDEO_PATH}') or not os.path.exists(f'../{CONST.SAVING_FRAMES_PATH}'): 
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}' or '../{CONST.SAVING_FRAMES_PATH}'") + '\n'
            )

        Video_Capture = Game_Capture(f'../{CONST.TESTING_VIDEO_PATH}')
        image = Image_Processing(Video_Capture.frame)

        total_frames = int(Video_Capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_index = 1
        
        print(COLOR_str.CURRENT_EXTRACTED_FRAMES
            .replace('{extracted_frame}', str(frame_index))
            .replace('{total_frames}', str(total_frames))
            .replace('{percentage}', '0'), end='\r', flush=True
        )

        while True:
            image.original_image = Video_Capture.read_frame()
            # No more frames in the video
            if isinstance(image.original_image, type(None)): print(); break

            cv2.imwrite(f'../{CONST.SAVING_FRAMES_PATH}/{frame_index}.png', image.original_image)

            # Inefficient? Maybe, but looks cool and doesn't affect the main code
            print(COLOR_str.CURRENT_EXTRACTED_FRAMES
                .replace('{extracted_frame}', str(frame_index + 1))
                .replace('{total_frames}', str(total_frames))
                .replace('{percentage}', str(int((frame_index + 1)/total_frames*100))), end='\r', flush=True
            )         

            frame_index += 1

        Video_Capture.stop()
        print(COLOR_str.SUCCESSFULLY_EXTRACTED_FRAMES.replace('{frames}', str(frame_index)) + '\n')

    #######################################################################################################################

    def process_video(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Processing video")
            .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}'")
        )

        if not os.path.exists(f'../{CONST.TESTING_VIDEO_PATH}'): 
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_VIDEO_PATH}'") + '\n'
            )

        Video_Capture = Game_Capture(f'../{CONST.TESTING_VIDEO_PATH}')
        image = Image_Processing(Video_Capture.frame)

        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'q'")
            .replace('{instruction}', 'exit the program')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'SPACE'")
            .replace('{instruction}', 'pause/resume the execution')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'a'")
            .replace('{instruction}', 'move a frame backwards')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'d'")
            .replace('{instruction}', 'move a frame forward')
        )

        counter = 0
        pause = False
        total_video_frames = int(Video_Capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        def process_single_frame(image, frame = None):
            if not isinstance(frame, type(None)): Video_Capture.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

            image.original_image = Video_Capture.read_frame()
            # No more frames in the video
            if isinstance(image.original_image, type(None)): return

            image.resize_image()
            image.get_mask()
            n_contours = image.get_rectangles()
            image.draw_star(n_contours)

            cv2.imshow(f'{CONST.BOT_NAME} - Mask', image.masked_image)
            cv2.imshow(f'{CONST.BOT_NAME} - Contours', image.contours_image)

        while True:
            if pause: 
                # Press 'SPACE' to resume the execution
                # Press 'a' or 'd' to move between frames
                # Press 'q' to stop the program
                key = cv2.waitKey(1)
                if key == ord('q') or key == ord('Q'): break
                elif key == ord(' '): pause = not pause
                elif key == ord('a') or key == ord('A'): 
                    if counter > 0: 
                        counter = counter - 1
                        process_single_frame(image, counter)
                        continue
                elif key == ord('d') or key == ord('D'):
                    if counter < total_video_frames:
                        counter = counter + 1
                        process_single_frame(image, counter)
                        continue

                time.sleep(0.1)
                continue

            process_single_frame(image)
            # No more frames in the video
            if isinstance(image.original_image, type(None)): break

            # Press 'SPACE' to pause the execution
            # Press 'q' to stop the program
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'): break
            if key == ord(' '): pause = not pause

            counter += 1
            time.sleep(0.1)

        Video_Capture.stop()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the video!') + '\n'
        )

    #######################################################################################################################

    main_menu()