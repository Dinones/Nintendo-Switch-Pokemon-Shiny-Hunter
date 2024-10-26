<!-- #################### GMAIL #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Gmail.svg" width="30px" align="top"/>
    ⠀Email Notifications
</h2>

<p>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>IMPORTANT:</strong>  Please, <b>never</b> share your credentials with anyone!</span>
</p>

This implementation only works with Google mail accounts <i>(gmail)</i>. I highly recommend using a completely new email instead of using any of your personal accounts.

### Enable 2MA 

1. Sign in to your [Google account](https://myaccount.google.com/security).
2. In the navigation panel, select <b>Security</b>.
3. You will find the <b>2-Step Verification</b> option under the <i>"How you sign in to Google"</i> section. 
4. Enable it. This is a MUST; messaging API will not work if this option is not enabled.
    <h3 align="center">
        <br>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Gmail%20Automation/2MA.png" width="80%" style="border-radius: 15px;">
        <br>
        <p>ㅤ</p>
    </h3>

### Get your API Credentials

1. Sing in to [App Passwords](https://myaccount.google.com/apppasswords).
2. Create a new App and take note of the password: You will <b>NOT</b> be able to see it anymore. 
    <h3 align="center">
        <br>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/Gmail%20Automation/App%20Password.png" width="70%" style="border-radius: 15px;">
        <br>
        <p>ㅤ</p>
    </h3>

### Connect with the Shiny Hunter

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
    [...]
    MAIL_NOTIFICATIONS = True
    [...]
    ```
### Test the Notifications

1. Open a terminal in the <i>/Modules/Mail/</i> folder and run the following command:

    <pre><code>python3 Mail.py</code></pre>

2. Select the "<i>Send shiny notification</i>" option. You should receive a testing email in a couple of seconds.

<!-- #################### TELEGRAM #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Telegram.svg" width="30px" align="top"/>
    ⠀Telegram Notifications
</h2>