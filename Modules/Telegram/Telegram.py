###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import requests
from dotenv import load_dotenv

import sys
folders = ['../', '../../']
for folder in folders: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))

import Constants as CONST
import Colored_Strings as COLOR_str

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

SHINY_FOUND_MESSAGE = "A shiny {pokemon_name} has been found!"
ERROR_MESSAGE = \
    f"Shiny Hunter has been more than {CONST.FAILURE_DETECTION_TIME//60} minutes without encountering any Pokémon."

###########################################################################################################################

SAVE_ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 
    f"../../{CONST.TELEGRAM_SETTINGS.get('save_credentials_file_path')}"))

###########################################################################################################################

class Telegram_Sender():
    def __init__(self) -> None:

        """
            Initializes the Telegram sender
        """

        if not CONST.TELEGRAM_NOTIFICATIONS: return

        self._protect_credentials()
        load_dotenv(SAVE_ENV_FILE_PATH)

        self.__bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.__chat_id = os.getenv('TELEGRAM_CHAT_ID')

        # Will not raise any error if credentials are wrong or missing, it will just skip the email sending
        if not self._check_valid_credentials:
            print(COLOR_str.EMPTY_CREDENTIALS
                .replace('{module}', 'Telegram')
                .replace('{path}', SAVE_ENV_FILE_PATH)
            )

    #######################################################################################################################

    def _check_valid_credentials(self):
        return all((isinstance(field, str) and field != '') for field in [self.__bot_token, self.__chat_id])

    #######################################################################################################################

    def _protect_credentials(self):

        """
            Prevent credentials from being accidentally pushed to the remote repository by renaming the credentials file
        """

        ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
            f"../../{CONST.TELEGRAM_SETTINGS.get('credentials_file_path')}"))
        TEMPLATE_ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
            f"../../{CONST.TELEGRAM_SETTINGS.get('credentials_template_file_path')}"))

        # SAVE_ENV_FILE_PATH is included in the .gitignore file so it will never be pushed to the remothe GitHub repository
        if os.path.exists(ENV_FILE_PATH) and not os.path.exists(SAVE_ENV_FILE_PATH): 
            os.rename(ENV_FILE_PATH, SAVE_ENV_FILE_PATH)
        if os.path.exists(TEMPLATE_ENV_FILE_PATH) and not os.path.exists(ENV_FILE_PATH): 
            with open(TEMPLATE_ENV_FILE_PATH, 'rb') as src_file:
                with open(ENV_FILE_PATH, 'wb') as dest_file:
                    dest_file.write(src_file.read())

    #######################################################################################################################

    def _send_telegram(self, text, image_path):
        url = f"https://api.telegram.org/bot{self.__bot_token}/sendPhoto"

        payload = {
            'chat_id': self.__chat_id,
            'caption': text,
            'text': text
        }

        files = {}
        if not os.path.exists(image_path):
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                f'../../{CONST.MESSAGES_PLACEHOLDER_IMAGE}'))
        try:
            with open(image_path, 'rb') as image:
                files['photo'] = image
                requests.post(url, data=payload, files=files, timeout=1)
        except:
            try:
                url = f"https://api.telegram.org/bot{self.__bot_token}/sendMessage"
                requests.post(url, data=payload, timeout=1)
            except Exception as error:
                print(COLOR_str.COULD_NOT_SEND_TELEGRAM
                    .replace('{chat_id}', self.__chat_id)
                    .replace('{error}', str(error))
                )
                return

        print(COLOR_str.TELEGRAM_SENT.replace('{chat_id}', self.__chat_id))

    #######################################################################################################################

    def send_shiny_found(self, pokemon_name: str, image_name: str) -> None:
        if not CONST.TELEGRAM_NOTIFICATIONS or not self._check_valid_credentials(): return

        text = SHINY_FOUND_MESSAGE.format(pokemon_name=pokemon_name)
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{image_name}'))
        self._send_telegram(text, image_path)

    #######################################################################################################################

    def send_error_detected(self) -> None:
        if not CONST.TELEGRAM_NOTIFICATIONS or not self._check_valid_credentials(): return

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{CONST.MESSAGES_ERROR_IMAGE}'))
        self._send_telegram(ERROR_MESSAGE, image_path)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Telegram'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Send shiny notification'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Send error notification'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Telegram'))

        menu_options = {
            '1': send_telegram,
            '2': send_telegram,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Mail') + '\n')

    #######################################################################################################################

    def send_telegram(option):
        if option == '1': action = 'shiny'
        elif option == '2': action = 'error'
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Telegram')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Sending {action} notification")
            .replace('{path}', '')
        )

        Telegram = Telegram_Sender()
        if option == '1': Telegram.send_shiny_found('Dinones', None)
        if option == '2': Telegram.send_error_detected()
        print()

    #######################################################################################################################

    main_menu()