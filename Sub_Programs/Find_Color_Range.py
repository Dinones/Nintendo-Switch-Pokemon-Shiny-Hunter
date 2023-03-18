###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
os.chdir(os.path.dirname(__file__))

from tkinter import *
from tkinter import ttk, filedialog

from PIL import Image, ImageTk
import numpy as np
import cv2

import sys; sys.path.append('../'); sys.path.append('../Utils/')
from Image_Processing import Image_Processing
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

Normal_Pokemon = None
Shiny_Pokemon = None
Pokemon_Images = {
    'Shiny'  :  Shiny_Pokemon,
    'Normal' :  Normal_Pokemon
}

###########################################################################################################################

# ↓↓ Create the GUI
root = Tk()

# ↓↓ Frame created to make the GUI responsive, every widget should be inside of it instead of the root
main_frame = Frame(root, bg='#333')
main_frame.pack(expand=True, padx=0, pady=0)
# ↓↓ Make the size of the window update automatically if a widget is added outside 
root.update_idletasks() 

###########################################################################################################################

# ↓↓ Define the button style and its frame
button_style = {
    'bg': '#222222',
    'fg': '#ffffff',
    'activebackground': '#444',
    'activeforeground': '#ffffff',
    'borderwidth': 0,
    'relief': 'flat',
    'font': ('Helvetica', 12),
    'width': 25,
}

frame_style = {
    'bg': '#444',
    'bd': 1,
}

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def build_gui():
    # ↓↓ Insert a title
    root.title("Pokemon Shiny Hunter")
    # ↓↓ Set the icon for the GUI
    root.iconbitmap("../Media/Metal Slime.ico")
    # ↓↓ Set the background color
    root.configure(bg='#333')
    # ↓↓ Set the font
    root.option_add('*font', ('Arial', 12))

    # ↓↓ Create image selection buttons
    for index, key in enumerate(Pokemon_Images.keys()):
        frame =  Frame(main_frame, **frame_style)
        frame.grid(row=0, column=index, padx=10, pady=10, sticky=N)
        if key == 'Normal': 
            Button(frame, text=f'Select {key} Pokemon', command=lambda: get_image('Normal'), **button_style).pack()
        else: Button(frame, text=f'Select {key} Pokemon', command=lambda: get_image('Shiny'), **button_style).pack()

    # ↓↓ Display a placeholder image
    for key in Pokemon_Images.keys():
        frame = Frame(main_frame, highlightthickness=1, highlightbackground ='#444')
        Pokemon_Images[key] = Image_Processing(Image.open(CONST.SELECT_IMAGE_PATH))
        Pokemon_Images[key].tkinter_image = ImageTk.PhotoImage(Pokemon_Images[key].original_image)
        Label(frame, image=Pokemon_Images[key].tkinter_image, borderwidth=0).pack()
        if key == 'Shiny': frame.grid(row=0, column=2, rowspan=5, padx=10, pady=(10, 20))
        else: frame.grid(row=6, column=2, rowspan=1, padx=10, pady=(20, 10))

    # ↓↓ Create a Canvas widget
    canvas = Canvas(main_frame, width=CONST.NEW_PIXEL_SIZE[0], height=1, highlightthickness=0)
    canvas.grid(row=5, column=2)
    # ↓↓ (Start-X, Start-Y, End-X, End-Y)
    canvas.create_rectangle(0, 0, CONST.NEW_PIXEL_SIZE[0], 1, fill='#222', width=0)

def get_image(name):
    try: file_path = filedialog.askopenfile(initialdir=f'{os.path.dirname(__file__)}/../Media/', title='Choose one file',
        filetypes=(('Valid Formats', ['*.png', '*.jpg', '*.jpeg']), ('All Files', '*.*'))).name
    # ↓↓ The selection window has been closed without selecting any element
    except: return print('No file selected!')

    # Image_Processing(Image.open(file_path))
    try: Pokemon_Images[name] = Image_Processing(Image.open(file_path))
    except: return print(f"[‼] Could not open '{file_path}'. Check if it is damaged.")
    
    # ↓↓ Get the desired aspect ratio and size
    aspect_ratio = CONST.ORIGINAL_FRAME_SIZE[0]/CONST.ORIGINAL_FRAME_SIZE[1]
    size = Pokemon_Images[name].original_image.size
    max_size_index = np.argmax(size)
    if not max_size_index: new_size = [CONST.NEW_PIXEL_SIZE[max_size_index], int(CONST.NEW_PIXEL_SIZE[max_size_index]/aspect_ratio)]
    else: new_size = [int(CONST.NEW_PIXEL_SIZE[max_size_index]*aspect_ratio), CONST.NEW_PIXEL_SIZE[max_size_index]]

    # ↓↓ Resize the image
    Pokemon_Images[name].resized_image = Pokemon_Images[name].original_image.resize(new_size, Image.BICUBIC)
    # ↓↓ Convert the image to tkinter compatible format
    Pokemon_Images[name].tkinter_image = ImageTk.PhotoImage(Pokemon_Images[name].resized_image)

    frame = Frame(main_frame, highlightthickness=1, highlightbackground ='#111')
    Label(frame, image=Pokemon_Images[name].tkinter_image, borderwidth=0).pack()

    if name == 'Shiny': frame.grid(row=0, column=2, rowspan=5, padx=10, pady=(10, 20))
    else: frame.grid(row=6, column=2, rowspan=1, padx=10, pady=(20, 10))

###########################################################################################################################

build_gui()
root.mainloop()