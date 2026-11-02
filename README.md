# Intergalactic Battle

A 2D space shooter game made with Python and pygame. Shoot and defeat all the enemies, then take on the final boss on level 4! Good luck!

## Requirements

- **Python 3.10 or newer** ([download](https://www.python.org/downloads/))
- **pygame-ce** (installed in the steps below)

## Installation

1. Download the project, either with git:

   ```
   git clone https://github.com/lmahendran/intergalactic_battle.git
   cd intergalactic_battle
   ```

   or by clicking **Code > Download ZIP** on GitHub and unzipping it.

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

> **Note:** This game uses [pygame-ce](https://pyga.me/) (pygame Community Edition), not the original `pygame` package. The two can't be installed together because both are imported as `pygame`. If you already have `pygame` installed, remove it first with `pip uninstall pygame`.

## Running the game

From the project folder, run:

```
python main.py
```

On macOS and Linux, you may need to use `python3` (and `pip3` above) instead.

The game opens in an 800x600 window. Click the play button on the start screen to begin.

## Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`**: the dependencies aren't installed for the Python you're running. Run `python -m pip install -r requirements.txt`, using the same `python` command you use to start the game.
- **`'python' is not recognized` (Windows)**: try `py main.py` instead, or reinstall Python with **Add python.exe to PATH** ticked.
- **The game runs too fast or too slow**: change `FPS` near the top of `main.py`. A higher value speeds the whole game up and a lower value slows it down.

## Credits

Made by Logesh Mahendran as a summative assignment for ICD2O (January 2024), building on the class "Space Battle" game.

### Music

All tracks are licensed under [Creative Commons: By Attribution 4.0](http://creativecommons.org/licenses/by/4.0/).

## Tracks

- "Mesmerizing Galaxy" by Kevin MacLeod ([incompetech.com](https://incompetech.com))
- "Cloud Dancer" by Kevin MacLeod ([incompetech.com](https://incompetech.com))
- "Brain Dance" by Kevin MacLeod ([incompetech.com](https://incompetech.com))
- "Blippy Trance" by Kevin MacLeod ([incompetech.com](https://incompetech.com))
- "Swift Strike" by PeriTune ([peritune.com](https://peritune.com/blog/2025/02/16/swift_strike/))
