<h1 align="center">
    <br><img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/Virtual%20Box%20and%20Linux.png" width="50%"></br>
</h1>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/SVG/Virtual%20Box.svg" width="30px" align="top"/>
    Download Virtual Box (VBox) and Linux ISO
</h2>

- Go to the [Virtual Box Official Webpage](https://www.virtualbox.org/wiki/Downloads). Download and install the correct *VirtualBox Platform Package* for your operating system. 
- Feel free to use the OS you feel more comfortable with; I'm using **XUbuntu**, but other Linux distributions will work as well. Go to [XUbuntu Webpage](https://cdimage.ubuntu.com/xubuntu/releases/20.04.3/release/). Select your nearest location to get the mirror and download the *xubuntu-xx.xx.x-desktop-amd64.iso*, where *xx.xx.x* is the version of the ISO (I'm currently using the version *20.04.6*). The file is about 1.8GB; it's the operating system of the Virtual Machine.

<!-- #################### SETUP VIRTUAL MACHINE #################### -->
⠀
<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/SVG/Gear.svg" width="30px" align="top"/>
    Setup the Virtual Machine
</h2>

### Create the Virtual Machine

<ul>
    <li>
        <p>Open <strong>Oracle VM VirtualBox</strong> and click the <code>Add New</code> button.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%201.png" width="50%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Write a name for the Virtual Machine and select the ISO. Click the <code>Next</code> button.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%202.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Create your username and password. If the <i>Additional Options</i> box raises a warning, replace spaces " " by "-". Click the <code>Next</code> button.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%203.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>The following step depends on the specifications of your computer. You can assign more or less RAM and Cores depending on how powerful your computer is. 4GB of RAM and 2 Cores are enough. Click the <code>Next</code> button.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%204.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Select the <i>Create Virtual Disc Now</i> option and assign it about 20GB of memory. Click the <code>Next</code> button and then, <code>Finish</code>.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%205.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>The Virtual Machine will automatically start. Wait until it completes the installation. From now on, you can make your mouse exit the Virtual Machine by pressing <i>Right Ctrl</i> key.</p>
    </li>
</ul>

⠀
### Configure the Virtual Machine

<ul>
    <li>
        <p>Once the installation has finished, XUbuntu will ask you to upgrade to the latest version; click <code>Don't Upgrade</code>. If your keyboard layout does not match with the <i>"English (US)"</i> one, go to the start menu, type <code>keyboard</code> and open the keyboard manager. Now, click on <i>Layout</i>, disable the <i>"Use System Default"</i> box and add your layout. Finally, place your language in the first position by using the arrows on the right. If the system still uses the English layout, remove it from the list.</p> 
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%207.png" width="40%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Install git and pip on your system. Open a terminal and run the following command:</p>
        <pre><code>sudo apt install git python3-pip
</code></pre>
    </li>
    <li>
        <p>You may have noticed that when opening VBox in fullscreen mode, it does not scale correctly, leaving gray spaces at the borders.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%208.png" width="70%" style="border-radius: 5px;">
        </h6>
        <p>To solve this issue, <i>Right Click</i> on the Desktop and select <i>Open in Terminal</i>. Run the following commands one by one:</p>
<pre><code>su 
nano /etc/sudoers</code></pre>
        <p>Add the following line changing <i>"dinones"</i> by your username:</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%209.png" width="70%" style="border-radius: 5px;">
        </h6>
        <p>Save the file by pressing <i>Ctrl + S</i> and then <i>Ctrl + X</i>. Close the terminal.</p>
    </li>
    <li>
        <p>Now, in the VBox top menu, click on <i>Devices</i> > <i>Insert Guest Additions CD Image</i>.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2010.png" width="60%" style="border-radius: 5px;">
        </h6>
        <p>A disc icon should appear in the desktop. Open it, <i>Right Click</i> inside the folder, and select <i>"Open Terminal Here"</i>. Run the following command:</p>
        <pre><code>./autorun.sh</code></pre>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2011.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Wait until the installation is finished and restart the Virtual Machine. Now, you should be able to use the fullscreen mode without seeing the gray borders. If not, go to the VBox top menu, click on <i>View</i> and <i>Adjust Window Size</i>.</p>
    </li>
</ul>

⠀
### Stablish Connection with Capture Card and Bluetooth Adapter

<ul>
    <li>
        <p>Once you have successfully installed and configured the VM, power it off. Open <strong>Oracle VM VirtualBox</strong>, select your VM and click the <code>Configuration</code> button.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2012.png" width="50%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Go to <i>USB</i> and enable the option "<i>Enable USB Controller</i>". Select the USB controller type that you have installed on your PC. If you don't know it, just select any of them; if it doesn't work, try another one. Now, click on the <code>Add New USB Filter</code> button and select your capture card device (<i>"Macrosilicon USB Video"</i> in my case, but yours will probably be different).</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2013.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Note that you have created a filter for your capture card on a specific port, which means that if you connect the device to a different physical port of your computer, it won't be detected. To avoid this, you can connect the capture card to all your ports and add the filters one by one. This example shows my configuration for the same device on two different ports:</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2014.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
    <li>
        <p>Click on the <code>Add New USB Filter</code> button and select your Bluetooth adapter (<i>"Intel Corp"</i> in my case, but it will vary depending on your adapter brand). If you don't know what your adapter is, try disconnecting all USB from your computer; it will filter all your external devices and make it easier to identify it.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2015.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
</ul>

⠀
### [Optional] Extra Configurations for the Virtual Machine 

The following configurations are completely optional, but highly recommended for a more friendly experience:

<ul>
    <li>
        <p><strong>Run <i>sudo</i> Commands without Entering Password</strong></p>
        <p>Open a terminal and run the following command:</p>
        <pre><code>sudo visudo</code></pre>
        <p>Add the following line changing <i>dinones</i> by your username:</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2016.png" width="70%" style="border-radius: 5px;">
        </h6>
        <p>Save the file pressing <i>Ctrl + S</i> and then <i>Ctrl + X</i>.</p>
    </li>
    <li>
        <p><strong>Enable Shared Clipboard</strong></p>
        <p>Power off the VM. Open <strong>Oracle VM VirtualBox</strong>, select your VM and click the <code>Configuration</code> button.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2012.png" width="50%" style="border-radius: 5px;">
        </h6>
        <p>Go to <i>General</i> > <i>Advanced</i> and change both options to "<i>Bidirectional</i>".</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2017.png" width="70%" style="border-radius: 5px;">
        </h6>
        <p>You should now be able to drag and drop files and also copy and paste text from/to the virtual machine to/from your personal computer.</p>
    </li>
    <li>
        <p><strong>Create a Shared Folder between your Computer and the VM</strong></p>
        <p>Power off the VM. Open <strong>Oracle VM VirtualBox</strong>, select your VM and click the <code>Configuration</code> button. Go to <i>Shared Folders</i> and click the <code>Add New Shared Folder</code> button. In the window that pops up, select your shared folder and check the <i>Automount</i> option.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2018.png" width="70%" style="border-radius: 5px;">
        </h6>
        <p>Turn on the VM, open a terminal and run the following command:</p>
        <pre><code>sudo adduser $USER vboxsf</code></pre>
        <p>Restart the VM. Open the file manager. There should be an extra folder whose content is shared with your personal computer.</p>
        <h6 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2019.png" width="70%" style="border-radius: 5px;">
        </h6>
    </li>
</ul>