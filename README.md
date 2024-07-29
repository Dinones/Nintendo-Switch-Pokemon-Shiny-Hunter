<h1 align="center">
    <br>
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Shiny%20Charizard.png" width="250">
    </br>
</h1>

<h4 align="center">Search for shiny pokémon on your Nintendo Switch while sleeping!</h4>

<div align="center">
    
<!-- [![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UCUDcDii2WU8SVoTCgYlQCiw?style=flat&logo=youtube&logoColor=ff0000&label=Youtube&color=ff0000)](https://www.youtube.com/watch?v=XE8Oeh71BQ4&ab_channel=Dinones) -->
[![GitHub Repo Stars](https://img.shields.io/github/stars/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter?label=%E2%9C%A8%20Stars&color=ffff00)](https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter)
[![Discord](https://img.shields.io/badge/contact-Dinones-blue?logo=discord&label=Discord&logoColor=5865f2&color=5865f2)](https://discordapp.com/users/177131156028784640)

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
</h1>

<!-- #################### KEY FEATURES #################### -->
⠀
<h2 id="key-features">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Star.svg" width="30px" align="top"/>
    ⠀Key Features
</h2>

<p>
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Raspberry.svg" width="20px" align="center"/>⠀ Use your computer or Raspberry Pi to automatically search for shiny pokémon. <br>
    </p><p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/NS%20Controller.svg" width="20px" align="center" style="margin-top:0px"/>⠀ Works on physical games running on a Nintendo Switch, <b>not emulators!</b> <br>
    </p>
    <!-- <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Pokemon.svg" width="20px" align="top"/>⠀ Compatible with all games that have static encounters (<a href="./Media/Docs/Compatible%20Games.md">see compatible games</a>). <br>
    </p> -->
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Camera.svg" width="20px" align="top"/>⠀ Automatically saves a video of the shiny encounter. <br>
    </p> 
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Music.svg" width="20px" align="top"/>⠀ Plays a sound whenever a shiny Pokémon is found. <br>
    </p> 
</p>

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

### Linux and Raspberry Pi OS

Install the necessary libraries. Open a terminal in the project folder and run the following commands:

```bash
sudo apt-get install -y python3-pyqt5 tesseract-ocr libtesseract-dev
```
```bash
sudo pip install -r Requirements.txt && pip install -r Requirements.txt 
```

**Note:** NXBT needs root privileges to toggle the BlueZ Input plugin. If you don't feel comfortable running this program as root, you can disable the Input plugin manually, and install NXBT as a regular user. I've always run the program as root, so you may need to investigate how to adapt it (Visit [NXBT](https://github.com/Brikwerk/nxbt) repository to learn more).

<img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/> **IMPORTANT:** Please, take a look at the configuration of the Virtual Machine mentioned in <a href="#windows-and-macos">Windows and MacOS</a>. Even if you know about Linux systems, there are some important things to do. If something fails, it is probably due to a misconfiguration. This configuration has been tested multiple times and following all the steps should never raise any error.

### Windows and MacOS

Install a Linux Virtual Machine and follow the installation steps for <a href="#linux-and-raspberry-pi-os">Linux and Raspberry Pi OS</a>. The program has been tested using Raspberry Pi OS 11 (Bullseye) and Virtual Box with XUbuntu 22.04.3. You can find a step-by-step guide on how to setup the Virtual Machine [here](./Media/Docs/VM%20Setup.md).

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
    ⠀Capture card that converts HDMI input into USB output. <br>
    &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Switch.svg" width="14px">
    ⠀Nintendo Switch Dock. <br>
    &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Cable.svg" width="14px">
    ⠀HDMI cable. <br>
</p>

### Setting Up the Nintendo Switch

Place the Nintendo Switch into the Dock. Connect the dock to the official Nintendo Switch charger. Connect the HDMI output of the Dock to the input of your capture card. Finally, connect your capture card to your computer / Raspberry via USB. If your game is not digital, insert the game card in the Nintendo.

<p>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>NOTE:</strong>  The program will always open the first game slot. Make sure the pokémon game you want to run is in the first position. If it's not, you can simply start the game and it'll move to the beginning.</span>
</p>

<!-- #################### RUNNING SHINY HUNTER #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Pokeball.svg" width="30px" align="top"/>
    ⠀Running the Shiny Hunter
</h2>

<img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>IMPORTANT:</strong> Before running the Shiny Hunter, there are a few variables of the **Constants.py** file that need to be mentioned. You will need to edit them in order to use the program. (See constants [here](./Media/Docs/Constants.md)).

Now, you must change the game configuration as follows:

<ul>
    <li><p><b>Text Speed:</b> Fast.</p></li>
    <li><p><b>Battle Effects:</b> Off.</p></li>
    <li><p><b>Autosave:</b> Off.</p></li>
</ul>

Finally, enter the game and place the player on the grass/water for a wild encounter; in front of the Pokémon for the static encounter; and one step before entering the lake for the starter encounter. See an example of the positions [here](./Media/Docs/Starting%20Positions.md). Once there, go to the home screen (leave the game as idle, don't close it); then, go to "<i>Controllers</i>" > "<i>Change Grip/Order Menu</i>". Plug in both controllers to the Nintendo Switch and if not, make sure they're not connected via Bluetooth. (See steps <a href="./Media/Docs/Change%20Grip%20Menu.md">here</a>).

<!-- #################### TROUBLESHOOTING #################### -->
⠀
<h2 id="troubleshooting">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Virus.svg" width="30px" align="top"/>
    ⠀Troubleshooting
</h2>

### Unable to install *`opencv-python`* library 

In some Raspberry Pi OS versions and other operating systems, OpenCV may take forever to install, eventually raising an error. If this happens, force the installation of the version 4.5.3.56 by running the following command:

```bash
pip install opencv-python==4.5.3.56 --force-reinstall
```

### Error when installing the *`dbus-python`* package

This error can occur due to missing dbus-related libraries on some Linux distributions. To fix this in most cases, `libdbus-glib-1-dev` and `libdbus-1-dev` need to be installed with your system's package manager:

```bash
sudo apt-get install libdbus-glib-1-dev libdbus-1-dev
```

<!-- #################### CREDITS #################### -->
⠀
<h2 id="credits">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Medal.svg" width="30px" align="top"/>
    ⠀Credits
</h2>

A big thank to all the contributors of [NXBT](https://github.com/Brikwerk/nxbt) repository. The whole program resolves around its work. Also thank to [Learn Code By Gaming](https://www.youtube.com/@LearnCodeByGaming) youtube channel, where I learnt most of what I know about image processing and object detection.