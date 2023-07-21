###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# ↓↓ Set the cwd to the one of the file
import os
if __name__ == '__main__': os.chdir(os.path.dirname(__file__))

from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk
import numpy as np
import copy
import cv2

import sys; sys.path.append('..'); sys.path.append('../Utils')
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
    'Normal' :  None,
    'Countours' : None,
}
Upper_Color = {
    'Red': IntVar(value=200),
    'Green': IntVar(value=255),
    'Blue': IntVar(value=70),
}
Lower_Color = {
    'Red': IntVar(value=55),
    'Green': IntVar(value=110),
    'Blue': IntVar(value=0),
}
GUI_Items = {
    'Match_Window': None,
    'Shiny_Canvas': {
        'Canvas': None,
        'ID': None,
    },
    'Normal_Canvas': {
        'Canvas': None,
        'ID': None,
    },
}
Show_Match = False

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

def update_items(_, color_range, specific_frame_items):
    # ↓↓ Prevent lower colors from being bigger than upper colors
    def solve_lower_upper_errors():
        colors = []
        # ↓↓ Check if the lower color is higher than the upper color for each RGB component
        if Lower_Color['Red'].get() > Upper_Color['Red'].get(): colors.append('Red')
        if Lower_Color['Green'].get() > Upper_Color['Green'].get(): colors.append('Green')
        if Lower_Color['Blue'].get() > Upper_Color['Blue'].get(): colors.append('Blue')
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
    # ↓↓ Prevent lower colors from being bigger than upper colors
    solve_lower_upper_errors()

    # ↓↓ Calculate and display the new masked image 
    def update_image(name):
        # ↓↓ Do not process the placeholder image
        if Pokemon_Images[name].resized_image is None: return
        
        lower_color = (Lower_Color['Red'].get(), Lower_Color['Green'].get(), Lower_Color['Blue'].get())
        upper_color = (Upper_Color['Red'].get(), Upper_Color['Green'].get(), Upper_Color['Blue'].get())
        # ↓↓ Get the masked image and convert it to tkinter compatible image
        Pokemon_Images[name].detect_color(lower_color, upper_color)
        Pokemon_Images[name].get_tkinter_image(Pokemon_Images[name].masked_image)

        if GUI_Items[f'{name}_Canvas']['Canvas'] is None:
            # ↓↓ Done with canvas to avoid white flashing when moving the slides fast
            GUI_Items[f'{name}_Canvas']['Canvas'] = Canvas(main_frame, bg='#000', highlightthickness=0, width=CONST.NEW_FRAME_SIZE[0],
                height=CONST.NEW_FRAME_SIZE[1])
            GUI_Items[f'{name}_Canvas']['ID'] = GUI_Items[f'{name}_Canvas']['Canvas'].create_image(0, 0, anchor='nw', image=Pokemon_Images[name].tkinter_image)
            if name == 'Shiny': GUI_Items[f'{name}_Canvas']['Canvas'].grid(row=0, column=2, rowspan=5, padx=10, pady=(10, 20))
            else: GUI_Items[f'{name}_Canvas']['Canvas'].grid(row=6, column=2, rowspan=1, padx=10, pady=(20, 10))
        else:
            GUI_Items[f'{name}_Canvas']['Canvas'].itemconfig(GUI_Items[f'{name}_Canvas']['ID'], image=str(Pokemon_Images[name].tkinter_image))

    for key in  ['Shiny', 'Normal']: update_image(key)
    
    # ↓↓ Show the image with the contours drawn
    if Show_Match: update_gui('Match_Window')
    else: destroy_gui('Match_Window')

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

###########################################################################################################################

