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
import os

import sys
folders = ['../', '../../']
for folder in folders:  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), folder)))

import Constants as CONST
import Colored_Strings as COLOR_str

###########################################################################################################################
#################################################     INITIALIZATIONS     #################################################
###########################################################################################################################

ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
    f"../../{CONST.MAIL_SETTINGS.get('credentials_file_path')}"))
SAVE_ENV_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
    f"../../{CONST.MAIL_SETTINGS.get('save_credentials_file_path')}"))
SHINY_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../{CONST.SHINY_HTML_PATH}'))

# This line will prevent credentials from being accidentally pushed
# SAVE_ENV_FILE_PATH is included in the .gitignore file so it will never be pushed to the remothe GitHub repository
if os.path.exists(ENV_FILE_PATH) and not os.path.exists(SAVE_ENV_FILE_PATH): os.rename(ENV_FILE_PATH, SAVE_ENV_FILE_PATH)

###########################################################################################################################

class Email_Sender():
    def __init__(self) -> None:

        """
            Initializes the Email_Sender and checks for errors.
        """

        load_dotenv(SAVE_ENV_FILE_PATH)

        self.__email_sender = os.getenv("EMAIL_SENDER")
        self.__password = os.getenv('EMAIL_APP_PASSWORD')
        self.__email_receiver = os.getenv('EMAIL_RECEIVER')
        self.__email_receiver_2 = os.getenv('EMAIL_RECEIVER_2')

        self.__port = CONST.MAIL_SETTINGS.get('port')
        self.__smtp_server = CONST.MAIL_SETTINGS.get('smtp_server')

        if not all(field != '' for field in [self.__email_sender, self.__password, self.__email_receiver]):
            print(COLOR_str.EMPTY_CREDENTIALS.replace('{path}', SAVE_ENV_FILE_PATH))

    #######################################################################################################################
   
    def _create_message(self, subject: str, content: str, receivers: dict) -> MIMEMultipart:

        """
            Creates a multipart email message with the given subject and content.
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

    def _send_email(self, message: MIMEMultipart, receivers: list) -> None:

        """
            Sends an email using the provided message.
            Args:
                message (MIMEMultipart): Object containing all the email information
                receivers (list): Contains all the email receivers [Primary + CC + BCC]
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

    def send_shiny_found(self, pokemon_name: str, image_name: str):

        """
            Sends shiny found email notification.
            Args:
                pokemon_name (str): Contains the pokémon name
                image_name (str): Contains the name of the image that is going to be attached
        """

        for index, receiver in enumerate([self.__email_receiver, self.__email_receiver_2]):
            if not receiver: continue

            content = ''
            if os.path.exists(SHINY_HTML_PATH):
                with open(SHINY_HTML_PATH, 'r', encoding='utf-8') as file: content = file.read()
                content = content \
                    .replace('{Pokémon}', pokemon_name) \
                    .replace('{Trainer}', receiver.split('@')[0].capitalize())
            else: print(COLOR_str.HTML_NOT_FOUND.replace('{html}', SHINY_HTML_PATH))

            receivers = {'Primary': [receiver], 'CC': [], 'BCC': []}
            # Don't send duplicated copy mails to the sender
            if index == 0: receivers['BCC'] = [self.__email_sender]
            message = self._create_message(f'[Pokémon Shiny Hunter] Shiny {pokemon_name} found!', content, receivers)

            image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../Media/Images/{image_name}'))
            if not os.path.exists(image_path):
                image_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                    f'../../{CONST.EMAIL_PLACEHOLDER_IMAGE}'))

            with open(image_path, 'rb') as image:
                image = MIMEImage(image.read())
                # Content-ID must match src in HTML
                image.add_header('Content-ID', '<shiny_pokemon_image>') 
                message.attach(image)

            receivers = receivers.get('Primary') + receivers.get('CC') + receivers.get('BCC')
            self._send_email(message, receivers)

###########################################################################################################################
#####################################################     PROGRAM     #####################################################
###########################################################################################################################

if __name__ == "__main__":
    def main_menu():
        print('\n' + COLOR_str.MENU.replace('{module}', 'Mail'))
        print(COLOR_str.MENU_OPTION.replace('{index}', '1').replace('{option}', 'Send shiny email'))

        # option = input('\n' + COLOR_str.OPTION_SELECTION.replace('{module}', 'Game Capture'))
        option = '1'

        menu_options = {
            '1': send_shiny_email,
        }

        if option in menu_options: menu_options[option](option)
        else: print(COLOR_str.INVALID_OPTION.replace('{module}', 'Mail') + '\n')

    #######################################################################################################################

    def send_shiny_email(option):
        print('\n' + COLOR_str.SELECTED_OPTION
            .replace('{module}', 'Mail')
            .replace('{option}', f"{option}")
            .replace('{action}', f"Sending shiny email")
            .replace('{path}', '')
        )

        Email = Email_Sender()
        Email.send_shiny_found('Dinones', None)

    #######################################################################################################################

    main_menu()