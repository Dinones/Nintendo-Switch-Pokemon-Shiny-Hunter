from abc import ABC, abstractmethod


class MessageSender(ABC):
    """
    Abstract class for a message sender.
    """

    @abstractmethod
    def send_shiny_found(self, pokemon_name: str, image_path: str):
        """
        Sends a message to the user that a shiny Pokemon has been found.
        param pokemon_name: The name of the shiny Pokemon.
        param image_path: The path to the image of the shiny Pokemon. Can be None.
        """
        pass

    @abstractmethod
    def send_failure_detected(self, error_message: str):
        """
        Sends a message to the user that an error has been detected.
        """
        pass

class DefaultMessageSender(MessageSender):
    """
    Class for sending messages to the console.
    """

    def send_shiny_found(self, pokemon_name: str, image_path: str):
        print(f'Shiny {pokemon_name} found! Image saved at {image_path}')

    def send_failure_detected(self, error_message: str):
        print(f'Error detected: {error_message}')
