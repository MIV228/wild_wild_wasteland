WIDTH = 1600
HEIGHT = 900

FPS = 60

TILE_IMAGES = {
    'wall': 'plank.png',
    'empty': 'grass.png'
}

PROJECTILE_IMAGES = {
    "bullet": "grass.png"
}

LEVEL_MAPS = {
    0: "map1.txt",
    1: "map2.txt"
}

PLAYER_IMAGE = 'mar.png'

TILE_WIDTH = TILE_HEIGHT = 100

SPIN_RECTS = {
    0: (WIDTH // 2 - 18, HEIGHT // 2 - 45, 8, 15),
    1: (WIDTH // 2 - 5, HEIGHT // 2 - 45, 8, 15),
    2: (WIDTH // 2 + 8, HEIGHT // 2 - 45, 8, 15)
}