###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import PyQt5.QtWidgets as pyqt_w
import PyQt5.QtCore as pyqt_c
import PyQt5.QtGui as pyqt_g

import subprocess
from time import sleep
from queue import Queue
from cllist import dllist
from playsound import playsound

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

image_label_style = "background-color: #000; border: 1px solid #aaa;"
text_label_style = "background-color: #222; border: 1px solid #aaa;"
text_style = "background-color: #222; border: 1px solid #aaa; color: #aaa; font-size: 13pt; font-family: Arial;"
clock_style = "background-color: #222; border: 1px solid #aaa; color: #aaa; font-size: 30pt; font-family: Arial;"
stop_button_style = """
    QPushButton {background-color: #111; border: 1px solid #aaa; color: #ddd; font-size: 25pt; font-family: Arial;} 
    QPushButton:pressed {background-color: #555; border: 1px solid #fff; color: #fff;}
"""

###########################################################################################################################

# Solve Queue memory leaks
class DllistQueue(Queue):
    def _init(self, maxsize):
        self.queue = dllist()

###########################################################################################################################

class App(pyqt_w.QApplication):
    def __init__(self):
        # Initialize the class QApplication object
        super().__init__([])

        self.setStyleSheet("QWidget { background-color: #333; }")

###########################################################################################################################
###########################################################################################################################

