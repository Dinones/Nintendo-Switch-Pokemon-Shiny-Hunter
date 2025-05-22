###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import logging
from time import sleep, perf_counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Modules.Game_Capture import Game_Capture
import Modules.Colored_Strings as STR
from Modules.Image_Processing import *
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

LEFT_ARROW_KEY_VALUE = 65361
RIGHT_ARROW_KEY_VALUE = 65363
MODULE_NAME = 'Image Processing'

IMAGES_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.IMAGES_FOLDER_PATH))
TESTING_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.TESTING_IMAGE_PATH))
TESTING_VIDEO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.TESTING_VIDEO_PATH))
FRAMES_OUTPUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.SAVING_FRAMES_PATH))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":

    def main_menu():
        print('\n' + STR.M_MENU.replace('{module}', 'Image Processing'))
        print(STR.M_MENU_OPTION.replace('{index}', '1').replace('{option}', 'Process image'))
        print(STR.M_MENU_OPTION.replace('{index}', '2').replace('{option}', 'Process video'))
        print(STR.M_MENU_OPTION.replace('{index}', '3').replace('{option}', 'Extract frames from video'))
        print(STR.M_MENU_OPTION.replace('{index}', '4').replace('{option}', 'Check lost shiny'))
        print(STR.M_MENU_OPTION.replace('{index}', '5').replace('{option}', 'Test debug video frame'))

        option = input('\n' + STR.M_OPTION_SELECTION.replace('{module}', 'Image Processing'))

        menu_options = {
            '1': process_image,
            '2': process_video,
            '3': extract_frames_from_video,
            '4': check_lost_shiny,
            '5': check_debug_video_frames,
        }

        if option in menu_options: menu_options[option](option)
        else: print(STR.M_INVALID_OPTION.replace('{module}', 'Image Processing') + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def process_image(option: str) -> None:

        """
        Loads, resizes, and displays a test image for visual inspection.

        Args:
            option (str): The menu option index triggering the action.

        Returns:
            None
        """

        print(STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action="Processing image",
            path=TESTING_IMAGE_PATH
        ))

        # Check if the image path is valid
        if not os.path.exists(TESTING_IMAGE_PATH):
            print(STR.G_INVALID_PATH_ERROR.format(module=MODULE_NAME, path=TESTING_IMAGE_PATH))
            return

        # Load the image
        image = Image_Processing(TESTING_IMAGE_PATH)
        if image.original_image is None:
            print(STR.IP_COULD_NOT_LOAD_IMAGE.format(module=MODULE_NAME, path=TESTING_IMAGE_PATH))
            return 

        image.resize_image()
        # FPS image will be used for display (linked to resized version)
        image.FPS_image = image.resized_image

        print(STR.G_PRESS_KEY_TO_INSTRUCTION.format(module=MODULE_NAME, key='any key', instruction='exit the program'))

        # Display the image
        cv2.imshow(f'{CONST.BOT_NAME}', image.FPS_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(STR.G_SUCCESS_EXIT_PROGRAM.format(module=MODULE_NAME, reason='Successfully processed the image!'))

    #######################################################################################################################
    #######################################################################################################################

    def process_video(option: str) -> None:

        """
        Processes a video file frame-by-frame with real-time controls: pause/resume, navigation, and screenshot capture.

        Args:
            option (str): The menu option index triggering the action.

        Returns:
            None
        """

        ###################################################################################################################
        ###################################################################################################################

        def process_single_frame(frame_num: int = None) -> None:
            
            """
            Loads and displays a single frame from the video.

            Args:
                frame_num (int): The index of the frame to load. If None, loads the next sequential frame.

            Returns:
                None
            """

            if frame_num is not None:
                video_capture.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

            image.original_image = video_capture.read_frame()
            if image.original_image is None:
                return

            image.resize_image()
            cv2.imshow(f'{CONST.BOT_NAME} - Resized', image.resized_image)
        
        ###################################################################################################################
        ###################################################################################################################

        print('\n' + STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action="Processing video",
            path=TESTING_VIDEO_PATH
        ))

        if not os.path.exists(TESTING_VIDEO_PATH):
            print(STR.G_INVALID_PATH_ERROR.format(
                module=MODULE_NAME,
                path=TESTING_VIDEO_PATH
            ) + '\n')
            return

        video_capture = Game_Capture(TESTING_VIDEO_PATH)
        image = Image_Processing(video_capture.frame)

        # Instruction prompts
        key_instructions = {
            "'Q'": "exit the program",
            "'SPACE'": "pause/resume the execution",
            "'A'": "move a frame backwards",
            "'D'": "move a frame forward",
            "'C'": "take a screenshot"
        }

        for key, instruction in key_instructions.items():
            print(STR.G_PRESS_KEY_TO_INSTRUCTION.format(module=MODULE_NAME, key=key, instruction=instruction))

        frame_index = 0
        pause = False
        total_frames = int(video_capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        while True:
            if pause:
                key = cv2.waitKeyEx(1)
                if key in [ord('q'), ord('Q')]:
                    break
                elif key == ord(' '):
                    pause = not pause
                elif key in [ord('a'), ord('A'), LEFT_ARROW_KEY_VALUE] and frame_index > 0:
                    frame_index -= 1
                    process_single_frame(frame_index)
                    continue
                elif key in [ord('d'), ord('D'), RIGHT_ARROW_KEY_VALUE] and frame_index < total_frames - 1:
                    frame_index += 1
                    process_single_frame(frame_index)
                    continue
                elif key in [ord('c'), ord('C')]:
                    screenshot_path = os.path.join(FRAMES_OUTPUT_PATH, f"{frame_index}.png")
                    cv2.imwrite(screenshot_path, image.original_image)
                    print(STR.GC_IMAGE_SAVED.format(path=screenshot_path))

                sleep(0.05)
                continue

            process_single_frame()
            if image.original_image is None:
                break

            key = cv2.waitKey(1)
            if key in [ord('q'), ord('Q')]:
                break
            elif key == ord(' '):
                pause = True

            frame_index += 1
            sleep(0.016) # ~60 FPS

        video_capture.stop()

        print(STR.G_SUCCESS_EXIT_PROGRAM.format(module=MODULE_NAME, reason='Successfully processed the video!'))

    #######################################################################################################################
    #######################################################################################################################

    def extract_frames_from_video(option: str) -> None:

        """
        Extracts and saves all frames from the test video to the configured saving directory.

        Args:
            option (str): The menu option index triggering the action.

        Returns:
            None
        """

        print(STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action="Extracting frames into",
            path=FRAMES_OUTPUT_PATH
        ))

        # Validate that input video and output folder exist
        if not os.path.exists(TESTING_VIDEO_PATH) or not os.path.exists(FRAMES_OUTPUT_PATH):
            print(STR.G_INVALID_PATH_ERROR.format(
                module=MODULE_NAME,
                path=f"{TESTING_VIDEO_PATH} or {FRAMES_OUTPUT_PATH}"
            ))
            return

        # Initialize video capture and image processor
        video_capture = Game_Capture(TESTING_VIDEO_PATH)
        image = Image_Processing(video_capture.frame)

        total_frames = int(video_capture.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_index = 0

        while True:
            # Read the next frame
            image.original_image = video_capture.read_frame()

            # No more frames in the video
            if image.original_image is None:
                break

            frame_index += 1
            percentage = int((frame_index) / total_frames * 100)
            # Inefficient? Maybe, but looks cool and doesn't affect the main code
            print(STR.IP_CURRENT_EXTRACTED_FRAMES.format(
                extracted_frame=frame_index,
                total_frames=total_frames,
                percentage=percentage
            ), end='\r', flush=True)

            # Save the image
            frame_filename = os.path.join(FRAMES_OUTPUT_PATH, f"{frame_index}.png")
            cv2.imwrite(frame_filename, image.original_image)

        video_capture.stop()

        print('\n' + STR.IP_SUCCESSFULLY_EXTRACTED_FRAMES.format(frames=frame_index))

    #######################################################################################################################
    #######################################################################################################################

    def check_lost_shiny(option: str) -> None:

        """
        Interactive viewer to manually check saved frames/images, allowing the user to pause, navigate, and optionally
        delete the images after viewing.

        Key Presses:
            - 'q' or 'Q': Quit the image processing loop.
            - ' ' (space): Pause or resume the image processing.
            - 'a', 'A', or Left Arrow: Move to the previous image (when paused).
            - 'd', 'D', or Right Arrow: Move to the next image (when paused).
            - If not paused, images will auto-progress at a configured interval.
        """

        print('\n' + STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action="Checking lost shiny",
            path=""
        ))

        if not os.path.exists(IMAGES_FOLDER_PATH):
            print(STR.G_INVALID_PATH_ERROR.format(
                module=MODULE_NAME,
                path=IMAGES_FOLDER_PATH
            ) + '\n')
            return

        images = sorted(
            [image for image in os.listdir(IMAGES_FOLDER_PATH) if image.lower().endswith(('.png', '.jpg', '.jpeg'))]  
        )

        if not images:
            print(STR.IP_NO_IMAGES_IN_FOLDER.format(path=IMAGES_FOLDER_PATH))
            return

        # Instruction prompts
        key_instructions = {
            "'Q'": "exit the program",
            "'SPACE'": "pause/resume the execution",
            "'A' or '<'": "move a frame backwards",
            "'D' or '>'": "move a frame forward"
        }

        print(STR.IP_SUCCESSFULLY_LOADED_IMAGES.format(images=len(images)))
        for key, instruction in key_instructions.items():
            print(STR.G_PRESS_KEY_TO_INSTRUCTION.format(module=MODULE_NAME, key=key, instruction=instruction))

        index = 0
        cached_index = -1
        # Start paused; if not, first images may be skipped
        pause = True
        second_text_position = [
            CONST.TEXT_PARAMS['position'][0],
            CONST.TEXT_PARAMS['position'][1] + 20
        ]

        while index < len(images):
            iteration_start = perf_counter()

            if index != cached_index:
                img_path = os.path.join(IMAGES_FOLDER_PATH, images[index])
                image = Image_Processing(img_path)
                image.resize_image()

                # Overlay index and filename text
                overlay_texts = [
                    (f'Count: {index + 1}/{len(images)}', CONST.TEXT_PARAMS['position']),
                    (images[index], second_text_position)
                ]

                for text, pos in overlay_texts:
                    cv2.putText(
                        image.resized_image, text, pos,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        CONST.TEXT_PARAMS['font_scale'],
                        CONST.TEXT_PARAMS['font_color'],
                        CONST.TEXT_PARAMS['thickness'],
                        cv2.LINE_AA
                    )

                cv2.imshow(f'{CONST.BOT_NAME} - Lost Shiny Checker', image.resized_image)
                cached_index = index

            remaining_time_ms = int(
                max(0.001, CONST.CHECK_LOST_SHINY_TIME - (perf_counter() - iteration_start)) * 1000
            )
            key = cv2.waitKeyEx(remaining_time_ms)

            if key in [ord('q'), ord('Q')]:
                break
            elif key == ord(' '):
                pause = not pause
            elif pause and key in [ord('a'), ord('A'), LEFT_ARROW_KEY_VALUE]:
                index = max(0, index - 1)
            elif pause and key in [ord('d'), ord('D'), RIGHT_ARROW_KEY_VALUE]:
                index = min(len(images) - 1, index + 1)
            elif not pause:
                index += 1

        sleep(1)

        print(STR.G_SUCCESS_EXIT_PROGRAM.format(
            module=MODULE_NAME,
            reason=f'Successfully checked {index}/{len(images)} images!'
        ))

        cv2.destroyAllWindows()

        delete_images = input(STR.IP_DELETE_IMAGES_QUESTION)
        if delete_images.lower().strip() in ('', 'y', 'yes'):
            print(STR.IP_DELETING_IMAGES.format(images=len(images)))
            for image in images:
                try:
                    os.remove(os.path.join(IMAGES_FOLDER_PATH, image))
                except Exception as e:
                    continue
            print(STR.IP_SUCCESSFULLY_DELETED_IMAGES.format(images=len(images)))

    #######################################################################################################################
    #######################################################################################################################

    def check_debug_video_frames(option: str) -> None:

        """
        Loads a test image and overlays a debug image with sample state and button information.

        Args:
            option (str): The menu option index triggering the action.

        Returns:
            None
        """

        print('\n' + STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action="Testing debug video frame",
            path=""
        ))

        if not os.path.exists(TESTING_IMAGE_PATH):
            print(STR.G_INVALID_PATH_ERROR.format(
                module=MODULE_NAME,
                path=TESTING_IMAGE_PATH
            ))
            return

        # Load test image
        image = Image_Processing(TESTING_IMAGE_PATH)
        if image.original_image is None:
            print(STR.IP_COULD_NOT_LOAD_IMAGE.format(module=MODULE_NAME, path=TESTING_IMAGE_PATH))
            return

        # Ensure it's in BGR format (strip alpha channel)
        if image.original_image.shape[2] == 4:
            image.original_image = cv2.cvtColor(image.original_image, cv2.COLOR_BGRA2BGR)

        image.resize_image()

        # Create and populate debug image
        debug_image = Debug_Image()
        stats = {
            'event': 'STATE_WITH_SUPER_LARGE_NAME',
            'button': 'HOME'
        }
        debug_image.populate_debug_image(stats)

        # Stack the debug and test images vertically
        combined_image = debug_image.stack_images(debug_image.FPS_image, image.resized_image)

        print(STR.G_PRESS_KEY_TO_INSTRUCTION.format(
            module=MODULE_NAME,
            key='any key',
            instruction='exit the program'
        ))

        cv2.imshow(f'{CONST.BOT_NAME} - Debug Frame', combined_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(STR.G_SUCCESS_EXIT_PROGRAM.format(module=MODULE_NAME, reason='Successfully processed the image!'))

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
    print()