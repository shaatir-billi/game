# shaatir-billi

Pygame based game created to utilize AI concepts. Concept based on Pink Panther: Pinkadelic Pursuit.

### Environment setup

```bash
# Use git bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

### Run the game

```python
python main.py
```

### Technical Documentation

#### Configuration Variables

##### Platform Configuration

To create a platform, you need to configure the following variables in the `play_screen.py` file:

- `x`: The x-coordinate of the platform.
- `y`: The y-coordinate of the platform.
- `width`: The width of the platform.
- `height`: The height of the platform.

Example:

```python
Platform("assets/map/platform.png", 2000, ground - 30, 100, 50)
```

##### Jumping Configuration

To configure the jumping mechanics, you need to adjust the following variables in the `sprite.py` file:

- `jump_velocity`: The initial velocity when the player jumps.
- `gravity`: The gravity applied to the player.
- `max_fall_speed`: The maximum speed at which the player can fall.

Example:

```python
self.jump_velocity = -20  # Improved jump velocity for smoother arc
self.gravity = 1.2  # Adjusted gravity for better jump
self.max_fall_speed = 15  # Limit falling speed
```

##### Hiding Spot Configuration

To create a hiding spot, you need to configure the following variables in the `play_screen.py` file:

- `x`: The x-coordinate of the hiding spot.
- `y`: The y-coordinate of the hiding spot.
- `width`: The width of the hiding spot.
- `height`: The height of the hiding spot.
- `scale`: The scale of the hiding spot.

Example:

```python
HidingSpot(platforms[index].rect.x + offset, platforms[index].rect.y - 50, 50, 50, scale)
```

##### Guard Configuration

To create a guard, you need to configure the following variables in the `guard.py` file:

- `sprite_sheet_path`: The path to the sprite sheet of the guard.
- `platform_rect`: The rectangle of the platform the guard is on.
- `frame_width`: The width of each frame in the sprite sheet.
- `frame_height`: The height of each frame in the sprite sheet.
- `scale`: The scale of the guard.

Example:

```python
Guard("assets/sprites/enemy/girl_walk.png", platforms[16].rect, 48, 48, 3)
```

#### File Paths

- `main.py`: The main entry point of the game.
- `screens/play_screen.py`: Contains the main game logic and configuration for platforms, hiding spots, and guards.
- `screens/options_screen.py`: Contains the options menu logic.
- `screens/main_menu.py`: Contains the main menu logic.
- `screens/game_over_screen.py`: Contains the game over screen logic.
- `utils/spritesheet.py`: Contains the logic for handling sprite sheets.
- `utils/button.py`: Contains the logic for handling buttons.
- `utils/font.py`: Contains the logic for handling fonts.
- `utils/globals.py`: Contains global variables and constants.
- `camera.py`: Contains the logic for handling the camera.
- `sprite.py`: Contains the logic for the player sprite.
- `guard.py`: Contains the logic for the guard sprite.
- `hiding_spot.py`: Contains the logic for the hiding spots.

#### Adding New Features

To add new features to the game, follow these steps:

1. Identify the file where the new feature should be added.
2. Define the necessary variables and configuration options.
3. Implement the logic for the new feature.
4. Test the new feature to ensure it works as expected.

Example: Adding a new type of enemy

1. Create a new file `enemy.py` in the `game` directory.
2. Define the necessary variables and configuration options for the new enemy.
3. Implement the logic for the new enemy in the `enemy.py` file.
4. Update the `play_screen.py` file to include the new enemy.
5. Test the new enemy to ensure it works as expected.

### Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them to your branch.
4. Create a pull request with a description of your changes.

### License

This project is licensed under the MIT License.
