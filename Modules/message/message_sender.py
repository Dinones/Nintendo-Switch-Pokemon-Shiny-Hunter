from abc import ABC, abstractmethod


class MessageSender(ABC):
    """
    Abstract class for a message sender.
    """

    @abstractmethod
    def send_shiny_found(self, pokemon_name: str, image_path: str):
        """
        Sends a message to the user that a shiny Pokemon has been found.
        """
        pass

    @abstractmethod
    def send_failure_detected(self, error_message: str):
        """
        Sends a message to the user that an error has been detected.
        """
        pass
