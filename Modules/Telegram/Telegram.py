###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
import requests
from typing import Optional
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import Constants as CONST
import Modules.Colored_Strings as STR

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

SHINY_FOUND_MESSAGE = "A shiny <b>{pokemon_name}</b> has been found! It took <b>{n_encounters}</b> encounters to find it."
ERROR_DETECTED_MESSAGE = (
    '<b>⚠️ Error Detected! ⚠️</b>\n\n{reason}\n\nIf the error persists, please report it on '
    '<a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/issues">GitHub</a> '
    'or <a href="https://discordapp.com/users/177131156028784640">Discord</a>.'
)

###########################################################################################################################
###########################################################################################################################

MODULE_NAME = 'Telegram'

CREDENTIALS_ENV_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../', CONST.TELEGRAM_SETTINGS.get('credentials_file_path'))
)

###########################################################################################################################
###########################################################################################################################

class Telegram_Sender():
    def __init__(self) -> None:

        """
        Initialize the Telegram sender and check if credentials are not empty.

        Args:
            None

        Output:
            None
        """

        if not CONST.TELEGRAM_NOTIFICATIONS: return

        self._generate_credentials_file()
        load_dotenv(CREDENTIALS_ENV_FILE_PATH)

        self.__bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.__chat_id = os.getenv('TELEGRAM_CHAT_ID')

        # Will not raise any error if credentials are wrong or missing, it will just skip the telegram sending
        if not self._check_valid_credentials():
            print(STR.G_EMPTY_CREDENTIALS.format(module=MODULE_NAME, path=CREDENTIALS_ENV_FILE_PATH))

    #######################################################################################################################
    #######################################################################################################################

    def send_shiny_found(self, pokemon_name: str, image_name: str, n_encounters: int) -> None:

        """
        Sends a Telegram notification when a shiny Pokémon is found. If Telegram notifications are disabled or credentials
        are invalid, the message is not sent.

        Args:
            pokemon_name (str): Name of the shiny Pokémon found.
            image_name (str): Relative path to the shiny Pokémon image.
            n_encounters (int): Number of encounters it took to find the shiny.

        Returns:
            None
        """

        if not CONST.TELEGRAM_NOTIFICATIONS or not self._check_valid_credentials():
            return

        text = SHINY_FOUND_MESSAGE.format(pokemon_name=pokemon_name, n_encounters=str(n_encounters))
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{image_name}'))

        self._send_telegram(text, image_path)

    #######################################################################################################################
    #######################################################################################################################

    def send_error_detected(self, error_type: Optional[str] = '', died_thread: Optional[str] = '') -> None:

        """
        Sends a Telegram notification when an error is detected. The message includes the reason for failure and links to
        GitHub/Discord for reporting.

        Args:
            error_type (Optional[str]): Can be "STUCK" or "THREAD_DIED".
            died_thread (Optional[str]): Name of the thread that died (used if error_type is "THREAD_DIED").

        Returns:
            None
        """

        if not CONST.TELEGRAM_NOTIFICATIONS or not self._check_valid_credentials():
            return

        error_message = ERROR_DETECTED_MESSAGE

        if error_type == "STUCK":
            minutes = CONST.FAILURE_DETECTION_TIME_ERROR // 60
            reason = f"Shiny Hunter has been more than <b>{minutes} minutes</b> without encountering any Pokémon."
        elif error_type == "THREAD_DIED":
            reason = f"Thread <b>{died_thread}</b> died."
        error_message = error_message.format(reason=reason)

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{CONST.MESSAGES_ERROR_IMAGE}'))
        self._send_telegram(error_message, image_path)
    
    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def _generate_credentials_file() -> None:

        """
        Generates the Telegram credentials file "Credentials.env" from a template if it doesn't already exist.

        Args:
            None

        Returns:
            None
        """

        if not os.path.exists(CREDENTIALS_ENV_FILE_PATH):
            TEMPLATE_ENV_FILE_PATH = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '../../', CONST.TELEGRAM_SETTINGS.get('credentials_template_file_path')
            ))
            with open(TEMPLATE_ENV_FILE_PATH, 'rb') as src_file, open(CREDENTIALS_ENV_FILE_PATH, 'wb') as dest_file:
                    dest_file.write(src_file.read())
    
    #######################################################################################################################
    #######################################################################################################################

    def _check_valid_credentials(self):
        return all((isinstance(field, str) and field.strip() != '') for field in [self.__bot_token, self.__chat_id])

    #######################################################################################################################
    #######################################################################################################################

    def _send_telegram(self, text: str, image_path: Optional[str]) -> None:

        """
        Sends a message to a Telegram chat, attaching the image. If the image is not found, a placeholder is used. Falls
        back to sending a plain text message if the photo request fails.

        Args:
            text (str): Message content to send (can include HTML formatting).
            image_path (Optional[str]): Path to the image to attach.

        Returns:
            None
        """

        photo_url = f"https://api.telegram.org/bot{self.__bot_token}/sendPhoto"
        message_url = f"https://api.telegram.org/bot{self.__bot_token}/sendMessage"

        payload = {
            'chat_id': self.__chat_id,
            'caption': text,
            'text': text, # Only used for fallback in case the image fails to load
            'parse_mode': 'HTML'
        }

        # Fallback to placeholder image if needed
        if not os.path.exists(image_path or ''):
            image_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), f'../../{CONST.MESSAGES_PLACEHOLDER_IMAGE}'
            ))

        try:
            with open(image_path, 'rb') as image_file:
                files = {'photo': image_file}
                requests.post(photo_url, data=payload, files=files, timeout=1)
        except Exception:
            # Fallback to text message
            try:
                requests.post(message_url, data=payload, timeout=1)
            except Exception as error:
                print(STR.TE_COULD_NOT_SEND_TELEGRAM.format(chat_id=self.__chat_id, error=str(error)))
                return

        print(STR.TE_TELEGRAM_SENT.format(chat_id=self.__chat_id))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == '__main__':
    import Debug.Telegram_Debug