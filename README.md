# JesterSight
 A Spelunky 2 True Crown timer that does not require reading the game's memory.

Jestersight analyzes the UI to extract:
 - If the player has the True Crown
 - The current level time in seconds
 - The current level

and uses this information to warn the player about upcoming teleports.  As the program only analyzes the UI, it does not need to read information from the game's memory.  Currently, JesterSight is lacking a proper UI for an end user.  The most significant drawback to this is that alerts are sent as console output instead of via sound.  As such it is likely not currently useful as a practice or run aid. With future work this will hopefully change.

Please note that JesterSight relies on [Tesseract](https://github.com/tesseract-ocr/tesseract), an OCR library to parse the in game-time and level.  Specifically, JesterSight has been tested and built with version `5.0.0-rc1.20211030` The program can be configured to expect Tesseract to be installed in a given folder instead of globally in `parse_text.py`.  