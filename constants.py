WIDTH = 1600
HEIGHT = 900

FPS = 60

TILE_IMAGES = {
    'sand_wall': 'sand_wall.png',
    'sand_wall1': 'sand_wall1.png',
    'sand_wall2': 'sand_wall2.png',
    'sand_wall3': 'sand_wall3.png',
    'sand_wall4': 'sand_wall4.png',
    'sand_wall5': 'sand_wall5.png',
    'sand_wall6': 'sand_wall6.png',
    'sand_wall7': 'sand_wall7.png',
    'sand_wall8': 'sand_wall8.png',
    'plank': 'plank.png',
    'empty': 'grass.png'
}

PROJECTILE_IMAGES = {
    "ammo": "ammo.png",
    "bullet": "bullet.png",
    "steel_ball": "steel_ball.png",
    "spin_ball": "spin_ball.png",
    "tornado": "tornado.png",
    "spike": "spike.png"
}

LEVEL_MAPS = {
    0: "tutorial.txt",
    1: "map1.txt"
}

LEVEL_MUSIC = {
    0: "tutorial.mp3",
    1: "gunpowder_canyon.mp3"
}

PLAYER_IMAGE = 'mar.png'

TILE_WIDTH = TILE_HEIGHT = 100

SPIN_RECTS = {
    0: (WIDTH // 2 - 18, HEIGHT // 2 - 45, 8, 15),
    1: (WIDTH // 2 - 5, HEIGHT // 2 - 45, 8, 15),
    2: (WIDTH // 2 + 8, HEIGHT // 2 - 45, 8, 15)
}

HEALTH_OFFSET = (30, 40)