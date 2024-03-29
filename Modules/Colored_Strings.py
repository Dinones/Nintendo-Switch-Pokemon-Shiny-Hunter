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
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not access to the video capture \033[0;m'+\
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

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__': 
    print("\n\t" + INFO, CORRECT, WARN, ERROR + "\n")