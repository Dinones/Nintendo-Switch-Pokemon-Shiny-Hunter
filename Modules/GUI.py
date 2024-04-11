###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

import tkinter as tk
from threading import Timer
from time import sleep, time

import sys; sys.path.append('..')
import Constants as CONST

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

frame_style = {
    'background': '#555',
    # Space left between the borders of the frame and the items inside it 
    'bd': 2,
}
canvas_style = {
    'background': '#000',
    'highlightthickness': 0,
}
text_frame_style = {
    'background': '#222',
    'highlightthickness': 1,
    'highlightbackground': '#444',
}
text_style = {
    'fg': '#aaa',
    'anchor': 'w',
    'background': '#222',
}

# GUI inherits from the class Thread. It will behave like a thread
class GUI():
    def __init__(self, queue):
        self.queue = queue
        self.timer = None
        
        # Create the GUI
        self.root = tk.Tk()
        # Insert a title
        self.root.title(CONST.BOT_NAME)
        # Set the background color
        self.root.configure(bg='#333')
        # Set the font
        self.root.option_add('*font', ('Arial', 12))

        def new_image(): return {'tkinter_image': None, 'image_id': None, 'canvas': None}

        self.items = {
            # Frame created to make the GUI responsive, every widget should be inside of it instead of the root
            'main_frame': tk.Frame(self.root, background='#333', 
                width=CONST.BOT_WINDOW_SIZE[0], height=CONST.BOT_WINDOW_SIZE[1]),

            'main_image_frame': None,
            'main_image': new_image(),

            'top_right_image_frame': None,
            'top_right_image': new_image(),

            'bottom_right_image_frame': None,
            'bottom_right_image': new_image(),

            'RAM_usage_frame': None,
            'RAM_usage_label': None,

            'current_state_frame': None,
            'current_state_label': None,

            'encounter_count_frame': None,
            'encounter_count_label': None,

            'switch_controller_frame': None,
            'switch_controller_image': new_image(),
        }

        ##### MAIN FRAME #####
        self.items['main_frame'].pack(expand=True, padx=0, pady=0)


        ##### MAIN IMAGE #####
        self.items['main_image_frame'] = tk.Frame(self.items['main_frame'], **frame_style)
        self.items['main_image_frame'].place(x=10, y=10)
        # Made with canvas to avoid white flashing when moving the slides fast
        self.items['main_image']['canvas'] = tk.Canvas(self.items['main_image_frame'], **canvas_style,
            width=CONST.MAIN_FRAME_SIZE[0], height=CONST.MAIN_FRAME_SIZE[1])
        self.items['main_image']['image_id'] = self.items['main_image']['canvas']\
            .create_image(0, 0, anchor='nw', image=None)
        self.items['main_image']['canvas'].pack()


        ##### RIGHT TOP IMAGE #####
        self.items['top_right_image_frame'] = tk.Frame(self.items['main_frame'], **frame_style)
        self.items['top_right_image_frame'].place(x=CONST.MAIN_FRAME_SIZE[0] + 20, y=10)
        # Made with canvas to avoid white flashing when moving the slides fast
        self.items['top_right_image']['canvas'] = tk.Canvas(self.items['top_right_image_frame'], **canvas_style,
            width=CONST.SECONDARY_FRAME_SIZE[0], height=CONST.SECONDARY_FRAME_SIZE[1])
        self.items['top_right_image']['image_id'] = self.items['top_right_image']['canvas']\
            .create_image(0, 0, anchor='nw', image=None)
        self.items['top_right_image']['canvas'].pack()


        ##### RIGHT BOTTOM IMAGE #####
        self.items['bottom_right_image_frame'] = tk.Frame(self.items['main_frame'], **frame_style)
        self.items['bottom_right_image_frame'].place(x=CONST.MAIN_FRAME_SIZE[0] + 20, y=CONST.MAIN_FRAME_SIZE[1]//2 + 16)
        # Made with canvas to avoid white flashing when moving the slides fast
        self.items['bottom_right_image']['canvas'] = tk.Canvas(self.items['bottom_right_image_frame'], **canvas_style,
            width=CONST.SECONDARY_FRAME_SIZE[0], height=CONST.SECONDARY_FRAME_SIZE[1])
        self.items['bottom_right_image']['image_id'] = self.items['bottom_right_image']['canvas']\
            .create_image(0, 0, anchor='nw', image=None)
        self.items['bottom_right_image']['canvas'].pack()


        ##### RAM USAGE #####
        self.items['RAM_usage_frame'] = tk.Frame(self.items['main_frame'], **text_frame_style)
        self.items['RAM_usage_frame'].place(x=10, y=CONST.MAIN_FRAME_SIZE[1] + 20)
        self.items['RAM_usage_label'] = \
            tk.Label(self.items['RAM_usage_frame'], text='  🔹⠀ RAM Usage: 0 MB', height=2, width=59, **text_style)
        self.items['RAM_usage_label'].pack(fill=tk.BOTH)


        ##### CURRENT STATE #####
        self.items['current_state_frame'] = tk.Frame(self.items['main_frame'], **text_frame_style)
        self.items['current_state_frame'].place(x=10, y=CONST.MAIN_FRAME_SIZE[1] + 10 + 59)
        self.items['current_state_label'] = \
            tk.Label(self.items['current_state_frame'], text='  🔹⠀ Current State: None', height=2, width=59, **text_style)
        self.items['current_state_label'].pack(fill=tk.BOTH)


        ##### ENCOUNTER COUNT #####
        self.items['encounter_count_frame'] = tk.Frame(self.items['main_frame'], **text_frame_style)
        self.items['encounter_count_frame'].place(x=10, y=CONST.MAIN_FRAME_SIZE[1] + 10 + 109)
        self.items['encounter_count_label'] = \
            tk.Label(self.items['encounter_count_frame'], text='  🔹⠀ Encounter Count: 0', height=2, width=59, **text_style)
        self.items['encounter_count_label'].pack(fill=tk.BOTH)


        ##### SWITCH CONTROLLER #####
        self.items['switch_controller_frame'] = tk.Frame(self.items['main_frame'], **frame_style)
        self.items['switch_controller_frame'].place(x=CONST.MAIN_FRAME_SIZE[0] + 20, y=CONST.MAIN_FRAME_SIZE[1] + 20)
        # Made with canvas to avoid white flashing when moving the slides fast
        self.items['switch_controller_image']['canvas'] = tk.Canvas(self.items['switch_controller_frame'], **canvas_style,
            width=CONST.SWITCH_CONTROLLER_FRAME_SIZE[0], height=CONST.SWITCH_CONTROLLER_FRAME_SIZE[1])
        self.items['switch_controller_image']['image_id'] = self.items['switch_controller_image']['canvas']\
                .create_image(0, 0, anchor='nw', image=None)
        self.items['switch_controller_image']['canvas'].pack()


        # Whenever the GUI geometry (size) is changed, it is automatically restored to the original one
        def enforce_geometry(event): self.root.geometry(f'{CONST.BOT_WINDOW_SIZE[0]}x{CONST.BOT_WINDOW_SIZE[1]}')
        self.root.bind("<Configure>", enforce_geometry)

        # Start the GUI
        self.update_GUI()
        self.root.mainloop()

    #######################################################################################################################

    def update_GUI(self):
        try: [image, memory_usage, switch_controller_image, current_state, shutdown_event, encounter_count] = \
            self.queue.get(block=True, timeout=1)
        except: 
            # Schedule the next update_GUI() call in 10 milliseconds
            self.timer = Timer(0.01, self.update_GUI)
            self.timer.start()
            return

        # Check if the GUI is still alive (hasn't been closed)
        try: self.root.winfo_exists()
        except: return
        
        # Convert images to a Tkinter compatible format
        image.get_tkinter_images(['FPS_image', 'masked_image', 'contours_image'])
        switch_controller_image.tkinter_images['switch_controller_image'] = \
            switch_controller_image.get_tkinter_image(switch_controller_image.contours_image)

        # Update images
        self.items['main_image']['canvas'].itemconfig(self.items['main_image']['image_id'],
            image=str(image.tkinter_images['FPS_image']))
        self.items['top_right_image']['canvas'].itemconfig(self.items['top_right_image']['image_id'],
            image=str(image.tkinter_images['masked_image']))
        self.items['bottom_right_image']['canvas'].itemconfig(self.items['bottom_right_image']['image_id'],
            image=str(image.tkinter_images['contours_image']))
        self.items['switch_controller_image']['canvas'].itemconfig(self.items['switch_controller_image']['image_id'],
            image=str(switch_controller_image.tkinter_images['switch_controller_image']))

        # Avoid white flasing
        self.items['main_image']['tkinter_image'] = image.tkinter_images['FPS_image']
        self.items['top_right_image']['tkinter_image'] = image.tkinter_images['masked_image']
        self.items['bottom_right_image']['tkinter_image'] = image.tkinter_images['contours_image']
        self.items['switch_controller_image']['tkinter_image'] = \
            switch_controller_image.tkinter_images['switch_controller_image']

        # Update RAM usage, current state and encounter count
        self.items['RAM_usage_label'].config(text=f'  🔹⠀ RAM Usage: {memory_usage:.2f} MB')
        self.items['current_state_label'].config(text=f'  🔹⠀ Current State: {current_state}')
        self.items['encounter_count_label'].config(text=f'  🔹⠀ Encounter Count: {str(encounter_count)}')

        # Schedule the next update_GUI() call in 10 milliseconds
        self.timer = Timer(0.01, self.update_GUI)
        self.timer.start()

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    from queue import Queue
    from threading import Thread, Event

    import Colored_Strings as COLOR_str
    from FPS_Counter import FPS_Counter
    from Game_Capture import Game_Capture
    from Image_Processing import Image_Processing
    
    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'GUI'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Open GUI using capture card'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'GUI'))

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

        Image_Queue = Queue()
        Video_Capture = Game_Capture(CONST.VIDEO_CAPTURE_INDEX)
        FPS = FPS_Counter()
        shutdown_event = Event()
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

                Image_Queue.put([image, FPS.memory_usage, switch_controller_image, None, None, 0])

        threads = []
        threads.append(Thread(target=lambda: test_GUI_control(shutdown_event), daemon=True))
        threads.append(Thread(target=lambda: FPS.get_memory_usage(shutdown_event), daemon=True))
        for thread in threads: thread.start()

        # Blocking function until the GUI is closed
        user_interface = GUI(Image_Queue)
        shutdown_event.set()

        print(COLOR_str.RELEASING_THREADS.replace('{module}', 'GUI').replace('{threads}', str(len(threads))) + '\n')        

    #######################################################################################################################

    main_menu()