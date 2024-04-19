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
import PyQt5.QtGui as pyqt_g
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
        self.pyqt_images = {}
        self.masked_image = None
        self.contours_image = None
        self.FPS_image = None
        self.n_contours = 0

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

    def draw_star(self):
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
        cv2.fillPoly(self.FPS_image, [star_points], color=(0, 255, 255))
        cv2.polylines(self.FPS_image, [star_points], isClosed=True, color=(0, 0, 0), thickness=2)

        cv2.putText(self.FPS_image, str(self.n_contours), (star_center_x - 5*len(str(self.n_contours)), star_center_y + 5),
            cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['star_num_color'],
            CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

    #######################################################################################################################

    # Convert the image to PyQt compatible format
    def get_pyqt_image(self, image):
        try: height, width, channel = image.shape
        except: height, width = image.shape

        bytes_per_line = 3 * width
        aux = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qt_image = pyqt_g.QImage(aux.data, width, height, bytes_per_line, pyqt_g.QImage.Format_RGB888)
        return pyqt_g.QPixmap.fromImage(qt_image)

    #######################################################################################################################

    def get_pyqt_images(self, images = []):
        if not isinstance(images, list): return
        for image in ['FPS_image', 'contours_image', 'masked_image']: 
            if not image in images: return

        self.pyqt_images['FPS_image'] = self.get_pyqt_image(self.FPS_image)
        for image_name in ['contours_image', 'masked_image']:
            self.pyqt_images[image_name] = cv2.resize(getattr(self, image_name), CONST.SECONDARY_FRAME_SIZE)
            self.pyqt_images[image_name] = self.get_pyqt_image(self.pyqt_images[image_name])

    #######################################################################################################################

    def draw_button(self, button = ''):
        if not isinstance(button, str): return

        self.contours_image = np.copy(self.resized_image)
        if button == 'A': cv2.circle(self.contours_image, (307, 80), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'B': cv2.circle(self.contours_image, (288, 99), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'Y': cv2.circle(self.contours_image, (269, 80), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'X': cv2.circle(self.contours_image, (288, 61), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'HOME': cv2.circle(self.contours_image, (275, 195), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'UP': cv2.circle(self.contours_image, (62, 129), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'DOWN': cv2.circle(self.contours_image, (61, 167), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'RIGHT': cv2.circle(self.contours_image, (81, 148), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        elif button == 'LEFT': cv2.circle(self.contours_image, (43, 148), 9, CONST.PRESSED_BUTTON_COLOR, -1)

    #######################################################################################################################

    # Return the requested pixel color. Default: top-left corner pixel
    def check_pixel_color(self, pixel = (5, 5)): return self.original_image[pixel[0]][pixel[1]]

    #######################################################################################################################

    # Return whether all the pixels of the specifiead row are white
    def check_multiple_pixel_colors(self, start, end, color = 255):
        pixels = []
        for index in range(start[1], end[1]):
            if all(pixel_value == color for pixel_value in self.resized_image[-index][start[0]]): pixels.append(True)
            # If one False is found, there is no need to check the other pixels
            else: pixels.append(False); break
        if CONST.TESTING: 
            for index in range(start[1], end[1]): self.FPS_image[-index][start[0]] = [255, 0, 255]
        return all(pixels)

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
        print(COLOR_str.MENU_OPTION.replace('{index}', '4').replace('{option}', 'Check lost shiny'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Image Processing'))

        menu_options = {
            '1': process_video,
            '2': process_image,
            '3': extract_frames_from_video,
            '4': check_lost_shiny,
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

        # cv2.imshow(f'{CONST.BOT_NAME} - Original', image.original_image)
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
            .replace('{key}', "'Q'")
            .replace('{instruction}', 'exit the program')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'SPACE'")
            .replace('{instruction}', 'pause/resume the execution')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'A'")
            .replace('{instruction}', 'move a frame backwards')
        )
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'D'")
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
            image.draw_star()

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
            time.sleep(0.05)

        Video_Capture.stop()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the video!') + '\n'
        )

    #######################################################################################################################

    def check_lost_shiny(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Checking lost shiny")
            .replace('{path}', f"")
        )

        if not os.path.exists(f'../{CONST.IMAGES_FOLDER_PATH}'): 
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.IMAGES_FOLDER_PATH}'") + '\n'
        )

        images = sorted([image for image in sorted(os.listdir(f'../{CONST.IMAGES_FOLDER_PATH}')) 
            if image.lower().endswith(('.png', '.jpg', 'jpeg'))], key = lambda x: int(x.split('.')[0]))

        # Instructions
        print(COLOR_str.SUCCESSFULLY_LOADED_IMAGES.replace('{images}', str(len(images))))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION.replace('{key}', "'SPACE'")
            .replace('{module}', 'Image Processing')
            .replace('{instruction}', 'pause the program'))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION.replace('{key}', "'A' or 'D'")
            .replace('{module}', 'Image Processing')
            .replace('{instruction}', 'go back / forward while in pause'))
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION.replace('{key}', "'Q'")
            .replace('{module}', 'Image Processing')
            .replace('{instruction}', 'stop the program'))

        index = 0
        pause = False
        timer = time.time()
        second_text_position = [CONST.TEXT_PARAMS['position'][0], CONST.TEXT_PARAMS['position'][1] + 20]

        while True and (index + 1) != len(images):
            if time.time() - timer >= 0.3:
                if pause: index -= 1
                image = Image_Processing(f'../{CONST.IMAGES_FOLDER_PATH}/{images[index]}')
                image.resize_image()
                cv2.putText(image.resized_image, f'Count: {index}/{len(images)}', CONST.TEXT_PARAMS['position'], 
                    cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'],
                    CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)
                cv2.putText(image.resized_image, f'{images[index]}', second_text_position, 
                    cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'],
                    CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)
                cv2.imshow('Lost Shiny Checker', image.resized_image)

                index += 1
                timer = time.time()

            # Press 'SPACE' to resume the execution
            # Press 'a' or 'd' to move between frames
            # Press 'q' to stop the program
            key = cv2.waitKey(1)
            if key in [ord('q'), ord('Q')]: break
            elif key == ord(' '): pause = not pause
            elif pause and key in [ord('a'), ord('A')]: index -= 1
            elif pause and key in [ord('d'), ord('D')]: index += 1 

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', f'Successfully checked {index + 1}/{len(images)} images!') + '\n'
        )

    main_menu()