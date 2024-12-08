<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Code.svg" width="30px" align="top"/>
    ⠀Function Codes
</h2>

<!-- #################### CHECK PAIRING COLOR #################### -->

<h3 id="check-pairing-color">Check Pairing Color</h3>


<p>Check if the top-left and top-right parts of the screen are of the gray color of the pairing screen.</p>

<details>
    <summary>Toggle to see example images</summary>
    <h3 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Pairing%20Screen%20Visible.png" width="70%">
        <p></p>
    </h3>
</details>

<hr>

<!-- #################### CHECK HOME COLOR #################### -->

<h3 id="check-home-color">Check Home Color</h3>

<p>Verify if the color of some specific pixels located in the top-left part of the screen match the gray color of the HOME screen.</p>

<details>
    <summary>Toggle to see example images</summary>
    <h3 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Home%20Screen%20Visible.png" width="70%">
        <p></p>
    </h3>
</details>

<hr>

<!-- #################### WHITE SCREEN VISIBLE #################### -->

<h3 id="white-screen-visible">White Screen Visible</h3>

<p>Check if the image is completely white by verifying that some specific positions in the image <i>(top-left, top-right, center, bottom-left, and bottom-right)</i> are white.</p>

<details>
    <summary>Toggle to see example images</summary>
    <h3 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/White%20Loadscreen%20Visible.png" width="70%">
        <p></p>
    </h3>
</details>

<hr>

<!-- #################### BLACK SCREEN VISIBLE #################### -->

<h3 id="black-screen-visible">Black Screen Visible</h3>

<p>Check if the image is completely black by verifying that some specific positions in the image <i>(top-left, top-right, center, bottom-left and bottom-right)</i> are black.</p>

<details>
    <summary>Toggle to see example images</summary>
    <h3 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Black%20Loadscreen%20Visible.png" width="70%">
        <p></p>
    </h3>
</details>

<hr>

<!-- #################### TEXT BOX VISIBLE #################### -->

<h3 id="text-box-visible">Text Box Visible</h3>

<p>Check if the text box is visible by verifying the left and right parts of the text box, as well as other points that are not white <i>(center, top-left, and top-right)</i>. This is done to avoid mistakenly detecting the screen as displaying the text box if it is entirely white.</p>

<details>
    <summary>Toggle to see example images</summary>
    <h3 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Text%20Box%20Visible.png" width="70%">
        <p></p>
    </h3>
</details>

<hr>

<!-- #################### LIFE BOX VISIBLE #################### -->

<h3 id="text-box-visible">Life Box Visible</h3>

<p>Check if the life box is visible by verifying the left part of the life box, as well as other points that are not white <i>(center, center-left, and top-left)</i>. This is done to avoid mistakenly detecting the screen as displaying the life box if it is entirely white.</p>

<details>
    <summary>Toggle to see example images</summary>
    <h3 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/Life%20Box%20Visible.png" width="70%">
        <p></p>
    </h3>
</details>

<hr>

<!-- #################### BDSP LOAD SCREEN VISIBLE #################### -->

<h3 id="bdsp-load-screen-visible">BDSP Load Screen Visible</h3>

<p>Check if the image is the BDSP black load screen by verifying that some specific positions in the image <i>(top-right, center-right, center-left and bottom-left)</i> are black.</p>

<details>
    <summary>Toggle to see example images</summary>
    <h3 align="center">
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/BDSP%20Loadscreen%20Visible%201.png" width="70%">
        <p></p>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/BDSP%20Loadscreen%20Visible%202.png" width="70%">
        <p></p>
            <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/BDSP%20Loadscreen%20Visible%203.png" width="70%">
        <p></p>
    </h3>
</details>

<br><br>

<!-- #################### WILD STATE MACHINE #################### -->

<h2>
    <img src="https://raw.githubusercontent.com/Dinones/Repository-Images/master/NS%20Shiny%20Hunter/SVG/Star.svg" width="30px" align="top"/>
    ⠀Wild Encounter State Machine
</h2>

