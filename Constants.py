###########################################################################################################################
#################################################     IMAGE PROCESSING     ################################################
###########################################################################################################################

# ↓↓ [RGB] Default Ranges
LOWER_COLOR = (110, 0, 65)
UPPER_COLOR = (255, 255, 105)
# ↓↓ [PIXELS] Nintendo Switch captured frames' size 
ORIGINAL_FRAME_SIZE = (1920, 1080)
# ↓↓ [PIXELS] Size the captured frame is resized to
NEW_FRAME_SIZE = (500, 281)
# ↓↓ Text style for the FPS counter
TEXT_PARAMS = {
    'font_scale': 0.5,
    # ↓↓ [RGB]
    'font_color': (255, 0, 125),
    'thickness': 2,
    # ↓↓ [PIXELS]
    'position': (2, 15)
}
RECTANGLES_PARAMS = {
    'color': (0, 255, 0),
    'thickness': 4
}
# ↓↓ [PIXELS²] Minimum area to detect something as a match
MIN_DETECT_SIZE = 50

###########################################################################################################################
#######################################################     GUI     #######################################################
###########################################################################################################################

# ↓↓ GUI title
BOT_NAME = "FBot Shiny Hunter"
# ↓↓ [PIXELS] GUI size
BOT_WINDOW_SIZE = (720, 405) # (1000, 562)
# ↓↓ Only image names
DEFAULT_SELECTION_IMAGE = "Select Image.png"
GUI_ICON = "Metal Slime.ico"

###########################################################################################################################
##################################################     VIDEO CAPTURE     ##################################################
###########################################################################################################################

VIDEO_CAPTURE_INDEX = 0
FPS_COUNTER = True
# ↓↓ [SECONDS]
REFRESH_FPS_TIME = 1
# ↓↓ Record a video for every attempt. Overwrites always the file
RECORD_VIDEO = True
RECORD_MULTIPLE_WINDOWS = True
VIDEO_FPS = 5
OUTPUT_VIDEO_NAME = 'Video.avi'
OUTPUT_CONTOURS_VIDEO_NAME = 'Video (Contours).avi'
SHINY_RECORDING_SECONDS = 60

###########################################################################################################################
################################################     SWITCH CONTROLLER     ################################################
###########################################################################################################################

CONTROLLER_BODY_COLOR = [0, 200, 0]
CONTROLLER_BUTTONS_COLOR = [200, 0, 0]
RESTART_BLUETOOTH_SECONDS = 4
WALKING_SECONDS = 2
BLACK_SCREEN_LOAD_SECONDS = 15
ENTER_COMBAT_WAIT_SECONDS = 3

###########################################################################################################################
######################################################     TESTS     ######################################################
###########################################################################################################################

TESTING_IMAGE = 'Select Image.png'
