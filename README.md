# Super Mario Bros Web

A classic Super Mario Bros game implemented in HTML5 Canvas and JavaScript.

## Features

- Classic Super Mario gameplay mechanics
- Multiple enemies (Goombas, Koopas, Piranhas)
- Power-ups (Mushrooms, Stars, Flowers)
- Coin collection and scoring system
- Multiple levels

## Setup

1. Create a `sprites` directory in the project root
2. Add the following sprite images to the `sprites` directory:
   - mario_small.png: Small Mario sprite sheet
   - mario_big.png: Big Mario sprite sheet
   - enemies.png: Enemy sprite sheet
   - items.png: Items sprite sheet
   - tiles.png: Tiles and platforms sprite sheet

You can find these sprite sheets from various Super Mario sprite resources online.

## Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Space: Jump
- Down Arrow: Duck (when big)

## Game Features

### Characters
- Small Mario
- Big Mario
- Fire Mario (with Fire Flower)

### Enemies
- Goomba: Basic enemy that walks back and forth
- Koopa: Turtle enemy that can be kicked as a shell
- Piranha Plant: Appears from pipes

### Items
- Coins: Collect for points
- Super Mushroom: Makes Mario big
- Star: Temporary invincibility
- Fire Flower: Allows Mario to throw fireballs

### Scoring
- Coin: 200 points
- Goomba defeat: 100 points
- Koopa defeat: 100 points
- Power-up: 1000 points

## Development

The game is built using vanilla JavaScript and HTML5 Canvas. The codebase is organized into several modules:

- `game.js`: Main game loop and initialization
- `player.js`: Player character logic
- `enemies.js`: Enemy behaviors
- `items.js`: Power-ups and collectibles
- `levels.js`: Level layouts and configuration
- `sprites.js`: Sprite management and animation
