<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Virtual%20Box.svg" width="30px" align="top"/>
    ⠀Download Ubuntu 24.04 ISO
</h2>

1. Go to the <a href="https://old-releases.ubuntu.com/releases/noble/" target="_blank">official Ubuntu webpage</a>.

2. Download: <code>ubuntu-24.04-desktop-amd64.iso</code>. The file is about 5.7 GB; it's the Ubuntu operating system.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/SVG/USB.svg" width="30px" align="top"/>
    ⠀Create a Flash USB
</h2>

1. Download <a href="https://rufus.ie/en/" target="_blank">Rufus</a>.

2. Plug in an empty USB (any data inside will be lost).
3. Open Rufus and set:
    - Device: <code>Your USB device</code>
    - Boot selection: <code>Select the Ubuntu ISO file</code>
    - Partition scheme: <code>GPT</code>
    - Target system: <code>UEFI (non-CSM)</code>
    - File system: <code>FAT32</code>
4. Click <b>Start</b>.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/SVG/Disk.svg" width="30px" align="top"/>
    ⠀Create a Disk Partition
</h2>

1. Press <code>Win + X</code> ➔ <code>Disk Management</code>.

2. Right-click your main partition (usually C:) and select <code>Shrink Volume</code>.
    - Shrink at least 25 GB, ideally ~50GB.
3. You will now see <b>“Unallocated Space”</b> in the disk.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Ubuntu.svg" width="30px" align="top"/>
    ⠀Boot Ubuntu
</h2>

1. Reboot your computer and press the BIOS key at startup. Usually <code>F2</code>, <code>F10</code>, <code>F12</code>, <code>DEL</code> or <code>ESC</code> (varies by brand).

    1. Go to the <code>Security</code> tab and disable the <code>Secure Boot</code> option.

    2. Save and exit by pressing <code>F10</code>.
2. Plug the Ubuntu USB stick.
3. Reboot your computer and press <code>F11</code> at startup.
    - Choose your USB device.
4. If you're prompted with multiple options, choose <b>"Try Ubuntu"</b>.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Gear 2.svg" width="30px" align="top"/>
    ⠀Install Ubuntu
</h2>

1. Once in the Ubuntu desktop preview, open the <code>Install Ubuntu</code> icon on the desktop

    - Select <code>Install Ubuntu alongside Windows Boot Manager</code>. This will automatically install Ubuntu in the unallocated space (disk partition).
2. Once everything is installed, unplug the USB stick and reboot.
3. You will have to press <code>F11</code> during the boot every time you want to boot Ubuntu instead of Windows (default).

<br>

> [!NOTE]
> After finishing the dual boot installation, continue with the <a href="./Installation.md#linux-installation">Linux installation</a> section.