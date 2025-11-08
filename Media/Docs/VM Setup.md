<!-- #################### INDEX #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Index.svg" width="30px" align="top"/>
    ⠀Index
</h2>

- <a href="#download-vbox-and-linux-iso">**Download Virtual Box (VBox) and Linux ISO**</a>
- <a href="#create-the-vm">**Create the Virtual Machine**</a>
    - <a href="#change-keyboard-distribution">Change Keyboard Distribution</a>
    - <a href="#auto-resize-vbox-window">Auto-Resize Virtual Box Window</a>
    - <a href="#install-python-3-11">Install Python 3.11</a>
    - <a href="#attach-bluetooth-and-capture-cards-to-vm">Attach Buetooth and Capture Cards to Virtual Box</a>
- <a href="#extra-vm-configurations">**Extra Configurations for the Virtual Machine**</a>
    - <a href="#run-sudo-commands-without-entering-password">Run Administrator Commands without Entering Password</a>
    - <a href="#enable-shared-clipboard-with-host">Enable Shared Clipboard with the Host</a>
    - <a href="#disable-idle-lock-screen">Disable Idle Lock Screen</a>
    - <a href="#make-vm-snapshot">Make a Snapshot of the Virtual Machine</a>

<br>

> [!NOTE]
> After finishing the VM installation, continue with the <a href="./Installation.md#linux-installation">Linux installation</a> section.

<br>

<!-- #################### DOWNLOAD VBOX AND ISO #################### -->

<h2 id="download-vbox-and-linux-iso">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Virtual%20Box.svg" width="30px" align="top"/>
    ⠀Download Virtual Box (VBox) and Linux ISO
</h2>

- Go to the <a href="https://www.virtualbox.org/wiki/Downloads" target="_blank">Virtual Box Official Webpage</a>. Download and install the correct **VirtualBox Platform Package** for your operating system. 
- Feel free to use the OS you feel more comfortable with; I'm using **Ubuntu 24.04**, but other Linux distributions will work as well. Go to the <a href="https://old-releases.ubuntu.com/releases/noble/" target="_blank">official Ubuntu webpage</a> and download the `ubuntu-xx.xx.x-desktop-amd64.iso`, where `xx.xx.x` is the version of the ISO. The file is about **5.7 GB**; it's the operating system of the Virtual Machine.

<br>

<!-- #################### CREATE THE VM #################### -->

<h2 id="create-the-vm">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Gear%202.svg" width="30px" align="top"/>
    ⠀Create the Virtual Machine
</h2>

- Open **Oracle VM VirtualBox** and click the `Add New` button.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%201.png" width="50%" style="border-radius: 5px;">
    </h6>

- Write a name for the Virtual Machine and select the ISO file. Click the `Next` button.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%202.png" width="70%" style="border-radius: 5px;">
    </h6>

- Create your username and password. If the **Additional Options** box raises a warning, replace spaces `" "` by `"-"`. Click the `Next` button.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%203.png" width="70%" style="border-radius: 5px;">
    </h6>

- The following step depends on the specifications of your computer. You can assign more or less RAM and Cores depending on how powerful your computer is. Allocating **4 GB** (4096 MB) of RAM and **2** Cores should be enough *(allocate more if possible for better performance)*. Click the `Next` button.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%204.png" width="70%" style="border-radius: 5px;">
    </h6>

- Select the `Create Virtual Disk Now` option and assign it about **20 GB** of memory. Click the `Next` button and then, `Finish`.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%205.png" width="70%" style="border-radius: 5px;">
    </h6>

    The Virtual Machine will automatically start. Wait until the installation is completed (it will take a while). From now on, you can make your mouse exit the Virtual Machine by pressing the `Right Ctrl` key. Once the installation has finished, the VM will automatically restart.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Ubuntu%20Installation.png" width="70%" style="border-radius: 5px;">
    </h6>

    After the restart, you'll see a message asking you to *"Upgrade to Ubuntu Pro"*. Just click `Skip for now` and then `Finish`.

<br>

<!-- #################### CONFIGURE THE VM #################### -->

<h2 id="configure-the-vm">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Gear%201.svg" width="30px" align="top"/>
    ⠀Configure the Virtual Machine
</h2>