def build_gui():
    # ↓↓ Insert a title
    root.title("Pokemon Shiny Hunter")
    # ↓↓ Set the icon for the GUI. It raises an error on Linux systems
    try: root.iconbitmap("../Media/Metal Slime.ico")
    except: pass
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
        Pokemon_Images[key] = Image_Processing(f'.{CONST.SELECT_IMAGE_PATH}')
        Pokemon_Images[key].get_tkinter_image(Pokemon_Images[key].original_image)
        Label(frame, image=Pokemon_Images[key].tkinter_image, borderwidth=0).pack()

    # ↓↓ Create a division line between the images
    canvas = Canvas(main_frame, width=CONST.NEW_FRAME_SIZE[0], height=1, highlightthickness=0)
    canvas.grid(row=5, column=2)
    # ↓↓ (Start-X, Start-Y, End-X, End-Y, extras)
    canvas.create_rectangle(0, 0, CONST.NEW_FRAME_SIZE[0], 1, fill='#222', width=0)

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
                command=lambda _: update_items(_, color_range, lower_slider_items if 'Lower' in text else upper_slider_items),
                cursor='sb_v_double_arrow'),
            # ↓↓ Green
            Scale(frame, from_=255, to=0, **slider_style, background='#0f0', activebackground='#040', variable=color_range['Green'],
                command=lambda _: update_items(_, color_range, lower_slider_items if 'Lower' in text else upper_slider_items),
                cursor='sb_v_double_arrow'),
            # ↓↓ Blue
            Scale(frame, from_=255, to=0, **slider_style, background='#00f', activebackground='#004', variable=color_range['Blue'],
                command=lambda _: update_items(_, color_range, lower_slider_items if 'Lower' in text else upper_slider_items),
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

    def toggle_match_showing(): global Show_Match; Show_Match = not Show_Match
    # ↓↓ Check match button
    # ↓↓ Body frame
    frame =  Frame(main_frame, **frame_style)
    frame.grid(row=5, column=0, columnspan=2, rowspan=10, sticky=N, pady=(230, 0))
    Button(frame, text=f'Toggle Check Match', command=lambda: toggle_match_showing(), **button_style).pack()

    return upper_slider_items, lower_slider_items

###########################################################################################################################

def destroy_gui(item_name = ''):
    if item_name not in GUI_Items.keys(): return
    if GUI_Items[item_name] is None: return
    GUI_Items[item_name].destroy()
    GUI_Items[item_name] = None

###########################################################################################################################

def update_gui(item_name = ''):
    # if item_name not in GUI_Items.keys(): return
    if Pokemon_Images['Normal'].masked_image is None or Pokemon_Images['Shiny'].masked_image is None: return
    
    if GUI_Items[item_name] is None: 
        GUI_Items[item_name] = Toplevel()
        GUI_Items[item_name].title('Matching Window')
        # ↓↓ It raises an error on Linux systems
        try: GUI_Items[item_name].iconbitmap("../Media/Metal Slime.ico")
        except: pass

    # ↓↓ Match window has been closed
    if not GUI_Items[item_name].winfo_exists(): 
        global Show_Match
        Show_Match = False
        return

    match = Pokemon_Images['Shiny'].get_rectangles()
    if match is None: return
    Pokemon_Images['Countours'] = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(Pokemon_Images['Shiny'].contours_image, cv2.COLOR_BGR2RGB)))
    Label(GUI_Items[item_name], image=Pokemon_Images['Countours'], borderwidth=0).grid(row=0, column=0)

###########################################################################################################################
    
def get_image(name):
    try: file_path = filedialog.askopenfile(initialdir=f'{os.path.dirname(__file__)}/../Media/', title='Choose one image',
        filetypes=(('Valid Formats', ['*.png', '*.jpg', '*.jpeg']), ('All Files', '*.*'))).name
    # ↓↓ The selection window has been closed without selecting any element
    except: return

    # ↓↓ Load the image
    Pokemon_Images[name] = Image_Processing(file_path)
    Pokemon_Images[name].resize_image(CONST.NEW_FRAME_SIZE)
    # ↓↓ Convert from BGR to RGB (I don't know why this one is the only one that is processed as BGR)
    aux_image = cv2.cvtColor(Pokemon_Images[name].resized_image, cv2.COLOR_BGR2RGB)
    Pokemon_Images[name].get_tkinter_image(cv2.cvtColor(aux_image, cv2.COLOR_BGR2RGB))
    # ↓↓ Reset the Canvas. If not, when updating it with the new image, it appears a white canvas 
    GUI_Items[f'{name}_Canvas']['Canvas'] = None

    # ↓↓ Body frame
    frame = Frame(main_frame, highlightthickness=1, highlightbackground ='#444')
    # ↓↓ Image
    Label(frame, image=Pokemon_Images[name].tkinter_image, borderwidth=0).pack()
    # ↓↓ Shiny: Top | Normal: Bottom
    if name == 'Shiny': frame.grid(row=0, column=2, rowspan=5, padx=10, pady=(10, 20))
    else: frame.grid(row=6, column=2, rowspan=1, padx=10, pady=(20, 10))

###########################################################################################################################
###########################################################################################################################

upper_slider_items, lower_slider_items = build_gui()
root.mainloop()