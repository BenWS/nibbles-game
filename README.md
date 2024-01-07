# About

This is a repository for the recreation of the "Nibbles" game, outlined on [this page](https://inventwithpython.com/blog/2012/02/20/i-need-practice-programming-49-ideas-for-game-clones-to-code/). More information below.

More available in the [architectural details](#architectural-details) section of this page.

# Installation and Usage

__Installation__

1. This program was developed using [Python 3.8](https://www.python.org/downloads/release/python-386/). For this reason it is recommended the user has installed at least that version of python in order for the program to run, but this may work fine on earlier versions of Python
2. Run a `git clone ...` command to copy the contents of repository to your local repository
3. You may then create a python virtual environmemnt in the root directory of their cloned repository via `python -m venv venv`
4. Once the virtual environment is activated, please run a `pip install -r requirements.txt` for the [`requirements.txt`](requirements.txt) file

__Starting the Game__

The game may be run via executing `python 'program/main.py'` at the root location of the cloned repository.

# Design

![Design Diagram](assets/program_design.jpg)

## Details

__`user_interface` Module__

The `user_interface` module is responsible for managing the screens each user sees and for loading and unloading graphics elements for each screen. The UI also sets event listeners and overall rules for human interface with the game.

__`graphics` Module__

The `graphics` module is responsible for constructing and managing movement of individual game entities. The UI sets the event listener but the graphics package determines what the game elements do upon an event.

__`gamerules` Module__

The `gamerules` module determines how the game is scored and is also used to determine whether the game is in a won/lost state. This package should not communicate directly with the main game loop but rather communicate via the `graphics` engine.

__`data_storage` Module__

The `data_storage` is the interface for how the program communicates with the database.

__`logging` Module__

The `logging` module provides utilities for logging application activity to enable more robust and effective debugging.

__`layout` Module__

The `layout` module provides an HTML div-like interface to managing screen elements via container objects