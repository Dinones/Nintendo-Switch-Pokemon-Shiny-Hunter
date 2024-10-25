###########################################################################################################################
#  Who doesn't like colors? Just a script to print with colors in the terminal making it more visual.                     #
###########################################################################################################################

###########################################################################################################################
####################################################     CONSTANTS     ####################################################
###########################################################################################################################

SPECIAL = {
    "Default"       : '0',
    "Bold"          : '1',
    "Italics"       : '3',
    "Underlined"    : '4',
    "Strikethrough" : '9'
}

COLORS = {
    "Black"     : '30',
    "Red"       : '31',
    "Green"     : '32',
    "Yellow"    : '33',
    "Blue"      : '34',
    "Magenta"   : '35',
    "Cyan"      : '36',
    "White"     : '37',

    "DarkGray"      : '90',
    "LightRed"      : '91',
    "LightGreen"    : '92',
    "LightYellow"   : '93',
    "LightBlue"     : '94',
    "LightMagenta"  : '95',
    "LightCyan"     : '96',
}

BACKGROUND = {
    "Black"     : '40',
    "Red"       : '41',
    "Green"     : '42',
    "Yellow"    : '43',
    "Blue"      : '44',
    "Magenta"   : '45',
    "Cyan"      : '46',
    "White"     : '47',
}

