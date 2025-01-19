import sys

import pygame

from constants import WIDTH, HEIGHT, FPS, LEVEL_MAPS, SPIN_RECTS
from extensions import load_level, load_image
from resources.camera import Camera
from screens import start_screen
from resources.player import Player
from resources.tile import Tile


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level, tiles_group, player_group, wall_group, all_sprites):
    if tiles_group:
        tiles_group.empty()
        player_group.empty()
        wall_group.empty()
        all_sprites.empty()
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

def draw_spin_rect(n, color):
    if n == 0:
        pygame.draw.rect(screen, color, SPIN_RECTS[0])
    elif n == 1:
        pygame.draw.rect(screen, color, SPIN_RECTS[0])
        pygame.draw.rect(screen, color, SPIN_RECTS[1])
    else:
        pygame.draw.rect(screen, color, SPIN_RECTS[0])
        pygame.draw.rect(screen, color, SPIN_RECTS[1])
        pygame.draw.rect(screen, color, SPIN_RECTS[2])

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wild Wild Wasteland")

    clock = pygame.time.Clock()

    button_group = []

    # отрисовываем начальный экран
    start_screen(screen, button_group)

    # основной персонаж
    camera = Camera()

    # группы спрайтов

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()

    # загружаем карту
    player, level_x, level_y = generate_level(load_level
                                              (LEVEL_MAPS[0]),
                                              tiles_group,
                                              player_group,
                                              wall_group,
                                              all_sprites)

    delta_time = 0

    font = pygame.font.Font("www_font.ttf", 60)
    black_fade = 1

    running = True
    curr_screen = 1 # 0 - игра, 1 - главное меню
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if curr_screen == 0:
                        curr_screen = 1
                        black_fade = 1
                        #start_screen(screen, button_group)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if curr_screen != 0 and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    for button in button_group[curr_screen - 1]:
                        if button.check_clicked(x, y):
                            if button.function_type == 0:
                                curr_screen = 0
                                player, level_x, level_y = generate_level(load_level
                                                                          (LEVEL_MAPS[button.par]),
                                                                          tiles_group,
                                                                          player_group,
                                                                          wall_group,
                                                                          all_sprites)
                                black_fade = 1
                            elif button.function_type == 1:
                                terminate()
                            elif button.function_type == 2:
                                curr_screen = button.par


        # если игра началась, то отрисовываем спрайты
        if curr_screen == 0:
            player_group.update(pygame.key.get_pressed(), pygame.mouse.get_pressed(), delta_time,
                                wall_group=wall_group)

            if player:
                camera.update(player)
                for sprite in all_sprites:
                    camera.apply(sprite)

            screen.fill((0, 0, 0))
            # сначала отрисовываем тайлы
            tiles_group.draw(screen)
            # а уже затем игрока, иначе игрок может пропадать за тайлами
            player_group.draw(screen)

            if player:
                if player.spin_seconds == 0:
                    pass

                elif 0 < player.spin_seconds < 0.16:
                    draw_spin_rect(0, (255, 255, 255))
                elif 0.16 <= player.spin_seconds < 0.33:
                    draw_spin_rect(1, (255, 255, 255))
                elif 0.33 <= player.spin_seconds < 0.5:
                    draw_spin_rect(2, (255, 255, 255))

                elif 0.5 <= player.spin_seconds < 1:
                    draw_spin_rect(0, (0, 169, 255))
                elif 1 <= player.spin_seconds < 1.5:
                    draw_spin_rect(1, (0, 169, 255))
                elif 1.5 <= player.spin_seconds < 2:
                    draw_spin_rect(2, (0, 169, 255))

                elif 2 <= player.spin_seconds < 2.9:
                    draw_spin_rect(0, (255, 196, 0))
                elif 2.9 <= player.spin_seconds < 3.8:
                    draw_spin_rect(1, (255, 196, 0))
                elif 3.8 <= player.spin_seconds < 4:
                    draw_spin_rect(2, (255, 196, 0))

                elif 4 <= player.spin_seconds < 5.33:
                    draw_spin_rect(0, (255, 106, 0))
                elif 5.33 <= player.spin_seconds < 6.66:
                    draw_spin_rect(1, (255, 106, 0))
                elif 6.66 <= player.spin_seconds < 8:
                    draw_spin_rect(2, (255, 106, 0))

                elif 8 <= player.spin_seconds < 10:
                    draw_spin_rect(0, (255, 0, 0))
                elif 10 <= player.spin_seconds < 12:
                    draw_spin_rect(1, (255, 0, 0))
                elif 12 <= player.spin_seconds < 14:
                    draw_spin_rect(2, (255, 0, 0))
        else:
            screen.blit(load_image("background.png", screen.get_width(), screen.get_height()), (0, 0))
            for button in button_group[curr_screen - 1]:
                screen.blit(button.image, (button.pos_x, button.pos_y))
                string_rendered = font.render(button.text.lower(), 1, (40, 24, 7))
                text_rect = string_rendered.get_rect()
                text_rect.y = button.pos_y + button.rect.h // 2 - text_rect.h // 2 + 5
                text_rect.x = button.pos_x + button.rect.w // 2 - text_rect.w // 2
                screen.blit(string_rendered, text_rect)

        if black_fade > 0:
            r = pygame.Surface((WIDTH, HEIGHT))
            r.set_alpha(black_fade * 255)
            r.fill((0, 0, 0))
            screen.blit(r, (0, 0))
            black_fade -= delta_time


        pygame.display.flip()
        delta_time = clock.tick(FPS) / 1000

    pygame.quit()
