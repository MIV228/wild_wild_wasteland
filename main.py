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
    pygame.display.set_caption("Wild Wild Wasteland")

    clock = pygame.time.Clock()

    button_group = []

    # отрисовываем начальный экран
    start_screen(screen, button_group)

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
    curr_screen = 1 # 0 - игра, 1 - главное меню
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if curr_screen != 0:
                        curr_screen = 0
                    else:
                        curr_screen = 1
                        start_screen(screen, button_group)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if curr_screen != 0:
                    x, y = pygame.mouse.get_pos()
                    for button in button_group:
                        if button.check_clicked(x, y):
                            if button.function_type == 0:
                                curr_screen = 1
                                start_screen(screen, button_group)

        # если игра началась, то отрисовываем спрайты
        if curr_screen == 0:
            player_group.update(pygame.key.get_pressed(), wall_group=wall_group)

            camera.update(player)
            for sprite in all_sprites:
                camera.apply(sprite)

            screen.fill((0, 0, 0))
            # сначала отрисовываем тайлы
            tiles_group.draw(screen)
            # а уже затем игрока, иначе игрок может пропадать за тайлами
            player_group.draw(screen)

        elif curr_screen == 1:
            font = pygame.font.Font(None, 50)
            for button in button_group:
                pygame.draw.rect(screen, pygame.Color("white"), button.rect, 5)
                string_rendered = font.render(button.text, 1, pygame.Color('white'))
                text_rect = string_rendered.get_rect()
                text_rect.y = button.pos_y + 20
                text_rect.x = button.pos_x + 20
                screen.blit(string_rendered, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
