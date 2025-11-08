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

RESET_FORMAT = '\033[0;m'

INFO = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[+] {RESET_FORMAT}'
CORRECT = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[>] {RESET_FORMAT}'
WARN = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[!] {RESET_FORMAT}'
ERROR = f'\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m[X] {RESET_FORMAT}'

###########################################################################################################################
#####################################################     GENERAL     #####################################################
###########################################################################################################################

G_INVALID_PATH_ERROR = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mInvalid path: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m"{"{path}"}"{RESET_FORMAT}'

G_INVALID_PATH_WARNING = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mInvalid path: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m"{"{path}"}"{RESET_FORMAT}'

G_SUCCESS_EXIT_PROGRAM = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mExiting program: {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{reason}"}{RESET_FORMAT}'

G_PRESS_KEY_TO_INSTRUCTION = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mPress {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{key}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m to {"{instruction}"}... {RESET_FORMAT}'

G_RELEASING_THREADS = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mReleasing {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{threads}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m thread(s)... {RESET_FORMAT}'

IMAGES_COUNT_WARNING = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mDetected {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{images}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m images inside {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m"{"{path}"}"{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m ({"{size}"}){RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mPlease, consider checking and deleting them...{RESET_FORMAT}'

USED_SPACE_WARNING = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mSpace in {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{path}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m is greater than {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"1.00GB ({used_space})"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mPlease, consider freeing some space...{RESET_FORMAT}'

AVAILABLE_SPACE_ERROR = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mSystem\'s available space is less than {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}m{"{threshold} ({available_space})"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}m: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}mPlease, free some space before continuing...{RESET_FORMAT}'

RUNNING_OUT_OF_SPACE = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mThere\'s only {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{available_space}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m of space left in the system: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mNo longer saving screenshots of the encounters...{RESET_FORMAT}'

THREAD_DIED_ERROR = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mThread {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{thread}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}m died: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}mShutting down program...{RESET_FORMAT}'

COULD_NOT_PLAY_SOUND = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not play sound: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m"{"{path}"}"{RESET_FORMAT}'

SHINY_FOUND = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mShiny {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{pokemon}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m found after {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{encounters}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m encounters!{RESET_FORMAT}'

STUCK_FOR_TOO_LONG_WARN_1 = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {"[{time}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mGot stuck in the {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{event}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m state for {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{seconds}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m seconds: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mTrying to restart the game...{RESET_FORMAT}'

STUCK_FOR_TOO_LONG_WARN_2 = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {"[{time}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mNo pokémon has been found for {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{minutes}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m minutes: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mTrying to restart the game...{RESET_FORMAT}'

STUCK_FOR_TOO_LONG_ERROR = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {"[{time}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mNo pokémon has been found for {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}m{"{minutes}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}m minutes: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}mStopping the program...{RESET_FORMAT}'

G_EMPTY_CREDENTIALS = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m{"{module}"} notifications cannot be sent: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mSome fields are missing in the {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m"{"{path}"}"{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m file{RESET_FORMAT}'

G_TOGGLING_NOTIFICATIONS = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m{"{module}"} notifications are disabled: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mRemember to enable them before running the shiny hunter{RESET_FORMAT}'

###########################################################################################################################
######################################################     MENU     #######################################################
###########################################################################################################################

M_SELECTED_OPTION = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mOption {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{option}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m selected: {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{action} "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Italics"]}m{"{path} "}{RESET_FORMAT}'

M_MENU = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSelection Menu:{RESET_FORMAT}'

M_MENU_OPTION = \
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m    [{"{index}"}] {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{option}"}{RESET_FORMAT}'

M_OPTION_SELECTION = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSelect an option: {RESET_FORMAT}'

M_INVALID_OPTION = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mInvalid option: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}mExiting the program...{RESET_FORMAT}'

###########################################################################################################################
###################################################     GAME CAPTURE     ##################################################
###########################################################################################################################

GC_INVALID_VIDEO_CAPTURE = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not access video capture {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}m{"{video_capture}"}{RESET_FORMAT}'

GC_AVAILABLE_CAPTURE_DEVICES = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mCapture devices found: {RESET_FORMAT}'
GC_CAPTURE_DEVICE_OK = \
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m    Video Capture nº{"{index}"}: {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}mOK{RESET_FORMAT}'
GC_CAPTURE_DEVICE_NOT_OK = \
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}m    Video Capture nº{"{index}"}: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}mNOT OK{RESET_FORMAT}'

GC_IMAGE_SAVED = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mImage saved: {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Italics"]}m{"{path}"}{RESET_FORMAT}'

GC_USING_DIFFERENT_CAPTURE_CARD = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not access video capture {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mnº{"{old_video_capture}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m. Connecting to video capture {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mnº{"{new_video_capture} "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}minstead...{RESET_FORMAT}'

GC_CAPTURE_CARD_LOST_CONNECTION = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture]"} {"[{time}]"} {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCapture card has been disconnected: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mPlease, reconnect it...{RESET_FORMAT}'

###########################################################################################################################
################################################     SWITCH CONTROLLER     ################################################
###########################################################################################################################

SC_NOT_LINUX_SYSTEM = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mNXBT is only available on Linux systems!{RESET_FORMAT}'

SC_NOT_SUDO = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mNXBT must be executed with administrator permissions: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}mRestarting using sudo...{RESET_FORMAT}'

SC_RESTARTING_BLUETOOTH = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mRestarting bluetooth systems...{RESET_FORMAT}'

SC_BLUETOOTH_RESTARTED = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mBluetooth restarted successfully!{RESET_FORMAT}'

SC_CONNECTING_TO_SWITCH = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mConnecting to Nintendo Switch...{RESET_FORMAT}'

SC_CONTROLLER_CONNECTED = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Switch Controller] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mController connected!{RESET_FORMAT}'

###########################################################################################################################
###################################################     FPS COUNTER     ###################################################
###########################################################################################################################

FPS_COUNTER = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[FPS Counter] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mFPS: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{current_fps}"}     {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mMax FPS: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{max_fps}"}     {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mMin FPS: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{min_fps}"}     {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mAverage FPS (last 100): {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{average_fps}"}     {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mRAM Usage: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{memory_usage} MB"}     {RESET_FORMAT}'

FPS_SYSTEM_AVAILABLE_SPACE = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[FPS Counter] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mTotal system space: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{total_space}"}     {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mUsed System Space: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{used_space}"}     {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mAvailable System Space: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{available_space}"}     {RESET_FORMAT}'

FPS_DIRECTORY_SIZE = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[FPS Counter] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSize of {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Italics"]}m{"{directory}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{size}"}{RESET_FORMAT}'

###########################################################################################################################
#################################################     IMAGE PROCESSING     ################################################
###########################################################################################################################

IP_SUCCESSFULLY_EXTRACTED_FRAMES = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully extracted {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{frames}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m frames!{RESET_FORMAT}'

IP_SUCCESSFULLY_LOADED_IMAGES = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully loaded {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{images}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m images!{RESET_FORMAT}'

IP_SUCCESSFULLY_DELETED_IMAGES = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully deleted {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{images}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m images!{RESET_FORMAT}'

IP_CURRENT_EXTRACTED_FRAMES = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mCurrently extracted {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{extracted_frame}"}/{"{total_frames}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m frames {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m({"{percentage}"}%){RESET_FORMAT}'

IP_DELETE_IMAGES_QUESTION = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mDo you want to delete all the images [Y/n]? {RESET_FORMAT}'

IP_DELETING_IMAGES = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mDeleting {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{images}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m images...{RESET_FORMAT}'

IP_COULD_NOT_LOAD_IMAGE = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not load image: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{path}"}{RESET_FORMAT}'

IP_NO_IMAGES_IN_FOLDER = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not find any image on: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{path}"}{RESET_FORMAT}'

###########################################################################################################################
#####################################################     DATABASE     ####################################################
###########################################################################################################################

DB_INITIALIZE_DATABASE = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully initialized database!{RESET_FORMAT}'

DB_DATABASE_INFO = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mDatabase Stats: {RESET_FORMAT}'

DB_DATABASE_STAT_VALUE = \
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m\t{"{stat}"}: {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{value}"}{RESET_FORMAT}'

DB_SELECT_POKEMON_TO_DELETE = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mWrite the pokémon you want to delete from the database: {RESET_FORMAT}'

DB_COULD_NOT_DELETE_POKEMON = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not delete pokémon: {RESET_FORMAT}'+\
    f'\033[{COLORS["Red"]}m{"{pokemon}"}{RESET_FORMAT}'

DB_ASK_POKEMON_TO_DELETE = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mAre you sure you want to permanently delete {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{pokemon}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m from the database? This action cannot be undone. (y/N): {RESET_FORMAT}'

DB_DELETION_CANCELLED = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mPokémon deletion cancelled.{RESET_FORMAT}'

DB_POKEMON_DELETED = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Database] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mPokémon {RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]}m{"{pokemon}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m deleted {RESET_FORMAT}'

###########################################################################################################################
#######################################################     GUI     #######################################################
###########################################################################################################################

GUI_COULD_NOT_LOAD_IMAGE = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[GUI] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not load image: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{path}"}{RESET_FORMAT}'

###########################################################################################################################
######################################################     EMAIL     ######################################################
###########################################################################################################################

EM_HTML_NOT_FOUND = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Mail] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not find HTML: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}m{"{html}"}{RESET_FORMAT}'

EM_EMAIL_SENT = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Mail] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully sent email to {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{email}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m!{RESET_FORMAT}'

EM_COULD_NOT_SEND_EMAIL = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Mail] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not send email to {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{email}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{error}"}{RESET_FORMAT}'

###########################################################################################################################
#####################################################     TELEGRAM     ####################################################
###########################################################################################################################

TE_TELEGRAM_SENT = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Telegram] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully sent telegram to chat {RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]}m{"{chat_id}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m!{RESET_FORMAT}'

TE_COULD_NOT_SEND_TELEGRAM = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Telegram] "}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not send telegram to chat {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{chat_id}"}{RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}m: {RESET_FORMAT}'+\
    f'\033[{COLORS["Yellow"]}m{"{error}"}{RESET_FORMAT}'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__': 
    print("\n\t" + INFO, CORRECT, WARN, ERROR + "\n")