INFO = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[+] \033[0;m'
CORRECT = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[>] \033[0;m'
WARN = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[!] \033[0;m'
ERROR = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[X] \033[0;m'

###########################################################################################################################
#####################################################     GENERAL     #####################################################
###########################################################################################################################

INVALID_PATH_ERROR = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mInvalid path: \033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'

INVALID_PATH_WARNING = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mInvalid path: \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'

SUCCESS_EXIT_PROGRAM = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mExiting program: \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{reason}"}\033[0;m'

PRESS_KEY_TO_INSTRUCTION = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mPress \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{key}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m to {"{instruction}"}... \033[0;m'

RELEASING_THREADS = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mReleasing \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{threads}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m thread(s)... \033[0;m'

IMAGES_COUNT_WARNING = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mDetected \033[0;m'+\
    f'\033[{COLORS["Yellow"]}m{"{images}"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m images inside \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m"{"{path}"}"\033[0;m'+\
    f'\033[{COLORS["Yellow"]}m ({"{size}"})\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: \033[0;m'+\
    f'\033[{COLORS["Yellow"]}mPlease, consider checking and deleting them...\033[0;m'

USED_SPACE_WARNING = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mSpace in \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m is greater than \033[0;m'+\
    f'\033[{COLORS["Yellow"]}m{"1.00GB ({used_space})"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: \033[0;m'+\
    f'\033[{COLORS["Yellow"]}mPlease, consider freeing some space...\033[0;m'

AVAILABLE_SPACE_ERROR = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mSystem\'s available space is less than \033[0;m'+\
    f'\033[{COLORS["Red"]}m{"{threshold} ({available_space})"}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}m: \033[0;m'+\
    f'\033[{COLORS["Red"]}mPlease, free some space before continuing...\033[0;m'

RUNNING_OUT_OF_SPACE = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mThere\'s only \033[0;m'+\
    f'\033[{COLORS["Yellow"]}m{"{available_space}"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m of space left in the system: \033[0;m'+\
    f'\033[{COLORS["Yellow"]}mNo longer saving screenshots of the encounters...\033[0;m'

THREAD_DIED_ERROR = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mThread \033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{thread}"}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}m died: \033[0;m'+\
    f'\033[{COLORS["Red"]}mShutting down program...\033[0;m'

COULD_NOT_PLAY_SOUND = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not play sound: \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'

SHINY_FOUND = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mShiny \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{pokemon}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m found after \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{encounters}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m encounters!\033[0;m'

STUCK_FOR_TOO_LONG = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mGot stuck in the same state for too long: \033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{event}"}\033[0;m'

###########################################################################################################################
######################################################     MENU     #######################################################
###########################################################################################################################

MENU = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSelection Menu:\033[0;m'
MENU_OPTION = \
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m    [{"{index}"}] \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{option}"}\033[0;m'

OPTION_SELECTION = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSelect an option: \033[0;m'

INVALID_OPTION = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mInvalid option: \033[0;m'+\
    f'\033[{COLORS["Red"]}mExiting the program...\033[0;m'

SELECTED_OPTION = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mOption \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{option}"}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m selected: \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{action} "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Italics"]}m{"{path} "}\033[0;m'

###########################################################################################################################
###################################################     GAME CAPTURE     ##################################################
###########################################################################################################################

INVALID_VIDEO_CAPTURE = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not access video capture \033[0;m'+\
    f'\033[{COLORS["Red"]}m{"{video_capture}"}\033[0;m'

AVAILABLE_CAPTURE_DEVICES = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mCapture devices found: \033[0;m'
CAPTURE_DEVICE_OK = \
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m    Video Capture nº{"{index}"}: \033[0;m'+\
    f'\033[{COLORS["Green"]}mOK\033[0;m'
CAPTURE_DEVICE_NOT_OK = \
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}m    Video Capture nº{"{index}"}: \033[0;m'+\
    f'\033[{COLORS["Red"]}mNOT OK\033[0;m'

IMAGE_SAVED = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mImage saved: \033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'

USING_DIFFERENT_CAPTURE_CARD = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not access video capture \033[0;m'+\
    f'\033[{COLORS["Yellow"]}mnº{"{old_video_capture}"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m. Connecting to video capture \033[0;m'+\
    f'\033[{COLORS["Yellow"]}mnº{"{new_video_capture} "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}minstead...\033[0;m'

###########################################################################################################################
################################################     SWITCH CONTROLLER     ################################################
###########################################################################################################################

NOT_LINUX_SYSTEM = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mNXBT is only available on Linux systems!\033[0;m'

NOT_SUDO = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mNXBT must be executed with administrator permissions: \033[0;m'+\
    f'\033[{COLORS["Yellow"]}mRestarting using sudo...\033[0;m'

RESTARTING_BLUETOOTH = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mRestarting bluetooth systems...\033[0;m'

BLUETOOTH_RESTARTED = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mBluetooth restarted successfully!\033[0;m'

CONNECTING_TO_SWITCH = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mConnecting to Nintendo Switch...\033[0;m'

CONTROLLER_CONNECTED = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mController connected!\033[0;m'

###########################################################################################################################
###################################################     FPS COUNTER     ###################################################
###########################################################################################################################

FPS_COUNTER = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[FPS Counter] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mFPS: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{current_fps}"}     \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mMax FPS: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{max_fps}"}     \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mMin FPS: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{min_fps}"}     \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mAverage FPS (last 100): \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{average_fps}"}     \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mRAM Usage: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{memory_usage} MB"}     \033[0;m'

SYSTEM_AVAILABLE_SPACE = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[FPS Counter] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mTotal system space: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{total_space}"}     \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mUsed System Space: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{used_space}"}     \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mAvailable System Space: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{available_space}"}     \033[0;m'

DIRECTORY_SIZE = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[FPS Counter] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSize of \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Italics"]}m{"{directory}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{size}"}\033[0;m'

###########################################################################################################################
#################################################     IMAGE PROCESSING     ################################################
###########################################################################################################################

COULD_NOT_PROCESS_IMAGE = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not process image: \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}mSkipping frame...\033[0;m'

SUCCESSFULLY_EXTRACTED_FRAMES = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully extracted \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{frames}"}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m frames!\033[0;m'

SUCCESSFULLY_LOADED_IMAGES = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully loaded \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{images}"}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m images!\033[0;m'

CONTOURS_FOUND = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mFound \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{contours}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m contours!\033[0;m'

CURRENT_EXTRACTED_FRAMES = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mCurrently extracted \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{extracted_frame}"}/{"{total_frames}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m frames \033[0;m'+\
    f'\033[{COLORS["Blue"]}m({"{percentage}"}%)\033[0;m'

DELETE_IMAGES_QUESTION = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mDo you want to delete all the images [Y/n]? \033[0;m'

DELETING_IMAGES = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mDeleting \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{images}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m images...\033[0;m'

SUCCESSFULLY_DELETED_IMAGES = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully deleted \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{images}"}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m images!\033[0;m'

COULD_NOT_LOAD_IMAGES = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not find any image on: \033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'

###########################################################################################################################
#####################################################     DATABASE     ####################################################
###########################################################################################################################

INITIALIZE_DATABASE = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully initialized database!\033[0;m'

DATABASE_INFO = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mDatabase Stats: \033[0;m'

DATABASE_STAT_VALUE = \
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m\t{"{stat}"}: \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{value}"}\033[0;m'

SELECT_POKEMON_TO_DELETE = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mWrite the pokémon you want to delete from the database: \033[0;m'

COULD_NOT_DELETE_POKEMON = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not delete pokémon: \033[0;m'+\
    f'\033[{COLORS["Red"]}m{"{pokemon}"}\033[0;m'

###########################################################################################################################
#######################################################     GUI     #######################################################
###########################################################################################################################

COULD_NOT_LOAD_IMAGE = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[GUI] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not load image: \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'

###########################################################################################################################
#####################################################     MESSAGES     ####################################################
###########################################################################################################################

HTML_NOT_FOUND = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Mail] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not find HTML: \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{html}"}\033[0;m'

EMAIL_SENT = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Mail] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully sent email to \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{email}"}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m!\033[0;m'

COULD_NOT_SEND_EMAIL = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Mail] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not send email to \033[0;m'+\
    f'\033[{COLORS["Yellow"]}m{"{email}"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: \033[0;m'+\
    f'\033[{COLORS["Yellow"]}m{"{error}"}\033[0;m'

EMPTY_CREDENTIALS = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m{"{module}"} notifications cannot be sent: \033[0;m'+\
    f'\033[{COLORS["Yellow"]}mSome fields are missing in the \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{path}"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]}m file\033[0;m'

TELEGRAM_SENT = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Telegram] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully sent telegram to chat \033[0;m'+\
    f'\033[{COLORS["Green"]}m{"{chat_id}"}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m!\033[0;m'

COULD_NOT_SEND_TELEGRAM = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Telegram] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not send telegram to chat \033[0;m'+\
    f'\033[{COLORS["Yellow"]}m{"{chat_id}"}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: \033[0;m'+\
    f'\033[{COLORS["Yellow"]}m{"{error}"}\033[0;m'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__': 
    print("\n\t" + INFO, CORRECT, WARN, ERROR + "\n")