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

SHINY_FOUND_MESSAGE = "A shiny <b>{pokemon_name}</b> has been found! It took <b>{n_encounters}</b> encounters to find it."

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
            'text': text,
            'parse_mode': 'HTML'
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

    def send_shiny_found(self, pokemon_name: str, image_name: str, n_encounters: int) -> None:
        if not CONST.TELEGRAM_NOTIFICATIONS or not self._check_valid_credentials(): return

        text = SHINY_FOUND_MESSAGE.replace('{pokemon_name}', pokemon_name).replace('{n_encounters}', str(n_encounters))
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{image_name}'))
        self._send_telegram(text, image_path)

    #######################################################################################################################

    def send_error_detected(self, error_type: str = str(), died_thread: str = str()) -> None:
        """
            Sends an error notification when the program has encountered an error. This message is only sent to the 
            primary recipient of the email
            Args: 
                error_type (Optional(str)): Can be "STUCK" or "THREAD_DIED"
                died_thread (Optional(str)): Name of the thread that has died
            Output: None
        """
        if not CONST.TELEGRAM_NOTIFICATIONS or not self._check_valid_credentials(): return

        error_message = "<b>⚠️ Error Detected! ⚠️</b>\n\n"
        if error_type == "STUCK":
            error_message += f"Shiny Hunter has been more than <b>{str(CONST.FAILURE_DETECTION_TIME_ERROR//60)} " +\
                "minutes</b> without encountering any Pokémon."
        elif error_type == "THREAD_DIED":
            error_message += f"Thread <b>{died_thread}</b> died."
        error_message += '\n\nIf the error persists, please report it on <a href="https://github.com/Dinones/Nintendo-' +\
            'Switch-Pokemon-Shiny-Hunter/issues">Github</a> or <a href="https://discordapp.com/users/177131156028784640 '+\
            '">Discord</a>.'

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{CONST.MESSAGES_ERROR_IMAGE}'))
        self._send_telegram(error_message, image_path)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    from random import randint

    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Telegram'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Send shiny notification'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Send error notifications'))

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
            .replace('{action}', f"Sending {action} notifications")
            .replace('{path}', '')
        )

        Telegram = Telegram_Sender()
        if option == '1': Telegram.send_shiny_found('Dinones', None, randint(1, 10000))
        if option == '2': 
            Telegram.send_error_detected('STUCK')
            Telegram.send_error_detected('THREAD_DIED', 'GUI_control')
        print()

    #######################################################################################################################

    main_menu()