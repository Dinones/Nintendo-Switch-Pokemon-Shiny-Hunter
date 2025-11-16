<!-- ############################################### -->
<!-- #################### INDEX #################### -->
<!-- ############################################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Index.svg" width="30px" align="top"/>
    ⠀Index
</h2>

- <a href="#troubleshooting">**Troubleshooting**</a>
- **Raspberry Pi Issues**
    - <a href="#raspberry-pi-installation-error">Raspberry Pi PyQt5 Installation Error</a>
    - <a href="#raspberry-pi-qt-plugin-error">PyQt5 Platform Plugin xcb Could Not Be Initialized</a>
- **Program Stuck Issues**
    - <a href="#program-getting-stuck-in-home-screen-light-mode">Program Getting Stuck in the HOME Screen</a>
    - <a href="#program-getting-stuck-in-pairing-screen-screen-size">Program Getting Stuck in the Pairing Screen (Black Borders)</a>
    - <a href="#program-getting-stuck-in-pairing-screen-pixel-detection">Program Getting Stuck in the Pairing Screen (Pixel Detection)</a>
- **Bluetooth Connection Issues**
    - <a href="#bluetooth-pairing-loop">Bluetooth Controller Enters in "Pairing" Loop</a>

<br>

<!-- ############################################### -->
<!-- ############### TROUBLESHOOTING ############### -->
<!-- ############################################### -->

<h1 id="troubleshooting">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Virus.svg" width="35px" align="top"/>
    ⠀Troubleshooting
</h1>

Please, before opening a new issue, try the troubleshooting steps listed below. These are common problems that other users have already encountered, and following these instructions might save both of us some time. Keep in mind that this project is maintained by a single person, so I may not be able to respond to every issue immediately. Thank you for your understanding! If your problem persists after trying these solutions, feel free to report it on the <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/issues">issues</a> page.

<br>

<!-- ##################################################################### -->
<!-- ############### Raspberry Pi PyQt5 Installation Error ############### -->
<!-- ##################################################################### -->

<h2 id="raspberry-pi-installation-error">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Raspberry%20Pi.svg" width="30px" align="top"/>
    ⠀Raspberry Pi <code>PyQt5</code> Installation Error
</h2>

If you get an error when installing the requirements:

```bash
pip install -r Requirements.txt
```

Open the `Requirements.txt` file and remove the lines containing `PyQt5==x.x.x`. Then, run the same command again to install the rest of the dependencies.

Once that's done, install `PyQt5` separately by running:

```bash
source .venv/bin/activate
pip install PyQt5==5.15.11 --config-settings --confirm-license= --verbose
```

This step can take quite a while (in my case, it took around 45 minutes). It might look like it's stuck at some point, but it's still working. I recommend starting the installation and doing something else *(like touching grass or getting sunlight)* until it finishes.

Once it finishes, reboot the Raspbeery Pi.

<br>

<!-- ################################################################################## -->
<!-- ############### PyQt5 Platform Plugin xcb Could Not Be Initialized ############### -->
<!-- ################################################################################## -->

<h2 id="raspberry-pi-qt-plugin-error">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Raspberry%20Pi.svg" width="30px" align="top"/>
    ⠀<code>PyQt5</code> Platform Plugin <code>xcb</code> Could Not Be Initialized
</h2>

If you encounter the following error while trying to install <code>PyQt5</code>:

```
QObject::moveToThread: Current thread (0x341923c0) is not the object's thread (0x345240f0).
Cannot move to target thread (0x341923c0)

qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "/home/.../Nintendo-Switch-Pokemon-Shiny-Hunter/.venv/lib/python3.11/site-packages/cv2/qt/plugins" even though it was found.

This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: xcb, eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx.

Aborted
```

It indicates that there's an issue related to the `PyQt5` platform plugin initialization. This typically happens when `OpenCV` or `PyQt5` cannot properly load the required graphical backend.

To fix the issue, we need to rename the `PyQt5` plugin directory used by your `cv2` installation to make it undiscoverable. Run the following commands:

```bash
PLUGINS_DIR="$(python3 -c 'import cv2, pathlib; p = pathlib.Path(cv2.__file__).parent / "qt" / "plugins"; print(p)')"
```
```bash
mv "$PLUGINS_DIR" "${PLUGINS_DIR}.bak"
```

Once it finished, reboot the Raspbeery Pi and try to run the code again.

<br>

<!-- ######################################################################## -->
<!-- ############### Program Getting Stuck in the HOME Screen ############### -->
<!-- ######################################################################## -->

