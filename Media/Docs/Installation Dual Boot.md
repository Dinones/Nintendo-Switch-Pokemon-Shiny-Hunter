<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Virtual%20Box.svg" width="30px" align="top"/>
    ⠀Download Ubuntu 24.04 ISO
</h2>

1. Go to the <a href="https://old-releases.ubuntu.com/releases/noble/" target="_blank">official Ubuntu webpage</a>.

2. Download: `ubuntu-24.04-desktop-amd64.iso`. The file is about **5.7 GB**; it's the Ubuntu operating system.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/USB.svg" width="30px" align="top"/>
    ⠀Create a Flash USB
</h2>

1. Download <a href="https://rufus.ie/en/" target="_blank">Rufus</a>.

2. Plug in an empty USB (**any data inside will be lost**).

3. Open Rufus and set:
    - Device: `Your USB device`
    - Boot selection: `Select the Ubuntu ISO file`
    - Partition scheme: `GPT`
    - Target system: `UEFI (non-CSM)`
    - File system: `FAT32`

4. Click **Start**.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Disk.svg" width="30px" align="top"/>
    ⠀Create a Disk Partition
</h2>

1. Press `Win + X` ➔ `Disk Management`.

2. Right-click your main partition (usually C:) and select `Shrink Volume`.
    - Shrink at least 25 GB, ideally ~50GB.

3. You will now see **"Unallocated Space"** in the disk.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Ubuntu.svg" width="30px" align="top"/>
    ⠀Boot Ubuntu
</h2>

1. Reboot your computer and press the BIOS key at startup. Usually `F2`, `F10`, `F12`, `DEL` or `ESC` (varies by brand).

    1. Go to the `Security` tab and disable the `Secure Boot` option.

    2. Save and exit by pressing `F10`.

2. Plug the Ubuntu USB stick.

3. Reboot your computer and press `F11` at startup.
    - Choose your USB device.

4. If you're prompted with multiple options, choose **"Try Ubuntu"**.

<br>

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Gear 2.svg" width="30px" align="top"/>
    ⠀Install Ubuntu
</h2>

1. Once in the Ubuntu desktop preview, open the `Install Ubuntu` icon on the desktop

    - Select `Install Ubuntu alongside Windows Boot Manager`. This will automatically install Ubuntu in the unallocated space (disk partition).

2. Once everything is installed, unplug the USB stick and reboot.

3. You will have to press `F11` during the boot every time you want to boot Ubuntu instead of Windows (default).

<br>

> [!NOTE]
> After finishing the dual boot installation, continue with the <a href="./Installation.md#linux-installation">Linux installation</a> section.