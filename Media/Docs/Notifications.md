<!-- ############################################### -->
<!-- #################### INDEX #################### -->
<!-- ############################################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Index.svg" width="30px" align="top"/>
    ⠀Index
</h2>

- <a href="#gmail">**Email Notifications (Gmail)**</a>
    - <a href="#gmail-enable-2ma">Enable 2MA</a>
    - <a href="#gmail-get-api-credentials">Get API Credentials</a>
    - <a href="#gmail-connect-with-shiny-hunter">Connect with the Shiny Hunter</a>
    - <a href="#gmail-test-notifications">Test the Notifications</a>
- <a href="#telegram">**Telegram Notifications**</a>
    - <a href="#telegram-create-new-bot">Create a New Bot</a>
    - <a href="#telegram-chat-id">Get Chat ID</a>
    - <a href="#telegram-disable-auto-deleting-messages">Disable Auto-deleting Messages</a>
    - <a href="#telegram-connect-with-shiny-hunter">Connect with the Shiny Hunter</a>
    - <a href="#telegram-create-new-bot">Create a New Bot</a>
- <a href="#discord">**Discord Notifications**</a>

<br>

> [!NOTE]
> I do **not** recommend activating all notifications simultaneously, as they perform similar functions and will increase resource consumption.

> [!CAUTION]
> Please, **never** share your credentials or tokens with anyone!

<br>

<!-- ############################################### -->
<!-- #################### GMAIL #################### -->
<!-- ############################################### -->

<h2 id="gmail">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Gmail.svg" width="30px" align="top"/>
    ⠀Email Notifications (Gmail)
</h2>

This implementation only works with Google mail accounts *(gmail)*. I highly recommend using a **brand new** email account instead of using any of your personal accounts.

<h3 id="gmail-enable-2ma">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Lock.svg" width="25px" align="top"/>
    ⠀Enable 2MA
</h3>

