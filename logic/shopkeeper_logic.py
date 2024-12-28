import pygame
import math


def handle_shopkeeper_movement(shopkeeper, player, shopkeeper_chasing, map_width, keys, graph):
    if not hasattr(shopkeeper, "current_path"):
        shopkeeper.current_path = []  # Initialize the path if not already present

    if shopkeeper_chasing:
        nodes = graph.nodes

        def weighted_manhattan_distance(node1, node2):
            dx = abs(node1[0] - node2[0])
            dy = abs(node1[1] - node2[1])
            # Apply weight if the node is higher
            weight = 2 if node2[1] < node1[1] else 1
            return dx + weight * dy

        shopkeeper_center = (shopkeeper.rect.centerx, shopkeeper.rect.centery)
        player_center = (player.rect.centerx, player.rect.centery)

        # Recalculate path only if current path is empty or target has moved
        if not shopkeeper.current_path or \
           weighted_manhattan_distance(shopkeeper.current_path[-1], player_center) > 50:
            closest_node = min(
                nodes, key=lambda node: weighted_manhattan_distance(node, shopkeeper_center))
            closest_node_to_player = min(
                nodes, key=lambda node: weighted_manhattan_distance(node, player_center))

            print("Closest node to shopkeeper:", closest_node)
            shopkeeper.current_path = graph.a_star_search(
                closest_node, closest_node_to_player)
            print("Path:", shopkeeper.current_path)

        if shopkeeper.current_path and len(shopkeeper.current_path) > 1:
            next_node = shopkeeper.current_path[1]
            print("Shopkeeper moving to node:", next_node)

            # Define a tolerance value
            TOLERANCE = 2

            # Calculate the differences
            dx = next_node[0] - shopkeeper.rect.centerx
            dy = next_node[1] - shopkeeper.rect.centery

            # Check if the shopkeeper is within the tolerance range of the next node
            if abs(dx) <= TOLERANCE and abs(dy) <= TOLERANCE:
                print("Reached node:", next_node)
                shopkeeper.current_path.pop(0)  # Move to the next node
            else:
                # Move horizontally or vertically toward the next node
                if abs(dx) > TOLERANCE:  # Horizontal movement
                    if dx > 0:  # Move right
                        shopkeeper.move(1, 0)
                    else:  # Move left
                        shopkeeper.move(-1, 0)
                elif abs(dy) > TOLERANCE:  # Vertical movement
                    if dy > 0:  # Move down
                        shopkeeper.move(0, 2)
                    else:  # Move up
                        shopkeeper.move(0, -2)
    else:
        if shopkeeper.rect.right >= 2600 and shopkeeper.rect.right < 3000 and shopkeeper.moving_right:
            shopkeeper.move(2, 0)

    if shopkeeper.rect.left < 0:
        shopkeeper.rect.left = 0
    elif shopkeeper.rect.right > map_width:
        shopkeeper.rect.right = map_width


def handle_shopkeeper_chase(shopkeeper, player, fish_picked_up, shopkeeper_chasing):
    if not fish_picked_up:
        shopkeeper_chasing = False
    return shopkeeper_chasing
