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

from queue import Queue
from cllist import dllist
from threading import Timer
from time import sleep, time

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

image_label_style = "background-color: #000; border: 1px solid #aaa;"
text_label_style = "background-color: #222; border: 1px solid #aaa;"
text_style = "background-color: #222; border: 1px solid #aaa; color: #aaa; font-size: 13pt; font-family: Arial;"

###########################################################################################################################

# Solve Queue memory leaks
class DllistQueue(Queue):
    def _init(self, maxsize):
        self.queue = dllist()

###########################################################################################################################

class App(pyqt_w.QApplication):
    def __init__(self):
        # Initializes the clas a QApplication object
        super().__init__([])

        self.setStyleSheet("QWidget { background-color: #333; }")

###########################################################################################################################

class GUI(pyqt_w.QWidget):
    def __init__(self, queue):
        # Initializes the clas a QWidget object
        super().__init__()

        # Used to share object between threads
        self.queue = queue
        self.timer = None

        self.setWindowTitle(CONST.BOT_NAME)
        # Prevent window from being resized
        self.setFixedSize(CONST.BOT_WINDOW_SIZE[0], CONST.BOT_WINDOW_SIZE[1])
        # Move the GUI to the middle of the screen
        self.setGeometry(CONST.SPAWN_POSITION[0], CONST.SPAWN_POSITION[1], 0, 0)

        self.items = {
            'main_image_label': pyqt_w.QLabel(self),
            'mask_image_label': pyqt_w.QLabel(self),
            'contours_image_label': pyqt_w.QLabel(self),
            'switch_controller_image_label': pyqt_w.QLabel(self),

            'RAM_usage_label': pyqt_w.QLabel(self),
            'current_state_label': pyqt_w.QLabel(self),
            'encounter_count_label': pyqt_w.QLabel(self),
        }
         
        ##### MAIN IMAGE #####
        self.items['main_image_label'].setFixedSize(CONST.MAIN_FRAME_SIZE[0], CONST.MAIN_FRAME_SIZE[1])
        self.items['main_image_label'].setStyleSheet(image_label_style)
        self.items['main_image_label'].move(10, 10)

        ##### RIGHT TOP IMAGE #####
        self.items['mask_image_label'].setFixedSize(CONST.SECONDARY_FRAME_SIZE[0], CONST.SECONDARY_FRAME_SIZE[1])
        self.items['mask_image_label'].setStyleSheet(image_label_style)
        self.items['mask_image_label'].move(CONST.MAIN_FRAME_SIZE[0] + 20, 10)

        ##### RIGHT BOTTOM IMAGE #####
        self.items['contours_image_label'].setFixedSize(CONST.SECONDARY_FRAME_SIZE[0], CONST.SECONDARY_FRAME_SIZE[1])
        self.items['contours_image_label'].setStyleSheet(image_label_style)
        self.items['contours_image_label'].move(CONST.MAIN_FRAME_SIZE[0] + 20, CONST.SECONDARY_FRAME_SIZE[1] + 21)

        ##### SWITCH CONTROLLER #####
        self.items['switch_controller_image_label'] \
            .setFixedSize(CONST.SWITCH_CONTROLLER_FRAME_SIZE[0], CONST.SWITCH_CONTROLLER_FRAME_SIZE[1])
        self.items['switch_controller_image_label'].setStyleSheet(image_label_style)
        self.items['switch_controller_image_label'].move(CONST.MAIN_FRAME_SIZE[0] + 20, CONST.MAIN_FRAME_SIZE[1] + 20)

        ##### RAM USAGE #####
        self.items['RAM_usage_label'].setFixedSize(2*CONST.MAIN_FRAME_SIZE[0]//3 - 10, CONST.SECONDARY_FRAME_SIZE[1]//5)
        self.items['RAM_usage_label'].setStyleSheet(text_style)
        self.items['RAM_usage_label'].move(10, CONST.MAIN_FRAME_SIZE[1] + 20)
        self.items['RAM_usage_label'].setText("  ★   RAM Usage: 0 MB")

        ##### CURRENT STATE #####
        self.items['current_state_label'].setFixedSize(2*CONST.MAIN_FRAME_SIZE[0]//3 - 10, CONST.SECONDARY_FRAME_SIZE[1]//5)
        self.items['current_state_label'].setStyleSheet(text_style)
        self.items['current_state_label'].move(10, CONST.MAIN_FRAME_SIZE[1] + CONST.SECONDARY_FRAME_SIZE[1]//5 + 30)
        self.items['current_state_label'].setText("  ★   Current State: None")

        ##### ENCOUNTER COUNT #####
        self.items['encounter_count_label'].setFixedSize(2*CONST.MAIN_FRAME_SIZE[0]//3 - 10, CONST.SECONDARY_FRAME_SIZE[1]//5)
        self.items['encounter_count_label'].setStyleSheet(text_style)
        self.items['encounter_count_label'].move(10, CONST.MAIN_FRAME_SIZE[1] + 2*CONST.SECONDARY_FRAME_SIZE[1]//5 + 40)
        self.items['encounter_count_label'].setText("  ★   Encounter Count: 0")

        self.timer = pyqt_c.QTimer(self)
        self.timer.timeout.connect(self.update_GUI)
        self.timer.start(16)

        # self.update_GUI()
        self.show()

    #######################################################################################################################

    def update_GUI(self):
        try: update_items = self.queue.get(block=True, timeout=1)
        except: 
            print('hello')
            # Schedule the next update_GUI() call (Max FPS: 60)
            # self.timer = Timer(0.016, self.update_GUI)
            # self.timer.start()
            return

        # GUI has been closed
        # if pyqt_g.QGuiApplication.instance() is None: return

        # Convert images to a PyQt compatible format
        update_items['image'].get_pyqt_images(['FPS_image', 'masked_image', 'contours_image'])
        update_items['switch_controller_image'].pyqt_images['switch_controller_image'] = \
            update_items['switch_controller_image'].get_pyqt_image(update_items['switch_controller_image'].contours_image)

        # Update images
        self.items['main_image_label'].setPixmap(update_items['image'].pyqt_images['FPS_image'])
        self.items['mask_image_label'].setPixmap(update_items['image'].pyqt_images['masked_image'])
        self.items['contours_image_label'].setPixmap(update_items['image'].pyqt_images['contours_image'])
        self.items['switch_controller_image_label'] \
            .setPixmap(update_items['switch_controller_image'].pyqt_images['switch_controller_image'])

        bad_luck = (1 - 1/4096)**update_items['encounter_count']
        # Update text boxes
        self.items['RAM_usage_label'].setText(f"  ★   RAM Usage: {update_items['memory_usage']:.2f} MB")
        self.items['current_state_label'].setText(f"  ★   Current State: {update_items['current_state']}")
        self.items['encounter_count_label'].setText(f"  ★   Encounter Count: {update_items['encounter_count']}" + \
            f'   -   ({bad_luck:.2f})%')

        # Schedule the next update_GUI() call (Max FPS: 60)
        # self.timer = Timer(0.016, self.update_GUI)
        # self.timer.start()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    from threading import Thread, Event

    import Colored_Strings as COLOR_str
    from FPS_Counter import FPS_Counter
    from Game_Capture import Game_Capture
    from Image_Processing import Image_Processing

    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'GUI'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Open GUI using capture card'))

        # option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'GUI'))
        option = '1'

        menu_options = {
            '1': test_GUI,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'GUI') + '\n')

    #######################################################################################################################

    def test_GUI(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'GUI')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Testing GUI with the capture card...")
            .replace('{path}', '')
        )

        FPS = FPS_Counter()
        Image_Queue = DllistQueue(maxsize = 2)
        shutdown_event = Event()
        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)

        switch_controller_image = Image_Processing(f'../{CONST.SWITCH_CONTROLLER_IMAGE_PATH}')
        switch_controller_image.resize_image(CONST.SWITCH_CONTROLLER_FRAME_SIZE)
        switch_controller_image.draw_button()

        def test_GUI_control(shutdown_event = None):
            if isinstance(shutdown_event, type(None)): return

            while not shutdown_event.is_set():
                image = Image_Processing(Video_Capture.read_frame())
                if isinstance(image.original_image, type(None)): continue

                image.resize_image()
                FPS.get_FPS()
                image.draw_FPS(FPS.FPS)
                image.get_mask()
                n_contours = image.get_rectangles()

                update_items = {
                    'image': image,
                    'current_state': None,
                    'shutdown_event': shutdown_event,
                    'encounter_count': 0,
                    'memory_usage': FPS.memory_usage,
                    'switch_controller_image': switch_controller_image,
                }

                Image_Queue.put(update_items)

        threads = []
        threads.append(Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True))
        for thread in threads: thread.start()

        GUI_App = App()
        gui = GUI(Image_Queue)
        # Blocking function until the GUI is closed
        GUI_App.exec_()

        # Kill all secondary threads
        shutdown_event.set()
        print(COLOR_str.RELEASING_THREADS.replace('{module}', 'GUI').replace('{threads}', str(len(threads))) + '\n')        

    #######################################################################################################################

    main_menu()