<h2 id="program-getting-stuck-in-home-screen-light-mode">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Monitor.svg" width="30px" align="top"/>
    ⠀Program Getting Stuck in the HOME Screen
</h2>

Try setting your Nintendo Switch to <b>light mode</b> and do <b>NOT</b> use any custom/animated theme. The program detects some specific pixels to determine if it is in the HOME screen; therefore, using dark mode or any custom/animated theme will break this feature.

<br>

<!-- ########################################################################################### -->
<!-- ############### Program Getting Stuck in the Pairing Screen (Black Borders) ############### -->
<!-- ########################################################################################### -->

<h2 id="program-getting-stuck-in-pairing-screen-screen-size">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Monitor.svg" width="30px" align="top"/>
    ⠀Program Getting Stuck in the Pairing Screen (Black Borders)
</h2>

When running the program, the controller connects successfully but remains stuck on the pairing screen, as shown in the image below.

<h3 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Troubleshooting%20Incorrect%20Screen%20Size.png" width="70%">
</h3>

If that happens, the issue is most likely related to your Nintendo Switch display settings. Notice the black borders around the image captured by your capture card; this indicates that the console's screen is being displayed at a size other than 100%, which prevents the program from recognizing the correct pairing state.

Please go to **System Settings → TV Settings → Screen Size** and set the value to **100%** on your Nintendo Switch.

After changing this, start the program as you did before, and everything should work.

If that didn't solve the issue, have a look at this <a href="#program-getting-stuck-in-pairing-screen-pixel-detection">solution</a>.

<br>

<!-- ############################################################################################# -->
<!-- ############### Program Getting Stuck in the Pairing Screen (Pixel Detection) ############### -->
<!-- ############################################################################################# -->

<h2 id="program-getting-stuck-in-pairing-screen-pixel-detection">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Monitor.svg" width="30px" align="top"/>
    ⠀Program Getting Stuck in the Pairing Screen (Pixel Detection)
</h2>

When running the program, the controller connects successfully but remains stuck on the pairing screen.
Please, have a look at this <a href="#program-getting-stuck-in-pairing-screen-screen-size">solution</a> before. If that didn't solve the issue, continue with this section.

It may be that your capture card is detecting slightly different colors compared to mine. Try going into the `Constants.py` file and changing the `PIXEL_COLOR_DIFF_THRESHOLD` value from `7` to something a bit higher, like `9` or `10`. Bigger numbers may cause missdetections in other states, so it's not recommended to increase its value much more than that.

<br>

<!-- ########################################################################### -->
<!-- ############### Program Getting Stuck in the Pairing Screen ############### -->
<!-- ########################################################################### -->

<h2 id="bluetooth-pairing-loop">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Controller.svg" width="30px" align="top"/>
    ⠀Bluetooth Controller Enters in "Pairing" Loop
</h2>

- This solution was proposed by **[@Lcocks](https://github.com/Lcocks)** in this [issue](https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/master/Media/Docs/Troubleshooting.md#bluetooth-pairing-loop).

<br>

If the Switch shows `Paired` but no controller fills slot 1, and you see connect/disconnect loops, edit the `/etc/bluetooth/main.conf` file by opening a terminal and running `sudo nano /etc/bluetooth/main.conf`. Search for the `[General]` section and set the specified parameters as follows:

```
[General]
Discoverable=true
DiscoverableTimeout=0
FastConnectable=true
RemoteNameRequest=false
DiscoverServices=false
BrEdrInterleaveEnabled=false
```

Save the file by pressing `Ctrl + S` and then `Ctrl + X`. Then run:

```bash
sudo systemctl restart bluetooth
```

Optionally (but recommended), reinstall `nxbt`. Open a terminal in the project folder and run:

```bash
# Activate the venv
source .venv/bin/activate

# Reinstall nxbt
pip install nxbt --force-reinstall
```

Add your user to the Bluetooth group:

```
sudo usermod -aG bluetooth $USER
```
Then, reboot the system so the new group permissions take effect.
   
Restart the Bluetooth service:

```bash
sudo systemctl restart bluetooth
```

Check that your user now has access. Run:

```bash
groups
```

And make sure `bluetooth` appears in the list.

Optionally verify adapter status:

```bash
bluetoothctl show

# It should show:
# Powered: yes
# Discoverable: yes
# Pairable: yes
```

Re-run the program and check if it works now. If it still fails, reboot once.