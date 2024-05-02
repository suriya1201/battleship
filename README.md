# Battleship (Group 1)

## What is Battleship?
Battleship is a two-player guessing game where players try to sink each other's ships on the field (grid).

## Why we chose Battleship
We chose Battleship as it is a classic game that is simple to pick up, it can be played against someone else or the computer.

## Features
- Single-player against AI or Multiplayer (1 vs 1)
- Customizable grid size and number of ships.
- Game is visually represented with ASCII characters.
- Clear indication of hits, misses, and sunk ships.
- Simple user interface with instructions provided.

## Installation
1. Clone the repository: `git clone https://github.com/your_username/battleship.git` OR download the zip file.
2. Navigate to the project directory: `cd battleship`
3. Ensure you have Python 3 installed (Tested on 3.11, does not work for 3.12).
4. Run the game: `python battleship.py` in command prompt (Ensure cmd is in full screen).

## How to Play
1. Launch the game by running `battleship.py`
2. Users will be prompted with grid size, number of ships, how and where they wish to play their ships.
3. Once the game starts, users will take turns guessing the coordinates of their opponent's ships.
4. If you hit an opponent's ship, the cell (-) will be marked with an "H". If you miss, it will be marked with an "M".
5. On your side, if your ship has been hit, it will be marked with a "0".
6. The player who sinks all of their opponent's ships first wins the game.

## Issues
Below are some issues which we have faced throughout the duration of coding the game, but were however unable to troubleshoot them on time.
1. Singleplayer:
   - For number of rows = 5, an error will be returned. However, for number of rows = 10, it will work.
   - Computer will keep attacking if number of rows = 5.
   - It has to be played in fullscreen, else the game will not work as intended.
2. Multiplayer:
   - If the screen is too small, the game will end abruptly once ships have been placed.
   - Ships placed can exceed beyond the grid, though error handling has been put in place.
