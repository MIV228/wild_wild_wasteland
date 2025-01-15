import sys

import pygame

from constants import WIDTH, HEIGHT, FPS
from extensions import load_level
from resources.camera import Camera
from screens import start_screen
from resources.player import Player
from resources.tile import Tile


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level, tiles_group, player_group, wall_group, all_sprites):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':
                Tile('wall', x, y, tiles_group, wall_group, all_sprites)
            elif level[y][x] == '@':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_player = Player(x, y, player_group, all_sprites)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario")

    clock = pygame.time.Clock()

    # отрисовываем начальный экран
    start_screen(screen)

    # основной персонаж
    player = None
    camera = Camera()

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()

    # загружаем карту
    player, level_x, level_y = generate_level(load_level('map1.txt'), tiles_group, player_group, wall_group, all_sprites)

    running = True
    # игра начнется после нажатия любой кнопки
    start_game = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start_game = True

        # если игра началась, то отрисовываем спрайты
        if start_game:
            player_group.update(pygame.key.get_pressed(), wall_group=wall_group)

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            # сначала отрисовываем тайлы
            tiles_group.draw(screen)
            # а уже затем игрока, иначе игрок может пропадать за тайлами
            player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