class GUI(pyqt_w.QWidget):
    def __init__(self, queue, shutdown_event, stop_event):
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
         
        ##### MAIN IMAGE #####
        self.items['main_image_label'].setFixedSize(CONST.MAIN_FRAME_SIZE[0], CONST.MAIN_FRAME_SIZE[1])
        self.items['main_image_label'].setStyleSheet(image_label_style)
        self.items['main_image_label'].move(10, 10)

        ##### SWITCH CONTROLLER #####
        self.items['switch_controller_image_label'] \
            .setFixedSize(CONST.SWITCH_CONTROLLER_FRAME_SIZE[0], CONST.SWITCH_CONTROLLER_FRAME_SIZE[1])
        self.items['switch_controller_image_label'].setStyleSheet(image_label_style)
        self.items['switch_controller_image_label'].move(CONST.MAIN_FRAME_SIZE[0] + 20, CONST.CLOCK_FRAME_SIZE[1] + 20)

        ##### TIME COUNTER #####
        self.items['clock_label'].setFixedSize(CONST.CLOCK_FRAME_SIZE[0], CONST.CLOCK_FRAME_SIZE[1])
        self.items['clock_label'].setStyleSheet(clock_style)
        self.items['clock_label'].move(CONST.MAIN_FRAME_SIZE[0] + 20, 10)
        self.items['clock_label'].setAlignment(pyqt_c.Qt.AlignCenter)
        self.items['clock_label'].setText("00 : 00 : 00")

        ##### STOP BUTTON #####
        self.items['stop_button'].setFixedSize(CONST.STOP_BUTTON_FRAME_SIZE[0], CONST.STOP_BUTTON_FRAME_SIZE[1])
        self.items['stop_button'].setStyleSheet(stop_button_style)
        self.items['stop_button'].move(CONST.MAIN_FRAME_SIZE[0] + 20, 
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + 30)
        self.items['stop_button'].setText("STOP")
        self.items['stop_button'].clicked.connect(stop_event.set)

        ##### MUSIC BUTTON #####
        def toggle_sound(value, play_activation_sound = True):
            # I'm editing the value of a constant. I know, I deserve to die!
            CONST.PLAY_SOUNDS = value
            
            relative_path = '..' if __name__ == "__main__" else '.'
            if CONST.PLAY_SOUNDS: 
                if play_activation_sound:
                    shiny_sound = relative_path + f'/{CONST.SHINY_STARS_SOUND_PATH}'
                    play_sound(shiny_sound)
                relative_path += f'/{CONST.SOUND_ON_IMAGE_PATH}'
            else: relative_path += f'/{CONST.SOUND_OFF_IMAGE_PATH}'
            image = pyqt_g.QIcon(relative_path)

            if not image.pixmap(2, 2).isNull(): 
                self.items['music_button'].setText('')
                self.items['music_button'].setIcon(image)
            else: 
                print(COLOR_str.COULD_NOT_LOAD_IMAGE.replace('{path}', relative_path))
                self.items['music_button'].setIcon(pyqt_g.QIcon())
                self.items['music_button'].setText("M" if CONST.PLAY_SOUNDS else "!M")

        self.items['music_button'].setFixedSize(CONST.STOP_BUTTON_FRAME_SIZE[1], CONST.STOP_BUTTON_FRAME_SIZE[1])
        self.items['music_button'].setStyleSheet(stop_button_style)
        self.items['music_button'].setIconSize(
            pyqt_c.QSize(CONST.STOP_BUTTON_FRAME_SIZE[1] - 15, CONST.STOP_BUTTON_FRAME_SIZE[1] - 15))
        self.items['music_button'].move(CONST.MAIN_FRAME_SIZE[0] + 20, 
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + CONST.STOP_BUTTON_FRAME_SIZE[1] + 41)
        self.items['music_button'].clicked.connect(lambda: toggle_sound(not CONST.PLAY_SOUNDS))
        toggle_sound(CONST.PLAY_SOUNDS, play_activation_sound = False)

        ##### DISCORD BUTTON #####
        self.items['discord_button'].setFixedSize(97, CONST.STOP_BUTTON_FRAME_SIZE[1])
        self.items['discord_button'].setStyleSheet(stop_button_style)
        self.items['discord_button'].setIconSize(
            pyqt_c.QSize(CONST.STOP_BUTTON_FRAME_SIZE[1] - 21, CONST.STOP_BUTTON_FRAME_SIZE[1] - 21))
        self.items['discord_button'].move(CONST.MAIN_FRAME_SIZE[0] + 30 + 63, 
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + CONST.STOP_BUTTON_FRAME_SIZE[1] + 41)
        self.items['discord_button'].clicked.connect(lambda: self.open_webpage(CONST.DISCORD_URL))

        relative_path = '..' if __name__ == "__main__" else '.'
        relative_path += f'/{CONST.DISCORD_IMAGE_PATH}'
        image = pyqt_g.QIcon(relative_path)
        if not image.pixmap(2, 2).isNull(): self.items['discord_button'].setIcon(image)
        else: 
            print(COLOR_str.COULD_NOT_LOAD_IMAGE.replace('{path}', relative_path))
            self.items['discord_button'].setText("Discord")

        ##### GITHUB BUTTON #####
        self.items['github_button'].setFixedSize(97, CONST.STOP_BUTTON_FRAME_SIZE[1])
        self.items['github_button'].setStyleSheet(stop_button_style)
        self.items['github_button'].setIconSize(
            pyqt_c.QSize(CONST.STOP_BUTTON_FRAME_SIZE[1] - 21, CONST.STOP_BUTTON_FRAME_SIZE[1] - 21))
        self.items['github_button'].move(CONST.MAIN_FRAME_SIZE[0] + 40 + 160, 
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + CONST.STOP_BUTTON_FRAME_SIZE[1] + 41)
        self.items['github_button'].clicked.connect(lambda: self.open_webpage(CONST.GITHUB_URL))

        relative_path = '..' if __name__ == "__main__" else '.'
        relative_path += f'/{CONST.GITHUB_IMAGE_PATH}'
        image = pyqt_g.QIcon(relative_path)
        if not image.pixmap(2, 2).isNull(): self.items['github_button'].setIcon(image)
        else: 
            print(COLOR_str.COULD_NOT_LOAD_IMAGE.replace('{path}', relative_path))
            self.items['github_button'].setText("GitHub")

        ##### LOGO BUTTON #####
        self.items['dinones_button'].setFixedSize(CONST.STOP_BUTTON_FRAME_SIZE[1], CONST.STOP_BUTTON_FRAME_SIZE[1])
        self.items['dinones_button'].setStyleSheet(stop_button_style)
        self.items['dinones_button'].setIconSize(
            pyqt_c.QSize(CONST.STOP_BUTTON_FRAME_SIZE[1] - 25, CONST.STOP_BUTTON_FRAME_SIZE[1] - 25))
        self.items['dinones_button'].move(CONST.MAIN_FRAME_SIZE[0] + 50 + 257, 
            CONST.CLOCK_FRAME_SIZE[1] + CONST.SWITCH_CONTROLLER_FRAME_SIZE[1] + CONST.STOP_BUTTON_FRAME_SIZE[1] + 41)
        self.items['dinones_button'].clicked.connect(lambda: self.open_webpage(CONST.DINONES_URL))
        
        relative_path = '..' if __name__ == "__main__" else '.'
        relative_path += f'/{CONST.DINONES_IMAGE_PATH}'
        image = pyqt_g.QIcon(relative_path)
        if not image.pixmap(2, 2).isNull(): self.items['dinones_button'].setIcon(image)
        else: 
            print(COLOR_str.COULD_NOT_LOAD_IMAGE.replace('{path}', relative_path))
            self.items['dinones_button'].setText("D")
            
        ##### RAM USAGE #####
        self.items['RAM_usage_label'].setFixedSize(CONST.TEXT_FRAME_SIZE[0], CONST.TEXT_FRAME_SIZE[1])
        self.items['RAM_usage_label'].setStyleSheet(text_style)
        self.items['RAM_usage_label'].move(10, CONST.MAIN_FRAME_SIZE[1] + 20)
        self.items['RAM_usage_label'].setText("  ★   RAM Usage: 0 MB")

        ##### CPU USAGE #####
        self.items['CPU_usage_label'].setFixedSize(CONST.TEXT_FRAME_SIZE[0], CONST.TEXT_FRAME_SIZE[1])
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

        # QTimer automatically calls the function when finishes the previous execution
        self.timer = pyqt_c.QTimer(self)
        self.timer.timeout.connect(lambda: self.update_GUI(shutdown_event))
        # Setting it to 16ms provides a maximum of 60FPS to not overload the program
        self.timer.start(16)

        self.show()

    #######################################################################################################################
    #######################################################################################################################

    def update_GUI(self, shutdown_event):
        if shutdown_event.is_set(): self.close()
        try: update_items = self.queue.get(block=True, timeout=1)
        except: return

        # Convert images to a PyQt compatible format
        update_items['image'].get_pyqt_image(update_items['image'].FPS_image)
        update_items['switch_controller_image'].get_pyqt_image(update_items['switch_controller_image'].FPS_image)

        # Update images
        self.items['main_image_label'].setPixmap(update_items['image'].pyqt_image)
        self.items['switch_controller_image_label'].setPixmap(update_items['switch_controller_image'].pyqt_image)

        # Update text boxes
        bad_luck = (1 - 1/4096)**update_items['global_encounter_count']*100 if \
            update_items['global_encounter_count'] else 100
        hours = update_items['clock']//3600
        minutes = (update_items['clock'] - hours*3600)//60
        seconds = update_items['clock'] - hours*3600 - minutes*60

        self.items['RAM_usage_label'].setText(f"  ★   RAM Usage: {update_items['memory_usage']:.2f} MB")
        self.items['CPU_usage_label'].setText(f"  ★   CPU Usage: {update_items['cpu_usage']:.2f} %")
        self.items['current_state_label'].setText(f"  ★   Current State: {update_items['current_state']}")
        self.items['encounter_count_label'].setText(f"  ★   Encounter Count: {update_items['global_encounter_count']}" + \
            f"   -   ({bad_luck:.2f}%)   -   {update_items['local_encounter_count']}")
        self.items['clock_label'].setText(f"{hours:02} : {minutes:02} : {seconds:02}")

    #######################################################################################################################
    #######################################################################################################################


    def open_webpage(self, url): 
        # Linux can't open browsers as sudo for security reasons
        user = os.environ.get('SUDO_USER', os.environ['USER'])
        subprocess.run(f"sudo -u {user} xdg-open {url}", shell=True)

