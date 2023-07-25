###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__': os.chdir(os.path.dirname(__file__))

import cv2
import numpy as np
from PIL import Image, ImageTk

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

class Image_Processing():
    def __init__(self, image = ''):
        self.original_image = None
        self.resized_image = None
        self.tkinter_image = None
        self.masked_image = None
        self.contours_image = None
        self.FPS_image = None

        # ↓↓ Load the image
        if type(image) is str: self.original_image = cv2.imread(image)
        else: self.original_image = image
        if self.original_image is None: return print(f'\t[χ] Could not load the image: {image}')

    #######################################################################################################################

    def resize_image(self, desired_size = CONST.BOT_WINDOW_SIZE):
        if self.original_image is None: return

        # ↓↓ Get the desired aspect ratio and size
        aspect_ratio = CONST.ORIGINAL_FRAME_SIZE[0]/CONST.ORIGINAL_FRAME_SIZE[1]
        # ↓↓ (width, height)
        original_size = self.original_image.shape[1::-1]
        max_size_index = np.argmax(original_size)
        if not max_size_index: new_size = [desired_size[max_size_index], int(desired_size[max_size_index]/aspect_ratio)]
        else: new_size = [int(desired_size[max_size_index]*aspect_ratio), desired_size[max_size_index]]

        # ↓↓ Resize the image
        self.resized_image = cv2.resize(self.original_image, new_size)

    #######################################################################################################################

    # ↓↓ Convert the image to tkinter compatible format
    # ↓↓ Will raise an error if used before creating a GUI (root = Tk())
    def get_tkinter_image(self, image = None):
        if image is None: return

        self.tkinter_image = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))

    #######################################################################################################################

    # ↓↓ Convert the images to tkinter compatible format
    # ↓↓ Will raise an error if used before creating a GUI (root = Tk())
    def get_multiple_tkinter_images(self):
        if self.contours_image is None or self.masked_image is None: return

        new_size = [old_size//3 for old_size in self.resized_image.shape[1::-1]]
        self.top_right_tkinter_image = ImageTk.PhotoImage(
            Image.fromarray(cv2.cvtColor(cv2.resize(self.contours_image, new_size), cv2.COLOR_BGR2RGB))
        )
        self.bottom_right_tkinter_image = ImageTk.PhotoImage(
            Image.fromarray(cv2.cvtColor(cv2.resize(self.masked_image, new_size), cv2.COLOR_BGR2RGB))
        )

    #######################################################################################################################

    def detect_color(self, lower_color = CONST.LOWER_COLOR, upper_color = CONST.UPPER_COLOR):
        if self.resized_image is None: return
        # ↓↓ Applies the filter to the image
        self.masked_image = cv2.inRange(self.resized_image, lower_color, upper_color)

    #######################################################################################################################

    def get_rectangles(self):
        if self.resized_image is None: return None
        self.contours_image = np.copy(self.resized_image)
        contours, hierarchy = cv2.findContours(self.masked_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        match = False
        if len(contours) != 0:
            for contour in contours:
                # ↓↓ Minimum object size to detect as a match
                if cv2.contourArea(contour) > CONST.MIN_DETECT_SIZE:
                    # ↓↓ Draws the rectangles
                    x, y, w, h = cv2.boundingRect(contour)
                    # ↓↓ (Image, (Lower left corner), (Upper right corner), Color, Thickness)
                    cv2.rectangle(self.contours_image, (x, y), (x + w, y + h), CONST.RECTANGLES_PARAMS['color'], CONST.RECTANGLES_PARAMS['thickness'])
                    match = True
        return match

    #######################################################################################################################

    def draw_FPS(self, FPS):
        self.FPS_image = np.copy(self.resized_image)
        cv2.putText(self.FPS_image, f'FPS: {FPS}', CONST.TEXT_PARAMS['position'], cv2.FONT_HERSHEY_SIMPLEX, 
            CONST.TEXT_PARAMS['font_scale'], CONST.TEXT_PARAMS['font_color'], CONST.TEXT_PARAMS['thickness'], cv2.LINE_AA)

    #######################################################################################################################

    def check_corner_color(self): 
        # ↓↓ Return upper-left pixel
        return self.original_image[0][0]

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    image = Image_Processing(f'../Media/{CONST.TESTING_IMAGE}')

    image.resize_image(CONST.NEW_FRAME_SIZE)
    image.detect_color()
    match = image.get_rectangles()
    print(f'\nResult: {match}')

    cv2.imshow('Resized', image.resized_image)
    cv2.imshow('Mask', image.masked_image)
    cv2.imshow('Contours', image.contours_image)

    # ↓↓ Press 'q' to stop the program
    while(True):
        if cv2.waitKey(1) == ord('q'): break
    cv2.destroyAllWindows()