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
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Star.svg" width="30px" align="top"/>
    ⠀Key Features
</h2>

<p>
    <p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Raspberry.svg" width="20px" align="center"/>⠀ Use your computer or Raspberry Pi to automatically search for shiny pokémon. <br>
    </p><p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/NS%20Controller.svg" width="20px" align="center" style="margin-top:0px"/>⠀ Works on physical games running on a Nintendo Switch, not emulators. <br>
    </p><p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Pokemon.svg" width="20px" align="top"/>⠀ Compatible with all games that have static encounters (<a href="./Media/Docs/Compatible%20Games.md">see compatible games</a>). <br>
    </p><p>
        &emsp; <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Camera.svg" width="20px" align="top"/>⠀ Automatically saves a video of the shiny encounter. <br>
    </p> 
</p>

<!-- #################### INSTALLATION #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Gear.svg" width="30px" align="top"/>
    ⠀Installation
</h2>

Download or clone the repository.
```bash
git clone https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter.git 
```

### Linux and Raspberry Pi OS

```bash
sudo apt-get install python3-tk
```
Go to the project folder and install the libraries.
```bash
sudo pip install -r Requirements.txt
```

**Please Note:** NXBT needs root privileges to toggle the BlueZ Input plugin. If you don't feel comfortable running this program as root, you can disable the Input plugin manually, and install NXBT as a regular user. I've always run the program as root, so you may need to investigate how to adapt it (Visit [NXBT](https://github.com/Brikwerk/nxbt) repository to learn more).

### Windows and MacOS

Install a Linux Virtual Machine and follow the installation steps for <a href="#linux-and-raspberry-pi-os">Linux and Raspberry Pi OS</a>. The program has been tested using Raspberry Pi OS 11 (Bullseye) and Virtual Box with XUbuntu 22.04.3. You can find a step-by-step guide on how to setup the Virtual Machine [here](./Media/Docs/VM%20Setup.md).

<!-- #################### GETTING STARTED #################### -->
⠀
<h2>
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

<p style="display: flex; align-items: start;">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>NOTE:</strong>  The program will always open the first game slot. Make sure the pokémon game you want to run is in the first position. If it's not, you can simply start the game and it'll move to the beginning.</span>
</p>

<!-- If your game has an auto-save option, disable it. Otherwise, in case you kill the pokémon you won't be able to restart the process. In the game, place your player right in front of the pokémon (overworld), you have to be able to enter the combat just by pressing "**A**", if you need to move forward some steps before, read the note in the <a href="#running-the-shiny-hunter">Running the Shiny Hunter</a> section. -->

Once in the home screen, go to <i>Controllers</i> > "<i>Change Grip/Order Menu</i>". Remove both controllers from the Nintendo Switch and make sure they're not connected via bluetooth. (See steps <a href="./Media/Docs/Change%20Grip%20Menu.md">here</a>).<br>

<!-- #################### DETECTING CAPTURE CARD #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Camera.svg" width="30px" align="top"/>
    ⠀Detecting the Capture Card
</h2>

Execute `/Sub_Programs/Find_Video_Capture.py`. It will print all the video capture devices found. Multiple devices may appear even if you only have one device connected: webcams and some drivers may raise extra devices.

To discover which is the good one, note all the detected devices. You will have to change the `VIDEO_CAPTURE_INDEX` variable of the `Constants.py` file. Now, execute `/Utils/Game_Capture.py`. It will open a window showing what is being captured. Repeat the process until you find the desired device.

<!-- #################### SELECTING SHINY POKEMON #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Diamond.svg" width="30px" align="top"/>
    ⠀Selecting the Shiny Pokémon
</h2>

<img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/> **CAUTION:** Make sure the desired shiny pokémon has not been shiny locked in the game.

Once you have selected your pokemon you have execute `/Sub_Programs/Find_Color_Range.py`. It will open the following interface:

<h1 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/master/Media/Color%20Selector%20Interface.png" width="80%" style="border-radius: 10px;">
</h1>

Now, you have to find on internet one image for each, the normal pokémon and the shiny one. Download them, and select the images using the two buttons that appear on the top of the interface.

Once both images are loaded in the interface, you can start moving the color slides. Follow the instructions that appear on the interface until you get a similar result to this one:

<h1 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/master/Media/Giratina%20Color%20Example.png" width="80%" style="border-radius: 10px;">
</h1>

As you can see, the image above has white pixels, while the one below does not. It doesn't matter if there are a few white pixels in the image below, just make sure they don't form a large grouping. Keep in mind that the better accuracy you achieve, the better the program will work. It's a good idea to spend some time trying to get precise results.

Once you have detected the colors, you can press the "Toggle Check Match" button. It will open a new window where you should see rectangles around the areas where the color is present. If any rectangle appears, your area is too small to be detected, try finding another color with larger area.

<h1 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/master/Media/Giratina%20Contour%20Example.png" width="80%" style="border-radius: 10px;">
</h1>

Once you've found the color ranges that fit the requirements, change the `LOWER_COLOR` and `UPPER_COLOR` variables in the `Constants.py` file to the new values.

<!-- #################### CONTROLLING NINTENDO SWITCH #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Controller.svg" width="30px" align="top"/>
    ⠀Controlling the Nintendo Switch
</h2>

Before executing the main program, check NXBT is successfully working in your system. Please, visit [NXBT repository](https://github.com/Brikwerk/nxbt#running-the-demo) and perform the demo testing.

It may not be working at the beginning, try restarting the computer and bluetooth systems, you can use `rfkill block bluetooth` and `rfkill unblock bluetooth`. If you are not able to connect your computer to the Nintendo, please, report to [NXBT](https://github.com/Brikwerk/nxbt).

<!-- #################### RUNNING SHINY HUNTER #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Pokeball.svg" width="30px" align="top"/>
    ⠀Running the Shiny Hunter
</h2>

**NOTE:** If your player needs to move forward some steps before entering the combat, change the `WALK_FORWARD_BEFORE_COMBAT` option to `True` in the `Constants.py` file.

Execute the `Shiny_Hunter.py` file. The controller should connect in a few seconds and the program will start it execution. For every combat, it will save an screenshot of the pokémon in `/Media/Results/` folder, just in case it missdetects the shiny pokémon you could check why. It will also save a video for each encounter in `/Media/` folder, **it always ovewrites the old video file**, don't worry about your disk space. If you want to disable these features, change the `SAVE_SCREENSHOTS` and `RECORD_VIDEO` options to `False` in the `Constants.py` file.

If you find a shiny pokémon and you want to search for another one, you must reset the number of the `/Media/Attempts.txt` file to zero, to keep track of the current resets for the new pokémon. It's also recomendable to delete all the images generated in the `/Media/Results/` folder.

<!-- #################### TROUBLESHOOTING #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Tools.svg" width="30px" align="top"/>
    ⠀Troubleshooting
</h2>

### Unable to install *`opencv-python`* library 

In some Raspberry Pi OS versions and other operating systems, OpenCV may take forever to install, eventually raising an error. If this happens, force the installation of the version 4.5.3.56 by running: `pip install opencv-python==4.5.3.56`.

### Error when installing the *`dbus-python`* package

This error can occur due to missing dbus-related libraries on some Linux distributions. To fix this in most cases, `libdbus-glib-1-dev` and `libdbus-1-dev` need to be installed with your system's package manager:

```bash
sudo apt-get install libdbus-glib-1-dev libdbus-1-dev
```

<!-- #################### ISSUES #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Virus.svg" width="30px" align="top"/>
    ⠀Issues
</h2>

### Failed to allocate *XXX* bytes in function 'OutOfMemoryError'
After some hours running, program may crash due to it has ran out of memory, this error only raises on Raspberry Pi. Still working on it, a new version will be uploaded as soon as possible. 

<!-- #################### CREDITS #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Medal.svg" width="30px" align="top"/>
    ⠀Credits
</h2>

A big thank to all the contributors of [NXBT](https://github.com/Brikwerk/nxbt) repository. The whole program resolves around its work. Also thank to [Learn Code By Gaming](https://www.youtube.com/@LearnCodeByGaming) youtube channel, where I learnt most of what I know about image processing and object detection.