<!-- #################### CHANGE KEYBOARD DISTRIBUTION #################### -->

<h3 id="change-keyboard-distribution">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Keyboard.svg" width="25px" align="top"/>
    ⠀Change Keyboard Distribution
</h3>

- First of all, if your keyboard layout does not match with the *"English (US)"* one, go to the start menu, type `keyboard` and open the keyboard manager.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Change%20Keyboard%20Distribution%201.png" width="70%" style="border-radius: 5px;">
    </h6>

- Now, go to the **Input Sources** section and click `Add Input Source`. Choose your keyboard layout from the list. Once it's added, move your language to the top of the list and/or remove the *"English (US)"* layout if you don't need it.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Change%20Keyboard%20Distribution%202.png" width="70%" style="border-radius: 5px;">
    </h6>

<!-- #################### AUTO-RESIZE VM WINDOW #################### -->

<h3 id="auto-resize-vbox-window">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Window.svg" width="25px" align="top"/>
    ⠀Auto-Resize Virtual Box Window
</h3>

- You may have noticed that when opening VBox in fullscreen mode, it does not scale correctly, leaving gray spaces at the borders.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Insert%20Guest%20Additions%201.png" width="70%" style="border-radius: 5px;">
    </h6>

- To solve this issue, `Right Click` on the Desktop and select `Open in Terminal`. Run the following commands one by one:

    ```bash
    sudo su
    nano /etc/sudoers
    ```

- Add the following line changing `dinones` by your username:

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%209.png" width="70%" style="border-radius: 5px;">
    </h6>

    Save the file by pressing `Ctrl + S` and then `Ctrl + X`. Close the terminal.

- Now, in the VBox top menu, click on `Devices` ➔ `Insert Guest Additions CD Image`.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2010.png" width="60%" style="border-radius: 5px;">
    </h6>

    A disk icon should appear in the desktop.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Insert%20Guest%20Additions%202.png" width="70%" style="border-radius: 5px;">
    </h6>

- Open it, *Right Click* inside the folder, and select *"Open Terminal Here"*. Run the following commands one by one:

    ```bash
    sudo apt update && sudo apt install -y bzip2 tar
    ./autorun.sh
    ```

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Insert%20Guest%20Additions%203.png" width="70%" style="border-radius: 5px;">
    </h6>

    Wait until the installation is finished and **restart the Virtual Machine**. Now, you should be able to use the fullscreen mode without seeing the gray borders. If not, go to the VBox top menu, click on `View` ➔ `Adjust Window Size` and `Auto-Resize Guest Display` to see if the VM window scales correctly. If it doesn't, open the `Virtual Display 1` settings and adjust the resolution manually until the window fits the way you want.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Insert%20Guest%20Additions%204.png" width="60%" style="border-radius: 5px;">
    </h6>

<!-- #################### INSTALL PYTHON 3.11 #################### -->

<h3 id="install-python-3-11">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Python.svg" width="25px" align="top"/>
    ⠀Install Python 3.11
</h3>

- This operating system comes with **Python 3.12** by default, but this version isn't compatible with the main library used by the project to emulate the controllers (`nxbt`). Because of that, you'll need to install **Python 3.11** instead. Open a terminal in the Desktop and run the following commands one by one to install it:

    ```bash
    sudo apt update && sudo apt install -y software-properties-common && sudo add-apt-repository ppa:deadsnakes/ppa -y && sudo apt update
    sudo apt install -y python3.11 python3.11-venv python3.11-dev
    ```

    Once installed, you’ll be ready to create a virtual environment using Python 3.11.

<!-- #################### ATTACH BLUETOOTH AND CAPTURE CARDS TO VBOX #################### -->

<h3 id="attach-bluetooth-and-capture-cards-to-vm">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/HDMI.svg" width="25px" align="top"/>
    ⠀Attach Buetooth and Capture Cards to Virtual Box
</h3>

- Once you have successfully installed and configured the VM, power it off. Open **Oracle VM VirtualBox**, select your VM and click the `Configuration` button.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2012.png" width="70%" style="border-radius: 5px;">
    </h6>

- Click on the `Add New USB Filter` button and select your Bluetooth adapter (*"Intel Corp"* in my case, but it will vary depending on your adapter brand). If you don't know what your adapter is, try disconnecting all USB from your computer; it will filter all your external devices and make it easier to identify it.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2013.png" width="70%" style="border-radius: 5px;">
    </h6>

