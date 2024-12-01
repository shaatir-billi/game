import pygame
from map import GameMap  # Import the map handling class
from sprite import Sprite  # Import the sprite class
from camera import Camera  # Import the camera for scrolling

# Define basic colors for the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)  # Grass color
BROWN = (165, 42, 42)  # Dirt color

# Initialize pygame
pygame.init()

# Set the screen/window size
screen_size = (800, 600)  # Width x Height in pixels
screen = pygame.display.set_mode(screen_size)  # Create the game window
pygame.display.set_caption("RTS Game")  # Set the window title

# Clock to control frames per second (FPS)
clock = pygame.time.Clock()

# Tile size and map dimensions (number of tiles in width and height)
tile_size = 50  # Each tile is 50x50 pixels
map_width, map_height = 20, 15  # 20 tiles wide, 15 tiles high

# Initialize the game map
game_map = GameMap(map_width, map_height, tile_size, GREEN, BROWN)

# Initialize the camera, which will allow movement around the map
camera = Camera(screen_size, map_width, map_height, tile_size)

# Initialize the sprite
player = Sprite("assets/sprites/player/attack_2.png", 100, 100)  # Change to your sprite's path

# Main game loop
running = True
while running:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input for sprite movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move(-5, 0)
    if keys[pygame.K_d]:
        player.move(5, 0)
    if keys[pygame.K_w]:
        player.move(0, -5)
    if keys[pygame.K_s]:
        player.move(0, 5)

    # Update camera to follow the sprite
    camera.follow_sprite(player)

    # Render the game map and sprite
    screen.fill(BLACK)
    game_map.draw(screen, camera)
    player.draw(screen, camera)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
