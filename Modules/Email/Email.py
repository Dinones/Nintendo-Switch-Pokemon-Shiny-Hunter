###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

import os
import sys
from dotenv import load_dotenv
from typing import Optional, List, Dict

from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import Constants as CONST
import Modules.Colored_Strings as STR

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

MODULE_NAME = 'Email'

CREDENTIALS_ENV_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../', CONST.MAIL_SETTINGS.get('credentials_file_path'))
)
SHINY_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', CONST.SHINY_HTML_PATH))
ERROR_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', CONST.ERROR_HTML_PATH))

###########################################################################################################################
###########################################################################################################################

class Email_Sender():
    def __init__(self) -> None:

        """
        Initialize the Email_Sender and check if credentials are not empty.

        Args:
            None

        Output:
            None
        """

        if not CONST.MAIL_NOTIFICATIONS: return

        # Make sure the credentials file exist before continuing
        self._generate_credentials_file()
        load_dotenv(CREDENTIALS_ENV_FILE_PATH)

        self.__email_sender = os.getenv("EMAIL_SENDER")
        self.__password = os.getenv('EMAIL_APP_PASSWORD')
        self.__email_receiver = os.getenv('EMAIL_RECEIVER')
        self.__email_receiver_2 = os.getenv('EMAIL_RECEIVER_2')

        self.__port = CONST.MAIL_SETTINGS.get('port')
        self.__smtp_server = CONST.MAIL_SETTINGS.get('smtp_server')

        # Will not raise any error if credentials are wrong or missing, it will just skip the email sending
        if not self._check_valid_credentials():
            print(STR.G_EMPTY_CREDENTIALS.format(module=MODULE_NAME, path=CREDENTIALS_ENV_FILE_PATH))

    #######################################################################################################################
    #######################################################################################################################

    def send_shiny_found(self, pokemon_name: str, image_name: str, n_encounters: int) -> None:

        """
        Sends an email notification when a shiny Pokémon is found. The message includes an embedded image of the shiny
        Pokémon (or a placeholder if missing).

        Args:
            pokemon_name (str): Name of the shiny Pokémon found.
            image_name (str): Path to the image to attach in the email.
            n_encounters (int): Number of encounters it took to find the shiny.

        Returns:
            None
        """

        if not CONST.MAIL_NOTIFICATIONS or not self._check_valid_credentials():
            return

        for index, receiver in enumerate([self.__email_receiver, self.__email_receiver_2]):
            if not receiver:
                continue

            # Personalize content for each receiver
            replace_info = {
                'pokemon_name': pokemon_name,
                'trainer': receiver.split('@')[0].capitalize(),
                'n_encounters': str(n_encounters)
            }
            content = self._create_content_with_html(SHINY_HTML_PATH, replace_info)

            receivers = {'Primary': [receiver], 'CC': [], 'BCC': []}
            # Copies the email sender only for the first email
            if index == 0:
                receivers['BCC'] = [self.__email_sender]

            subject = f"[Pokémon Shiny Hunter] Shiny {pokemon_name} found!"
            message = self._craft_message(subject, content, receivers)

            # Resolve and validate image path
            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', image_name))
            if not image_name or not os.path.exists(image_path):
                image_path = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), '../../', CONST.MESSAGES_PLACEHOLDER_IMAGE
                ))

            # Try to attach image to the email
            try:
                with open(image_path, 'rb') as image_file:
                    image = MIMEImage(image_file.read())
                    image.add_header('Content-ID', '<shiny_pokemon_image>')
                    message.attach(image)
            except Exception:
                pass

            # Flatten receiver list for sending
            all_receivers = (receivers.get('Primary', []) + receivers.get('CC', []) + receivers.get('BCC', []))
            self._send_email(message, all_receivers)

    #######################################################################################################################
    #######################################################################################################################

    def send_error_detected(self, error_type: Optional[str] = '', died_thread: Optional[str] = '') -> None:

        """
        Sends an email alert when an error is detected in the program execution. This notification is only sent to the
        primary recipient.

        Args:
            error_type (Optional[str]): The type of error. Accepts:
                - "STUCK": No encounters detected for an extended period.
                - "THREAD_DIED": A thread has stopped unexpectedly.
            died_thread (Optional[str]): Name of the thread that died (if applicable).

        Returns:
            None
        """

        if not CONST.MAIL_NOTIFICATIONS or not self._check_valid_credentials():
            return

        # Generate dynamic HTML error message
        if error_type == "STUCK":
            error_message = (
                f"Shiny Hunter has been more than <b>{CONST.FAILURE_DETECTION_TIME_ERROR // 60} minutes</b> "
                "without encountering any Pokémon."
            )
        elif error_type == "THREAD_DIED":
            error_message = f"Thread <b>{died_thread}</b> died."
        else:
            error_message = "An unknown error has occurred."

        replace_info = {
            'trainer': self.__email_receiver.split('@')[0].capitalize(),
            'error_message': error_message
        }
        content = self._create_content_with_html(ERROR_HTML_PATH, replace_info)

        receivers = {'Primary': [self.__email_receiver], 'CC': [], 'BCC': [self.__email_sender]}
        subject = '[Pokémon Shiny Hunter] An error has occurred!'
        message = self._craft_message(subject, content, receivers)

        # Load error image for the email
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', CONST.MESSAGES_ERROR_IMAGE))

        try:
            with open(image_path, 'rb') as image_file:
                image = MIMEImage(image_file.read())
                image.add_header('Content-ID', '<error_image>')
                message.attach(image)
        except Exception:
            pass

        all_receivers = receivers.get('Primary', []) + receivers.get('CC', []) + receivers.get('BCC', [])
        self._send_email(message, all_receivers)

    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def _generate_credentials_file() -> None:

        """
        Generates the mail credentials (.env) file from a template if it doesn't already exist.

        Args:
            None

        Returns:
            None
        """

        if not os.path.exists(CREDENTIALS_ENV_FILE_PATH):
            TEMPLATE_ENV_FILE_PATH = os.path.abspath(os.path.join(
                os.path.dirname(__file__), '../../', CONST.MAIL_SETTINGS.get('credentials_template_file_path')
            ))
            with open(TEMPLATE_ENV_FILE_PATH, 'rb') as src_file, open(CREDENTIALS_ENV_FILE_PATH, 'wb') as dest_file:
                    dest_file.write(src_file.read())
    
    #######################################################################################################################
    #######################################################################################################################

    def _check_valid_credentials(self) -> bool:

        """
        Checks whether the stored email credentials are valid strings. Returns True only if all required fields are
        non-empty strings.

        Args:
            None

        Returns:
            bool: True if all credential fields are valid, False otherwise.
        """

        return all(
            isinstance(field, str) and field != ''
                for field in (self.__email_sender, self.__password, self.__email_receiver)
        )

    #######################################################################################################################
    #######################################################################################################################
   
    def _craft_message(self, subject: str, content: str, receivers: Dict[str, List[str]]) -> MIMEMultipart:
   
        """
            Creates a multipart email message with HTML content and properly assigned recipients.

            Args:
                subject (str): Subject of the email.
                content (str): HTML content for the email body.
                receivers (Dict[str, List[str]]): Dictionary containing recipient lists. Expected keys: 'Primary', 'CC' and
                    'BCC'.

            Returns:
                MIMEMultipart: The composed email message object ready to be sent.
        """

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.__email_sender
        message["To"] = ', '.join(receivers.get('Primary', []))

        if receivers.get('CC'):
            message["Cc"] = ', '.join(receivers.get('CC'))

        message["Subject"] = subject

        # Attach the HTML body
        message.attach(MIMEText(content, "html"))

        return message

    #######################################################################################################################
    #######################################################################################################################

    @staticmethod
    def _create_content_with_html(html_path: str, replace_info: Dict[str, str]) -> str:

        """
        Loads an HTML file and replaces placeholders with provided values. Placeholders in the HTML must be in the format
        {KEY} to be replaced.

        Args:
            html_path (str): Path to the HTML template file.
            replace_info (Dict[str, str]): Dictionary of replacements for placeholders.

        Returns:
            str: The final HTML content with applied replacements. Returns an empty string if the file does not exist.
        """

        content = ''
        
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as file:
                content = file.read()
            for key, value in replace_info.items():
                content = content.replace(f'{{{key}}}', value)
        else:
            print(STR.EM_HTML_NOT_FOUND.format(html=html_path))

        return content

    #######################################################################################################################
    #######################################################################################################################

    def _send_email(self, message: MIMEMultipart, receivers: List[str]) -> None:

        """
        Sends an email using the configured SMTP server with the given message and recipients.

        Args:
            message (MIMEMultipart): The full email content including headers and body.
            receivers (List[str]): All recipient email addresses (To, CC, BCC).

        Returns:
            None
        """

        try:
            with SMTP(self.__smtp_server, self.__port) as server:
                server.starttls()
                server.login(self.__email_sender, self.__password)
                server.sendmail(self.__email_sender, receivers, message.as_string())
                print(STR.EM_EMAIL_SENT.format(email=receivers[0]))
        except Exception as error:
            print(STR.EM_COULD_NOT_SEND_EMAIL.format(email=receivers[0], error=str(error)))

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################