1. Sign in to your [Google account](https://myaccount.google.com/security).

2. In the navigation panel, select **Security**.

3. You will find the **2-Step Verification** option under the *"How you sign in to Google"* section.
 
4. Enable it. This is a **MUST**; messaging API will not work if this option is not enabled.
    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/2MA.png" width="80%" style="border-radius: 15px;">
    </h6>

<h3 id="gmail-get-api-credentials">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Key.svg" width="25px" align="top"/>
    ⠀Get API Credentials
</h3>

1. Sing in to [App Passwords](https://myaccount.google.com/apppasswords).

2. Create a new App and take note of the password. You will <b>NOT</b> be able to see the password anymore.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/App%20Password.png" width="60%" style="border-radius: 15px;">
    </h6>

<h3 id="gmail-connect-with-shiny-hunter">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Pikachu.svg" width="25px" align="top"/>
    ⠀Connect with the Shiny Hunter
</h3>

1. Go to the `Modules/Email/` folder and delete the `Credentials.env` file, if exists.

2. Execute the `Email.py` script by opening a terminal in the project folder and running the following command and selecting the `Send shiny notification` option:

    ```bash
    .venv/bin/python Modules/Email/Email.py
    ```

    You should get a warning like this:

    ```
    [!] [Email] Email notifications cannot be sent: Some fields are missing in the ".../Nintendo-Switch-Pokemon-Shiny-Hunter/Modules/Email/Credentials.env" file
    ```

3. Open the `Email_Credentials.env` file and write your credentials there. Where:
    - **EMAIL_SENDER:** The email you have used to create your App.

    - **EMAIL_APP_PASSWORD:** Your App password (not your email password). Include the spaces and make sure they are indeed spaces, not a different invisible character.

    - **EMAIL_RECEIVER:** Main recipient who will be notified of all events. This email does not need to be a Gmail account.

    - **EMAIL_RECEIVER_2 *(Optional)*:** You can add a secondary recipient who will also receive email notifications. This recipient will only receive success notifications, not error alerts. This does not need to be a Gmail account.

    They should look as follows:

    ```
    EMAIL_SENDER = sender@gmail.com 
    EMAIL_APP_PASSWORD = xxxx xxxx xxxx xxxx
    EMAIL_RECEIVER = main_receiver@gmail.com
    EMAIL_RECEIVER_2 = secondary_receiver@gmail.com
    ```

4. Edit the `Constants.py` file. It can be found in the main project folder and you can edit it by double-clicking on it as if it was a simple `.txt` file. Change the `MAIL_NOTIFICATIONS` constant from `False` to `True`:

    ```python
    MAIL_NOTIFICATIONS = True
    ```

<h3 id="gmail-test-notifications">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Notification.svg" width="25px" align="top"/>
    ⠀Test the Notifications
</h3>

1. Open a terminal in the main project folder and run the following command:

    ```bash
    .venv/bin/python Modules/Email/Email.py
    ```

2. Select the `Send shiny notification` option. You should receive a testing email in a couple of seconds.

<br>
⠀
<!-- ################################################## -->
<!-- #################### TELEGRAM #################### -->
<!-- ################################################## -->

<h2 id="telegram">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Telegram.svg" width="30px" align="top"/>
    ⠀Telegram Notifications
</h2>

<h3 id="telegram-create-new-bot">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Developer.svg" width="25px" align="top"/>
    ⠀Create a New Bot
</h3>

1. Open the Telegram app on your mobile device and search for the **BotFather** user.

2. Start a conversation with the message `/newbot` and follow the instructions to create the bot.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/Create%20Bot.png" width="40%" style="border-radius: 15px;">
    </h6>

3. Start a conversation with your bot by sending it any message you want.

<h3 id="telegram-chat-id">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Chat.svg" width="25px" align="top"/>
    ⠀Get Chat ID
</h3>

1. Open your browser and go to the following address replacing the `{your_bot_token}` parameter by your actual bot token *(without the `{}` brackets)*:

    ```bash
    https://api.telegram.org/bot{your_bot_token}/getUpdates
    ```

2. Once you are in the webpage, send the bot a new random message.

3. Update the webpage, a text message will appear, there you can find your Chat ID.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/Get%20Chat%20ID.png" width="90%" style="border-radius: 5px;">
    </h6>

<h3 id="telegram-disable-auto-deleting-messages">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Trash.svg" width="25px" align="top"/>
    ⠀Disable Auto-deleting Messages
</h3>

1. Enter your bot conversation and click on its name.

2. Go to the **3 dots** located on the top-right corner, select `Auto-delete` > `Custom` and set it to `Off`. 

<h3 id="telegram-connect-with-shiny-hunter">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Pikachu.svg" width="25px" align="top"/>
    ⠀Connect with the Shiny Hunter
</h3>

1. Go to the `Modules/Telegram/` folder and delete the `Credentials.env` file, if exists.

2. Execute the `Telegram.py` script by opening a terminal in the project folder and running the following command and selecting the `Send shiny notification` option:

    ```bash
    .venv/bin/python Modules/Telegram/Telegram.py
    ```

    You should get a warning like this:

    ```
    [!] [Telegram] Telegram notifications cannot be sent: Some fields are missing in the ".../Nintendo-Switch-Pokemon-Shiny-Hunter/Modules/Telegram/Credentials.env" file
    ```

2. Open the `Telegram_Credentials.env` file and write your credentials there. Where:
    - **TELEGRAM_BOT_TOKEN:** The bot token that **BotFather** provided to you.

    - **TELEGRAM_CHAT_ID:** The chat ID you got from the Telegram webpage.

3. They should look as follows:

    ```
    TELEGRAM_BOT_TOKEN = xxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    TELEGRAM_CHAT_ID = xxxxxxxxxx
    ```

4. Edit the `Constants.py` file. It can be found in the main project folder and you can edit it by double-clicking on it as if it was a simple `.txt` file. Change the `TELEGRAM_NOTIFICATIONS` constant from `False` to `True`:

    ```python
    TELEGRAM_NOTIFICATIONS = True
    ```

<h3 id="telegram-test-notifications">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Notification.svg" width="25px" align="top"/>
    ⠀Test the Notifications
</h3>

1. Open a terminal in the main project folder and run the following command:

    ```bash
    .venv/bin/python Modules/Telegram/Telegram.py
    ```

2. Select the `Send shiny notification` option. You should receive a testing Telegram message in a couple of seconds.

<br>

<!-- ################################################# -->
<!-- #################### DISCORD #################### -->
<!-- ################################################# -->

<h2 id="discord">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Discord.svg" width="30px" align="top"/>
    ⠀Discord Notifications
</h2>

> [!NOTE]
> Not implemented yet.