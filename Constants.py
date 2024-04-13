###########################################################################################################################
##################################################     VIDEO CAPTURE     ##################################################
###########################################################################################################################

VIDEO_CAPTURE_INDEX = 0
FPS_COUNTER = True
# [SECONDS]
REFRESH_FPS_TIME = 1
MAX_VIDEO_DEVICES_ANALIZED = 5
VIDEO_FPS = 27
OUTPUT_VIDEO_PATH = 'Media/Videos/Video.avi'
SHINY_RECORDING_SECONDS = 60

###########################################################################################################################
#################################################     IMAGE PROCESSING     ################################################
###########################################################################################################################

# [PIXELS] Nintendo Switch captured frames' size 
ORIGINAL_FRAME_SIZE = (1920, 1080)
RECTANGLES_PARAMS = {
    'color': (0, 255, 0),
    'thickness': 4
}
TEXT_PARAMS = {
    'font_scale': 0.5,
    # [BGR]
    'font_color': (255, 0, 125),
    'thickness': 2,
    # [PIXELS]
    'position': (2, 15),
    'star_num_color': (0, 0, 255)
}
# [PIXELS²] Minimum area to detect something as a match
MIN_DETECT_SIZE = 5
MIN_DETECTED_CONTOURS = 10
LOWER_COLOR = 235
UPPER_COLOR = 255
PRESSED_BUTTON_COLOR = (255, 0, 200)
IMAGES_FOLDER_PATH = 'Media/Images/'

###########################################################################################################################
#######################################################     GUI     #######################################################
###########################################################################################################################

# GUI title
BOT_NAME = "FB Pokemon Shiny Hunter by @Dinones"
# [PIXELS] GUI size
BOT_WINDOW_SIZE = (1104, 718)
MAIN_FRAME_SIZE = (720, 405)
SECONDARY_FRAME_SIZE = (350, 197)
SWITCH_CONTROLLER_FRAME_SIZE = (350, 280)
SWITCH_CONTROLLER_IMAGE_PATH = 'Media/Interface/Switch Controller.png'

###########################################################################################################################
################################################     SWITCH CONTROLLER     ################################################
###########################################################################################################################

RESTART_BLUETOOTH_SECONDS = 4
CONTROLLER_BODY_COLOR = (0, 200, 0)
CONTROLLER_BUTTONS_COLOR = (200, 0, 0)

###########################################################################################################################
##################################################     CONTROL SYSTEM     #################################################
###########################################################################################################################

# Time the player is moving in each direction
WILD_WALKING_SECONDS = 1
# 'NS': Up/Down | 'EW': Right/Left
WILD_WALKING_DIRECTION = 'NS'
# How long has the bot been stuck in the same state before restarting the game
STUCK_TIMER_SECONDS = 30
ENCOUNTERS_TXT_PATH = 'Media/Encounters.txt'
HOME_MENU_COLOR = 255
PAIRING_MENU_COLOR = 240
ESCAPE_COMBAT_BLACK_COLOR = 7
GAME_LOAD_SCREEN_BLACK_COLOR = 8
TEXT_BOX_LINE = {
    'x': int(MAIN_FRAME_SIZE[0] // 16 * 1.2),
    'y1': int(MAIN_FRAME_SIZE[1] // 16 * 1),
    'y2': int(MAIN_FRAME_SIZE[1] // 16 * 2), 
    'color': 255
}
LIFE_BOX_LINE = {
    'x': int(MAIN_FRAME_SIZE[0] // 96 * 1),
    'y1': int(MAIN_FRAME_SIZE[1] // 16 * 2),
    'y2': int(MAIN_FRAME_SIZE[1] // 16 * 2.6),
    'color': 250
}

###########################################################################################################################
######################################################     TESTS     ######################################################
###########################################################################################################################

TESTING = True
TESTING_VIDEO_PATH = 'Media/Tests/Shiny Abomasnow.mp4'
TESTING_IMAGE_PATH = 'Media/Interface/Switch Controller.png'