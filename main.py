import pygame
from map import GameMap  # Import the map handling class
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

# Main game loop
running = True
while running:
    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user closes the game window
            running = False  # Exit the game loop

    # Handle user input for camera movement using arrow keys
    keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
    if keys[pygame.K_LEFT]:  # Move camera left
        camera.move(-10, 0)
    if keys[pygame.K_RIGHT]:  # Move camera right
        camera.move(10, 0)
    if keys[pygame.K_UP]:  # Move camera up
        camera.move(0, -10)
    if keys[pygame.K_DOWN]:  # Move camera down
        camera.move(0, 10)

    # Render the game map and update the screen
    screen.fill(BLACK)  # Clear the screen by filling it with black
    game_map.draw(screen, camera)  # Draw the map with the camera's view
    pygame.display.flip()  # Update the display with the new frame

    # Limit the game loop to 60 frames per second
    clock.tick(60)

# Quit pygame after exiting the loop
pygame.quit()
