###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

from __future__ import annotations

import os
import sys

import PyQt5.QtWidgets as pyqt_w
import PyQt5.QtCore as pyqt_c
import PyQt5.QtGui as pyqt_g

import subprocess
from time import sleep
from queue import Queue
from playsound3 import playsound
from typing import TYPE_CHECKING

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Modules.Colored_Strings as STR
import Constants as CONST

if TYPE_CHECKING:
    from threading import Event

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'GUI'

SHINY_STARS_SOUND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.SHINY_STARS_SOUND_PATH))
SOUND_OFF_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.SOUND_OFF_IMAGE_PATH))
SOUND_ON_IMAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONST.SOUND_ON_IMAGE_PATH))

# Interface widgets configurations
image_label_style = "background-color: #000; border: 1px solid #aaa;"
text_label_style = "background-color: #222; border: 1px solid #aaa;"
text_style = "background-color: #222; border: 1px solid #aaa; color: #aaa; font-size: 13pt; font-family: Arial;"
clock_style = "background-color: #222; border: 1px solid #aaa; color: #aaa; font-size: 30pt; font-family: Arial;"
stop_button_style = """
    QPushButton {background-color: #111; border: 1px solid #aaa; color: #ddd; font-size: 25pt; font-family: Arial;} 
    QPushButton:pressed {background-color: #555; border: 1px solid #fff; color: #fff;}
"""

###########################################################################################################################
###########################################################################################################################

class App(pyqt_w.QApplication):
    def __init__(self):
        # Initialize the class QApplication object
        super().__init__([])

        # Apply a dark background theme to all QWidget elements
        self.setStyleSheet("QWidget { background-color: #333; }")

###########################################################################################################################
###########################################################################################################################

