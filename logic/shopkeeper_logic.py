def handle_shopkeeper_movement(shopkeeper, player, shopkeeper_chasing, map_width):
    if shopkeeper_chasing:
        # Make the shopkeeper chase the player
        if player.rect.x < shopkeeper.rect.x:
            shopkeeper.move(-2, 0)  # Move left
        elif player.rect.x > shopkeeper.rect.x:
            shopkeeper.move(2, 0)  # Move right
    else:
        # Make the shopkeeper patrol
        if shopkeeper.rect.right >= 2600 and shopkeeper.rect.right < 4000 and shopkeeper.moving_right:
            shopkeeper.move(2, 0)
            if shopkeeper.rect.right >= 4000:
                shopkeeper.moving_right = False
        elif shopkeeper.rect.right <= 4000 and not shopkeeper.moving_right:
            shopkeeper.move(-2, 0)
            if shopkeeper.rect.right <= 2600:
                shopkeeper.moving_right = True

    # Ensure the shopkeeper stays within the map bounds
    if shopkeeper.rect.left < 0:
        shopkeeper.rect.left = 0
    elif shopkeeper.rect.right > map_width:
        shopkeeper.rect.right = map_width


def handle_shopkeeper_chase(shopkeeper, player, fish_picked_up, shopkeeper_chasing):
    if not fish_picked_up:
        shopkeeper_chasing = False
    return shopkeeper_chasing
