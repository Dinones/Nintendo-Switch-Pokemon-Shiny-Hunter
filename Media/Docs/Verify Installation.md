<!-- #################### CAPTURE CARD #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Camera.svg" width="30px" align="top"/>
    ⠀Detecting the Capture Card
</h2>

<p>Open a terminal in the <i>/Modules/</i> folder and run the following command:</p>

<pre><code>python3 Game_Capture.py</code></pre>

Select the "<i>Print all available video devices</i>" option. You should obtain at least one <b>OK</b>. If not, your capture card is not connected properly, please read [VM Setup Guide](./VM%20Setup.md).

<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Capture%20Card%20Verification.png" width="70%" style="border-radius: 5px;">
</h6>

If you obtained more than one <b>OK</b>, you can check what capture card is being used by running the previous command again and selecting the "<i>Check current capture device</i>" option. 

⠀
<!-- #################### GUI #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Monitor.svg" width="30px" align="top"/>
    ⠀Verify the User Interface
</h2>

<p>Open a terminal in the <i>/Modules/</i> folder and run the following command:</p>

<pre><code>python3 GUI.py</code></pre>

Select any "<i>Open GUI using capture card</i>" or "<i>Open GUI using a template image</i>" options. In both cases, you should see the main program user interface. 

<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/GUI%20Verification.png" width="70%" style="border-radius: 5px;">
</h6>

⠀
<!-- #################### DATABASE #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Database.svg" width="30px" align="top"/>
    ⠀Initialize the Database
</h2>

<p>Open a terminal in the <i>/Modules/</i> folder and run the following command:</p>

<pre><code>python3 Database.py</code></pre>

Select the "<i>Print database</i>" option. It should print an empty database, which will automatically store all the encounters and data related to your game. For example, how many Pokémon have you encountered, the total time running the program or the shiny count. You can check it whenever you want, as it may be interesting to you.

⠀
<!-- #################### SWITCH CONTROLLER #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Controller.svg" width="30px" align="top"/>
    ⠀Controlling the Nintendo Switch
</h2>

<img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Warning.svg" width="17px" align="left"/><span><strong>IMPORTANT:</strong> When using the Bluetooth system in the VM, Bluetooth may not work as expected on your Windows/MacOS computer.

On the Nintendo Switch home screen, go to "<i>Controllers</i>" > "<i>Change Grip/Order Menu</i>". Plug in both controllers to the Nintendo Switch and if not, make sure they're not connected via Bluetooth. (See steps [here](./Change%20Grip%20Menu.md)).<br>


<p>Open a terminal in the <i>/Modules/</i> folder and run the following command:</p>

<pre><code>python3 Switch_Controller.py</code></pre>

Select the "<i>Test Switch Controller</i>" option. It should appear a pairing request, which you will have to accept. It may ask you for the root password too.

<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Pairing%20Request%201.png" width="60%" style="border-radius: 5px;">
</h6>
<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Pairing%20Request%202.png" width="50%" style="border-radius: 5px;">
</h6>

After accepting it, the program should run a testing macro, which will go to the home menu and return to the pairing screen. It may not be working at the beginning, try restarting the **whole** computer (not just the Virtual Machine) and Bluetooth systems. If you are not able to connect your computer to the Nintendo, please, report it to [NXBT](https://github.com/Brikwerk/nxbt).

⠀
<!-- #################### SAVESTATE #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/SVG/Gear.svg" width="30px" align="top"/>
    Save the Virtual Machine's State
</h2>

If everything worked correctly, I highly recommend saving the state of the machine so you can recover it from this point in case it is messed up.

<p>Power off the VM. Open Oracle VM VirtualBox, select your VM, click the 3 dots next to its name and select "<i>Snapshots</i>".</p>
<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2021.png" width="70%" style="border-radius: 5px;">
</h6>
<p>Now, click on "<i>Take a Snapshot</i>", write a name and save it.</p>
<h6 align="center">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/VBox%20Instructions/VBox%2022.png" width="70%" style="border-radius: 5px;">
</h6>
<p>From now on, you can restore the Virtual Machine to this exact point by right-clicking the snapshot and selecting "<i>Restore</i>".</p>