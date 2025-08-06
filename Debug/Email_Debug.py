###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
from random import randint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
import Modules.Colored_Strings as STR
from Modules.Email.Email import Email_Sender

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Email'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

def main_menu():
    print('\n' + STR.M_MENU.format(module=MODULE_NAME).format(module=MODULE_NAME))
    print(STR.M_MENU_OPTION.format(index = '1', option = 'Send shiny notification'))
    print(STR.M_MENU_OPTION.format(index = '2', option = 'Send error notifications (all errors)'))

    option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

    menu_options = {
        '1': _send_email,
        '2': _send_email,
    }

    if option in menu_options: menu_options[option](option)
    else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME) + '\n')

###########################################################################################################################
###########################################################################################################################

def _send_email(option: str) -> None:

    """
    Sends a test email notification based on the given option.

    - Option '1' triggers a shiny found notification.
    - Option '2' sends both a "stuck" and "thread died" error notification.

    Args:
        option (str): Email type to send. Must be '1' (shiny) or '2' (error).

    Returns:
        None
    """

    if option == '1':
        action = 'shiny'
    elif option == '2':
        action = 'error'

    print('\n' + STR.M_SELECTED_OPTION.format(
        module=MODULE_NAME,
        option=option,
        action=f"Sending {action} notification(s)",
        path=''
    ))

    if not CONST.MAIL_NOTIFICATIONS:
        print(STR.G_TOGGLING_NOTIFICATIONS.format(module=MODULE_NAME))
        CONST.MAIL_NOTIFICATIONS = True

    Email = Email_Sender()

    if option == '1':
        Email.send_shiny_found('Dinones', '', randint(1, 10000))
    elif option == '2':
        Email.send_error_detected('STUCK')
        Email.send_error_detected('THREAD_DIED', 'controller_control')

###########################################################################################################################
###########################################################################################################################

main_menu()
print()