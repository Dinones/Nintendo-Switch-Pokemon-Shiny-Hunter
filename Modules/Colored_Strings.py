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

INVALID_PATH = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mInvalid path: \033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{path}"}\n\033[0;m'

###########################################################################################################################
######################################################     MENU     #######################################################
###########################################################################################################################

MENU = \
    f'\n{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSelection Menu: \n    \033[0;m'+\
    f'\033[{COLORS["Blue"]}m{"{options}"}\033[0;m'

OPTION_SELECTION = \
    f'\n{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mSelect an option: \033[0;m'

INVALID_OPTION = \
    f'\n{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mInvalid option: \033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}mExiting the program...\n\033[0;m'

SELECTED_OPTION = \
    f'\n{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[{module}] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mOption selected: \033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Italics"]}m{"{action}"}\033[0;m'

###########################################################################################################################
###################################################     GAME CAPTURE     ##################################################
###########################################################################################################################

INVALID_VIDEO_CAPTURE = \
    f'{ERROR}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Game Capture] "}\033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Bold"]}mCould not access to the video capture \033[0;m'+\
    f'\033[{COLORS["Red"]};{SPECIAL["Italics"]}m{"{video_capture}"}\n\033[0;m'

###########################################################################################################################
#################################################     IMAGE PROCESSING     ################################################
###########################################################################################################################

COULD_NOT_PROCESS_IMAGE = \
    f'{WARN}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Bold"]}mCould not process image: \033[0;m'+\
    f'\033[{COLORS["Yellow"]};{SPECIAL["Italics"]}mSkipping frame...\n\033[0;m'

SUCCESSFULLY_EXTRACTED_FRAMES = \
    f'{CORRECT}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}mSuccessfully extracted \033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Italics"]}m{"{frames}"}\033[0;m'+\
    f'\033[{COLORS["Green"]};{SPECIAL["Bold"]}m frames!\n\033[0;m'

CONTOURS_FOUND = \
    f'{INFO}\033[{SPECIAL["Bold"]};{COLORS["Magenta"]}m{"[Image Processing] "}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}mFound \033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Italics"]}m{"{contours}"}\033[0;m'+\
    f'\033[{COLORS["Blue"]};{SPECIAL["Bold"]}m contours!\033[0;m'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__': 
    print("\n\t" + INFO, CORRECT, WARN, ERROR + "\n")