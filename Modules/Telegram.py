import requests
from . import MessageSender

SHINY_FOUND_MESSAGE = "A shiny {pokemon_name} has been found!"
ERROR_MESSAGE = "An error has been detected: {error_message}"

class TelegramSender(MessageSender):
    """
    Class for sending messages via Telegram.
    """

    def __init__(self, config: dict):
        """
        Initializes the TelegramSender.
        """
        self.__bot_token = config.get('bot_token')
        self.__chat_id = config.get('chat_id')

    def send_shiny_found(self, pokemon_name: str, image_path: str):
        url = f"https://api.telegram.org/bot{self.__bot_token}/sendPhoto"
        caption = SHINY_FOUND_MESSAGE.format(pokemon_name=pokemon_name)

        # Open the image file in binary mode
        with open(image_path, 'rb') as photo:
            # Create a dictionary for the payload
            payload = {
                'chat_id': self.__chat_id,
                'caption': caption  # Add the caption parameter
            }
            # Create a files dictionary to send the image
            files = {
                'photo': photo
            }

            # Send the POST request
            requests.post(url, data=payload, files=files, timeout=1)

    def send_failure_detected(self, error_message: str):
        url = f"https://api.telegram.org/bot{self.__bot_token}/sendMessage?chat_id={self.__chat_id}&text={content}"
        content = ERROR_MESSAGE.format(error_message=error_message)

        # Send the message
        requests.get(url, timeout=1)
            