###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
from random import randint

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import Constants as CONST
import Modules.Colored_Strings as STR
from Modules.Telegram.Telegram import Telegram_Sender

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Telegram'

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":

    def main_menu():
        print('\n' + STR.M_MENU.format(module=MODULE_NAME))
        print(STR.M_MENU_OPTION.format(index='1', option='Send shiny notification'))
        print(STR.M_MENU_OPTION.format(index='2', option='Send error notifications'))

        option = input('\n' + STR.M_OPTION_SELECTION.format(module=MODULE_NAME))

        menu_options = {
            '1': send_telegram,
            '2': send_telegram,
        }

        if option in menu_options: menu_options[option](option)
        else: print(STR.M_INVALID_OPTION.format(module=MODULE_NAME) + '\n')

    #######################################################################################################################
    #######################################################################################################################

    def send_telegram(option):
        if option == '1':
            action = 'shiny'
        elif option == '2':
            action = 'error'

        print('\n' + STR.M_SELECTED_OPTION.format(
            module=MODULE_NAME,
            option=option,
            action=f"Sending {action} notifications",
            path=''
        ))

        if not CONST.TELEGRAM_NOTIFICATIONS:
            print(STR.G_TOGGLING_NOTIFICATIONS.format(module=MODULE_NAME))
            CONST.TELEGRAM_NOTIFICATIONS = True

        Telegram = Telegram_Sender()
        if option == '1':
            Telegram.send_shiny_found('Dinones', None, randint(1, 10000))
        if option == '2': 
            Telegram.send_error_detected('STUCK')
            Telegram.send_error_detected('THREAD_DIED', 'GUI_control')

    #######################################################################################################################
    #######################################################################################################################

    main_menu()
    print()