class GUI(pyqt_w.QWidget):

    """
    Main graphical interface for the bot. Displays key info (RAM, CPU, encounter count, etc.) and provides controls like
    stop, toggle sound, and social/media buttons.

    Args:
        queue (Queue): Shared queue used for inter-thread communication.
        shutdown_event (Event): Event used to signal when the app should close.
        stop_event (Event): Event used to signal the bot to stop its main loop.
    """

    def __init__(self, queue: Queue, shutdown_event: Event, stop_event: Event) -> None:
        # Initialize the class QWidget object
        super().__init__()

        # Used to share object between threads
        self.queue = queue

        self.setWindowTitle(CONST.BOT_NAME)

        # Prevent window from being resized
        self.setFixedSize(CONST.BOT_WINDOW_SIZE[0], CONST.BOT_WINDOW_SIZE[1])
        self.setFixedSize(CONST.BOT_WINDOW_SIZE[0], 572)

        # Move the GUI to the middle of the screen
        self.setGeometry(CONST.SPAWN_POSITION[0], CONST.SPAWN_POSITION[1], 0, 0)

        # All widgets stored for easy access
        self.items = {
            'main_image_label': pyqt_w.QLabel(self),
            'clock_label': pyqt_w.QLabel(self),
            'switch_controller_image_label': pyqt_w.QLabel(self),
            'stop_button': pyqt_w.QPushButton(self),
            'music_button': pyqt_w.QPushButton(self),
            'discord_button': pyqt_w.QPushButton(self),
            'github_button': pyqt_w.QPushButton(self),
            'dinones_button': pyqt_w.QPushButton(self),
            'RAM_usage_label': pyqt_w.QLabel(self),
            'CPU_usage_label': pyqt_w.QLabel(self),
            'current_state_label': pyqt_w.QLabel(self),
            'encounter_count_label': pyqt_w.QLabel(self),
        }

        # MAIN IMAGE
        self.items['main_image_label'].setFixedSize(*CONST.MAIN_FRAME_SIZE)
        self.items['main_image_label'].setStyleSheet(image_label_style)
        self.items['main_image_label'].move(10, 10)

        ##### SWITCH CONTROLLER #####
        self.items['switch_controller_image_label'].setFixedSize(*CONST.SWITCH_CONTROLLER_FRAME_SIZE)
        self.items['switch_controller_image_label'].setStyleSheet(image_label_style)
        self.items['switch_controller_image_label'].move(CONST.MAIN_FRAME_SIZE[0] + 20, CONST.CLOCK_FRAME_SIZE[1] + 20)

        ##### TIME COUNTER #####
        self.items['clock_label'].setFixedSize(*CONST.CLOCK_FRAME_SIZE)
        self.items['clock_label'].setStyleSheet(clock_style)
        self.items['clock_label'].move(CONST.MAIN_FRAME_SIZE[0] + 20, 10)
        self.items['clock_label'].setAlignment(pyqt_c.Qt.AlignCenter)
        self.items['clock_label'].setText("00 : 00 : 00")

        ##### STOP BUTTON #####
        self.items['stop_button'].setFixedSize(*CONST.STOP_BUTTON_FRAME_SIZE)
        self.items['stop_button'].setStyleSheet(stop_button_style)
        self.items['stop_button'].move(
            CONST.MAIN_FRAME_SIZE[0] + 20,
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + 30
        )
        self.items['stop_button'].setText("STOP")
        self.items['stop_button'].clicked.connect(stop_event.set)

        ###################################################################################################################
        ###################################################################################################################

        ##### MUSIC BUTTON #####
        def toggle_sound(value, play_activation_sound = True):
            CONST.PLAY_SOUNDS = value

            if CONST.PLAY_SOUNDS: 
                if play_activation_sound:
                    play_sound(SHINY_STARS_SOUND_PATH)
                image = pyqt_g.QIcon(SOUND_ON_IMAGE_PATH)
            else:
                image = pyqt_g.QIcon(SOUND_OFF_IMAGE_PATH)

            if not image.pixmap(2, 2).isNull():
                self.items['music_button'].setText('')
                self.items['music_button'].setIcon(image)
            else:
                print(STR.GUI_COULD_NOT_LOAD_IMAGE.format(
                    path=SOUND_ON_IMAGE_PATH if CONST.PLAY_SOUNDS else SOUND_OFF_IMAGE_PATH
                ))
                self.items['music_button'].setIcon(pyqt_g.QIcon())
                self.items['music_button'].setText("M" if CONST.PLAY_SOUNDS else "!M")

        ###################################################################################################################
        ###################################################################################################################

        self.items['music_button'].setFixedSize(CONST.STOP_BUTTON_FRAME_SIZE[1], CONST.STOP_BUTTON_FRAME_SIZE[1])
        self.items['music_button'].setStyleSheet(stop_button_style)
        self.items['music_button'].setIconSize(
            pyqt_c.QSize(CONST.STOP_BUTTON_FRAME_SIZE[1] - 15, CONST.STOP_BUTTON_FRAME_SIZE[1] - 15)
        )
        self.items['music_button'].move(
            CONST.MAIN_FRAME_SIZE[0] + 20,
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + CONST.STOP_BUTTON_FRAME_SIZE[1] + 41
        )
        self.items['music_button'].clicked.connect(lambda: toggle_sound(not CONST.PLAY_SOUNDS))
        toggle_sound(CONST.PLAY_SOUNDS, play_activation_sound=False)

        ##### DISCORD, GITHUB & DINONES BUTTONS #####
        self._init_social_button('discord_button', CONST.DISCORD_IMAGE_PATH, CONST.DISCORD_URL, x_offset=63)
        self._init_social_button('github_button', CONST.GITHUB_IMAGE_PATH, CONST.GITHUB_URL, x_offset=170)
        self._init_social_button(
            'dinones_button', CONST.DINONES_IMAGE_PATH, CONST.DINONES_URL, x_offset=277, is_square=True
        )
            
        ##### RAM USAGE #####
        self.items['RAM_usage_label'].setFixedSize(*CONST.TEXT_FRAME_SIZE)
        self.items['RAM_usage_label'].setStyleSheet(text_style)
        self.items['RAM_usage_label'].move(10, CONST.MAIN_FRAME_SIZE[1] + 20)
        self.items['RAM_usage_label'].setText("  ★   RAM Usage: 0 MB")

        ##### CPU USAGE #####
        self.items['CPU_usage_label'].setFixedSize(*CONST.TEXT_FRAME_SIZE)
        self.items['CPU_usage_label'].setStyleSheet(text_style)
        self.items['CPU_usage_label'].move(CONST.MAIN_FRAME_SIZE[0]//2 + 15, CONST.MAIN_FRAME_SIZE[1] + 20)
        self.items['CPU_usage_label'].setText("  ★   CPU Usage: 0 %")

        ##### CURRENT STATE #####
        self.items['current_state_label'].setFixedSize(CONST.MAIN_FRAME_SIZE[0], CONST.TEXT_FRAME_SIZE[1])
        self.items['current_state_label'].setStyleSheet(text_style)
        self.items['current_state_label'].move(10, CONST.MAIN_FRAME_SIZE[1] + CONST.TEXT_FRAME_SIZE[1] + 30)
        self.items['current_state_label'].setText("  ★   Current State: None")

        ##### ENCOUNTER COUNT #####
        self.items['encounter_count_label'].setFixedSize(CONST.MAIN_FRAME_SIZE[0], CONST.TEXT_FRAME_SIZE[1])
        self.items['encounter_count_label'].setStyleSheet(text_style)
        self.items['encounter_count_label'].move(10, CONST.MAIN_FRAME_SIZE[1] + 2*CONST.TEXT_FRAME_SIZE[1] + 40)
        self.items['encounter_count_label'].setText("  ★   Encounter Count: 0")

        # QTimer automatically calls the function when finishes the previous execution. Setting it to 16ms provides a
        # maximum of 60FPS to not overload the program
        self.timer = pyqt_c.QTimer(self)
        self.timer.timeout.connect(lambda: self.update_GUI(shutdown_event))
        self.timer.start(16)

        self.show()

    #######################################################################################################################
    #######################################################################################################################

    def _init_social_button(self, name: str, image_path: str, url: str, x_offset: int, is_square: bool = False):

        """
        Helper function to initialize a social/media button with an icon.

        Args:
            name (str): Key in self.items for the button.
            image_path (str): Path to the icon image.
            url (str): URL to open when clicked.
            x_offset (int): Horizontal position offset.
            is_square (bool): Whether the button is square-shaped or rectangular.
        """

        button = self.items[name]
        size = CONST.STOP_BUTTON_FRAME_SIZE[1]

        # Set size depending on whether it's square or rectangular
        button.setFixedSize(size, size) if is_square else button.setFixedSize(97, size)
        button.setStyleSheet(stop_button_style)
        button.setIconSize(pyqt_c.QSize(size - 21, size - 21))
        button.move(
            CONST.MAIN_FRAME_SIZE[0] + 30 + x_offset,
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + size + 41
        )
        button.clicked.connect(lambda: self.open_webpage(url))

        # Load the image
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', image_path))
        image = pyqt_g.QIcon(image_path)

        if not image.pixmap(2, 2).isNull():
            button.setIcon(image)
        else:
            print(STR.GUI_COULD_NOT_LOAD_IMAGE.replace('{path}', image_path))
            button.setText(name.split('_')[0].capitalize())

    #######################################################################################################################
    #######################################################################################################################

    def update_GUI(self, shutdown_event: Event) -> None:

        """
        Updates the GUI based on new data received from the shared queue.

        Args:
            shutdown_event (Event): Event that signals when the GUI should close.
        """

        if shutdown_event.is_set():
            self.close()
            return
        
        try:
            update_items = self.queue.get(block=True, timeout=1)
        except Exception:
            return

        # Convert images to a PyQt compatible format
        update_items['image'].get_pyqt_image(update_items['image'].FPS_image)
        update_items['switch_controller_image'].get_pyqt_image(update_items['switch_controller_image'].FPS_image)

        # Update images
        self.items['main_image_label'].setPixmap(update_items['image'].pyqt_image)
        self.items['switch_controller_image_label'].setPixmap(update_items['switch_controller_image'].pyqt_image)

        # Update elapsed time
        total_seconds = update_items['clock']
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Calculate shiny odds percentage (bad luck chance)
        encounters = update_items['global_encounter_count']
        bad_luck = 100 - ((1 - 1 / 4096) ** encounters * 100 if encounters else 100)

        # Update labels with formatted stats
        self.items['RAM_usage_label'].setText(f"  ★   RAM Usage: {update_items['memory_usage']:.2f} MB")
        self.items['CPU_usage_label'].setText(f"  ★   CPU Usage: {update_items['cpu_usage']:.2f} %")
        self.items['current_state_label'].setText(f"  ★   Current State: {update_items['current_state']}")
        self.items['encounter_count_label'].setText(
            f"  ★   Total Encounter Count: {update_items['global_encounter_count']}" + \
            f"   -   Bad luck: {bad_luck:.2f}%   -   Current Encounter Count: {update_items['local_encounter_count']}"
        )
        self.items['clock_label'].setText(f"{hours:02} : {minutes:02} : {seconds:02}")

    #######################################################################################################################
    #######################################################################################################################
    
    def open_webpage(self, url: str) -> None:
    
        """
        Opens the specified URL in the default system browser as a non-root user.
        
        On Linux, running as root (e.g. via sudo) can prevent GUI applications like browsers from launching. This method
        uses the "SUDO_USER" environment variable to determine the original user and executes "xdg-open" under their
        account.

        Args:
            url (str): The URL to open in the browser.
        """
        # Determine the real user running the program (not root)
        user = os.environ.get('SUDO_USER', os.environ.get('USER'))

        # Run xdg-open under the user's session to avoid permission issues
        subprocess.run(['sudo', '-u', user, 'xdg-open', url], check=False)

###########################################################################################################################
###########################################################################################################################

def play_sound(path: str) -> None:

    """
    Plays a sound from the given path if sound is enabled.

    Suppresses stderr output from the "playsound" library, which prints tons of messages. Temporarily redirects stderr to
    "/dev/null" and restores it afterward.

    Args:
        path (str): Path to the audio file.
    """

    def restore_stderr(original_fd: int, saved_fd: int) -> None:

        """
        Restores the original stderr after redirection.

        Args:
            original_fd (int): File descriptor of the original stderr.
            saved_fd (int): Duplicated file descriptor to restore from.

        Returns:
            None
        """

        sys.stderr.flush()
        os.dup2(saved_fd, original_fd)
        os.close(saved_fd)

    if CONST.PLAY_SOUNDS:
        # Redirect stderr to suppress playsound output
        original_stderr_fd = sys.stderr.fileno()
        saved_stderr_fd = os.dup(original_stderr_fd)
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull_fd, original_stderr_fd)
        os.close(devnull_fd)

        try:
            playsound(path, block=False)
            # Let the async play begin
            sleep(0.1)
        except Exception:
            print(STR.COULD_NOT_PLAY_SOUND.format(module=MODULE_NAME, path=path))
        finally:
            restore_stderr(original_stderr_fd, saved_stderr_fd)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    import Debug.GUI_Debug