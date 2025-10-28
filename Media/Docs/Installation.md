<!-- #################### INDEX #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Index.svg" width="30px" align="top"/>
    ⠀Index
</h2>

- <a href="#linux-installation">**Linux**</a>
- <a href="#windows-installation">**Windows**</a>
    - <a href="#windows-10-installation">Windows 10</a>
        - <a href="#windows-10-vm-installation">VM Installation</a>
    - <a href="#windows-11-installation">Windows 11</a>
        - <a href="#windows-11-dual-boot">Dual Boot</a>
        - <a href="#windows-11-live-usb">Live USB</a>
- <a href="#macos-installation">**MacOS**</a>
- <a href="#raspberry-pi-installation">**Raspberry Pi**</a>

<br>

<!-- #################### LINUX INSTALLATION #################### -->

<h2 id="linux-installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Linux.svg" width="25px" align="top"/>
    ⠀Linux
</h2>

> [!WARNING]
> This project is **not** compatible with Python 3.12 due to the removal of the `imp` module, which affects dependencies like `dbus-python`. Please use Python 3.11 or earlier to avoid issues (I'm currently using 3.11.13). If you are following the installation guide, don't worry about this warning.

Install all required dependencies for your system. Open a terminal in the Desktop directory and run the following command:

```bash
sudo apt update && sudo apt install -y git python3-pip python3-dev python3-pyqt5 tesseract-ocr libtesseract-dev ffmpeg bluetooth libdbus-1-dev libglib2.0-dev
```

Once system dependencies are installed, open a terminal inside the project folder and execute the following commands one by one (line by line):

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```
```bash
pip install -r Requirements.txt
```

<br>

<!-- #################### WINDOWS INSTALLATION #################### -->

<h2 id="windows-installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Windows.svg" width="25px" align="top"/>
    ⠀Windows
</h2>

<h3 id="windows-10-installation">
    Windows 10 (Using VirtualBox VM)
</h3>

Windows 10 works pretty well with VirtualBox. It usually lets you share things like Bluetooth devices with the virtual machine without many issues.
For detailed instructions on creating and configuring a VirtualBox VM from scratch, see the following documentation.

- <a id="windows-10-vm-installation" href="./VM%20Setup.md">VM Installation</a>

<h3 id="windows-11-installation">
    Windows 11 (Dual Boot or Live USB)
</h3>

<p>
    Windows 11 is more aggressive in sharing Bluetooth components between VirtualBox and your computer, so a VM setup will likely fail to connect. Instead, I recommend creating a disk partition and installing Linux alongside Windows 11. Another option is to use a Linux USB instead, though I haven't tested its performance.
</p>

- <a id="windows-11-dual-boot" href="./Installation%20Dual%20Boot.md">Dual Boot</a>

- <a id="windows-11-live-usb" href="./Installation%20Live%20USB.md">Live USB</a>

<br>

<!-- #################### MAC OS INSTALLATION #################### -->

<h2 id="macos-installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Apple.svg" width="25px" align="top"/>
    ⠀MacOS
</h2>

<p>
    I'm not rich enough to own one... so I have no idea how to make it work. This is completely untested.
</p>

<!-- #################### MAC OS INSTALLATION #################### -->
⠀
<h2 id="raspberry-pi-installation">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Raspberry%20Pi.svg" width="25px" align="top"/>
    ⠀Raspberry Pi
</h2>

The setup has been tested on a **Raspberry Pi 5 (16 GB)** with an **SSD** running the official **Raspberry Pi OS**, and the performance is excellent. However, it hasn't been tested on older models like the Raspberry Pi 4 or 3, so performance on those devices may vary.

The installation process on a Raspberry Pi is exactly the same as on <a href="#linux-installation">Linux</a>. The only difference is that the PyQt5 library, which handles the interface, can sometimes cause issues during installation.

If you get an error when installing the requirements or when running the program, please read this troubleshooting sections:

- <a href="./Troubleshooting.md#raspberry-pi-installation-error">Raspberry Pi <code>PyQt5</code> Installation Error</a>

- <a href="./Troubleshooting.md#raspberry-pi-qt-plugin-error"><code>PyQt5</code> Platform Plugin <code>xcb</code> Could Not Be Initialized</a>