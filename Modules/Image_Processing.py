###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import cv2
import pytesseract
import numpy as np
from time import time
import PyQt5.QtGui as pyqt_g

# import sys; sys.path.append('..')
import sys; sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Colored_Strings as COLOR_str
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Image_Processing():
    def __init__(self, image = ''):
        self.original_image = None
        self.resized_image = None
        self.pyqt_image = None
        self.FPS_image = None
        self.shiny_detection_time = 0

        # Used to send a notification to the user
        self.saved_image_path: str = ''

        # Load the image
        if isinstance(image, str): self.original_image = cv2.imread(image, cv2.IMREAD_UNCHANGED)
        else: self.original_image = image
        if isinstance(self.original_image, type(None)): return print(COLOR_str.COULD_NOT_PROCESS_IMAGE)

    #######################################################################################################################

    # Resize the image
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

    # Draw FPS at the top-left corner
    def draw_FPS(self, FPS = 0):
        if isinstance(self.FPS_image, type(None)):
            # Without copy() method, images would be linked, meaning that modifying one image would also alter the other
            self.FPS_image = np.copy(self.resized_image)

        cv2.putText(self.FPS_image, f'FPS: {FPS}', CONST.TEXT_PARAMS['position'], cv2.FONT_HERSHEY_SIMPLEX,
            CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'], CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

    #######################################################################################################################

    # Write the spcified at the top-left corner
    def write_text(self, text = '', position_offset = (0, 0)):
        if isinstance(self.FPS_image, type(None)):
            # Without copy() method, images would be linked, meaning that modifying one image would also alter the other
            self.FPS_image = np.copy(self.resized_image)

        cv2.putText(self.FPS_image, text, tuple(a + b for a, b in zip(CONST.TEXT_PARAMS['position'], position_offset)),
            cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'], 
            CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

    #######################################################################################################################

    # Convert the image to PyQt compatible format
    def get_pyqt_image(self, image):
        try: height, width, channel = image.shape
        except: height, width = image.shape

        bytes_per_line = 3 * width
        aux = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qt_image = pyqt_g.QImage(aux.data, width, height, bytes_per_line, pyqt_g.QImage.Format_RGB888)
        self.pyqt_image = pyqt_g.QPixmap.fromImage(qt_image)

    #######################################################################################################################

    # Draw the pressed button in the switch controller image
    def draw_button(self, button = ''):
        if not isinstance(button, str): return
        if isinstance(self.FPS_image, type(None)):
            # Without copy() method, images would be linked, meaning that modifying one image would also alter the other
            self.FPS_image = np.copy(self.resized_image)

        self.FPS_image = np.copy(self.resized_image)
        button_coordinates = {
            'A': (307, 80),
            'B': (288, 99),
            'Y': (269, 80),
            'X': (288, 61),
            'HOME': (275, 195),
            'UP': (62, 129),
            'DOWN': (61, 167),
            'RIGHT': (81, 148),
            'LEFT': (43, 148)
        }
        if button in button_coordinates.keys():
            cv2.circle(self.FPS_image, button_coordinates[button], 9, CONST.PRESSED_BUTTON_COLOR, -1)

    #######################################################################################################################

    # Return the requested pixel color. Default: top-left corner pixel
    def get_pixel_color(self, pixel = (20, 20)): return self.original_image[pixel[0]][pixel[1]]

    #######################################################################################################################

    # Return if the pixel is of the specified color
    def check_pixel_color(self, color, pixel = (20, 20)):
        # return all(self.original_image[pixel[0]][pixel[1]] == color)
        differences = [abs(self.original_image[pixel[0]][pixel[1]][color_index] - color[color_index])
            for color_index in range(3)]
        return all(difference <= CONST.PIXEL_COLOR_DIFF_THRESHOLD for difference in differences)

    #######################################################################################################################

    # Return if all the pixels of the specifiead row are of the specified color
    def check_multiple_pixel_colors(self, start, end, color):
        if isinstance(self.FPS_image, type(None)):
            # Without copy() method, images would be linked, meaning that modifying one image would also alter the other
            self.FPS_image = np.copy(self.resized_image)

        match_pixels = True
        for index in range(start[1], end[1]):
            # if all(self.resized_image[-index][start[0]] == color): continue
            differences = [abs(self.resized_image[-index][start[0]][color_index] - color[color_index])
                for color_index in range(3)]
            if all(difference <= CONST.PIXEL_COLOR_DIFF_THRESHOLD for difference in differences): continue
            # If one False is found, there is no need to check the other pixels
            else: match_pixels = False; break

        # Color all the pixels that are being checked
        if CONST.TESTING:
            for index in range(start[1], end[1]): self.FPS_image[-index][start[0]] = CONST.TESTING_COLOR

        return match_pixels

    #######################################################################################################################

    # Read the pokémon name
    def recognize_pokemon(self):
        # Format: [y1:y2, x1:x2]
        # Wild Pokémon: [27:43, 535:650] | Player Pokémon: [y1:y2, x1:x2] | Text Box: [333:365, 50:670]
        name_image = self.resized_image[333:365, 50:670]
        name_image = cv2.cvtColor(name_image, cv2.COLOR_BGR2GRAY)

        # --oem 1: Faster and use less resources
        # --psm 6: Assume a single uniform block of text
        custom_config = '--oem 1 --psm 6'
        text = pytesseract.image_to_string(name_image, config=custom_config)

        # EN: Dialga appeared! | A wild Drifloon appeared! | Go! Chimchar!
        # FR: Dialga apparaît! | Un Baudrive sauvage apparaît! | Ouisticram! Go!
        # ES: ¡Es Dialga! | ¡Ha aparecido un Drifloon salvaje! | ¡Adelante, Chimchar!
        # IT: È apparso Dialga! | Ah! È apparso un Drifloon selvatico! | Avanti, Chimchar!
        # DE: Dialga erscheint! | Ein Driftlon (wild) erscheint! | Los, Panflam!
        # For the KO, ZH-CN and ZH-TW cases, it will return the whole text line
        if CONST.LANGUAGE in ('FR', 'ES', 'EN', 'DE', 'IT'):
            # Replace '¡' and "Go!" for the Spanish and French cases.
            pokemon_name = text
            for part in ['Go!', '¡', '!']: pokemon_name = pokemon_name.replace(part, '')
            pokemon_name = pokemon_name.split(' ')
            for word in pokemon_name[::-1]:
                # Empty spaces ['Ouisticram!', ''] will make it crash
                if word and word[0].isupper():
                    text = word; break
       
        text = text.strip()
        return text

    #######################################################################################################################

    # Save the image
    def save_image(self, pokemon_name = ''):
        file_name = f'{pokemon_name}_{str(int(time()))}' if pokemon_name else str(int(time()))
        self.saved_image_path = f'./{CONST.IMAGES_FOLDER_PATH}{file_name}.png'
        cv2.imwrite(self.saved_image_path, self.original_image)

    #######################################################################################################################

    # Color the specified pixel of the original image
    def replace_pixels(self, pixel_color):
        mask = np.all(self.original_image == pixel_color, axis=-1)
        self.original_image[mask] = CONST.TESTING_COLOR
          
###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    from time import sleep
    from Game_Capture import Game_Capture
   
    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Image Processing'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Process image'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Process video'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '3').replace('{option}', 'Extract frames from video'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '4').replace('{option}', 'Check lost shiny'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Image Processing'))

        menu_options = {
            '1': process_image,
            '2': process_video,
            '3': extract_frames_from_video,
            '4': check_lost_shiny,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Image Processing') + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def process_image(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Image Processing')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Processing image")
            .replace('{path}', f"'../{CONST.TESTING_IMAGE_PATH}'")
        )

        if not os.path.exists(f'../{CONST.TESTING_IMAGE_PATH}'):
            return print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'Image Processing')
                .replace('{path}', f"'../{CONST.TESTING_IMAGE_PATH}'") + '\n'
            )

        image = Image_Processing(f'../{CONST.TESTING_IMAGE_PATH}')
        if isinstance(image.original_image, type(None)): return
        image.resize_image()
        # Linked images: If one image is edited, the other one is too
        image.FPS_image = image.resized_image

        # image.replace_pixels([141, 140, 130])
        # print(image.check_pixel_color())
        # cv2.circle(image.original_image, (20, 20), 9, CONST.PRESSED_BUTTON_COLOR, -1)
        # cv2.rectangle(image.resized_image, (50, 333), (670, 365), (255, 255, 0), 1)
        # print(image.recognize_pokemon())
        # print(image.check_multiple_pixel_colors(
        #     [int(CONST.MAIN_FRAME_SIZE[0] // 16 * 13), int(CONST.MAIN_FRAME_SIZE[1] // 16 * 4)],
        #     [int(CONST.MAIN_FRAME_SIZE[0] // 16 * 13), int(CONST.MAIN_FRAME_SIZE[1] // 16 * 5)],
        #     CONST.SELECTION_BOX_LINE['color']
        # ))

        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'q'")
            .replace('{instruction}', 'exit the program')
        )

        # cv2.imshow(f'{CONST.BOT_NAME} - Resized', image.original_image[0:500])
        cv2.imshow(f'{CONST.BOT_NAME} - Resized', image.resized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the image!') + '\n'
        )

    #######################################################################################################################
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
        print(COLOR_str.PRESS_KEY_TO_INSTRUCTION
            .replace('{module}', 'Image Processing')
            .replace('{key}', "'C'")
            .replace('{instruction}', 'take a screenshot')
        )

        frame_index = 0
        pause = False
        total_video_frames = int(Video_Capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        def process_single_frame(image, frame = None):
            if not isinstance(frame, type(None)): Video_Capture.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame)

            image.original_image = Video_Capture.read_frame()
            # No more frames in the video
            if isinstance(image.original_image, type(None)): return

            image.resize_image()

            cv2.imshow(f'{CONST.BOT_NAME} - Resized', image.resized_image)

        while True:
            if pause:
                # Press 'SPACE' to resume the execution
                # Press 'a' or 'd' to move between frames
                # Press 'q' to stop the program
                key = cv2.waitKey(1)
                if key == ord('q') or key == ord('Q'): break
                elif key == ord(' '): pause = not pause
                elif key == ord('a') or key == ord('A'):
                    if frame_index > 0:
                        frame_index = frame_index - 1
                        process_single_frame(image, frame_index)
                        continue
                elif key == ord('d') or key == ord('D'):
                    if frame_index < total_video_frames:
                        frame_index = frame_index + 1
                        process_single_frame(image, frame_index)
                        continue
                elif key == ord('c') or key == ord('C'):
                    cv2.imwrite(f'../{CONST.SAVING_FRAMES_PATH}/{frame_index}.png', image.original_image)
                    print(COLOR_str.IMAGE_SAVED.replace('{path}', f"'../{CONST.SAVING_FRAMES_PATH}/{frame_index}.png'"))

                # Reduce workload
                sleep(0.05)
                continue

            process_single_frame(image)
            # No more frames in the video
            if isinstance(image.original_image, type(None)): break

            # Press 'SPACE' to pause the execution
            # Press 'q' to stop the program
            key = cv2.waitKey(1)
            if key == ord('q') or key == ord('Q'): break
            if key == ord(' '): pause = not pause

            frame_index += 1
            sleep(0.016)

        Video_Capture.stop()

        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', 'Successfully processed the video!') + '\n'
        )

    #######################################################################################################################
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
            if image.lower().endswith(('.png', '.jpg', 'jpeg'))])

        if not len(images):
            print(COLOR_str.COULD_NOT_LOAD_IMAGES.replace('{path}', f"'../{CONST.IMAGES_FOLDER_PATH}'") + '\n')
            return

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
        timer = time()
        second_text_position = [CONST.TEXT_PARAMS['position'][0], CONST.TEXT_PARAMS['position'][1] + 20]           

        while True and (index) != len(images):
            if time() - timer >= 0.1:
                image = Image_Processing(f'../{CONST.IMAGES_FOLDER_PATH}/{images[index]}')
                image.resize_image()
                cv2.putText(image.resized_image, f'Count: {index + 1}/{len(images)}', CONST.TEXT_PARAMS['position'],
                    cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'],
                    CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)
                cv2.putText(image.resized_image, f'{images[index]}', second_text_position,
                    cv2.FONT_HERSHEY_SIMPLEX, CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'],
                    CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)
                if type(image.resized_image) is not type(None):
                    cv2.imshow(f'{CONST.BOT_NAME} - Lost Shiny Checker', image.resized_image)

                if not pause: index += 1
                timer = time()

            # Press 'SPACE' to resume the execution
            # Press 'a' or 'd' to move between frames
            # Press 'q' to stop the program
            key = cv2.waitKey(1)
            if key in [ord('q'), ord('Q')]: break
            elif key == ord(' '): pause = not pause
            elif pause and key in [ord('a'), ord('A')]: index -= 1
            elif pause and key in [ord('d'), ord('D')]: index += 1

        sleep(1)
        print(COLOR_str.SUCCESS_EXIT_PROGRAM
            .replace('{module}', 'Image Processing')
            .replace('{reason}', f'Successfully checked {index}/{len(images)} images!')
        )

        cv2.destroyAllWindows()
        delete = input(COLOR_str.DELETE_IMAGES_QUESTION)
        if delete.lower().strip() in ('', 'y', 'yes'):
            print(COLOR_str.DELETING_IMAGES.replace('{images}', str(len(images))))
            for image in images: os.remove(f'../{CONST.IMAGES_FOLDER_PATH}/{image}')
            print(COLOR_str.SUCCESSFULLY_DELETED_IMAGES.replace('{images}', str(len(images))) + '\n')

    #######################################################################################################################
    #######################################################################################################################

    main_menu()