```mermaid
graph TD
    %%%%%%%%%%%%%%%% WAIT_PAIRING_SCREEN %%%%%%%%%%%%%%%%

    START((·)) --> WAIT_PAIRING_SCREEN("
        <b>WAIT_PAIRING_SCREEN</b>
        <span style='font-size:14px; color:#C00;'>Pairing Screen</span>
    ")
    WAIT_PAIRING_SCREEN --> CHECK_PAIRING_COLOR{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#check-pairing-color" style='text-decoration:none;'>Check</br>Pairing</br>Color</a>
    "}
    CHECK_PAIRING_COLOR -- "⠀✘⠀" --> WAIT_PAIRING_SCREEN
    CHECK_PAIRING_COLOR -- "⠀✔⠀" --> WAIT_HOME_SCREEN("
        <b>WAIT_HOME_SCREEN</b>
        <span style='font-size:14px; color:#C00;'>Home Screen</span> 
        <span style='font-size:13px; color:#C0C;'><i>fast_start_macro</i></span>
    ")


    %%%%%%%%%%%%%%%% WAIT_HOME_SCREEN %%%%%%%%%%%%%%%%
    
    WAIT_HOME_SCREEN --> CHECK_HOME_COLOR{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#check-home-color" style='text-decoration:none;'>Check</br>Home</br>Color</a>
    "}
    CHECK_HOME_COLOR -- "⠀✘⠀" --> WAIT_HOME_SCREEN
    CHECK_HOME_COLOR -- "⠀✔⠀" --> MOVE_PLAYER("
        <b>MOVE_PLAYER</b>
        <span style='font-size:14px; color:#C00;'>Overworld</span>
        <span style='font-size:13px; color:#C0C;'><i>move_player_wild_macro</i></span>
    ")


    %%%%%%%%%%%%%%%% MOVE_PLAYER %%%%%%%%%%%%%%%%

    MOVE_PLAYER --> WHITE_SCREEN_VISIBLE_1{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#white-screen-visible" style='text-decoration:none;'>White</br>Screen</br>Visible</a>
    "}
    WHITE_SCREEN_VISIBLE_1 -- "⠀✘⠀" --> MOVE_PLAYER
    WHITE_SCREEN_VISIBLE_1 -- "⠀✔⠀" --> ENTER_COMBAT_1("
        <b>ENTER_COMBAT_1</b>
        <span style='font-size:14px; color:#C00;'>Combat White Loadscreen</span>
    ")


    %%%%%%%%%%%%%%%% ENTER_COMBAT %%%%%%%%%%%%%%%%

    ENTER_COMBAT_1 --> WHITE_SCREEN_VISIBLE_2{"
        Time > 0.5s
        + not <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#white-screen-visible" style='text-decoration:none;'>White</br>Screen</br>Visible</a>
    "}
    WHITE_SCREEN_VISIBLE_2 -- "⠀✘⠀" --> ENTER_COMBAT_1
    WHITE_SCREEN_VISIBLE_2 -- "⠀✔⠀" --> ENTER_COMBAT_2("
        <b>ENTER_COMBAT_2</b>
        <span style='font-size:14px; color:#C00;'>Loading Combat</span>
        <span style='font-size:14px; color:#C00;'>(Wild Pokémon Appears)</span>
    ")


    ENTER_COMBAT_2 --> TEXT_BOX_VISIBLE_1{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#text-box-visible" style='text-decoration:none;'>Text Box</br>Visible</a>
    "}
    TEXT_BOX_VISIBLE_1 -- "⠀✘⠀" --> ENTER_COMBAT_2
    TEXT_BOX_VISIBLE_1 -- "⠀✔⠀" --> ENTER_COMBAT_3("
        <b>ENTER_COMBAT_3</b>
        <span style='font-size:14px; color:#C00;'>Loading Combat</span>
    ")


    ENTER_COMBAT_3 --> TEXT_BOX_VISIBLE_2{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#text-box-visible" style='text-decoration:none;'>Text Box</br>Visible</a>
    "}
    TEXT_BOX_VISIBLE_2 -- "⠀✔⠀" --> ENTER_COMBAT_3
    TEXT_BOX_VISIBLE_2 -- "⠀✘⠀" --> CHECK_SHINY("
        <b>CHECK_SHINY</b>
        <span style='font-size:14px; color:#C00;'>Loading Combat</span>
        <span style='font-size:14px; color:#C00;'>(Trainer Throws Pokémon)</span>
    ")


    %%%%%%%%%%%%%%%% CHECK_SHINY %%%%%%%%%%%%%%%%

    CHECK_SHINY --> TEXT_BOX_VISIBLE_3{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#text-box-visible" style='text-decoration:none;'>Text Box</br>Visible</a>
    "}
    TEXT_BOX_VISIBLE_3 -- "⠀✘⠀" --> CHECK_SHINY
    TEXT_BOX_VISIBLE_3 -- "⠀✔⠀" --> ESCAPE_COMBAT_1("
        <b>ESCAPE_COMBAT_1</b>
        <span style='font-size:14px; color:#C00;'>Loading Combat</span>
    ")


    CHECK_SHINY --> SHINY_TIMER{"Time > 2s"}
    SHINY_TIMER -- "⠀✘⠀" --> CHECK_SHINY
    SHINY_TIMER -- "⠀✔⠀" --> SHINY_FOUND("
        <b>SHINY_FOUND</b>
        <span style='font-size:14px; color:#C00;'>Loading Combat</span>
    ")


    %%%%%%%%%%%%%%%% SHINY_FOUND %%%%%%%%%%%%%%%%

    SHINY_FOUND --> SHINY_RECORDING_TIME{{"Record Video for 60s"}}
    SHINY_RECORDING_TIME --> STOP("
        <b>STOP</b>
        <span style='font-size:14px; color:#C00;'>Combat Loaded</span>
        <span style='font-size:13px; color:#C0C;'><i>stop_macro</i></span>
    ")
    STOP --> END((·))


    %%%%%%%%%%%%%%%% ESCAPE_COMBAT %%%%%%%%%%%%%%%%

    ESCAPE_COMBAT_1 --> LIFE_BOX_VISIBLE_1{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#life-box-visible" style='text-decoration:none;'>Life Box</br>Visible</a>
    "}
    LIFE_BOX_VISIBLE_1 -- "⠀✘⠀" --> ESCAPE_COMBAT_1
    LIFE_BOX_VISIBLE_1 -- "⠀✔⠀" --> ESCAPE_COMBAT_2("
        <b>ESCAPE_COMBAT_2</b>
        <span style='font-size:14px; color:#C00;'>Combat Loaded</span>
        <span style='font-size:13px; color:#C0C;'><i>escape_combat_macro</i></span>
    ")


    ESCAPE_COMBAT_2 --> TEXT_BOX_VISIBLE_4{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#text-box-visible" style='text-decoration:none;'>Text Box</br>Visible</a>
    "}
    TEXT_BOX_VISIBLE_4 -- "⠀✘⠀" --> ESCAPE_COMBAT_2
    TEXT_BOX_VISIBLE_4 -- "⠀✔⠀" --> ESCAPE_COMBAT_3("
        <b>ESCAPE_COMBAT_3</b>
        <span style='font-size:14px; color:#C00;'>Combat Loaded</span>
    ")


    ESCAPE_COMBAT_3 --> TEXT_BOX_VISIBLE_5{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#text-box-visible" style='text-decoration:none;'>Text Box</br>Visible</a>
    "}
    TEXT_BOX_VISIBLE_5 -- "⠀✔⠀" --> ESCAPE_COMBAT_3
    TEXT_BOX_VISIBLE_5 -- "⠀✘⠀" --> ESCAPE_COMBAT_4("
        <b>ESCAPE_COMBAT_4</b>
        <span style='font-size:14px; color:#C00;'>Combat Loaded</span>
    ")


    ESCAPE_COMBAT_4 --> LIFE_BOX_VISIBLE_2{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#life-box-visible" style='text-decoration:none;'>Life Box</br>Visible</a>
    "}
    LIFE_BOX_VISIBLE_2 -- "⠀✘⠀" --> ESCAPE_COMBAT_4
    LIFE_BOX_VISIBLE_2 -- "⠀✔⠀" --> ESCAPE_FAILED_1("
        <b>ESCAPE_FAILED_1</b>
        <span style='font-size:14px; color:#C00;'>Combat Loaded</span>
    ")


    %%%%%%%%%%%%%%%% ESCAPE_FAILED %%%%%%%%%%%%%%%%

    %% Written in the middle to avoid arrows crossing each other
    %% ESCAPE_COMBAT section continues below this section

    ESCAPE_FAILED_1 --> LIFE_BOX_VISIBLE_3{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#life-box-visible" style='text-decoration:none;'>Life Box</br>Visible</a>
    "}
    LIFE_BOX_VISIBLE_3 -- "⠀✘⠀" --> ESCAPE_FAILED_1
    LIFE_BOX_VISIBLE_3 -- "⠀✔⠀" --> ESCAPE_FAILED_2("
        <b>ESCAPE_FAILED_2</b>
        <span style='font-size:14px; color:#C00;'>Combat Loaded</span>
        <span style='font-size:13px; color:#C0C;'><i>press_A_macro</i></span>
    ")


    ESCAPE_FAILED_2 --> TEXT_BOX_VISIBLE_6{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#text-box-visible" style='text-decoration:none;'>Text Box</br>Visible</a>
    "}
    TEXT_BOX_VISIBLE_6 -- "⠀✘⠀" --> ESCAPE_FAILED_2
    TEXT_BOX_VISIBLE_6 -- "⠀✔⠀" --> ESCAPE_COMBAT_3


    %%%%%%%%%%%%%%%% ESCAPE_COMBAT %%%%%%%%%%%%%%%%

    ESCAPE_COMBAT_4 --> BLACK_SCREEN_VISIBLE_1{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#black-screen-visible" style='text-decoration:none;'>Black</br>Screen</br>Visible</a>
    "}
    BLACK_SCREEN_VISIBLE_1 -- "⠀✘⠀" --> ESCAPE_COMBAT_4
    BLACK_SCREEN_VISIBLE_1 -- "⠀✔⠀" --> ESCAPE_COMBAT_5("
        <b>ESCAPE_COMBAT_5</b>
        <span style='font-size:14px; color:#C00;'>Overworld Black Loadscreen</span>
    ")


    ESCAPE_COMBAT_5 --> BLACK_SCREEN_VISIBLE_2{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#black-screen-visible" style='text-decoration:none;'>Black</br>Screen</br>Visible</a>
    "}
    BLACK_SCREEN_VISIBLE_2 -- "⠀✔⠀" --> ESCAPE_COMBAT_5
    BLACK_SCREEN_VISIBLE_2 -- "⠀✘⠀" --> MOVE_PLAYER


    %%%%%%%%%%%%%%%% Styles %%%%%%%%%%%%%%%%

    classDef Start fill:#ccc;
    class START,END Start;

    classDef Check_Functions font-size:13px;
    class CHECK_PAIRING_COLOR,CHECK_HOME_COLOR,WHITE_SCREEN_VISIBLE_1,WHITE_SCREEN_VISIBLE_2,TEXT_BOX_VISIBLE_1,TEXT_BOX_VISIBLE_2,TEXT_BOX_VISIBLE_3,SHINY_TIMER,SHINY_RECORDING_TIME,LIFE_BOX_VISIBLE_1,TEXT_BOX_VISIBLE_4,TEXT_BOX_VISIBLE_5,LIFE_BOX_VISIBLE_2,BLACK_SCREEN_VISIBLE_1,BLACK_SCREEN_VISIBLE_2,LIFE_BOX_VISIBLE_3,TEXT_BOX_VISIBLE_6 Check_Functions;
```

