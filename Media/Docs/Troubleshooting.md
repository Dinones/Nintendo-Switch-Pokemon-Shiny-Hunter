<h1 id="troubleshooting">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Virus.svg" width="30px" align="top"/>
    ⠀Troubleshooting
</h1>

<br>

<h2 id="raspberry-pi-installation-error">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Raspberry%20Pi.svg" width="25px" align="top"/>
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

<h2 id="raspberry-pi-qt-plugin-error">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Raspberry%20Pi.svg" width="25px" align="top"/>
    ⠀<code>PyQt5</code> Platform Plugin <code>xcb</code> Could Not Be Initialized
</h2>

If you encounter the following error while running the code:

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

Once it finished, reboot the Raspbeery Pi and try to run the code again.piendsa 