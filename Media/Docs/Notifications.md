<!-- #################### GENERAL #################### -->

<h1 align="center">
    <br><img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/Gmail%20Telegram%20Discord.png" width="80%"></br>
</h1>

<b>Note:</b> I do not recommend activating all notifications simultaneously, as they perform similar functions and will increase resource consumption.

<p align="center">
    <a href="#gmail">Email</a> •
    <a href="#telegram">Telegram</a> •
    <a href="#discord">Discord</a>
</p>

⠀
<!-- #################### GMAIL #################### -->

<h2 id="gmail">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/SVG/Gmail.svg" width="30px" align="top"/>
    ⠀Email Notifications
</h2>

<p>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/SVG/Warning.svg" width="17px" align="left"/><span><strong>IMPORTANT:</strong>  Please, <b>never</b> share your credentials with anyone!</span>
</p>

This implementation only works with Google mail accounts <i>(gmail)</i>. I highly recommend using a completely new email instead of using any of your personal accounts.

## Enable 2MA 

1. Sign in to your [Google account](https://myaccount.google.com/security).
2. In the navigation panel, select <b>Security</b>.
3. You will find the <b>2-Step Verification</b> option under the <i>"How you sign in to Google"</i> section. 
4. Enable it. This is a MUST; messaging API will not work if this option is not enabled.
    <h3 align="center">
        <br>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/2MA.png" width="80%" style="border-radius: 15px;">
        <br>
        <p>ㅤ</p>
    </h3>

## Get your API Credentials

1. Sing in to [App Passwords](https://myaccount.google.com/apppasswords).
2. Create a new App and take note of the password: You will <b>NOT</b> be able to see it anymore. 
    <h3 align="center">
        <br>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/App%20Password.png" width="60%" style="border-radius: 15px;">
        <br>
        <p>ㅤ</p>
    </h3>

## Connect with the Shiny Hunter

1. Go to the <i>/Modules/Mail/</i> folder and delete the <i>Credentials.env</i> file, if exists.
2. Open the <i>Email_Credentials.env</i> file and write your credentials there. Where:
    <ol type="a">
        <li>
            <strong>EMAIL_SENDER:</strong> The email you have used to create your App.
        </li><li>
            <strong>EMAIL_APP_PASSWORD:</strong> Your App password, not your email password. Include the spaces and make sure they are indeed spaces, not a different invisible character.
        </li><li>
            <strong>EMAIL_RECEIVER:</strong> Main recipient who will be notified of all events. This does not need to be a Gmail account.
        </li><li>
            <strong>EMAIL_RECEIVER_2 (Optional):</strong> You can add a secondary recipient who will also receive email notifications. This recipient will only receive success notifications, not error alerts. This does not need to be a Gmail account.
        </li>
    </ol>
3. They should look as follows:

    ```bash
    EMAIL_SENDER = sender@gmail.com 
    EMAIL_APP_PASSWORD = xxxx xxxx xxxx xxxx
    EMAIL_RECEIVER = main_receiver@gmail.com
    EMAIL_RECEIVER_2 = secondary_receiver@gmail.com
    ```
4. Edit the <i>Constants.py</i> file. It can be found in the main project folder and you can edit it by double-clicking on it as if it was a simple *.txt* file. Change the <b>MAIL_NOTIFICATIONS</b> constant from <i>False</i> to <i>True</i>:

    ```bash
    MAIL_NOTIFICATIONS = True
    ```

## Test the Notifications

1. Open a terminal in the <i>/Modules/Mail/</i> folder and run the following command:

    <pre><code>python3 Mail.py</code></pre>

2. Select the "<i>Send shiny notification</i>" option. You should receive a testing email in a couple of seconds.

⠀
<!-- #################### TELEGRAM #################### -->

<h2 id="telegram">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/SVG/Telegram.svg" width="30px" align="top"/>
    ⠀Telegram Notifications
</h2>

<p>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/SVG/Warning.svg" width="17px" align="left"/><span><strong>IMPORTANT:</strong>  Please, <b>never</b> share your credentials with anyone!</span>
</p>

## Create your Bot

1. Open the Telegram app on your mobile device and search for the <b>BotFather</b> user.
2. Start a conversation with the message "<i>/newbot</i>" and follow the instructions to create the bot.

    <h3 align="center">
        <br>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/Create%20Bot.png" width="40%" style="border-radius: 15px;">
        <br>
    </h3>
3. Start a conversation with your bot by sending it any message you want: <i>you can remember him how cool it is</i>.

## Get your Caht ID

1. Go to the following address replacing the <b>{your_bot_token}</b> parameter by your actual bot token <i>(without the {} brackets)</i>:
    ```bash
    https://api.telegram.org/bot{your_bot_token}/getUpdates
    ```
2. Once you are in the webpage, send the bot a new random message.
3. Update the webpage, a text message will appear, there you can find your Chat ID.
    <h3 align="center">
        <br>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/Get%20Chat%20ID.png" width="90%" style="border-radius: 15px;">
        <br>
    </h3>

## Disable Auto-deleting Messages

1. Enter your bot conversation and click on its name.
2. Go to the 3 dots located on the top-right corner and select <i>Auto-delete</i> > <i>Custom</i> and set it to <i>Off</i>. 

## Connect with the Shiny Hunter

1. Go to the <i>/Modules/Telegram/</i> folder and delete the <i>Credentials.env</i> file, if exists.
2. Open the <i>Telegram_Credentials.env</i> file and write your credentials there. Where:
    <ol type="a">
        <li>
            <strong>TELEGRAM_BOT_TOKEN:</strong> The bot token that <b>BotFather</b> provided to you.
        </li><li>
            <strong>TELEGRAM_CHAT_ID:</strong> The chat ID you got from the Telegram webpage.
        </li>
    </ol>
3. They should look as follows:

    ```bash
    TELEGRAM_BOT_TOKEN = xxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    TELEGRAM_CHAT_ID = xxxxxxxxxx
    ```
4. Edit the <i>Constants.py</i> file. It can be found in the main project folder and you can edit it by double-clicking on it as if it was a simple *.txt* file. Change the <b>TELEGRAM_NOTIFICATIONS</b> constant from <i>False</i> to <i>True</i>:

    ```bash
    TELEGRAM_NOTIFICATIONS = True
    ```

⠀
<!-- #################### DISCORD #################### -->

<h2 id="discord">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Automatic%20Notifications/SVG/Discord.svg" width="30px" align="top"/>
    ⠀Discord Notifications
</h2>