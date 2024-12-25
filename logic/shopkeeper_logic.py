def handle_shopkeeper_movement(shopkeeper, player, shopkeeper_chasing, map_width):
    if shopkeeper_chasing:
        # Make the shopkeeper chase the player
        if player.rect.x < shopkeeper.rect.x:
            shopkeeper.move(-2, 0)  # Move left
        elif player.rect.x > shopkeeper.rect.x:
            shopkeeper.move(2, 0)  # Move right
    else:
        shopkeeper.move(shopkeeper.horizontal_velocity,
                        0)  # Move shopkeeper normally

    # Ensure the shopkeeper stays within the map bounds
    if shopkeeper.rect.left < 0:
        shopkeeper.rect.left = 0
    elif shopkeeper.rect.right > map_width:
        shopkeeper.rect.right = map_width


def handle_shopkeeper_chase(shopkeeper, player, fish_picked_up, shopkeeper_chasing):
    if not fish_picked_up:
        shopkeeper_chasing = False
    return shopkeeper_chasing
