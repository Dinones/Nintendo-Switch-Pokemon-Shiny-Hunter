<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Index.svg" width="30px" align="top"/>
    ⠀Index
</h2>

- <a href="#linux-installation">Linux</a></li>
- <a href="#windows-installation">Windows</a>
    - <a href="#windows-10-installation">Windows 10</a></li>
    - <a href="#windows-11-installation">Windows 11</a></li>
        - <a href="#windows-11-dual-boot">Dual Boot</a></li>
        - <a href="#windows-11-live-usb">Live USB</a></li>
- <a href="#macos-installation">MacOS</a></li>

<!-- #################### LINUX INSTALLATION #################### -->
⠀
<h2 id="linux-installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Linux.svg" width="25px" align="top"/>
    ⠀Linux
</h2>

> [!WARNING]
> This project is not compatible with Python 3.12 due to the removal of the <code>imp</code> module, which affects dependencies like <code>dbus-python</code>. Please use Python 3.11 or earlier to avoid issues (I'm currently using 3.11.13). If you are following the installation guide, don't worry about this warning.</span>

Install the necessary libraries. Open a terminal in the project folder and run the following commands:

```bash
sudo apt-get install -y python3-pyqt5 tesseract-ocr libtesseract-dev ffmpeg bluetooth
```
```bash
sudo pip install -r Requirements.txt && pip install -r Requirements.txt 
```

<!-- #################### WINDOWS INSTALLATION #################### -->
⠀
<h2 id="windows-installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Windows.svg" width="25px" align="top"/>
    ⠀Windows
</h2>

<h3 id="windows-10-installation">
    Windows 10 (Using VirtualBox VM)
</h3>

<h3 id="windows-11-installation">
    Windows 11 (Dual Boot or Live USB)
</h3>

<p>
    Windows 11 is more aggressive in sharing Bluetooth components between VirtualBox and your computer, so a VM setup will likely fail to connect. Instead, I recommend creating a disk partition and installing Linux alongside Windows 11. Another option is to use a Linux USB instead, though I haven’t tested this.
</p>

- <h3 id="windows-11-dual-boot">
    <a href="./Installation%20Dual%20Boot.md">Dual Boot</a>
</h3>

- <h3 id="windows-11-live-usb">
    <a href="./Installation%20Live%20USB.md">Live USB</a>
</h3>

<!-- #################### MAC OS INSTALLATION #################### -->
⠀
<h2 id="macos-installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Apple.svg" width="25px" align="top"/>
    ⠀MacOS
</h2>

<p>
    I’m not rich enough to own one... so I have no idea how to make it work. This is completely untested.
</p>
