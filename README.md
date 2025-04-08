# Jungle Chess (Dou Shou Qi)

## Description

Jungle Chess, also known as Dou Shou Qi or Animal Chess, is a traditional Chinese board game. This implementation features a graphical interface with AI opponents of varying difficulties.

## Table of Contents
- [Description](#description)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Features](#features)
- [Player Types](#player-types)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)

## How to Play

1. Run `run_game.py` to start the game
2. Click the "START GAME" button on the main menu
3. Select Player 1 type (Human/AI)
4. Select Player 2 type (Human/AI)
5. The game alternates between players, with Player 1 at the bottom and Player 2 at the top

## Game Rules

### Pieces (from strongest to weakest):
1. Elephant (8)
2. Lion (7)
3. Tiger (6)
4. Leopard (5)
5. Wolf (4)
6. Dog (3)
7. Cat (2)
8. Mouse (1)
   
### Rules:
- All pieces can move one tile at a time horizontally or vertically but not diagonally
- Pieces can capture opposing pieces with lower or equal strength by moving on them
- A player wins by entering the opponent's lair
- A player who cannot make any move loses
  
### Special Rules:
- Mouse can capture Elephant (special case)
- Mouse can swim in water but cannot jump out of water and capture an Elephant at the same time
- Lion and Tiger can jump across water horizontally or vertically if there is no Mouse in the way
- Enemy pieces in a trap can be captured by any piece

## Features

- Graphical interface with start menu
- Multiple AI difficulty levels
- Player type selection for both players
- Move validation and game state tracking
- Interactive piece selection and movement
- Game replay functionality

## Player Types

### Available Players:
1. **Human**: Manual control with mouse input
2. **Easy AI**: Basic strategic decisions (depth=2)
3. **Medium AI**: Improved strategy (depth=3)
4. **Hard AI**: Advanced strategy (depth=4)
5. **Random AI**: Makes random legal moves

## Requirements

- Python 3.8 or higher
- Pygame library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/FilipeZheng/Assignment1EIACD.git
cd Assignment1EIACD
```

2. Install Pygame:
```bash
pip install pygame
```

## Usage

Run the game:
```bash
python3 run_game.py
```

## Credits

This implementation was created as part of Assignment 1 for EIACD.
