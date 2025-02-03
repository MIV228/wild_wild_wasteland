import random
import sys

import pygame

from constants import WIDTH, HEIGHT, FPS, LEVEL_MAPS, SPIN_RECTS, HEALTH_OFFSET, LEVEL_MUSIC
from extensions import load_level, load_image, load_sound
from scripts.camera import Camera
from scripts.enemies import GunEnemy, Box, ShotgunEnemy, Cactus, Plank, MinigunEnemy
from scripts.player import Player
from scripts.sign import Sign
from scripts.tile import Tile
from scripts.screens import start_screen


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level, *delete_groups):
    global kills, level_time, tiles_group, player_group, enemy_group, dead_enemies, curr_level,\
        sign_group, wall_group, particle_group, level_objective_group, all_sprites,\
        property_damage, total_dollars, level_end_group
    if tiles_group:
        tiles_group.empty()
        player_group.empty()
        wall_group.empty()
        all_sprites.empty()
        projectiles.clear()
        pickups.clear()
        enemy_group.empty()
        dead_enemies.empty()
        particle_group.empty()
        level_objective_group.empty()
        level_end_group.empty()
        sign_group.empty()
        if delete_groups:
            for g in delete_groups:
                g.empty()
        kills = 0
        level_time = 0
        property_damage = 0
        total_dollars = 0
    pygame.mixer.music.load(load_sound(LEVEL_MUSIC[curr_level]))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.8)
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if curr_level == 0:
                if level[y][x] == '.':
                    Tile('empty', x, y, tiles_group, all_sprites)
                elif level[y][x] == '#':
                    if x != 0 and x != len(level[0]) - 1 and y != 0 and y != len(level) - 1:
                        if level[y][x + 1] != "#":
                            if level[y - 1][x] != "#":
                                Tile('sand_wall3', x, y, tiles_group, wall_group, all_sprites)
                            elif level[y + 1][x] != "#":
                                Tile('sand_wall5', x, y, tiles_group, wall_group, all_sprites)
                            else:
                                Tile('sand_wall4', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y][x - 1] != "#":
                            if level[y - 1][x] != "#":
                                Tile('sand_wall1', x, y, tiles_group, wall_group, all_sprites)
                            elif level[y + 1][x] != "#":
                                Tile('sand_wall7', x, y, tiles_group, wall_group, all_sprites)
                            else:
                                Tile('sand_wall8', x, y, tiles_group, wall_group, all_sprites)
                            # сверху - снизу
                        elif level[y - 1][x] != "#":
                            Tile('sand_wall2', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y + 1][x] != "#":
                            Tile('sand_wall6', x, y, tiles_group, wall_group, all_sprites)
                            # по диагонали
                        elif level[y + 1][x - 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y + 1][x + 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y - 1][x - 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y - 1][x + 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        else:
                            Tile('sand_wall', x, y, tiles_group, all_sprites)
                    else:
                        Tile('sand_wall', x, y, tiles_group, all_sprites)
                elif level[y][x] == '@':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    new_player = Player(x, y, particle_group, player_group, all_sprites)
                elif level[y][x] == '+':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Box(x, y, particle_group, enemy_group, wall_group, all_sprites)
                elif level[y][x] == '*':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Cactus(x, y - 1, particle_group, enemy_group, wall_group, all_sprites)
                elif level[y][x] == "=":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Plank(x, y, particle_group, enemy_group, wall_group, all_sprites)
                elif level[y][x] == "]":
                    Tile('empty', x, y, tiles_group, level_objective_group, wall_group, all_sprites)
                elif level[y][x] == "[":
                    Tile('empty', x, y, tiles_group, level_end_group, all_sprites)
                elif level[y][x] == "0":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Sign(x, y, "use WASD to move", sign_group, all_sprites)
                elif level[y][x] == "1":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Sign(x, y, "hold [LMB] to spin the ball, release to shoot it", sign_group,
                         all_sprites)
                elif level[y][x] == "2":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Sign(x, y, "balls with perfect rotation deal double damage", sign_group,
                         all_sprites)
                elif level[y][x] == "3":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Sign(x, y, "press [RMB] to quickdraw a shotgun blast", sign_group, all_sprites)
                elif level[y][x] == "4":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Sign(x, y, "most things here explode when deformed", sign_group, all_sprites)
                elif level[y][x] == "5":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Sign(x, y, "destroy strongholds to get $20000 extra", sign_group, all_sprites)
            else:
                if level[y][x] == '.':
                    Tile('empty', x, y, tiles_group, all_sprites)
                elif level[y][x] == '#':
                    if x != 0 and x != len(level[0]) - 1 and y != 0 and y != len(level) - 1:
                        if level[y][x + 1] != "#":
                            if level[y - 1][x] != "#":
                                Tile('sand_wall3', x, y, tiles_group, wall_group, all_sprites)
                            elif level[y + 1][x] != "#":
                                Tile('sand_wall5', x, y, tiles_group, wall_group, all_sprites)
                            else:
                                Tile('sand_wall4', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y][x - 1] != "#":
                            if level[y - 1][x] != "#":
                                Tile('sand_wall1', x, y, tiles_group, wall_group, all_sprites)
                            elif level[y + 1][x] != "#":
                                Tile('sand_wall7', x, y, tiles_group, wall_group, all_sprites)
                            else:
                                Tile('sand_wall8', x, y, tiles_group, wall_group, all_sprites)
                            # сверху - снизу
                        elif level[y - 1][x] != "#":
                            Tile('sand_wall2', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y + 1][x] != "#":
                            Tile('sand_wall6', x, y, tiles_group, wall_group, all_sprites)
                            # по диагонали
                        elif level[y + 1][x - 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y + 1][x + 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y - 1][x - 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        elif level[y - 1][x + 1] != "#":
                            Tile('sand_wall', x, y, tiles_group, wall_group, all_sprites)
                        else:
                            Tile('sand_wall', x, y, tiles_group, all_sprites)
                    else:
                        Tile('sand_wall', x, y, tiles_group, all_sprites)
                elif level[y][x] == '@':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    new_player = Player(x, y, particle_group, player_group, all_sprites)
                elif level[y][x] == 'E':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    GunEnemy(x, y, particle_group, enemy_group, all_sprites)
                elif level[y][x] == '+':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Box(x, y, particle_group, enemy_group, wall_group, all_sprites)
                elif level[y][x] == '!':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Box(x, y, particle_group, enemy_group, level_objective_group, wall_group,
                        all_sprites)
                elif level[y][x] == 'S':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    ShotgunEnemy(x, y, particle_group, enemy_group, all_sprites)
                elif level[y][x] == 'M':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    MinigunEnemy(x, y, particle_group, enemy_group, all_sprites)
                elif level[y][x] == '*':
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Cactus(x, y - 1, particle_group, enemy_group, wall_group, all_sprites)
                elif level[y][x] == "=":
                    Tile('empty', x, y, tiles_group, all_sprites)
                    Plank(x, y, particle_group, enemy_group, wall_group, all_sprites)
                elif level[y][x] == "]":
                    Tile('empty', x, y, tiles_group, wall_group, all_sprites)
                elif level[y][x] == "[":
                    Tile('empty', x, y, tiles_group, level_end_group, all_sprites)
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
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    # screen = pygame.display.set_mode((1200, 675))
    pygame.display.set_caption("Wild Wild Wasteland")

    clock = pygame.time.Clock()

    button_group = []

    # отрисовываем начальный экран
    start_screen(button_group)

    # основной персонаж
    camera = Camera()

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    dead_enemies = pygame.sprite.Group()
    particle_group = pygame.sprite.Group()
    level_objective_group = pygame.sprite.Group()
    level_end_group = pygame.sprite.Group()

    sign_group = pygame.sprite.Group()

    projectiles = []
    pickups = []

    kills = 0
    kill_bonus = 0
    level_time = 0
    property_damage = 0
    total_dollars = 0
    curr_level = 0

    # загружаем карту
    player, level_x, level_y = None, None, None

    savefile = open("data/savefile.txt", mode="a+", encoding="utf-8")
    savefile.seek(0)
    lines = savefile.read().split("\n")
    if len(lines) < 3:
        lines = ["0", "0", "0", "0", "0"]

    delta_time = 0

    font = pygame.font.Font("www_font.ttf", 60)
    big_font = pygame.font.Font("www_font.ttf", 90)
    black_fade = 1

    heart_image = pygame.transform.scale_by(load_image("heart.png"), 2)
    ammo_image = pygame.transform.scale_by(load_image("ammo.png"), 4)
    interface_bg = pygame.transform.scale_by(load_image("interface_bg.png"), 4)
    scope_image = pygame.transform.scale_by(load_image("scope.png"), 4)

    sounds = {
        "box": pygame.mixer.Sound(load_sound("plank_break.wav")),
        "plank": pygame.mixer.Sound(load_sound("plank_break.wav")),
        "cactus": pygame.mixer.Sound(load_sound("cactus_explosion.wav")),
        "damage": pygame.mixer.Sound(load_sound("damage.wav")),
        "death": pygame.mixer.Sound(load_sound("death.wav")),
        "pickup": pygame.mixer.Sound(load_sound("pickup.wav")),
        "gun": pygame.mixer.Sound(load_sound("gun_shot.wav")),
        "shotgun": pygame.mixer.Sound(load_sound("shotgun_shot.wav"))
    }

    running = True
    curr_screen = 1  # -2 - конец игры, -1 - конец уровня, 0 - игра, 1... - главное меню
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if curr_screen == 0 or curr_screen == -1:
                        curr_screen = 1
                        black_fade = 1
                        pygame.mouse.set_visible(True)
                        button_group.clear()
                        start_screen(button_group)
                elif event.key == pygame.K_SPACE:
                    if curr_screen == -1:
                        if curr_level < len(LEVEL_MAPS) - 1:
                            curr_level += 1
                            player, level_x, level_y = generate_level(
                                load_level(LEVEL_MAPS[curr_level]))
                            black_fade = 1
                            curr_screen = 0
                        else:
                            curr_screen = -2
                            black_fade = 1
                            pygame.mouse.set_visible(True)
                            pygame.mixer.music.stop()
                    elif curr_screen == -2:
                        curr_screen = 1
                        black_fade = 1
                        pygame.mouse.set_visible(True)
                        button_group.clear()
                        start_screen(button_group)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if curr_screen >= 1 and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    for button in button_group[curr_screen - 1]:
                        if button.check_clicked(x, y):
                            if button.function_type == 0:
                                curr_screen = 0
                                curr_level = button.par
                                player, level_x, level_y = generate_level(
                                    load_level(LEVEL_MAPS[button.par]))
                                black_fade = 1
                                pygame.mouse.set_visible(False)
                            elif button.function_type == 1:
                                terminate()
                            elif button.function_type == 2:
                                curr_screen = button.par
                                if button.par == 2 and lines[4] == "0":
                                    curr_screen = 0
                                    curr_level = 0
                                    player, level_x, level_y = generate_level(
                                        load_level(LEVEL_MAPS[0]))
                                    black_fade = 1
                                    pygame.mouse.set_visible(False)

        if curr_screen == 0:
            player_group.update(pygame.key.get_pressed(), pygame.mouse.get_pressed(), delta_time,
                                wall_group=wall_group, screen=screen, projectiles=projectiles)
            enemy_group.update(delta_time,
                               wall_group=wall_group, screen=screen, projectiles=projectiles,
                               player=player, pickups=pickups)
            particle_group.update()

            level_time += delta_time

            if player.health <= 0 and player.dead_timer <= 0:
                player, level_x, level_y = generate_level(load_level(LEVEL_MAPS[curr_level]))
                black_fade = 1

            enemies_to_delete = []
            for enemy in enemy_group:
                if enemy.is_dead:
                    enemies_to_delete.append(enemy)
            if enemies_to_delete:
                for enemy in enemies_to_delete:
                    if enemy not in wall_group:
                        kills += 1
                    enemy_group.remove(enemy)
                    dead_enemies.add(enemy)
            if player:
                camera.update(player)
                for sprite in all_sprites:
                    camera.apply(sprite)

            # сейв - файл:
            # 1) total kills
            # 2) property damage
            # 3) total strongholds
            # 4) total revenue
            # 5) current level
            for hitbox in level_end_group:
                if player.rect.colliderect(hitbox.rect):
                    if kills != 0:
                        kill_bonus = random.randint(1, 999)
                    else:
                        kill_bonus = 0
                    curr_screen = -1
                    total_dollars = (property_damage + kills * 1000 + kill_bonus
                                     + (1000 if level_time < 200 else 500))
                    if len(level_objective_group) == 0:
                        total_dollars += 20000

                    if len(lines) < 3:
                        lines = ["0", "0", "0", "0", "0"]
                    savefile.truncate(0)
                    savefile.write("\n".join([str(int(lines[0]) + kills),
                                              str(int(lines[1]) + property_damage),
                                              str(int(lines[2]) + 1 if len(
                                                  level_objective_group) == 0 else 0),
                                              str(int(lines[3]) + total_dollars),
                                              str(curr_level) if curr_level > int(lines[4]) else
                                              lines[4]]))
                    savefile.seek(0)
                    lines = savefile.read().split("\n")

                    pygame.mixer.music.set_volume(0.3)

            screen.fill((0, 0, 0))
            # сначала отрисовываем тайлы
            tiles_group.draw(screen)
            proj_to_delete = []
            if projectiles:
                for p in projectiles:
                    p.update()
                    if p.player_friendly:
                        for enemy in enemy_group:
                            if p.rect.colliderect(enemy.rect):
                                s_id = enemy.hurt(p.damage)
                                if s_id is not None:
                                    sounds[s_id].stop()
                                    sounds[s_id].play()
                                if not p.piercing:
                                    p.lifetime = 0
                                if len(enemy.groups()) == 0:  # нет групп - значит коробка
                                    property_damage += enemy.dollars
                    else:
                        if p.rect.colliderect(player.rect):
                            player.hurt(p.damage)
                            sounds["damage"].stop()
                            sounds["damage"].play()
                            if not p.piercing:
                                p.lifetime = 0
                    if not p.passes_env:
                        for wall in wall_group:
                            if p.rect.colliderect(wall.rect):
                                if not wall in enemy_group or not p.player_friendly:
                                    p.lifetime = 0
                                    break
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
                        elif p.p_type == "minigun.png":
                            player.curr_weapon = "minigun"
                            player.s_shotgun = pygame.mixer.Sound(load_sound("gun_shot.wav"))
                            pygame.mixer.music.load(load_sound("last_call.wav"))
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.8)
                        sounds["pickup"].stop()
                        sounds["pickup"].play()
                        pickups_to_delete.append(p)
                if pickups_to_delete:
                    for p in pickups_to_delete:
                        pickups.remove(p)

            sign_group.draw(screen)
            # а уже затем игрока, иначе игрок может пропадать за тайлами
            dead_enemies.draw(screen)
            player_group.draw(screen)
            enemy_group.draw(screen)

            screen.blit(interface_bg, (40, 138))
            for i in range(player.health):
                screen.blit(heart_image, (HEALTH_OFFSET[0] + i * 100, HEALTH_OFFSET[1]))
            screen.blit(ammo_image, (54, 154))
            text = font.render(str(player.ammo), 1, (40, 24, 7))
            text_rect = text.get_rect()
            text_rect.y = 149
            text_rect.x = 120
            screen.blit(text, text_rect)

            particle_group.draw(screen)

            sign_group.update(player.rect.centerx, player.rect.centery, screen=screen)

            if player:
                if player.shoot_cd > 0:
                    pygame.draw.rect(screen, pygame.Color("white"),
                                     (WIDTH // 2 - 20, HEIGHT // 2 + 40, int(player.shoot_cd * 80),
                                      10))
                if player.spin_seconds == 0:
                    pass

                elif 0 < player.spin_seconds < 0.16:
                    draw_spin_rect(0, (255, 255, 255))
                elif 0.16 <= player.spin_seconds < 0.33:
                    draw_spin_rect(1, (255, 255, 255))
                elif 0.33 <= player.spin_seconds < 0.5:
                    draw_spin_rect(2, (255, 255, 255))

                elif 0.5 <= player.spin_seconds < 0.8:
                    draw_spin_rect(0, (0, 169, 255))
                elif 0.8 <= player.spin_seconds < 1.2:
                    draw_spin_rect(1, (0, 169, 255))
                elif 1.2 <= player.spin_seconds < 1.5:
                    draw_spin_rect(2, (0, 169, 255))

                elif 1.5 <= player.spin_seconds < 2.4:
                    draw_spin_rect(0, (255, 196, 0))
                elif 2.4 <= player.spin_seconds < 3.3:
                    draw_spin_rect(1, (255, 196, 0))
                elif 3.3 <= player.spin_seconds < 3.5:
                    draw_spin_rect(2, (255, 196, 0))

                elif 3.5 <= player.spin_seconds < 5.33:
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

            screen.blit(scope_image, (pygame.mouse.get_pos()[0] - scope_image.get_width() // 2,
                                      pygame.mouse.get_pos()[1] - scope_image.get_height() // 2))
        elif curr_screen == -1:
            screen.blit(load_image("endscreen_bg.png", screen.get_width(), screen.get_height()),
                        (0, 0))
            texts = [f"enemies killed:  {kills}", f"time taken:  {int(level_time)}",
                     f"property damage:  ${property_damage}"]
            text_pos_1 = (WIDTH // 2 - 350, HEIGHT // 2 - 300)
            for i in range(len(texts)):
                text = font.render(texts[i], 1, (40, 24, 7))
                text_rect = text.get_rect()
                text_rect.y = text_pos_1[1] + i * 80
                text_rect.x = text_pos_1[0]
                screen.blit(text, text_rect)

            texts_dollars = [f"${kills * 1000 + kill_bonus}",
                             f"${1000 if level_time < 200 else 500}",
                             f"${property_damage}"]
            for i in range(len(texts)):
                text = font.render(texts_dollars[i], 1, (40, 24, 7))
                text_rect = text.get_rect()
                text_rect.y = text_pos_1[1] + i * 80
                text_rect.x = text_pos_1[0] + 630
                screen.blit(text, text_rect)

            if len(level_objective_group) == 0:  # склад разрушен
                text = font.render("stronghold destruction bonus:", 1, (40, 24, 7))
                text_rect = text.get_rect()
                text_rect.y = text_pos_1[1] + 3 * 80
                text_rect.x = text_pos_1[0]
                screen.blit(text, text_rect)

                text2 = big_font.render("$20000!", 1, (40, 24, 7))
                text_rect2 = text2.get_rect()
                text_rect2.y = text_pos_1[1] + 3 * 80
                text_rect2.x = text_pos_1[0] + 630
                screen.blit(text2, text_rect2)

            text1 = big_font.render("total revenue:", 1, (40, 24, 7))
            text_rect1 = text1.get_rect()
            text_rect1.y = text_pos_1[1] + 5 * 80
            text_rect1.x = text_pos_1[0]
            screen.blit(text1, text_rect1)

            text2 = big_font.render(f"${total_dollars}", 1, (40, 24, 7))
            text_rect2 = text2.get_rect()
            text_rect2.y = text_pos_1[1] + 5 * 80
            text_rect2.x = text_pos_1[0] + 630
            screen.blit(text2, text_rect2)

            text3 = font.render("[esc] - main menu      [space] - next level", 1, (40, 24, 7))
            text_rect3 = text3.get_rect()
            text_rect3.y = text_pos_1[1] + int(7 * 80)
            text_rect3.x = WIDTH // 2 - text_rect3.w // 2
            screen.blit(text3, text_rect3)
        elif curr_screen == -2:
            # сейв - файл:
            # 1) total kills
            # 2) property damage
            # 3) total strongholds
            # 4) total revenue
            # 5) current level
            screen.blit(load_image("endscreen_bg.png", screen.get_width(), screen.get_height()),
                        (0, 0))
            texts = [f"total kills:  {lines[0]}", f"total property damage:  ${lines[1]}",
                     f"strongholds destroyed:  {lines[2]}"]
            text_pos_1 = (WIDTH // 2 - 350, HEIGHT // 2 - 300)
            for i in range(len(texts)):
                text = font.render(texts[i], 1, (40, 24, 7))
                text_rect = text.get_rect()
                text_rect.y = text_pos_1[1] + i * 80
                text_rect.x = text_pos_1[0]
                screen.blit(text, text_rect)

            text1 = font.render(f"total revenue:  ${lines[3]}", 1, (40, 24, 7))
            text_rect1 = text1.get_rect()
            text_rect1.y = text_pos_1[1] + 4 * 80
            text_rect1.x = text_pos_1[0]
            screen.blit(text1, text_rect1)

            text2 = big_font.render("thanks for playing!", 1, (40, 24, 7))
            text_rect2 = text2.get_rect()
            text_rect2.y = text_pos_1[1] + 6 * 80
            text_rect2.x = WIDTH // 2 - text_rect2.w // 2
            screen.blit(text2, text_rect2)

            text3 = font.render("[space] - main menu", 1, (40, 24, 7))
            text_rect3 = text3.get_rect()
            text_rect3.y = text_pos_1[1] + int(7.5 * 80)
            text_rect3.x = WIDTH // 2 - text_rect3.w // 2
            screen.blit(text3, text_rect3)
        else:
            screen.blit(load_image("background.png", screen.get_width(), screen.get_height()),
                        (0, 0))
            for button in button_group[curr_screen - 1]:
                screen.blit(button.image, (button.pos_x, button.pos_y))
                text = font.render(button.text.lower(), 1, (40, 24, 7))
                text_rect = text.get_rect()
                text_rect.y = button.pos_y + button.rect.h // 2 - text_rect.h // 2 + 5
                text_rect.x = button.pos_x + button.rect.w // 2 - text_rect.w // 2
                screen.blit(text, text_rect)

        if black_fade > 0:
            fade_rect = pygame.Surface((WIDTH, HEIGHT))
            fade_rect.set_alpha(black_fade * 255)
            fade_rect.fill((0, 0, 0))
            screen.blit(fade_rect, (0, 0))
            black_fade -= delta_time

        pygame.display.flip()
        delta_time = clock.tick(FPS) / 1000

    savefile.close()
    pygame.quit()
