<!-- #################### INDEX #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Index.svg" width="30px" align="top"/>
    ⠀Index
</h2>

- <a href="#detecting-capture-card">**Detecting the Capture Card**</a>
- <a href="#verify-user-interface">**Verify the User Interface**</a>
- <a href="#initialize-database">**Initialize the Database**</a>
- <a href="#controlling-nintendo-switch">**Controlling the Nintendo Switch**</a>

<br>

<!-- #################### CAPTURE CARD #################### -->

<h2 id="detecting-capture-card">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Camera.svg" width="30px" align="top"/>
    ⠀Detecting the Capture Card
</h2>

Open a terminal in the main project folder and run the following command:

```bash
.venv/bin/python3 Modules/Game_Capture.py
```

Select the `Print all available video devices` option. You should obtain at least one **OK**. If not, your capture card is not connected properly, please read <a href="./VM%20Setup.md">VM Setup Guide</a> again.

<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Capture%20Card%20Verification.png" width="70%" style="border-radius: 5px;">
</h6>

If you obtained more than one **OK**, you can check what capture card is being used by running the previous command again and selecting the `Check current capture device` option. 

<br>

<!-- #################### GUI #################### -->

<h2 id="verify-user-interface">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Monitor.svg" width="30px" align="top"/>
    ⠀Verify the User Interface
</h2>

Open a terminal in the main project folder and run the following command:

```bash
.venv/bin/python3 Modules/sGUI.py
```

Select any `Open GUI using capture card` or `Open GUI using a template image` options. In both cases, you should see the main program user interface. 

<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/GUI%20Verification.png" width="70%" style="border-radius: 5px;">
</h6>

<br>

<!-- #################### DATABASE #################### -->

<h2 id="initialize-database">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Database.svg" width="30px" align="top"/>
    ⠀Initialize the Database
</h2>

Open a terminal in the main project folder and run the following command:

```bash
.venv/bin/python3 Modules/Database.py
```

Select the `Print database` option. It should print an empty database, which will automatically store all the encounters and data related to your game. For example, how many Pokémon have you encountered, the total time running the program or the shiny count. You can check it whenever you want, as it may be interesting to you.

<br>

<!-- #################### SWITCH CONTROLLER #################### -->

<h2 id="controlling-nintendo-switch">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Controller.svg" width="30px" align="top"/>
    ⠀Controlling the Nintendo Switch
</h2>

> [!WARNING]
> When using the Bluetooth system in the VM, Bluetooth may not work as expected on your host system (Windows/MacOS).

On the Nintendo Switch home screen, go to `Controllers` ➔ `Change Grip/Order Menu` (see steps <a href="./Change%20Grip%20Menu.md">here</a>). Plug in both controllers to the Nintendo Switch and if not, make sure they're not connected via Bluetooth.


Open a terminal in the main project folder and run the following command:

```bash
.venv/bin/python3 Modules/Switch_Controller.py
```

Select the `Test Switch Controller` option. A pairing request should appear, which you will have to accept. It may ask you for the root password too.

<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Pairing%20Request%201.png" width="60%" style="border-radius: 5px;">
</h6>
<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Pairing%20Request%202.png" width="50%" style="border-radius: 5px;">
</h6>

After accepting it, the program should run a testing macro, which will go to the **HOME** menu and return to the pairing screen. It may not be working at the beginning, try restarting the **whole** computer (not just the Virtual Machine) and Bluetooth systems. If you are not able to connect your computer to the Nintendo, please, report it to <a href="https://github.com/Brikwerk/nxbt" target="_blank">NXBT</a>.