- Now, repeat the previous point with the capture card (*"Macrosilicon USB Video"* in my case, but yours will probably be different). You should have something similar to this:

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2023.png" width="70%" style="border-radius: 5px;">
    </h6>

    If your capture card is not working or is not correctly detected, try using both USB options, **3.0** and **2.0**.

    Also, keep in mind that a USB filter only works for the specific port where your capture card is connected. If you plug it into a different USB port, the virtual machine won't detect it. To avoid this, you can connect the capture card to each USB port on your computer once and create a separate filter for every port.

- Accept the changes and start the Virtual Machine. You should now be able to see the Bluetooth symbol in the top-right corner of the window.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2014.png" width="50%" style="border-radius: 5px;">
    </h6>

<br>

<!-- #################### EXTRA CONFIGURATIONS #################### -->

<h2 id="extra-vm-configurations">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Gear%203.svg" width="30px" align="top"/>
    ⠀Extra Configurations for the Virtual Machine
</h2>

The following settings are completely optional, but **highly recommended**, as they'll make your life a lot easier. They only take a couple of extra minutes to set up, and they'll save you time later on.

<!-- #################### RUN SUDO COMMANDS WITHOUT PASSWORD #################### -->

<h3 id="run-sudo-commands-without-entering-password">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Lock.svg" width="25px" align="top"/>
    ⠀Run Administrator Commands without Entering Password
</h3>

- Open a terminal and run the following command:

    ```bash
    sudo visudo
    ```

- Add the following lines changing `dinones` by your username:

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2016.png" width="70%" style="border-radius: 5px;">
    </h6>

    Save the file by pressing `Ctrl + S` and then `Ctrl + X`. Close the terminal.

<!-- #################### ENABLE SHARED CLIPBOARD #################### -->

<h3 id="enable-shared-clipboard-with-host">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Clipboard.svg" width="25px" align="top"/>
    ⠀Enable Shared Clipboard with the Host
</h3>

This option lets you copy text on your host computer and paste it inside the VM, and viceversa. It's especially useful when you need to paste commands into the terminal.

- Power off the VM. Open **Oracle VM VirtualBox**, select your VM and click the `Configuration` button. Go to `Shared Folders` and click the `Add New Shared Folder` button. In the window that pops up, select your shared folder and check the `Automount` option.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2018.png" width="70%" style="border-radius: 5px;">
    </h6>

- Turn on the VM, open a terminal in the Desktop and run the following command:

    ```bash
    sudo adduser $USER vboxsf
    ```

    Restart the VM. Open the file manager. There should be an extra folder whose content is shared with your personal computer.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Shared%20Folder.png" width="70%" style="border-radius: 5px;">
    </h6>

<!-- #################### DISABLE IDLE LOCK SCREEN #################### -->

<h3 id="disable-idle-lock-screen">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Sleep.svg" width="25px" align="top"/>
    ⠀Disable Idle Lock Screen
</h3>

- Go to the start menu, type `Privacy and Security` and open the configuration.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Disable%20Lock%20Screen.png" width="70%" style="border-radius: 5px;">
    </h6>

- Now, click on `Screen Lock` and disable all the options.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Disable%20Lock%20Screen%202.png" width="70%" style="border-radius: 5px;">
    </h6>

<!-- #################### DISABLE IDLE LOCK SCREEN #################### -->

<h3 id="make-vm-snapshot">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Camera.svg" width="25px" align="top"/>
    ⠀Make a Snapshot of the Virtual Machine
</h3>

You can create a snapshot of the virtual machine so that if something goes wrong later, you don't have to repeat all the setup steps. The snapshot saves the current state of the VM, letting you easily roll back to this exact point whenever you need.

- To do so, power off the VM. Open **Oracle VM VirtualBox**, select your VM, click on `Options` ➔ `Snapshots` and create a snapshot.

    <h6 align="center">
        <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Create%20VM%20Snapshot.png" width="70%" style="border-radius: 5px;">
    </h6>

> [!NOTE]
> After finishing the VM installation, continue with the <a href="./Installation.md#linux-installation">Linux installation</a> section.