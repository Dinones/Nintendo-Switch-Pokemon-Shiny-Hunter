###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import cv2
import numpy as np
from datetime import datetime
from typing import Optional, List, Union, Tuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Modules.Colored_Strings as STR
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# Disable warning messages
cv2.setLogLevel(0)

OUTPUT_VIDEO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.OUTPUT_VIDEO_PATH))

###########################################################################################################################
###########################################################################################################################

class Game_Capture():
    def __init__(self, video_capture_index = CONST.VIDEO_CAPTURE_INDEX):

        """
        Initializes the video capture device with the specified index. If the device is not available, it automatically
        tries to use the first available capture card.

        Args:
            video_capture_index (int): Index of the video capture device to use.
        """

        # Initialize the main video capture
        self.video_capture = cv2.VideoCapture(video_capture_index)

        # Use MJPEG codec to improve FPS (if supported by device)
        self.video_capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

        # If the capture couldn't be opened, try another available capture card
        if not self.video_capture.isOpened():
            video_captures = self.find_available_video_captures()
            # If no other devices are found
            if not any(video_captures):
                return

            self.video_capture.release()
            first_available_capture_card = video_captures.index(True)
            self.video_capture = cv2.VideoCapture(first_available_capture_card)

            print(
                STR.GC_USING_DIFFERENT_CAPTURE_CARD.format(
                    old_video_capture = str(video_capture_index),
                    new_video_capture = str(first_available_capture_card)
                )
            )

        # Set fixed resolution
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, CONST.ORIGINAL_FRAME_SIZE[0])
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CONST.ORIGINAL_FRAME_SIZE[1])

        self.video_recorder = None
        self.frame = None
        self.previous_frame_skipped = False
        self.connection_error_image = None

    #######################################################################################################################
    #######################################################################################################################

    def read_frame(self) -> Optional[np.ndarray]:

        """
        Captures a single frame from the video capture device.

        Returns:
            Optional[np.ndarray]: The captured frame if successful, otherwise None.
        """

        success, self.frame = self.video_capture.read()

        # If frame capture fails, generate a black frame with a connection error message
        if not success:
            self._get_connection_error_image()
            # Try to initialize the capture card again
            self.__init__()
        elif self.previous_frame_skipped:
            self.previous_frame_skipped = False

        return self.frame

    #######################################################################################################################
    #######################################################################################################################

    def stop(self) -> None:

        """
        Releases the video capture device and closes any OpenCV windows. This should be called when the video processing is
        finished to free up system resources.
        """

        self.video_capture.release()
        cv2.destroyAllWindows()

    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def find_available_video_captures() -> List[bool]:

        """
        Scans and returns a list indicating which video capture devices are available.

        Returns:
            List[bool]: A list of booleans where each element corresponds to whether the capture device at that index is
                available (True) or not (False).
        """

        video_captures = []

        for index in range(CONST.MAX_VIDEO_DEVICES_ANALIZED):
            video_capture = cv2.VideoCapture(index)
            video_captures.append(video_capture.isOpened())
            video_capture.release()

        return video_captures   

    #######################################################################################################################
    #######################################################################################################################

    def start_recording(self) -> None:

        """
        Initializes the video recorder if recording is enabled in the configuration. Depending on debug mode, it adjusts
        the output frame size to include extra debug UI height.
        """

        if CONST.ENABLE_VIDEO_RECORDING:
            # Determine the frame size depending on debug mode
            if CONST.DEBUG_VIDEO:
                frame_size = (
                    CONST.MAIN_FRAME_SIZE[0],
                    CONST.MAIN_FRAME_SIZE[1] + CONST.DEBUG_FRAME_SIZE[1]
                )
            else:
                frame_size = CONST.ORIGINAL_FRAME_SIZE

            # Initialize the video writer with XVID codec
            self.video_recorder = cv2.VideoWriter(
                OUTPUT_VIDEO_PATH, cv2.VideoWriter_fourcc(*'XVID'), CONST.VIDEO_FPS, frame_size
            )

    #######################################################################################################################
    #######################################################################################################################

    def save_video(self, special_name: str = '') -> None:

        """
        Saves the current video recording by releasing the video writer and renaming the file if a special name is
        provided.

        Args:
            special_name (str): Optional custom filename (without extension) for the saved video. If not provided, the
                default output filename remains unchanged.
        """

        if CONST.ENABLE_VIDEO_RECORDING:
            self.video_recorder.release()

            try:
                if special_name:
                    new_video_path = os.path.abspath(os.path.join(
                        os.path.dirname(__file__),
                        '..',
                        f"{'/'.join(CONST.OUTPUT_VIDEO_PATH.split('/')[:-1])}/{special_name}.avi"
                    ))
                    print(new_video_path)
                    os.rename(OUTPUT_VIDEO_PATH, new_video_path)
            except Exception:
                pass

    #######################################################################################################################
    #######################################################################################################################

    def add_frame_to_video(self, image: Union[np.ndarray, None]) -> None:

        """
        Adds a frame to the current video recording. If recording is enabled but not yet initialized, it starts recording
        first.

        Args:
            image (Union[np.ndarray, None]): The frame to write to the video. Must match the initialized frame size and
                color format (BGR).
        """

        if CONST.ENABLE_VIDEO_RECORDING:
            # Start recording if not already initialized
            if self.video_recorder is None:
                self.start_recording()

            self.video_recorder.write(image)

    #######################################################################################################################
    #######################################################################################################################

    def _get_connection_error_image(self) -> None:

        """
        Create a black frame with the "Capture card disconnected. Please, reconnect it..." message.

        Args:
            position_offset (Tuple[int, int]): (x, y) offset added to the default position.

        Returns:
            None
        """

        if self.connection_error_image is None:
            # Create a black image
            self.connection_error_image = np.zeros(
                (CONST.ORIGINAL_FRAME_SIZE[1], CONST.ORIGINAL_FRAME_SIZE[0], 3), dtype=np.uint8
            )

            # Compute the final position by adapting it to the CONST.ORIGINAL_FRAME_SIZE
            position = tuple(
                a + b for a, b in zip(CONST.TEXT_PARAMS['position'],
                    (0, (CONST.ORIGINAL_FRAME_SIZE[0] * 100) // 1920))
            )

            # Draw the text on the black image adapting its size to the CONST.ORIGINAL_FRAME_SIZE
            cv2.putText(
                self.connection_error_image,
                "Capture card disconnected. Please, reconnect it...",
                position,
                cv2.FONT_HERSHEY_SIMPLEX,
                (CONST.ORIGINAL_FRAME_SIZE[0] * 2) / 1920,
                CONST.TEXT_PARAMS['font_color'],
                (CONST.ORIGINAL_FRAME_SIZE[0] * 5) // 1920,
                cv2.LINE_AA
            )

        self.frame = np.copy(self.connection_error_image)

        if not self.previous_frame_skipped:
            print(STR.GC_CAPTURE_CARD_LOST_CONNECTION.format(time = datetime.now().strftime("%H:%M:%S")))
            self.previous_frame_skipped = True

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

