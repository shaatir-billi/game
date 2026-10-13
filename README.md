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
- `screens/howtoplay_screen.py`: Contains the logic for the "How to Play" screen.
- `screens/game_finish_screen.py`: Contains the logic for the game finish screen.
- `utils/spritesheet.py`: Contains the logic for handling sprite sheets.
- `utils/button.py`: Contains the logic for handling buttons.
- `utils/font.py`: Contains the logic for handling fonts.
- `utils/globals.py`: Contains global variables and constants.
- `utils/health_display.py`: Contains the logic for displaying and updating the player's health.
- `camera.py`: Contains the logic for handling the camera.
- `sprite.py`: Contains the logic for the player sprite.
- `guard.py`: Contains the logic for the guard sprite.
- `hiding_spot.py`: Contains the logic for the hiding spots.
- `logic/game_logic.py`: Contains the game logic for handling collisions, hiding, and item pickups.
- `logic/draw_logic.py`: Contains the logic for drawing game elements on the screen.
- `logic/shopkeeper_logic.py`: Contains the logic for handling shopkeeper movements and interactions.
- `logic/shopkeeper_marl_env.py`: Contains the multi-agent reinforcement learning environment for the shopkeeper.
- `logic/marl_env.py`: Contains the multi-agent reinforcement learning environment for the cat chase scenario.
- `train_shopkeeper_marl.py`: Script for training the shopkeeper using multi-agent reinforcement learning.
- `train_marl.py`: Script for training the cat chase scenario using multi-agent reinforcement learning.
- `map.py`: Contains the logic for the game map and platforms.

#### Directory Structure

```
shaatir-billi/
├── assets/
│   ├── map/
│   ├── sprites/
│   └── ...
│   ├── screens/
│   │   ├── play_screen.py
│   │   ├── options_screen.py
│   │   ├── main_menu.py
│   │   ├── game_over_screen.py
│   │   ├── howtoplay_screen.py
│   │   └── game_finish_screen.py
│   ├── utils/
│   │   ├── spritesheet.py
│   │   ├── button.py
│   │   ├── font.py
│   │   ├── globals.py
│   │   └── health_display.py
│   ├── logic/
│   │   ├── game_logic.py
│   │   ├── draw_logic.py
│   │   ├── shopkeeper_logic.py
│   │   ├── shopkeeper_marl_env.py
│   │   └── marl_env.py
│   ├── camera.py
│   ├── sprite.py
│   ├── guard.py
│   ├── hiding_spot.py
│   ├── train_shopkeeper_marl.py
│   ├── train_marl.py
│   ├── map.py
│   └── main.py
├── requirements.txt
└── README.md
```

#### Logic Files Documentation

##### `logic/game_logic.py`

Contains the game logic for handling collisions, hiding, and item pickups.

- `handle_guard_collision(player, Guards, update_health_display)`: Handles collisions between the player and guards.
- `handle_hiding(player, hiding_spot_objects, keys, last_hiding_time, hiding_cooldown, hiding_buffer, current_hiding_spot)`: Manages the hiding mechanics for the player.
- `handle_shopkeeper_collision(player, shopkeeper, fish_picked_up, original_shopkeeper_position, original_fish_position)`: Handles collisions between the player and the shopkeeper.
- `handle_fish_pickup(player, fish, fish_picked_up, fish_position, last_fish_action_time, fish_cooldown)`: Manages the logic for picking up and dropping fish.

##### `logic/draw_logic.py`

Contains the logic for drawing game elements on the screen.

- `draw_game_elements(SCREEN, camera, game_map, platforms, Guards, shopkeeper, hiding_spot_objects, fish, fish_picked_up, fish_position, player, message_surface, barrel_image, barrel_rect, health_display, current_hiding_spot, Walls, player_health)`: Draws all game elements on the screen.

##### `logic/shopkeeper_logic.py`

Contains the logic for handling shopkeeper movements and interactions.

- `handle_shopkeeper_movement(shopkeeper, player, shopkeeper_chasing, map_width, keys, graph, current_hiding_spot, shopkeeper_speed)`: Manages the movement of the shopkeeper.
- `handle_shopkeeper_chase(shopkeeper, player, fish_picked_up, shopkeeper_chasing)`: Handles the logic for the shopkeeper chasing the player.

##### `logic/shopkeeper_marl_env.py`

Contains the multi-agent reinforcement learning environment for the shopkeeper.

- `ShopkeeperEnv`: Custom environment class for the shopkeeper using Gym.

##### `logic/marl_env.py`

