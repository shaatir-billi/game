import pygame
import math


def handle_shopkeeper_movement(shopkeeper, player, shopkeeper_chasing, map_width, keys, graph):
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

        closest_node = min(nodes, key=lambda node: weighted_manhattan_distance(
            node, shopkeeper_center))

        closest_node_to_player = min(nodes, key=lambda node: weighted_manhattan_distance(
            node, player_center))

        path = graph.a_star_search(closest_node, closest_node_to_player)

        print("Shopkeeper closest node:", closest_node)
        print("Player closest node:", closest_node_to_player)
        print("Path:", path)

        if len(path) > 1:
            next_node = path[1]
            print("Shopkeeper moving to node:", next_node)
            if shopkeeper.rect.x < next_node[0]:
                shopkeeper.move(2, 0)
            elif shopkeeper.rect.x > next_node[0]:
                shopkeeper.move(-2, 0)

            # check for vertical movement, with some lee-way
            if shopkeeper.rect.centery < next_node[1] - 10:
                print("moving down")
                print("shopkeeper rect y:", shopkeeper.rect.centery)
                print("next node y:", next_node[1])
                shopkeeper.move(0, 2)
            elif shopkeeper.rect.centery > next_node[1] + 10:
                print("moving up")
                print("shopkeeper rect y:", shopkeeper.rect.centery)
                print("next node y:", next_node[1])
                shopkeeper.move(0, -2)

            # if shopkeeper.rect.y  < next_node[1]:
            #     shopkeeper.move(0, 2)
            # elif shopkeeper.rect.y > next_node[1]:
            #     shopkeeper.move(0, -2)
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
