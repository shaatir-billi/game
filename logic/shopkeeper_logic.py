import pygame
import math


def handle_shopkeeper_movement(shopkeeper, player, shopkeeper_chasing, map_width, keys, graph, current_hiding_spot):
    if not hasattr(shopkeeper, "current_path"):
        shopkeeper.current_path = []  # Initialize the path if not already present
    if not hasattr(shopkeeper, "last_path_update"):
        shopkeeper.last_path_update = pygame.time.get_ticks()  # Initialize the timer

    if shopkeeper_chasing:
        nodes = graph.nodes

        def manhattan_distance(node1, node2):
            return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

        # Get the current time
        current_time = pygame.time.get_ticks()

        shopkeeper_center = (shopkeeper.rect.centerx, shopkeeper.rect.centery)
        player_center = (player.rect.centerx, player.rect.centery)

        if current_hiding_spot:
            # Move to the nearest node and stop
            closest_node_to_hiding_spot = min(
                nodes, key=lambda node: manhattan_distance(node, shopkeeper_center))
            shopkeeper.current_path = [
                shopkeeper_center, closest_node_to_hiding_spot]
            shopkeeper_chasing = False  # Stop chasing when player is hidden
        else:
            closest_node = min(
                nodes, key=lambda node: manhattan_distance(node, shopkeeper_center))
            closest_node_to_player = min(
                nodes, key=lambda node: manhattan_distance(node, player_center))

            # if closest node has (50) in the y axis, then update the path after 10 seconds, else update the path after 1 seconds
            path_update_time = 10000 if closest_node[1] == 50 else 5000

            # Recalculate path only if current path is empty or target has moved
            if not shopkeeper.current_path or \
               current_time - shopkeeper.last_path_update > path_update_time:
                shopkeeper.last_path_update = current_time  # Update the timer

                shopkeeper.current_path = graph.a_star_search(
                    closest_node, closest_node_to_player)
                print("Path:", shopkeeper.current_path)

        if shopkeeper.current_path and len(shopkeeper.current_path) > 1:
            next_node = shopkeeper.current_path[1]
            print("Shopkeeper moving to node:", next_node)

            # Define a tolerance value
            TOLERANCE = 5

            # Calculate the differences
            dx = next_node[0] - shopkeeper.rect.centerx
            dy = next_node[1] - shopkeeper.rect.centery

            # Check if the shopkeeper is within the tolerance range of the next node
            if abs(dx) <= TOLERANCE and abs(dy) <= TOLERANCE:
                print("Reached node:", next_node)
                shopkeeper.current_path.pop(0)  # Move to the next node
            else:
                print("abs(dx):", abs(dx), "abs(dy):", abs(dy))
                # Move horizontally or vertically toward the next node
                if abs(dx) > TOLERANCE:  # Horizontal movement
                    if dx > 0:  # Move right
                        print("Moving right")
                        shopkeeper.move(2, 0)
                    else:  # Move left
                        print("Moving left")
                        shopkeeper.move(-2, 0)
                elif abs(dy) > TOLERANCE:  # Vertical movement
                    if dy > 0:  # Move down
                        print("Moving down")
                        shopkeeper.move(0, 2)
                    else:  # Move up
                        print("Moving up")
                        shopkeeper.move(0, -2)
    else:
        # Make the shopkeeper patrol
        if shopkeeper.rect.right >= 2800 and shopkeeper.rect.right < 4000 and shopkeeper.moving_right:
            shopkeeper.move(2, 0)
            if shopkeeper.rect.right >= 4000:
                shopkeeper.moving_right = False
        elif shopkeeper.rect.right <= 4000 and not shopkeeper.moving_right:
            shopkeeper.move(-2, 0)
            if shopkeeper.rect.right <= 2800:
                shopkeeper.moving_right = True

    if shopkeeper.rect.left < 0:
        shopkeeper.rect.left = 0
    elif shopkeeper.rect.right > map_width:
        shopkeeper.rect.right = map_width


def handle_shopkeeper_chase(shopkeeper, player, fish_picked_up, shopkeeper_chasing):
    if not fish_picked_up:
        shopkeeper_chasing = False
    return shopkeeper_chasing
