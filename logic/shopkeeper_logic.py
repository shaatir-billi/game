import pygame
import math


def handle_shopkeeper_movement(shopkeeper, player, shopkeeper_chasing, map_width, keys, graph):
    if shopkeeper_chasing:
        nodes = graph.nodes
        # # Make the shopkeeper chase the player
        # if player.rect.x < shopkeeper.rect.x:
        #     shopkeeper.move(-2, 0)  # Move left
        # elif player.rect.x > shopkeeper.rect.x:
        #     shopkeeper.move(2, 0)  # Move right
        # calculate the closest node

        def euclidean_distance(node1, node2):
            return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

        closest_node = min(nodes, key=lambda node: euclidean_distance(
            node, (shopkeeper.rect.x, shopkeeper.rect.y)))

        # closest_node = None

        # for node in nodes:
        #     if closest_node is None:
        #         closest_node = node
        #     elif abs(node[0] - shopkeeper.rect.x) < abs(closest_node[0] - shopkeeper.rect.x):
        #         closest_node = node

        # go to the closest node
        if shopkeeper.rect.x < closest_node[0]:
            shopkeeper.move(2, 0)
        else:
            shopkeeper.move(-2, 0)

        # calculate the closest node to the player

        closest_node_to_player = min(nodes, key=lambda node: euclidean_distance(
            node, (player.rect.x, player.rect.y)))

        # closest_node_to_player = None

        # for node in nodes:
        #     if closest_node_to_player is None:
        #         closest_node_to_player = node
        #     elif abs(node[0] - player.rect.x) < abs(closest_node_to_player[0] - player.rect.x):
        #         closest_node_to_player = node

        # calculate a path to player node to shopkeeper node using A* algorithm
        path = graph.a_star_search(closest_node, closest_node_to_player)

        print("Shopkeeper closest node:", closest_node)
        print("Player closest node:", closest_node_to_player)
        print("Path:", path)

        # move the shopkeeper to the next node in the path

        if len(path) > 1:
            next_node = path[1]
            if shopkeeper.rect.x < next_node[0]:
                shopkeeper.move(2, 0)
            else:
                shopkeeper.move(-2, 0)

    else:
        # Make the shopkeeper patrol
        if shopkeeper.rect.right >= 2600 and shopkeeper.rect.right < 3000 and shopkeeper.moving_right:
            shopkeeper.move(2, 0)
        #     if shopkeeper.rect.right >= 4000:
        #         shopkeeper.moving_right = False
        # elif shopkeeper.rect.right <= 4000 and not shopkeeper.moving_right:
        #     shopkeeper.move(-2, 0)
        #     if shopkeeper.rect.right <= 2600:
        #         shopkeeper.moving_right = True

    # Ensure the shopkeeper stays within the map bounds
    if shopkeeper.rect.left < 0:
        shopkeeper.rect.left = 0
    elif shopkeeper.rect.right > map_width:
        shopkeeper.rect.right = map_width


def handle_shopkeeper_chase(shopkeeper, player, fish_picked_up, shopkeeper_chasing):
    if not fish_picked_up:
        shopkeeper_chasing = False
    return shopkeeper_chasing
