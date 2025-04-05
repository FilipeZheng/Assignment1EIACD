# Jungle Chess (Dou Shou Qi)

## Description

Jungle Chess, also known as Dou Shou Qi or Animal Chess, is a traditional Chinese board game. This implementation features a modern interface with AI opponents.

## Table of Contents
- [Description](#description)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## How to Play

1. Run `run_game.py` to start the game
2. Click the "START GAME" button on the main menu
3. The game alternates between players, with Player 1 at the bottom and Player 2 at the top

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

### Special Rules:
- Mouse can swim in water and capture while in water
- Lion and Tiger can jump across water horizontally or vertically
- Stronger animals capture weaker ones
- Mouse can defeat Elephant (special case)
- Only Mouse can enter water tiles
- Traps weaken enemy pieces to 0 strength
- Win by entering the opponent's den

## Features

- Modern graphical interface
- AI opponents with different strategies
- Move validation and game state tracking
- Interactive piece selection and movement
- Game replay functionality

## Requirements

- Python 3.x
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
python run_game.py
```

## Screenshots

[Screenshots will be added soon]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

This implementation was created as part of Assignment 1 for EIACD.