###########################################################################################################################
###########################################################################################################################

def play_sound(path): 
    def restore_std(original_stderr_fd, saved_stderr_fd):
        sys.stderr.flush()
        os.dup2(saved_stderr_fd, original_stderr_fd)

    if CONST.PLAY_SOUNDS:
        # Disable playsound messages. It prints SO MANY of logging messages
        original_stderr_fd = sys.stderr.fileno()
        saved_stderr_fd = os.dup(original_stderr_fd)
        devnull = os.open(os.devnull, os.O_WRONLY)
        sys.stderr.flush()
        os.dup2(devnull, sys.stderr.fileno())

        try: playsound(path, block=False)
        except: 
            sleep(0.1)
            restore_std(original_stderr_fd, saved_stderr_fd)
            print(COLOR_str.COULD_NOT_PLAY_SOUND
                .replace('{module}', 'Shiny Hunter')
                .replace('{path}', path)
            )
        else: 
            sleep(0.1)
            restore_std(original_stderr_fd, saved_stderr_fd)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    import time
    from threading import Thread, Event

    import Colored_Strings as COLOR_str
    from FPS_Counter import FPS_Counter
    from Game_Capture import Game_Capture
    from Image_Processing import Image_Processing

    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'GUI'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Open GUI using capture card'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Open GUI using a template image'))

        # option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'GUI'))
        option = '2'

        menu_options = {
            '1': test_GUI_capture_card,
            '2': test_GUI_template_image,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'GUI') + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def test_GUI_capture_card(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'GUI')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Testing GUI with the capture card...")
            .replace('{path}', '')
        )

        FPS = FPS_Counter()
        initial_time = time.time()
        Image_Queue = DllistQueue(maxsize = 2)
        shutdown_event = Event()

        switch_controller_image = Image_Processing(f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}')
        if isinstance(switch_controller_image.original_image, type(None)):
            print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'GUI')
                .replace('{path}', f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}') + '\n'
            )
            return
        switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
        switch_controller_image.draw_button()

        def test_GUI_control(shutdown_event):
            Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
            if not Video_Capture.video_capture.isOpened(): 
                Video_Capture.stop()
                print(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'"))
                shutdown_event.set()
                return

            while not shutdown_event.is_set():
                image = Image_Processing(Video_Capture.read_frame())
                if isinstance(image.original_image, type(None)): 
                    if Video_Capture.skipped_frames < CONST.SKIPPED_FRAMES_TO_RECONNECT - 1: 
                        Video_Capture.skipped_frames += 1
                        time.sleep(0.1); continue
                    Video_Capture.stop()
                    Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
                    if not Video_Capture.video_capture.isOpened(): 
                        Video_Capture.stop()
                        print(COLOR_str.INVALID_VIDEO_CAPTURE.replace('{video_capture}', f"'{CONST.VIDEO_CAPTURE_INDEX}'"))
                        shutdown_event.set()
                    continue

                image.resize_image()
                FPS.get_FPS()
                image.draw_FPS(FPS.FPS)

                update_items = {
                    'image': image,
                    'current_state': 'TESTING',
                    'shutdown_event': shutdown_event,
                    'global_encounter_count': 0,
                    'local_encounter_count': 0,
                    'memory_usage': FPS.memory_usage,
                    'switch_controller_image': switch_controller_image,
                    'clock': int(time.time() - initial_time),
                }

                Image_Queue.put(update_items)

        threads = []
        threads.append(Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True))
        for thread in threads: thread.start()

        GUI_App = App()
        gui = GUI(Image_Queue, shutdown_event, shutdown_event)
        # Blocking function until the GUI is closed
        GUI_App.exec_()

        shutdown_event.set()
        print(COLOR_str.RELEASING_THREADS.replace('{module}', 'GUI').replace('{threads}', str(len(threads))) + '\n')        

    #######################################################################################################################
    #######################################################################################################################

    def test_GUI_template_image(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'GUI')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Testing GUI using a template image...")
            .replace('{path}', '')
        )

        FPS = FPS_Counter()
        initial_time = time.time()
        Image_Queue = DllistQueue(maxsize = 2)
        shutdown_event = Event()

        switch_controller_image = Image_Processing(f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}')
        if isinstance(switch_controller_image.original_image, type(None)):
            print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'GUI')
                .replace('{path}', f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}') + '\n'
            )
            return
        switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
        switch_controller_image.draw_button()

        image = Image_Processing(f'../{CONST.TEMPLATE_IMAGE_PATH}')
        if isinstance(image.original_image, type(None)):
            print(COLOR_str.INVALID_PATH_ERROR
                .replace('{module}', 'GUI')
                .replace('{path}', f'../{CONST.TEMPLATE_IMAGE_PATH}') + '\n'
            )
            return
        image.resize_image()

        def test_GUI_control(shutdown_event):
            while not shutdown_event.is_set():
                FPS.get_FPS()
                image.draw_FPS(FPS.FPS)

                update_items = {
                    'image': image,
                    'current_state': 'TESTING',
                    'shutdown_event': shutdown_event,
                    'global_encounter_count': 0,
                    'local_encounter_count': 0,
                    'memory_usage': FPS.memory_usage,
                    'cpu_usage': FPS.cpu_usage,
                    'switch_controller_image': switch_controller_image,
                    'clock': int(time.time() - initial_time),
                }

                Image_Queue.put(update_items)

        threads = []
        threads.append(Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True))
        for thread in threads: thread.start()

        GUI_App = App()
        gui = GUI(Image_Queue, shutdown_event, shutdown_event)
        # Blocking function until the GUI is closed
        GUI_App.exec_()

        shutdown_event.set()
        print(COLOR_str.RELEASING_THREADS.replace('{module}', 'GUI').replace('{threads}', str(len(threads))) + '\n')        

    #######################################################################################################################
    #######################################################################################################################

    main_menu()