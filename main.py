import sys

import pygame

from constants import WIDTH, HEIGHT, FPS, LEVEL_MAPS, SPIN_RECTS, HEALTH_OFFSET
from extensions import load_level, load_image
from resources.camera import Camera
from screens import start_screen
from resources.player import Player
from resources.tile import Tile
from resources.enemies import GunEnemy, Box, ShotgunEnemy


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level, tiles_group, player_group, enemy_group, dead_enemies, wall_group, all_sprites, *delete_groups):
    if tiles_group:
        tiles_group.empty()
        player_group.empty()
        wall_group.empty()
        all_sprites.empty()
        projectiles.clear()
        pickups.clear()
        enemy_group.empty()
        dead_enemies.empty()
        if delete_groups:
            for g in delete_groups:
                g.empty()
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, tiles_group, all_sprites)
            elif level[y][x] == '#':
                if x != 0 and x != len(level[0]) - 1 and y != 0 and y != len(level) - 1:
                    if level[y][x + 1] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    elif level[y][x - 1] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    elif level[y + 1][x] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    elif level[y + 1][x - 1] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    elif level[y + 1][x + 1] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    elif level[y - 1][x] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    elif level[y - 1][x - 1] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    elif level[y - 1][x + 1] != "#":
                        Tile('wall', x, y, tiles_group, wall_group, all_sprites)
                    else:
                        Tile('wall', x, y, tiles_group, all_sprites)
                else:
                    Tile('wall', x, y, tiles_group, all_sprites)
            elif level[y][x] == '@':
                Tile('empty', x, y, tiles_group, all_sprites)
                new_player = Player(x, y, player_group, all_sprites)
            elif level[y][x] == 'E':
                Tile('empty', x, y, tiles_group, all_sprites)
                GunEnemy(x, y, enemy_group, all_sprites)
            elif level[y][x] == '+':
                Tile('empty', x, y, tiles_group, all_sprites)
                Box(x, y, enemy_group, wall_group, all_sprites)
            elif level[y][x] == 'S':
                Tile('empty', x, y, tiles_group, all_sprites)
                ShotgunEnemy(x, y, enemy_group, all_sprites)
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
    enemy_group = pygame.sprite.Group()
    dead_enemies = pygame.sprite.Group()
    projectiles = []
    pickups = []

    # загружаем карту
    player, level_x, level_y = generate_level(load_level
                                              (LEVEL_MAPS[0]),
                                              tiles_group,
                                              player_group,
                                              enemy_group,
                                              dead_enemies,
                                              wall_group,
                                              all_sprites)

    delta_time = 0

    font = pygame.font.Font("www_font.ttf", 60)
    black_fade = 1

    heart_image = pygame.transform.scale_by(load_image("heart.png"), 2)
    ammo_image = pygame.transform.scale_by(load_image("ammo.png"), 4)
    interface_bg = pygame.transform.scale_by(load_image("interface_bg.png"), 4)

    running = True
    curr_screen = 1  # 0 - игра, 1 - главное меню
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if curr_screen == 0:
                        curr_screen = 1
                        black_fade = 1
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
                                                                          enemy_group,
                                                                          dead_enemies,
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
                                wall_group=wall_group, screen=screen, projectiles=projectiles)
            enemy_group.update(delta_time,
                                wall_group=wall_group, screen=screen, projectiles=projectiles,
                               player=player, pickups=pickups)

            if player.health <= 0 and player.dead_timer <= 0:
                curr_screen = 1
                black_fade = 1

            enemies_to_delete = []
            for enemy in enemy_group:
                if enemy.is_dead:
                    enemies_to_delete.append(enemy)
            if enemies_to_delete:
                for enemy in enemies_to_delete:
                    enemy_group.remove(enemy)
                    dead_enemies.add(enemy)
            if player:
                camera.update(player)
                for sprite in all_sprites:
                    camera.apply(sprite)

            screen.fill((0, 0, 0))
            # сначала отрисовываем тайлы
            tiles_group.draw(screen)
            proj_to_delete = []
            if projectiles:
                for p in projectiles:
                    p.update()
                    if not p.piercing:
                        for wall in wall_group:
                            if p.rect.colliderect(wall.rect):
                                p.lifetime = 0
                                break
                    if p.player_friendly:
                        for enemy in enemy_group:
                            if p.rect.colliderect(enemy.rect):
                                enemy.hurt(p.damage)
                                if not p.piercing:
                                    p.lifetime = 0
                    else:
                        if p.rect.colliderect(player.rect):
                            player.hurt(p.damage)
                            if not p.piercing:
                                p.lifetime = 0
                    p.lifetime -= delta_time
                    if p.lifetime <= 0:
                        proj_to_delete.append(p)
                if proj_to_delete:
                    for p in proj_to_delete:
                        projectiles.remove(p)
            pickups_to_delete = []
            if pickups:
                for p in pickups:
                    p.update(player.rect.x, player.rect.y)
                    if p.rect.colliderect(player.rect):
                        if p.p_type == "heart.png":
                            player.health += 1
                        elif p.p_type == "ammo.png":
                            player.ammo += 1

                        pickups_to_delete.append(p)
                if pickups_to_delete:
                    for p in pickups_to_delete:
                        pickups.remove(p)

            # а уже затем игрока, иначе игрок может пропадать за тайлами
            dead_enemies.draw(screen)
            player_group.draw(screen)
            enemy_group.draw(screen)

            screen.blit(interface_bg, (40, 138))
            for i in range(player.health):
                screen.blit(heart_image, (HEALTH_OFFSET[0] + i * 100, HEALTH_OFFSET[1]))
            screen.blit(ammo_image, (54, 154))
            ammo_string = font.render(str(player.ammo), 1, (40, 24, 7))
            text_rect = ammo_string.get_rect()
            text_rect.y = 149
            text_rect.x = 120
            screen.blit(ammo_string, text_rect)

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
                ammo_string = font.render(button.text.lower(), 1, (40, 24, 7))
                text_rect = ammo_string.get_rect()
                text_rect.y = button.pos_y + button.rect.h // 2 - text_rect.h // 2 + 5
                text_rect.x = button.pos_x + button.rect.w // 2 - text_rect.w // 2
                screen.blit(ammo_string, text_rect)

        if black_fade > 0:
            fade_rect = pygame.Surface((WIDTH, HEIGHT))
            fade_rect.set_alpha(black_fade * 255)
            fade_rect.fill((0, 0, 0))
            screen.blit(fade_rect, (0, 0))
            black_fade -= delta_time

        pygame.display.flip()
        delta_time = clock.tick(FPS) / 1000

    pygame.quit()
