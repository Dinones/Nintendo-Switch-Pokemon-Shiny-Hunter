###########################################################################################################################
####################################################     LIBRARIES     ####################################################
###########################################################################################################################

# Set the cwd to the one of the file
import os
if __name__ == '__main__':
    try: os.chdir(os.path.dirname(__file__))
    except: pass

from dotenv import load_dotenv

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

import sys
folders = ['../', '../../']
for folder in folders: sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))

import Constants as CONST
import Colored_Strings as COLOR_str

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

SAVE_ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
    f"../../{CONST.MAIL_SETTINGS.get('save_credentials_file_path')}"))
SHINY_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{CONST.SHINY_HTML_PATH}'))
ERROR_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{CONST.ERROR_HTML_PATH}'))

###########################################################################################################################

class Email_Sender():
    def __init__(self) -> None:

        """
            Initializes the Email_Sender and checks for errors
            Args: None
            Output: None
        """

        if not CONST.MAIL_NOTIFICATIONS: return

        self._protect_credentials()
        # Will not raise an error if file not found
        load_dotenv(SAVE_ENV_FILE_PATH)

        self.__email_sender = os.getenv("EMAIL_SENDER")
        self.__password = os.getenv('EMAIL_APP_PASSWORD')
        self.__email_receiver = os.getenv('EMAIL_RECEIVER')
        self.__email_receiver_2 = os.getenv('EMAIL_RECEIVER_2')

        self.__port = CONST.MAIL_SETTINGS.get('port')
        self.__smtp_server = CONST.MAIL_SETTINGS.get('smtp_server')

        # Will not raise any error if credentials are wrong or missing, it will just skip the email sending
        if not self._check_valid_credentials():
            print(COLOR_str.EMPTY_CREDENTIALS
                .replace('{module}', 'Email')
                .replace('{path}', SAVE_ENV_FILE_PATH)
            )

    #######################################################################################################################

    def _check_valid_credentials(self):
        return all((isinstance(field, str) and field != '') 
            for field in [self.__email_sender, self.__password, self.__email_receiver])

    #######################################################################################################################
   
    def _craft_message(self, subject: str, content: str, receivers: dict) -> MIMEMultipart:

        """
            Creates a multipart email message with the given subject and content
            Args:
                subject (str): Contains the subject of the email
                content (str): Contains the content of the email
                receivers (dict): Contains all the email receivers. {'Primary':[], 'CC':[], 'BCC':[]}
            Output:
                message (MIMEMultipart): Object containing all the email information
        """
       
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.__email_sender
        message["To"] = ', '.join(receivers.get('Primary'))
        if receivers.get('CC'): message["Cc"] = ', '.join(receivers.get('CC'))
        message["Subject"] = subject

        # Attach the HTML part
        message.attach(MIMEText(content, "html"))

        return message

    #######################################################################################################################

    @staticmethod
    def _create_content_with_html(html_path: str, replace_info: dict) -> str:

        """
            Creates message content with the 
            Args:
                message (str): Path of the desired HTML
                replace_info (dict): Contains any extra information that may need to be replaced in the HTML file. 
                    For example, trainer name, pokémon name, etc.
            Output: 
                content (str): Message content containing the HTML. Empty string if HTML is not found
        """

        content = ''
        # If can't find the HTML, an empty email will be sent with the image attached to it
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as file: content = file.read()
            for key, text in replace_info.items(): content = content.replace(f'{{{key}}}', text)
        else: print(COLOR_str.HTML_NOT_FOUND.replace('{html}', html_path))

        return content

    #######################################################################################################################

    def _send_email(self, message: MIMEMultipart, receivers: list) -> None:

        """
            Sends an email using the provided message
            Args:
                message (MIMEMultipart): Object containing all the email information
                receivers (list): Contains all the email receivers [Primary + CC + BCC]
            Output: None
        """

        try:
            with SMTP(self.__smtp_server, self.__port) as server:
                server.starttls()
                server.login(self.__email_sender, self.__password)
                server.sendmail(self.__email_sender, receivers, message.as_string())
                print(COLOR_str.EMAIL_SENT.replace('{email}', receivers[0]))
        except Exception as error:
            print(COLOR_str.COULD_NOT_SEND_EMAIL.replace('{email}', receivers[0]).replace('{error}', str(error)))

    #######################################################################################################################

    @staticmethod
    def _protect_credentials() -> None:

        """
            Prevent credentials from being accidentally pushed to the remote repository by renaming the credentials file
            Args: None
            Output: None
        """

        ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
            f"../../{CONST.MAIL_SETTINGS.get('credentials_file_path')}"))
        TEMPLATE_ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
            f"../../{CONST.MAIL_SETTINGS.get('credentials_template_file_path')}"))

        # SAVE_ENV_FILE_PATH is included in the .gitignore file so it will never be pushed to the remothe GitHub repository
        if os.path.exists(ENV_FILE_PATH) and not os.path.exists(SAVE_ENV_FILE_PATH): 
            os.rename(ENV_FILE_PATH, SAVE_ENV_FILE_PATH)
        if os.path.exists(TEMPLATE_ENV_FILE_PATH) and not os.path.exists(ENV_FILE_PATH): 
            with open(TEMPLATE_ENV_FILE_PATH, 'rb') as src_file:
                with open(ENV_FILE_PATH, 'wb') as dest_file:
                    dest_file.write(src_file.read())

    #######################################################################################################################

    def send_shiny_found(self, pokemon_name: str, image_name: str, n_encounters: int) -> None:

        """
            Sends shiny found email notification
            Args:
                pokemon_name (str): Contains the pokémon name
                image_name (str): Contains the name of the image that is going to be attached
                n_encounters (int): Contains the number of encounters that it took to get the shiny
            Output: None
        """

        if not CONST.MAIL_NOTIFICATIONS or not self._check_valid_credentials(): return

        for index, receiver in enumerate([self.__email_receiver, self.__email_receiver_2]):
            if not receiver: continue

            replace_info = {
                'pokemon_name': pokemon_name,
                'trainer': receiver.split('@')[0].capitalize(),
                'n_encounters': str(n_encounters)
            }
            content = self._create_content_with_html(SHINY_HTML_PATH, replace_info)

            receivers = {'Primary': [receiver], 'CC': [], 'BCC': []}
            # Don't send duplicated copy mails to the sender
            if index == 0: receivers['BCC'] = [self.__email_sender]
            message = self._craft_message(f'[Pokémon Shiny Hunter] Shiny {pokemon_name} found!', content, receivers)

            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{image_name}'))
            if not image_name or not os.path.exists(image_path):
                image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                    f'../../{CONST.MESSAGES_PLACEHOLDER_IMAGE}'))

            try:
                with open(image_path, 'rb') as image:
                    image = MIMEImage(image.read())
                    # Content-ID must match src in HTML
                    image.add_header('Content-ID', '<shiny_pokemon_image>') 
                    message.attach(image)
            except: pass

            receivers = receivers.get('Primary') + receivers.get('CC') + receivers.get('BCC')
            self._send_email(message, receivers)

    #######################################################################################################################

    def send_error_detected(self, error_type: str = str(), died_thread: str = str()) -> None:

        """
            Sends an error email notification when the program has encountered an error. This message is only sent to the 
            primary recipient of the email
            Args: 
                error_type (Optional(str)): Can be "STUCK" or "THREAD_DIED"
                died_thread (Optional(str)): Name of the thread that has died
            Output: None
        """

        if not CONST.MAIL_NOTIFICATIONS or not self._check_valid_credentials(): return

        error_message = str()
        if error_type == "STUCK":
            error_message = f"Shiny Hunter has been more than <b>{str(CONST.FAILURE_DETECTION_TIME_ERROR//60)} " +\
                "minutes</b> without encountering any Pokémon."
        elif error_type == "THREAD_DIED":
            error_message = f"Thread <b>{died_thread}</b> died."

        replace_info = {
            'trainer': self.__email_receiver.split('@')[0].capitalize(),
            'error_message': error_message
        }
        content = self._create_content_with_html(ERROR_HTML_PATH, replace_info)

        receivers = {'Primary': [self.__email_receiver], 'CC': [], 'BCC': [self.__email_sender]}
        message = self._craft_message(f'[Pokémon Shiny Hunter] An error has occurred!', content, receivers)

        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{CONST.MESSAGES_ERROR_IMAGE}'))

        try:
            with open(image_path, 'rb') as image:
                image = MIMEImage(image.read())
                # Content-ID must match src in HTML
                image.add_header('Content-ID', '<error_image>') 
                message.attach(image)
        except: pass

        receivers = receivers.get('Primary') + receivers.get('CC') + receivers.get('BCC')
        self._send_email(message, receivers)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    from random import randint

    #######################################################################################################################

    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Mail'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Send shiny notification'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '2').replace('{option}', 'Send error notifications'))

        option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Mail'))

        menu_options = {
            '1': send_email,
            '2': send_email,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Mail') + '\n')

    #######################################################################################################################

    def send_email(option):
        if option == '1': action = 'shiny'
        elif option == '2': action = 'error'
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Mail')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Sending {action} notifications")
            .replace('{path}', '')
        )

        Email = Email_Sender()
        if option == '1': Email.send_shiny_found('Dinones', str(), randint(1, 10000))
        if option == '2': 
            Email.send_error_detected('STUCK',)
            Email.send_error_detected('THREAD_DIED', 'controller_control')
        print()

    #######################################################################################################################

    main_menu()