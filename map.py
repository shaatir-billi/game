import pygame
import math
import heapq
from utils.globals import SCREEN_WIDTH, SCREEN_HEIGHT, map_width


class GameMap:
    def __init__(self, sky_image_path, upper_layer_image_path):
        """
        Initialize the game map.
        :param sky_image_path: Path to the background image
        :param upper_layer_image_path: Path to the upper layer image
        :param building_image_path: Path to the building/ground image
        """
        # Load and scale the background image
        self.sky_image = pygame.image.load(sky_image_path).convert()
        self.sky_image = pygame.transform.scale(
            self.sky_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.sky_width = self.sky_image.get_width()

        # Load and scale the upper layer image
        self.upper_layer_image = pygame.image.load(
            upper_layer_image_path).convert_alpha()
        self.upper_layer_image = pygame.transform.scale(
            self.upper_layer_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.upper_layer_width = self.upper_layer_image.get_width()

        self.ground_tile_height = 50  # Height of the ground tile
        self.ground_level = SCREEN_HEIGHT - self.ground_tile_height  # Ground level

    def draw(self, screen, camera):
        """
        Draw the map's repeating background, upper layer, and ground.
        :param screen: The game window surface to draw on
        :param camera: The camera for horizontal scrolling
        """
        tiles_sky = math.ceil(map_width / self.sky_width)
        tiles_upper = math.ceil(map_width / self.upper_layer_width)

        # Draw the background considering camera's offset
        for x in range(0, tiles_sky):
            screen.blit(self.sky_image,
                        ((x * self.sky_width) - camera.x_offset, 0))

        # Draw the upper layer considering camera's offset
        for x in range(0, tiles_upper):
            screen.blit(self.upper_layer_image,
                        ((x * self.upper_layer_width) - camera.x_offset, 0))


class Platform:
    def __init__(self, image_path, x, y, width, height):
        """
        Initialize the platform.
        :param image_path: Path to the platform image
        :param x: x-coordinate of the platform
        :param y: y-coordinate of the platform
        :param width: Width of the platform
        :param height: Height of the platform
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen, camera):
        """
        Draw the platform on the screen with camera adjustment.
        :param screen: The game window
        :param camera: Camera object
        """
        screen.blit(self.image, (self.rect.x - camera.x_offset, self.rect.y))


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = {}

    def add_node(self, x, y):
        self.nodes.append((x, y))
        self.edges[(x, y)] = []

    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)

    def heuristic(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def a_star_search(self, start, goal):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {node: float('inf') for node in self.nodes}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.nodes}
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for neighbor in self.edges[current]:
                tentative_g_score = g_score[current] + \
                    self.heuristic(current, neighbor)
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + \
                        self.heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def draw(self, screen, camera):
        font = pygame.font.Font(None, 24)  # Font for the coordinates
        for node in self.nodes:
            adjusted_node = (node[0], node[1] + 100)  # Shift node back by +100
            pygame.draw.circle(screen, (0, 255, 0),
                               (adjusted_node[0] - camera.x_offset, adjusted_node[1]), 5)
            text_surface = font.render(
                f"{adjusted_node}", True, (0, 0, 0))  # Black color
            screen.blit(
                text_surface, (adjusted_node[0] - camera.x_offset, adjusted_node[1] - 20))
        for from_node, to_nodes in self.edges.items():
            for to_node in to_nodes:
                adjusted_from_node = (from_node[0], from_node[1] + 100)
                adjusted_to_node = (to_node[0], to_node[1] + 100)
                color = (255, 0, 0) if adjusted_to_node[1] < adjusted_from_node[1] else (
                    0, 0, 255)  # Red for upward, Blue for downward
                pygame.draw.line(screen, color, (
                    adjusted_from_node[0] - camera.x_offset, adjusted_from_node[1]), (adjusted_to_node[0] - camera.x_offset, adjusted_to_node[1]), 2)
