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
# Can't be greater than 110s!
SHINY_RECORDING_SECONDS = 60
SKIPPED_FRAMES_TO_RECONNECT = 3
# Used to debug issues and to save the video of the encounter. Disable this if you have performance issues
ENABLE_VIDEO_RECORDING = True

# Video size to save. ORIGINAL: Original size (ORIGINAL_FRAME_SIZE) | RESIZED: Resized size (MAIN_FRAME_SIZE)
# If you have performance issues, use RESIZED
SAVED_VIDEO_SIZE = 'ORIGINAL'

###########################################################################################################################
#################################################     IMAGE PROCESSING     ################################################
###########################################################################################################################

# Supported languages: ES, EN, DE, FR and IT
# Not supported languages: KO, ZH-CN and ZH-TW (Program will work, but database will do weird things)
LANGUAGE = 'EN'
# [PIXELS] Nintendo Switch captured frames' possible sizes 1080p: (1920, 1080) | 720p: (1280, 720)
# If you want to capture image and video in full HD, use 1080p, if you want better performance, use 720p.
ORIGINAL_FRAME_SIZE = (1920, 1080)

TEXT_PARAMS = {
    'font_scale': 0.5,
    # [BGR]
    'font_color': (255, 0, 125),
    'thickness': 2,
    # [PIXELS]
    'position': (2, 15),
    'star_num_color': (0, 0, 255)
}
PRESSED_BUTTON_COLOR = (255, 0, 200)
SAVE_IMAGES = True
IMAGES_FOLDER_PATH = 'Media/Images/'

# Image size to save. ORIGINAL: Original size (ORIGINAL_FRAME_SIZE) | RESIZED: Resized size (MAIN_FRAME_SIZE)
# If you have performance issues, use RESIZED
SAVED_IMAGE_SIZE = 'ORIGINAL'

# [BYTES] 1GB = 1073741824B
CRITICAL_AVAILABLE_SPACE = 1*1073741824
PIXEL_COLOR_DIFF_THRESHOLD = 7
# [SECONDS] Time the program will take to switch between the images
CHECK_LOST_SHINY_TIME = 0.15

###########################################################################################################################
#######################################################     GUI     #######################################################
###########################################################################################################################

# GUI title
BOT_NAME = "FB Pokemon Shiny Hunter by @Dinones"
SPAWN_POSITION = (300, 200)
# [PIXELS] GUI size
BOT_WINDOW_SIZE = (1100, 570)
MAIN_FRAME_SIZE = (720, 405)
SWITCH_CONTROLLER_FRAME_SIZE = (350, 280)
CLOCK_FRAME_SIZE = (350, 115)
TEXT_FRAME_SIZE = (355, 39)
STOP_BUTTON_FRAME_SIZE = (350, 63)
SOCIAL_BUTTON_FRAME_SIZE = (350, 63)

SWITCH_CONTROLLER_IMAGE_PATH = 'Media/Interface/Switch Controller.png'
TEMPLATE_IMAGE_PATH = 'Media/Interface/Background Template.png'
SOUND_ON_IMAGE_PATH = 'Media/Interface/Sound On.png'
SOUND_OFF_IMAGE_PATH = 'Media/Interface/Sound Off.png'
DINONES_IMAGE_PATH = 'Media/Interface/Dinones.png'
DISCORD_IMAGE_PATH = 'Media/Interface/Discord.png'
GITHUB_IMAGE_PATH = 'Media/Interface/Github.png'

PLAY_SOUNDS = True
SHINY_SOUND_PATH = 'Media/Interface/Shiny.mp3'
SHINY_STARS_SOUND_PATH = 'Media/Interface/Shiny Stars.mp3'
ERROR_SOUND_PATH = 'Media/Interface/Error.mp3'

DINONES_URL = 'https://www.youtube.com/@DinoDinones'
DISCORD_URL = 'https://discordapp.com/users/330983876367482880'
GITHUB_URL = 'https://github.com/Dinones'

###########################################################################################################################
################################################     SWITCH CONTROLLER     ################################################
###########################################################################################################################

RESTART_BLUETOOTH_SECONDS = 4
CONTROLLER_BODY_COLOR = (0, 200, 0)
CONTROLLER_BUTTONS_COLOR = (200, 0, 0)

###########################################################################################################################
##################################################     CONTROL SYSTEM     #################################################
###########################################################################################################################

IMAGES_COUNT_WARNING = 300
# Time the player is moving in each direction
WILD_WALKING_SECONDS = 1
# 'NS': Up/Down | 'EW': Right/Left
WILD_WALKING_DIRECTION = 'EW'
MOVE_FORWARD_STATIC_ENCOUNTER = False

# Variable used to skip a white screen flash (some static encounters have two white screen flashes)
# - Default value is 2
# - Dialga and Palkia: 4
# - Arceus: 6.5
# - Uxie: 3
# - Regigigas: 7
STATIC_ENCOUNTERS_DELAY = 2

