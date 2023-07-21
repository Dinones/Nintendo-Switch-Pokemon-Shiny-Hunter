###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__': os.chdir(os.path.dirname(__file__))

from threading import Thread, Timer
from tkinter import filedialog
import tkinter as tk

from PIL import Image, ImageTk
import numpy as np
import queue
import copy
import cv2

from Image_Processing import Image_Processing

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# ↓↓ Define default frame style
frame_style = {
    'background': '#555',
    # ↓↓ Space left between the borders of the frame and the items inside it 
    'bd': 2,
}
# ↓↓ Define default canvas style
canvas_style = {
    'background': '#000',
    'highlightthickness': 0,
}

###########################################################################################################################

# ↓↓ GUI inherits from the class Thread. It will behave like a thread
class GUI(Thread):
    def __init__(self, queue):
        # ↓↓ Initialize the Thread part of the GUI object, so we can use its functions and attributes
        Thread.__init__(self)
        # ↓↓ Kill the thread when the main thread finishes
        self.daemon = True
        self.queue = queue
        self.timer = None

    #######################################################################################################################

    # ↓↓ Overwrite the run() method from thread. This code will be executed when using GUI.start()
    def run(self):
        # ↓↓ Create the GUI
        self.root = tk.Tk()
        # ↓↓ Insert a title
        self.root.title("Pokemon Shiny Hunter")
        # ↓↓ Set the icon for the GUI. It raises an error on Linux systems
        try: root.iconbitmap("../Media/Metal Slime.ico")
        except: pass
        # ↓↓ Set the background color
        self.root.configure(bg='#333')
        # ↓↓ Set the font
        self.root.option_add('*font', ('Arial', 12))
        # ↓↓ Make the size of the window update automatically if a widget is added outside 
        self.root.update_idletasks()
        
        self.items = {
            # ↓↓ Frame created to make the GUI responsive, every widget should be inside of it instead of the root
            'main_frame': tk.Frame(self.root, background='#333'),
            'main_image_frame': None,
            'main_image': {
                'tkinter_image': None,
                'image_id': None,
                'canvas': None,
            },
            'top_right_image_frame': None,
            'top_right_image': {
                'tkinter_image': None,
                'image_id': None,
                'canvas': None,
            },
            'bottom_right_image_frame': None,
            'bottom_right_image': {
                'tkinter_image': None,
                'image_id': None,
                'canvas': None,
            },
        }

        # ↓↓ MAIN FRAME
        self.items['main_frame'].pack(expand=True, padx=0, pady=0)

        # ↓↓ MAIN IMAGE
        self.items['main_image_frame'] = tk.Frame(self.items['main_frame'], **frame_style)
        self.items['main_image_frame'].grid(row=0, column=0, rowspan=5, padx=10, pady=10)
        # ↓↓ Made with canvas to avoid white flashing when moving the slides fast
        self.items['main_image']['canvas'] = tk.Canvas(self.items['main_image_frame'], **canvas_style,
            width=CONST.BOT_WINDOW_SIZE[0], height=CONST.BOT_WINDOW_SIZE[1])
        self.items['main_image']['canvas'].pack()

        # ↓↓ TOP RIGHT IMAGE
        self.items['top_right_image_frame'] = tk.Frame(self.items['main_frame'], **frame_style)
        self.items['top_right_image_frame'].grid(row=0, column=1, rowspan=2, padx=10, pady=70)
        # ↓↓ Made with canvas to avoid white flashing when moving the slides fast
        self.items['top_right_image']['canvas'] = tk.Canvas(self.items['top_right_image_frame'], **canvas_style,
            width=CONST.BOT_WINDOW_SIZE[0]//3, height=CONST.BOT_WINDOW_SIZE[1]//3)
        self.items['top_right_image']['canvas'].pack()

        # ↓↓ BOTTOM RIGHT IMAGE
        self.items['bottom_right_image_frame'] = tk.Frame(self.items['main_frame'], **frame_style)
        self.items['bottom_right_image_frame'].grid(row=2, column=1, rowspan=2, padx=10)
        # ↓↓ Made with canvas to avoid white flashing when moving the slides fast
        self.items['bottom_right_image']['canvas'] = tk.Canvas(self.items['bottom_right_image_frame'], **canvas_style,
            width=CONST.BOT_WINDOW_SIZE[0]//3, height=CONST.BOT_WINDOW_SIZE[1]//3)
        self.items['bottom_right_image']['canvas'].pack()

        self.update_GUI()
        self.root.mainloop()

    #######################################################################################################################

    def update_GUI(self):
        try: image = self.queue.get(block=True)
        except: 
            # ↓↓ Schedule the next update_GUI() call in 10 milliseconds
            self.timer = Timer(0.01, self.update_GUI)
            self.timer.start()
            return
        
        if not self.is_alive(): return
                
        image.get_tkinter_image(image.FPS_image)
        image.get_multiple_tkinter_images()
        # ↓↓ Update the images
        if self.items['main_image']['tkinter_image'] is None:
            self.items['main_image']['image_id'] = self.items['main_image']['canvas'].create_image(0, 0, anchor='nw', image=image.tkinter_image)
            self.items['top_right_image']['image_id'] = self.items['top_right_image']['canvas'].create_image(0, 0, anchor='nw', image=image.top_right_tkinter_image)
            self.items['bottom_right_image']['image_id'] = self.items['bottom_right_image']['canvas'].create_image(0, 0, anchor='nw', image=image.bottom_right_tkinter_image)
        else: 
            self.items['main_image']['canvas'].itemconfig(self.items['main_image']['image_id'], image=str(image.tkinter_image))
            self.items['top_right_image']['canvas'].itemconfig(self.items['top_right_image']['image_id'], image=str(image.top_right_tkinter_image))
            self.items['bottom_right_image']['canvas'].itemconfig(self.items['bottom_right_image']['image_id'], image=str(image.bottom_right_tkinter_image))
        # ↓↓ Avoid white flasing
        self.items['main_image']['tkinter_image'] = image.tkinter_image
        self.items['top_right_image']['tkinter_image'] = image.top_right_tkinter_image
        self.items['bottom_right_image']['tkinter_image'] = image.bottom_right_tkinter_image

        # ↓↓ Schedule the next update_GUI() call in 10 milliseconds
        self.timer = Timer(0.01, self.update_GUI)
        self.timer.start()