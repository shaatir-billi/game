from map import *
from guard import Guard
from hiding_spot import HidingSpot
from shopkeeper import Shopkeeper


def create_game_map():
    game_map = GameMap("assets/map/sky.jpeg", "assets/map/ground.png")
    return game_map


def create_platforms(ground):
    return [
        # 2 tiles
        Platform("assets/map/platform.png", 2000, ground - 30, 100, 50),
        Platform("assets/map/platform.png", 2100, ground - 80, 100, 50),
        Platform("assets/map/platform.png", 2200, ground - 140, 100, 50),
        Platform("assets/map/platform.png", 1200, ground - 350, 100, 50),
        Platform("assets/map/platform.png", 1200, ground - 350, 100, 50),
        Platform("assets/map/platform.png", 3600, ground - 100, 100, 50),

        # 3 tiles
        Platform("assets/map/platform.png", 2300, ground - 250, 200, 50),
        Platform("assets/map/platform.png", 1600, ground - 630, 200, 50),
        Platform("assets/map/platform.png", 1900, ground - 630, 200, 50),
        Platform("assets/map/platform.png", 2700, ground - 550, 200, 50),
        Platform("assets/map/platform.png", 2580, ground - 100, 200, 50),

        # 4 tiles
        Platform("assets/map/platform.png", 1000, ground - 200, 250, 50),
        Platform("assets/map/platform.png", 2100, ground - 400, 250, 50),
        Platform("assets/map/platform.png", 3500, ground - 550, 250, 50),
        Platform("assets/map/platform.png", 2630, ground - 280, 250, 50),
        Platform("assets/map/platform.png", 3350, ground - 290, 250, 50),

        # Long platforms
        Platform("assets/map/platform.png", 1350, ground - 270, 800, 50),
        Platform("assets/map/platform.png", 700, ground - 400, 400, 50),
        Platform("assets/map/platform.png", 1000, ground - 550, 500, 50),
        Platform("assets/map/platform.png", 0, ground - 640, 900, 50),
        Platform("assets/map/platform.png", 2230, ground - 700, 1200, 50),
        Platform("assets/map/platform.png", 2900, ground - 200, 600, 50),
        Platform("assets/map/platform.png", 3000, ground - 460, 400, 50),
    ]


def create_walls():
    return [
        Platform("assets/map/platform.png", 2500, 300, 50, 550),
    ]


def create_guards(platforms):
    return [
        Guard("assets/sprites/guard/girl_walk.png",
              platforms[16].rect, 48, 48, 3),
        Guard("assets/sprites/guard/girl_walk.png",
              platforms[15].rect, 48, 48, 3)
    ]


def create_hiding_spots(platforms):
    hiding_spots = [
        (16, 80, 1),  # Platform index 16, 80 pixels from the left, scale 3
        (2, 30, 1),  # Platform index 2, 30 pixels from the left, scale 2
        (5, 50, 1),  # Platform index 5, 50 pixels from the left, scale 2.5
    ]
    return [
        HidingSpot(platforms[index].rect.x + offset,
                   platforms[index].rect.y - 50, 50, 50, scale)
        for index, offset, scale in hiding_spots
    ]


def create_graph(platforms, ground_level, walls, max_fall_distance=100, max_jump_height=185, jump_decay=0.5):
    graph = Graph()

    # Add ground nodes
    for x in range(0, map_width, 200):
        graph.add_node(x, ground_level)

    # Add platform nodes
    for platform in platforms:
        graph.add_node(platform.rect.left, platform.rect.top)
        graph.add_node(platform.rect.right, platform.rect.top)

    def is_horizontal_reachable(dx):
        """Check if the horizontal distance is within reachable range."""
        return abs(dx) <= 300

    def is_jump_reachable(dx, dy):
        """Check if the vertical distance is reachable based on jumping."""
        if dy < 0:  # Upward jump
            reduced_jump_height = max_jump_height - abs(dx) * jump_decay
            return abs(dy) <= max(reduced_jump_height, 0)
        elif dy > 0:  # Downward movement
            return dy <= max_fall_distance
        return True

    def does_edge_intersect_wall(from_node, to_node):
        """Check if the edge intersects any wall."""
        for wall in walls:
            if wall.rect.clipline(from_node, to_node):
                return True
        return False

    # Calculate edges based on jump capability
    for from_node in graph.nodes:
        for to_node in graph.nodes:
            if from_node == to_node:
                continue

            dx = to_node[0] - from_node[0]
            dy = to_node[1] - from_node[1]

            # Perform all checks
            if (is_horizontal_reachable(dx) and
                is_jump_reachable(dx, dy) and
                    not does_edge_intersect_wall(from_node, to_node)):
                graph.add_edge(from_node, to_node)

    return graph