# [SECONDS] How long has the bot been stuck in the same state before trying to restart the game
STUCK_TIMER_SECONDS = 25
# [SECONDS] How long no pokemon has been found before completely stopping program (ERROR)
FAILURE_DETECTION_TIME_WARN = 3*60
# [SECONDS] How long no pokemon has been found before completely stopping program (ERROR)
FAILURE_DETECTION_TIME_ERROR = 5*60
# Time to wait before detecting a shiny, used for BDSP and SWSH
SHINY_DETECTION_TIME = 2
HOME_MENU_COLOR = (237, 237, 237)
PAIRING_MENU_COLOR = (135, 135, 125)
LOAD_SCREEN_BLACK_COLOR = (5, 5, 5)
SWSH_COMBAT_BOX = {
    'x_black_grey': 10,
    'y1_black_grey': 20,
    'y2_black_grey': 45,
    'color_black_grey': (38, 38, 38),
    'x_grey': 65,
    'y1_grey': 20,
    'y2_grey': 45,
    'color_grey': (51, 51, 51),
}
TEXT_BOX_LINE = {
    'x': int(MAIN_FRAME_SIZE[0] // 16 * 1.2),
    'y1': int(MAIN_FRAME_SIZE[1] // 16 * 1),
    'y2': int(MAIN_FRAME_SIZE[1] // 16 * 2), 
    # [BGR]
    'color': (250, 250, 250),
    'overworld_x': int(MAIN_FRAME_SIZE[0] // 16 * 3.5),
}
LIFE_BOX_LINE = {
    'x': int(MAIN_FRAME_SIZE[0] // 96 * 1),
    'y1': int(MAIN_FRAME_SIZE[1] // 16 * 2),
    'y2': int(MAIN_FRAME_SIZE[1] // 16 * 2.6),
    # [BGR]
    'color': (250, 250, 250)
}
SELECTION_BOX_LINE = {
    'x': int(MAIN_FRAME_SIZE[0] // 16 * 13),
    'y1': int(MAIN_FRAME_SIZE[1] // 16 * 4),
    'y2': int(MAIN_FRAME_SIZE[1] // 16 * 5),
    # [BGR]
    'color': (250, 250, 250)
}
# 'L': Left | 'C': Center | 'R': Right 
STARTER = 'R'

###########################################################################################################################
#####################################################     DATABASE     ####################################################
###########################################################################################################################

DATABASE_PATH = 'Media/Database.db'

###########################################################################################################################
#####################################################     MESSAGES     ####################################################
###########################################################################################################################

# You will receive mail notifications when a shiny is found or an error occurs
MAIL_NOTIFICATIONS = False
# If you have configured the email notifications, fill in the following fields
MAIL_SETTINGS = {
    'port': 587,                        # Port TLS: 587 | SSL: 465
    'smtp_server': 'smtp.gmail.com',    # SMTP server

    'credentials_file_path': 'Modules/Mail/Email_Credentials.env',
    'save_credentials_file_path': 'Modules/Mail/Credentials.env',
    'credentials_template_file_path': 'Media/Messages/Email_Credentials_Template.env'
}

MESSAGES_PLACEHOLDER_IMAGE = 'Media/Messages/Dinones.png'
MESSAGES_ERROR_IMAGE = 'Media/Messages/Dizzy Dinones.png'
SHINY_HTML_PATH = 'Modules/Mail/Shiny.html'
ERROR_HTML_PATH = 'Modules/Mail/Error.html'

TELEGRAM_NOTIFICATIONS = False
TELEGRAM_SETTINGS = {
    'credentials_file_path': 'Modules/Telegram/Telegram_Credentials.env',
    'save_credentials_file_path': 'Modules/Telegram/Credentials.env',
    'credentials_template_file_path': 'Media/Messages/Telegram_Credentials_Template.env'
}

###########################################################################################################################
######################################################     TESTS     ######################################################
###########################################################################################################################

# Will color the pixels that are being used to detect the state. Videos will be recorded without colored pixels
TESTING = True
LOG_LEVEL = 'INFO'
SAVE_ERROR_VIDEOS = False
TESTING_COLOR = (255, 0, 255)
TESTING_VIDEO_PATH = 'Media/Tests/XXXX.mp4'
TESTING_IMAGE_PATH = 'Media/Tests/XXXX.png'
TESTING_DATABASE_PATH = 'Media/Tests/Test_Database.db'
SAVING_FRAMES_PATH = 'Media/Tests'
DEBUG_FRAME_SIZE = (720, 40)
DEBUG_IMAGE_TEXT_PARAMS = {
    'font_scale': 0.8,
    # [BGR]
    'font_color': (255, 0, 125),
    'thickness': 2,
    # [PIXELS]
    'position': (10, 28),
    'star_num_color': (0, 0, 255)
}