Contains the multi-agent reinforcement learning environment for the cat chase scenario.

- `CatChaseEnv`: Custom environment class for the cat chase scenario using Gym.

#### Screens Files Documentation

##### `screens/play_screen.py`

Contains the main game logic and configuration for platforms, hiding spots, and guards.

- `play(SCREEN)`: Main function to run the game.

##### `screens/options_screen.py`

Contains the options menu logic.

- `options(SCREEN)`: Function to display the options menu.

##### `screens/main_menu.py`

Contains the main menu logic.

- `main_menu(SCREEN)`: Function to display the main menu.

##### `screens/game_over_screen.py`

Contains the game over screen logic.

- `game_over(SCREEN, play_function)`: Function to display the game over screen.

##### `screens/howtoplay_screen.py`

Contains the logic for the "How to Play" screen.

- `how_to_play(SCREEN)`: Function to display the "How to Play" screen.

##### `screens/game_finish_screen.py`

Contains the logic for the game finish screen.

- `game_finish(SCREEN)`: Function to display the game finish screen.

#### Utils Files Documentation

##### `utils/spritesheet.py`

Contains the logic for handling sprite sheets.

- `image_at(rectangle, colorkey=None)`: Loads an image from a specific rectangle.
- `images_at(rects, colorkey=None)`: Loads multiple images from a list of rectangles.
- `load_strip(rect, image_count, colorkey=None)`: Loads a strip of images and returns them as a list.

##### `utils/button.py`

Contains the logic for handling buttons.

- `update(screen)`: Updates the button's appearance on the screen.
- `checkForInput(position)`: Checks if the button is clicked.
- `changeColor(position)`: Changes the button's color when hovered.

##### `utils/font.py`

Contains the logic for handling fonts.

- `get_font(size)`: Returns a font object of the specified size.
- `draw_text_with_border(screen, text, font, text_color, border_color, pos, border_width=2)`: Draws text with a border.

##### `utils/globals.py`

Contains global variables and constants.

- `SCREEN_WIDTH`: The width of the game screen.
- `SCREEN_HEIGHT`: The height of the game screen.
- `map_width`: The width of the game map.
- `sky_image_path`: The path to the background image.
- `ENABLE_GRAPH_VISUALIZATION`: Option to enable or disable graph visualization.

##### `utils/health_display.py`

Contains the logic for displaying and updating the player's health.

- `create_health_display(health)`: Creates the health display based on the player's health.
- `update_health_display(health_display, health)`: Updates the health display based on the player's health.

#### Root Directory Files Documentation

##### `train_shopkeeper_marl.py`

Script for training the shopkeeper using multi-agent reinforcement learning.

- `env = ShopkeeperEnv()`: Creates the environment for the shopkeeper.
- `model = PPO("MlpPolicy", env, verbose=1)`: Initializes the PPO model.
- `model.learn(total_timesteps=10000)`: Trains the model.
- `obs = env.reset()`: Resets the environment for testing.
- `for _ in range(100)`: Tests the trained model.

##### `train_marl.py`

Script for training the cat chase scenario using multi-agent reinforcement learning.

- `env = CatChaseEnv(cat_position, shopkeeper_position, guard_positions, guard_platforms)`: Creates the environment for the cat chase scenario.
- `model = PPO("MlpPolicy", env, verbose=1)`: Initializes the PPO model.
- `model.learn(total_timesteps=100000)`: Trains the model.
- `model.save("marl_model")`: Saves the trained model.
- `model = PPO.load("marl_model")`: Loads the trained model for inference.
- `for _ in range(1000)`: Tests the trained model.

##### `map.py`

Contains the logic for the game map and platforms.

- `GameMap`: Class for handling the game map.
- `Platform`: Class for handling platforms.
- `Graph`: Class for handling the graph used for pathfinding.

##### `main.py`

The main entry point of the game.

- `main_menu(SCREEN)`: Runs the main menu.

##### `sprite.py`

Contains the logic for the player sprite.

- `Sprite`: Class for handling the player sprite.

##### `shopkeeper.py`

Contains the logic for the shopkeeper sprite.

- `Shopkeeper`: Class for handling the shopkeeper sprite.

##### `hiding_spot.py`

Contains the logic for the hiding spots.

- `HidingSpot`: Class for handling the hiding spots.

##### `guard.py`

Contains the logic for the guard sprite.

- `Guard`: Class for handling the guard sprite.

##### `fish.py`

Contains the logic for the fish sprite.

- `Fish`: Class for handling the fish sprite.

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
