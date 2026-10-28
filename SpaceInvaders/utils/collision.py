def check_collision(object1, object2):

    return object1.rect.colliderect(
        object2.rect
    )