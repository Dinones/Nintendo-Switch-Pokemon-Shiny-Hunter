<!-- #################### INDEX #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Index.svg" width="30px" align="top"/>
    ⠀Index
</h2>

- <a href="#constant-variables">**Constant Variables**</a>
- <a href="#important-variables">**Important Variables**</a>
    - <a href="#VIDEO_CAPTURE_INDEX">VIDEO_CAPTURE_INDEX</a>
    - <a href="#LANGUAGE">LANGUAGE</a>
    - <a href="#SAVE_IMAGES">SAVE_IMAGES</a>
    - <a href="#ENABLE_VIDEO_RECORDING">ENABLE_VIDEO_RECORDING</a>
    - <a href="#WILD_WALKING_SECONDS">WILD_WALKING_SECONDS</a>
    - <a href="#WILD_WALKING_DIRECTION">WILD_WALKING_DIRECTION</a>
    - <a href="#STARTER">STARTER</a>
    - <a href="#STATIC_ENCOUNTERS_DELAY">STATIC_ENCOUNTERS_DELAY</a>
- <a href="#other-variables">**Other Variables**</a>
    - <a href="#SHINY_RECORDING_SECONDS">SHINY_RECORDING_SECONDS</a>
    - <a href="#PLAY_SOUNDS">PLAY_SOUNDS</a>

<br>

<h2 id="constant-variables">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Code.svg" width="30px" align="top"/>
    ⠀Constant Variables
</h2>

The `Constants.py` file stores important global variables that are used and shared throughout the program through all the Python files. It can be found in the main project folder and you can edit it by double-clicking on it as if it was a simple `.txt` file. 

<br>

<h2 id="important-variables">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Star.svg" width="30px" align="top"/>
    ⠀Important Variables
</h2>

- <span id="VIDEO_CAPTURE_INDEX"> **VIDEO_CAPTURE_INDEX:** If you have multiple capture devices or webcams, the default one may not be the desired one. You can change the value of this variable to select which device to use.
You can run the `Game_Capture.py` script to help you find the desired index:

    ```bash
    .venv/bin/python Modules/Game_Capture.py
    # Select option 1: Print all available video devices
    # Select option 2: Check current capture device
    ```

    - *The value must be an integer number starting from `0` (included)*.

- <span id="LANGUAGE"> **LANGUAGE:** Select your in-game language. For `KO`, `ZH-CN` and `ZH-TW` the program will work, but the database module will do weird things.

    - *The value must be a literal string of the following: `ES`, `EN`, `DE`, `FR`, `IT`, `KO`, `ZH-CN` or `ZH-TW`.*

- <span id="SAVE_IMAGES"> **SAVE_IMAGES:** The program will automatically save an image of every encounter *(by default)* in the `Media/Images/`. You can stop saving images with this variable. Remember to erase the images from time to time to not run out of space.

    - *The value must be a boolean `True` or `False`.*

    You can check the saved images afterwards by running the `Image_Processing.py` script:

    ```bash
    .venv/bin/python Modules/Image_Processing.py
    # Select option 4: Check lost shiny
    ```

- <span id="ENABLE_VIDEO_RECORDING"> **ENABLE_VIDEO_RECORDING:** The program will automatically save a video of the shiny encounter *(by default)* in the `Media/Videos/` folder. This may cause a huge degradation in the program performance in less powerful systems (like some Raspberry Pi). You can disable this feature with this variable.

    - *The value must be a boolean `True` or `False`.*

- <span id="WILD_WALKING_SECONDS"> **WILD_WALKING_SECONDS:** Specifies the amount of time (seconds) the player will move in each direction when searching a wild Pokémon.

    - *The value must be an integer number greater than `0`.*

- <span id="WILD_WALKING_DIRECTION"> **WILD_WALKING_DIRECTION:** Specifies if the playes has to move from North to South (`"NS"`) or from East to West (`"EW"`).

    - *The value must be a literal string of the following: `"NS"` or `"EW"`.*

- <span id="STARTER"> **STARTER:** Specifies which starter Pokémon the program will select: the left (`"L"`), the center (`"C"`) or the right `"R"` one.

    - *The value must be a literal string of the following: `"L"`, `"C"` or `"R"`.*

- <span id="STATIC_ENCOUNTERS_DELAY"> **STATIC_ENCOUNTERS_DELAY:** Some static encounters make a white screen flash before entering the combat. This variable is really important for a precise detection of the Pokémon. The default value is `2` and works for most of the static encounters. Nevertheless, you must raise this value for some pokémon:

    - *The value must be an integer number equal or greater than `2`.*
    - Default: `2`.
    - Uxie: `3`.
    - Dialga and Palkia: `4`.
    - Arceus: `6.5`.
    - Regigigas: `7`.

<br>

<h2 id="other-variables">
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/SVG/Gear%201.svg" width="30px" align="top"/>
    ⠀Other Variables
</h2>

- <span id="SHINY_RECORDING_SECONDS"> **SHINY_RECORDING_SECONDS:** Whenever a shiny Pokémon is found, the program automatically saves a video of the encounter in the `Media/Videos/` folder. You can edit the length of the video (seconds) with this variable.

    - *The value must be an integer number greater than `0` and lower than `110`.*

- <span id="PLAY_SOUNDS"> **PLAY_SOUNDS:** Whenever a shiny Pokémon is found or if an error occurs, the program will play a sound to let you know. You can toggle it during the program execution by pressing the sound button on the interface. Nevertheless, you can set the default value with this variable.

    - *The value must be a boolean `True` or `False`.*