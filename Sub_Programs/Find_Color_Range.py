###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
os.chdir(os.path.dirname(__file__))

from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk
import numpy as np
import cv2

import sys; sys.path.append('../'); sys.path.append('../Utils/')
from Image_Processing import Image_Processing
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

# ↓↓ Create the GUI
root = Tk()
# ↓↓ Frame created to make the GUI responsive, every widget should be inside of it instead of the root
main_frame = Frame(root, bg='#333')
main_frame.pack(expand=True, padx=0, pady=0)
# ↓↓ Make the size of the window update automatically if a widget is added outside 
root.update_idletasks() 

###########################################################################################################################

Pokemon_Images = {
    'Shiny'  :  None,
    'Normal' :  None
}
Upper_Color = {
    'Red': IntVar(value=255),
    'Green': IntVar(value=255),
    'Blue': IntVar(value=255),
}
Lower_Color = {
    'Red': IntVar(),
    'Green': IntVar(),
    'Blue': IntVar(),
}

###########################################################################################################################

# ↓↓ Define the button style
button_style = {
    'background': '#222',
    'foreground': '#fff',
    'activebackground': '#444',
    'activeforeground': '#fff',
    'borderwidth': 0,
    'relief': 'flat',
    'font': ('Helvetica', 12),
    'width': 25,
}
# ↓↓ Define default frame style
frame_style = {
    'background': '#444',
    'bd': 1,
}
# ↓↓ Define slider style
slider_style = {
    'troughcolor': '#444',
    'foreground': 'cyan',
    'bd': 1,
    'borderwidth': 0,
    'highlightthickness':1,
    'highlightbackground': '#666',
    'showvalue': 0,
    'sliderrelief': FLAT,
}

