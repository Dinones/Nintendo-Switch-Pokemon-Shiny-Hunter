from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
import os
from . import MessageSender

# HTML content with an image embedded
html = """\
<html>
<body>
    <p>Dear Pokemon Trainer,<br>
    A shiny Pokemon has been found!<br>
    Have a nice day!<br>

    <img src="cid:image1">.</p>
</body>
</html>
"""

error_html = """\
<html>
<body>
    <p>Dear Pokemon Trainer,<br>
    An error has been detected!<br>
    Error message: {error_message}<br>
    Have a nice day!<br>
</body>
</html>
"""

class MailSender(MessageSender):
    """
    Class for sending messages via email.
    """

    def __init__(self, config: dict):
        """
        Initializes the MailSender.
        """
        self.__sender_email = config.get('sender_email')
        self.__receiver_email = config.get('receiver_email')
        
        self.__port = config.get('port')
        self.__smtp_server = config.get('smtp_server')
        self.__login = config.get('login')
        self.__password = config.get('password')

    def send_shiny_found(self, pokemon_name: str, image_path: str):

        message = self._create_message(f'Pokemon Hunter - Shiny {pokemon_name} found!', html)

        # Open the image file in binary mode
        with open(image_path, 'rb') as img:
            # Attach the image file
            msg_img = MIMEImage(img.read(), name=os.path.basename(image_path))
            # Define the Content-ID header to use in the HTML body
            msg_img.add_header('Content-ID', '<image1>')
            # Attach the image to the message
            message.attach(msg_img)

        # Send the email
        self._send_email(message)

    def send_failure_detected(self, error_message: str):

        content = error_html.format(error_message=error_message)
        message = self._create_message('Pokemon Hunter - Error detected!', content)

        # Send the email
        self._send_email(message)

    def _create_message(self, subject: str, content: str) -> MIMEMultipart:
        """
        Creates a multipart email message with the given subject and content.
        """
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.__sender_email
        message["To"] = self.__receiver_email
        message["Subject"] = subject

        # Attach the HTML part
        message.attach(MIMEText(content, "html"))
        
        return message

    def _send_email(self, message: MIMEMultipart):
        """
        Sends an email using the provided message.
        """
        with SMTP(self.__smtp_server, self.__port) as server:
            server.starttls()
            server.login(self.__login, self.__password)
            server.sendmail(self.__sender_email, self.__receiver_email, message.as_string())
