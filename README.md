<h1 align="center">
    <br>
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Shiny%20Charizard.png" width="250">
    </br>
</h1>

<h4 align="center">Search for shiny pokémon on your Nintendo Switch while sleeping!</h4>

<div align="center">
    
<!-- [![GitHub Repo Stars](https://img.shields.io/github/stars/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter?label=%E2%9C%A8%20Stars&color=ff0000)](https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter) -->
[![Discord](https://img.shields.io/badge/contact-Dinones-blue?logo=discord&label=Discord&logoColor=5865f2&color=5865f2)](https://discordapp.com/users/177131156028784640)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UCUDcDii2WU8SVoTCgYlQCiw?style=flat&logo=youtube&logoColor=ff0000&label=Youtube&color=ff0000)](https://www.youtube.com/watch?v=XE8Oeh71BQ4&ab_channel=Dinones)

</div>

<p align="center">
    <a href="#key-features">Key Features</a> •
    <a href="#installation">Installation</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#troubleshooting">Troubleshooting</a> •
    <a href="#credits">Credits</a>
</p>

<h1 align="center">
    <br>
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Shiny%20Pokemon%20Collection.png" width="80%" style="border-radius: 15px;">
    <br>
    <p>ㅤ</p>
</h1>

<!-- #################### CREATION PROCESS #################### -->
⠀
<h2 id="youtube">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Youtube.svg" width="30px" align="top"/>
    ⠀Creation Process
</h2>

<p>In my <a href="https://www.youtube.com/@DinoDinones">Youtube Channel</a> you can follow the entire creation process of the project. Don’t miss it!</p>

<!-- #################### KEY FEATURES #################### -->
⠀
<h2 id="key-features">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Star.svg" width="30px" align="top"/>
    ⠀Key Features
</h2>

<p>
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Raspberry.svg" width="20px" align="center"/>⠀ Use your computer to <b>automatically</b> search for shiny pokémon. <br>
    </p><p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/NS%20Controller.svg" width="20px" align="center" style="margin-top:0px"/>⠀ Works on physical games running on a Nintendo Switch, <b>not emulators</b>! <br>
    </p>
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Camera.svg" width="20px" align="top"/>⠀ Automatically saves a video of the shiny encounter. <br>
    </p> 
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Music.svg" width="20px" align="top"/>⠀ Plays a sound whenever a shiny Pokémon is found. <br>
    </p> 
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Notification.svg" width="20px" align="top"/>⠀ Sends an email, Telegram and/or Discord <b>notification</b> when a shiny is found. <br>
    </p> 
</p>

<p>⠀</p>

<div align="center">

| Feature             | BDSP |⠀⠀⠀⠀⠀⠀⠀⠀| Special Encounters   | BDSP |
|---------------------|:----:|:--------:|:--------------------:|:----:|
| Starters            | ✔️    |⠀⠀⠀⠀⠀⠀⠀⠀| Dialga & Palkia      | ✔️    |
| Wild Pokémon        | ✔️    |⠀⠀⠀⠀⠀⠀⠀⠀| Arceus               | ✔️    |
| Static Encounters   | ✔️    |⠀⠀⠀⠀⠀⠀⠀⠀| Shaymin              | ❌    |
| Fishing             | ❌    |⠀⠀⠀⠀⠀⠀⠀⠀| Mesprit & Cresselia  | ❌    |
| Pokéradar           | ❌    |⠀⠀⠀⠀⠀⠀⠀⠀| Happiny Egg          | ❌    |
| Fossils             | ❌    |⠀⠀⠀⠀⠀⠀⠀⠀| Riolu Egg            | ❌    |
| Eggs                | ❌    |⠀⠀⠀⠀⠀⠀⠀⠀|
| Auto-catching       | ❌    |⠀⠀⠀⠀⠀⠀⠀⠀|

</div>

<!-- #################### INSTALLATION #################### -->
⠀
<h2 id="installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Gear.svg" width="30px" align="top"/>
    ⠀Installation
</h2>

If you are not familiar with Linux systems, please read <a href="#windows-and-macos">Windows and MacOS</a> before. Then, come back here.

Download or clone the repository. Open a terminal and run the following command:
```bash
git clone https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter.git 
```

### Linux Distributions

<p>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>Warning:</strong>  This project is not compatible with Python 3.12 due to the removal of the <code>imp</code> module, which affects dependencies like <code>dbus-python</code>. Please use Python 3.11 or earlier to avoid issues. If you followed the VM installation guide, don't worry about this warning.</span>
</p>

Install the necessary libraries. Open a terminal in the project folder and run the following commands:

```bash
sudo apt-get install -y python3-pyqt5 tesseract-ocr libtesseract-dev
```
```bash
sudo pip install -r Requirements.txt && pip install -r Requirements.txt 
```

Please, take a look at the configuration of the Virtual Machine mentioned in <a href="#windows-and-macos">Windows and MacOS</a>. Even if you know about Linux systems, there are some important things to do. If something fails, it is probably due to a misconfiguration. This configuration has been tested multiple times and following all the steps should never raise any error.

### Windows and MacOS

Install a Linux Virtual Machine and follow the installation steps for <a href="#linux-distributions">Linux Distributions</a>. The program has been tested using Virtual Box with XUbuntu 22.04.3. You can find a step-by-step guide on how to setup the Virtual Machine [here](./Media/Docs/VM%20Setup.md).

### Verify Installation

In order to verify if everything has been properly installed, follow [these steps](./Media/Docs/Verify%20Installation.md). 

<!-- #################### GETTING STARTED #################### -->
⠀
<h2 id="getting-started">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Rocket.svg" width="30px" align="top"/>
    ⠀Getting Started
</h2>

### Material List

<p>
    &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/USB.svg" width="14px">
    ⠀Capture card that converts HDMI input into USB output. <i>Mine is just 7€ worth</i>.<br>
    &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Switch.svg" width="14px">
    ⠀Nintendo Switch Dock. <br>
    &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Cable.svg" width="14px">
    ⠀HDMI cable. <br>
</p>

### Setting Up the Nintendo Switch

Place the Nintendo Switch into the Dock. Connect the dock to the official Nintendo Switch charger. Connect the HDMI output of the Dock to the input of your capture card. Finally, connect your capture card to your computer / Raspberry via USB. If your game is not digital, insert the game card in the Nintendo.

<p>
    <strong>NOTE:</strong>  The program will always open the first game slot. Make sure the pokémon game you want to run is in the first position. If it's not, you can simply start the game and it'll move to the beginning.</span>
</p>

<p>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>IMPORTANT:</strong>  Set your Nintendo Switch to <b>light mode</b> and do <b>NOT</b> use any custom/animated theme.</span>
</p>

<!-- #################### RUNNING SHINY HUNTER #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Pokeball.svg" width="30px" align="top"/>
    ⠀Running the Shiny Hunter
</h2>

<img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>IMPORTANT:</strong> Before running the Shiny Hunter, there are a few variables of the **Constants.py** file that need to be mentioned. You will need to edit them in order to use the program. (See constants [here](./Media/Docs/Constants.md)).

<b>NOTE:</b> If you want to receive an email and/or Telegram notification whenever a shiny is found or an error occurs, you will have to set the notifications up as it is outlined in the [Notifications section](./Media/Docs/Notifications.md).

Now, you <b>must</b> change the game configuration as follows:

<ul>
    <li><p><b>Text Speed:</b> Fast.</p></li>
    <li><p><b>Battle Effects:</b> Off.</p></li>
    <li><p><b>Autosave:</b> Off.</p></li>
</ul>

Finally, enter the game and place the player on the grass/water for a wild encounter; in front of the Pokémon for the static encounter; and one step before entering the lake for the starter encounter. See an example of the positions [here](./Media/Docs/Starting%20Positions.md). Once there, <b>save the game</b> and go to the home screen (leave the game as idle, don't close it); then, go to "<i>Controllers</i>" > "<i>Change Grip/Order Menu</i>". Plug in both controllers to the Nintendo Switch and if not, make sure they're not connected via Bluetooth. (See steps [here](./Media/Docs/Change%20Grip%20Menu.md)).

Now, you are ready to go! Open a terminal in the project folder, run the following command, and follow the instructions that will appear:

```bash
sudo python3 Shiny_Hunter.py
```

<!-- #################### TROUBLESHOOTING #################### -->
⠀
<h2 id="troubleshooting">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Virus.svg" width="30px" align="top"/>
    ⠀Troubleshooting
</h2>

### Program is getting stuck in the Home screen
<p>Try setting your Nintendo Switch to <b>light mode</b> and do <b>NOT</b> use any custom/animated theme. The program detects some specific pixels to determine if it is in the Home screen; therefore, using any custom/animated theme will break this feature.</p>

<!-- #################### CONTRIBUTORS #################### -->
⠀
<h2 id="contributors">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Developer.svg" width="30px" align="top"/>
    ⠀Top Contributors
</h2>

- [@David34920](https://github.com/David34920) - General 
- [@Gr33nBug](https://github.com/Gr33nBug) - Shaymin integration

<!-- #################### CREDITS #################### -->
⠀
<h2 id="credits">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Medal.svg" width="30px" align="top"/>
    ⠀Credits
</h2>

A big thank to all the contributors of [NXBT](https://github.com/Brikwerk/nxbt) repository. The whole program resolves around its work. Also thank to [Learn Code By Gaming](https://www.youtube.com/@LearnCodeByGaming) youtube channel, where I learnt most of what I know about image processing and object detection.