<!-- #################### RESTART GAME STATE DIAGRAM #################### -->
⠀
> [!NOTE]
> If at any point during the execution of the previous state machine it: <ul><p><li>Gets stuck in any state (excluding ENTER_LAKE_4, MOVE_PLAYER, SHINY_FOUND, WAIT_HOME_SCREEN and WAIT_PAIRING_SCREEN states) for more than <code>CONST.STUCK_TIMER_SECONDS</code>.</li></p><p><li>Stays more than <code>CONST.FAILURE_DETECTION_TIME_WARN</code> seconds without encountering any pokémon (if not in any of the ENTER_LAKE_4, RESTART_GAME_1, SHINY_FOUND, WAIT_HOME_SCREEN and WAIT_PAIRING_SCREEN states). This happens when the program got stuck in a loop where states are changing, but no Pokémon is found; such as repeatedly trying to escape from combat without success.</li></p></ul> 
> It will restart the game by executing the following state machine:

⠀
```mermaid
graph TD
    %%%%%%%%%%%%%%%% START STATE %%%%%%%%%%%%%%%%

    START((·)) --> RESTART_GAME_1("
        <b>RESTART_GAME_1</b>
        <span style='font-size:13px; color:#C0C;'><i>restart_game_macro</i></span>
    ")
    RESTART_GAME_1 --> BDSP_BLACK_LOAD_SCREEN_1{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#bdsp-load-screen-visible" style='text-decoration:none;'>BDSP</br>Load<br>Screen</br>Visible</a>
    "}
    BDSP_BLACK_LOAD_SCREEN_1 -- "⠀✘⠀" --> RESTART_GAME_1
    BDSP_BLACK_LOAD_SCREEN_1 -- "⠀✔⠀" --> RESTART_GAME_2("
        <b>RESTART_GAME_2</b>
        <span style='font-size:14px; color:#C00;'>BDSP Black Loadscreen</span>
        <span style='font-size:13px; color:#C0C;'><i>press_A_macro</i></span>
    ")


    RESTART_GAME_2 --> BDSP_BLACK_LOAD_SCREEN_2{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#bdsp-load-screen-visible" style='text-decoration:none;'>BDSP</br>Load<br>Screen</br>Visible</a>
    "}
    BDSP_BLACK_LOAD_SCREEN_2 -- "⠀✔⠀" --> RESTART_GAME_2
    BDSP_BLACK_LOAD_SCREEN_2 -- "⠀✘⠀" --> RESTART_GAME_3("
        <b>RESTART_GAME_3</b>
        <span style='font-size:14px; color:#C00;'>Dialga/Palkia Animation</span>
        <span style='font-size:13px; color:#C0C;'><i>press_A_macro</i></span>
    ")


    RESTART_GAME_3 --> BDSP_BLACK_LOAD_SCREEN_3{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#bdsp-load-screen-visible" style='text-decoration:none;'>BDSP</br>Load<br>Screen</br>Visible</a>
    "}
    BDSP_BLACK_LOAD_SCREEN_3 -- "⠀✘⠀" --> RESTART_GAME_3
    BDSP_BLACK_LOAD_SCREEN_3 -- "⠀✔⠀" --> RESTART_GAME_4("
        <b>RESTART_GAME_4</b>
        <span style='font-size:14px; color:#C00;'>BDSP Black Loadscreen</span>
    ")


    RESTART_GAME_4 --> BDSP_BLACK_LOAD_SCREEN_4{"
        <a href="https://github.com/Dinones/Nintendo-Switch-Pokemon-Shiny-Hunter/blob/develop/Media/Docs/State%20Machines/Wild%20State%20Machine.md#bdsp-load-screen-visible" style='text-decoration:none;'>BDSP</br>Load<br>Screen</br>Visible</a>
    "}
    BDSP_BLACK_LOAD_SCREEN_4 -- "⠀✔⠀" --> RESTART_GAME_4
    BDSP_BLACK_LOAD_SCREEN_4 -- "⠀✘⠀" --> MOVE_PLAYER("
        <b>MOVE_PLAYER</b>
        <span style='font-size:14px; color:#C00;'>Overworld</span>
        <span style='font-size:13px; color:#C0C;'><i>move_player_wild_macro</i></span>
    ")


    MOVE_PLAYER --> END((·))


    %%%%%%%%%%%%%%%% Styles %%%%%%%%%%%%%%%%

    classDef Start fill:#ccc;
    class START,END Start;

    classDef Check_Functions font-size:13px;
    class BDSP_BLACK_LOAD_SCREEN_1,BDSP_BLACK_LOAD_SCREEN_2,BDSP_BLACK_LOAD_SCREEN_3,BDSP_BLACK_LOAD_SCREEN_4 Check_Functions;
```