INSTRUCTIONS = [
        '🔹⠀ Find the ranges that only show (in white) the shiny pokémon',
        '🔹⠀ Before closing this program, save the color range values',
        '🔹⠀ Avoid background colors from being detected',
        '🔹⠀ Top image must be the shiny one',
    ]

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def update_color(_, color_range, specific_frame_items):
    # ↓↓ Prevent lower colors from being bigger than upper colors
    def solve_lower_upper_errors(colors):
        if not len(colors): return
        for color in colors:
            # ↓↓ Set lower color to the upper color
            Lower_Color[color].set(Upper_Color[color].get())
        text = f'({Lower_Color["Red"].get()}, {Lower_Color["Green"].get()}, {Lower_Color["Blue"].get()})'
        lower_slider_items['Value_Text'].destroy()
        lower_slider_items['Value_Text'] = Label(lower_slider_items['Color_Rectangle'], text=text,  background='#222', fg='#fff')
        lower_slider_items['Value_Text'].grid(row=3, column=0, columnspan=3, pady=(0, 10))

        # ↓↓ Update the color of the rectangle on the top of the slider
        # ↓↓ Body frame
        frame2 = Frame(lower_slider_items['Color_Rectangle'], highlightthickness=1, highlightbackground='#444')
        frame2.grid(row=1, columnspan=3, pady=(10, 5))
        # ↓↓ Top rectangle
        canvas = Canvas(frame2, width=90, height=10, highlightthickness=0)
        color = (Lower_Color['Red'].get(), Lower_Color['Green'].get(), Lower_Color['Blue'].get())
        # ↓↓ (Start-X, Start-Y, End-X, End-Y, extras)
        canvas.create_rectangle(0, 0, 500, 10, fill='#{:02x}{:02x}{:02x}'.format(*color), width=0)
        canvas.pack()

    colors = []
    # ↓↓ Prevent lower colors from being bigger than upper colors
    if Lower_Color['Red'].get() > Upper_Color['Red'].get(): colors.append('Red')
    if Lower_Color['Green'].get() > Upper_Color['Green'].get(): colors.append('Green')
    if Lower_Color['Blue'].get() > Upper_Color['Blue'].get(): colors.append('Blue')
    solve_lower_upper_errors(colors)

    # ↓↓ Update the color of the rectangle on the top of the slider
    # ↓↓ Body frame
    frame2 = Frame(specific_frame_items['Color_Rectangle'], highlightthickness=1, highlightbackground='#444')
    frame2.grid(row=1, columnspan=3, pady=(10, 5))
    # ↓↓ Top rectangle
    canvas = Canvas(frame2, width=90, height=10, highlightthickness=0)
    color = (color_range['Red'].get(), color_range['Green'].get(), color_range['Blue'].get())
    # ↓↓ (Start-X, Start-Y, End-X, End-Y, extras)
    canvas.create_rectangle(0, 0, 500, 10, fill='#{:02x}{:02x}{:02x}'.format(*color), width=0)
    canvas.pack()
    text = f'({color_range["Red"].get()}, {color_range["Green"].get()}, {color_range["Blue"].get()})'
    # ↓↓ Update the text displayed at the bottom of the sliders
    specific_frame_items['Value_Text'].destroy()
    specific_frame_items['Value_Text'] = Label(specific_frame_items['Color_Rectangle'], text=text,  background='#222', fg='#fff')
    specific_frame_items['Value_Text'].grid(row=3, column=0, columnspan=3, pady=(0, 10))

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
        # ↓↓ Body frame
        frame =  Frame(main_frame, **frame_style)
        frame.grid(row=0, column=index, padx=10, pady=10, sticky=N)
        # ↓↓ Button
        if key == 'Normal': 
            Button(frame, text=f'Select {key} Pokemon', command=lambda: get_image('Normal'), **button_style).pack()
        else: Button(frame, text=f'Select {key} Pokemon', command=lambda: get_image('Shiny'), **button_style).pack()

    # ↓↓ Display a placeholder image
    for key in Pokemon_Images.keys():
        # ↓↓ Body frame
        frame = Frame(main_frame, highlightthickness=1, highlightbackground ='#444')
        if key == 'Shiny': frame.grid(row=0, column=2, rowspan=5, padx=10, pady=(10, 20))
        else: frame.grid(row=6, column=2, rowspan=1, padx=10, pady=(20, 10))
        # ↓↓ Image
        Pokemon_Images[key] = Image_Processing(Image.open(CONST.SELECT_IMAGE_PATH))
        Pokemon_Images[key].tkinter_image = ImageTk.PhotoImage(Pokemon_Images[key].original_image)
        Label(frame, image=Pokemon_Images[key].tkinter_image, borderwidth=0).pack()

    # ↓↓ Create a division line between the images
    canvas = Canvas(main_frame, width=CONST.NEW_PIXEL_SIZE[0], height=1, highlightthickness=0)
    canvas.grid(row=5, column=2)
    # ↓↓ (Start-X, Start-Y, End-X, End-Y, extras)
    canvas.create_rectangle(0, 0, CONST.NEW_PIXEL_SIZE[0], 1, fill='#222', width=0)

    # ↓↓ Create the sliders 
    def create_slider(color_range, text):
        # ↓↓ Body frame
        frame = Frame(main_frame, background='#222', highlightthickness=1, highlightbackground='#444')
        frame.grid(row=1, column='Upper' in text)
        # ↓↓ Title
        Label(frame, text=text, fg='#fff', background='#222').grid(row=0, columnspan=3, padx=10, pady=(5, 0))
        # ↓↓ Internal frame
        frame2 = Frame(frame, highlightthickness=1, highlightbackground='#444')
        frame2.grid(row=1, columnspan=3, pady=(10, 5))
        # ↓↓ Top rectangle
        canvas = Canvas(frame2, width=90, height=10, highlightthickness=0)
        color = (color_range['Red'].get(), color_range['Green'].get(), color_range['Blue'].get())
        canvas.create_rectangle(0, 0, 500, 10, fill='#{:02x}{:02x}{:02x}'.format(*color), width=0)
        canvas.pack()
        # ↓↓ Value text
        _text = f'({color_range["Red"].get()}, {color_range["Green"].get()}, {color_range["Blue"].get()})'
        label = Label(frame, text=_text, background='#222', fg='#fff')
        label.grid(row=3, column=0, columnspan=3, pady=(0, 10))

        # ↓↓ Scales
        scales = [
            # ↓↓ Red
            Scale(frame, from_=255, to=0, **slider_style, background='#f00', activebackground='#400', variable=color_range['Red'],
                command=lambda _: update_color(_, color_range, lower_slider_items if 'Lower' in text else upper_slider_items),
                cursor='sb_v_double_arrow'),
            # ↓↓ Green
            Scale(frame, from_=255, to=0, **slider_style, background='#0f0', activebackground='#040', variable=color_range['Green'],
                command=lambda _: update_color(_, color_range, lower_slider_items if 'Lower' in text else upper_slider_items),
                cursor='sb_v_double_arrow'),
            # ↓↓ Blue
            Scale(frame, from_=255, to=0, **slider_style, background='#00f', activebackground='#004', variable=color_range['Blue'],
                command=lambda _: update_color(_, color_range, lower_slider_items if 'Lower' in text else upper_slider_items),
                cursor='sb_v_double_arrow'),
        ]

        # ↓↓ Allow scrolling to increase/decrease the slider value
        def scroll_scale_value(scale, event):
            if event.delta > 0: scale.set(scale.get() + 1)
            elif event.delta < 0: scale.set(scale.get() - 1)
        
        # ↓↓ Make the scales scrollable
        for index, scale in enumerate(scales):
            # ↓↓ Allow scrolling to increase/decrease the slider value
            scale.bind("<MouseWheel>", lambda event, s=scale: scroll_scale_value(s, event))
            # ↓↓ Add some space between each slider
            if index == 1: scale.grid(row=2, column=index, padx=0, pady=10)
            else: scale.grid(row=2, column=index, padx=20, pady=10)

        return frame, label

    lower_slider_items = {}; upper_slider_items = {}
    lower_slider_items['Color_Rectangle'], lower_slider_items['Value_Text'] = create_slider(Lower_Color, 'Lower Color')
    upper_slider_items['Color_Rectangle'], upper_slider_items['Value_Text'] = create_slider(Upper_Color, 'Upper Color')

    # ↓↓ Instructions
    # ↓↓ Body frame
    frame = Frame(main_frame, background='#222', highlightthickness=1, highlightbackground='#444')
    frame.grid(row=4, column=0, columnspan=2, rowspan=5, sticky=N, pady=(31, 0))
    for instruction in INSTRUCTIONS:
        Label(frame, text=instruction, background='#222', fg='#aaa', width=50, anchor='w').pack(padx=15, pady=10)

    return upper_slider_items, lower_slider_items

def get_image(name):
    try: file_path = filedialog.askopenfile(initialdir=f'{os.path.dirname(__file__)}/../Media/', title='Choose one image',
        filetypes=(('Valid Formats', ['*.png', '*.jpg', '*.jpeg']), ('All Files', '*.*'))).name
    # ↓↓ The selection window has been closed without selecting any element
    except: return print('No file selected!')

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

    # ↓↓ Body frame
    frame = Frame(main_frame, highlightthickness=1, highlightbackground ='#222')
    # ↓↓ Image
    Label(frame, image=Pokemon_Images[name].tkinter_image, borderwidth=0).pack()
    # ↓↓ Shiny: Top | Normal: Bottom
    if name == 'Shiny': frame.grid(row=0, column=2, rowspan=5, padx=10, pady=(10, 20))
    else: frame.grid(row=6, column=2, rowspan=1, padx=10, pady=(20, 10))

###########################################################################################################################

upper_slider_items, lower_slider_items = build_gui()
root.mainloop()