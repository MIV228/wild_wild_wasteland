import random

import pygame

from constants import PLAYER_IMAGE, TILE_WIDTH, TILE_HEIGHT
from extensions import load_image, load_sound
from scripts.projectile import Projectile
from scripts.pickups import Pickup
from scripts.particles import create_particles


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, particle_group, image, dead_image, *groups):
        super().__init__(*groups)
        self.image = load_image(image)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)
        # шаг определяем как размер клетки
        self.health = 30

        self.saw_player = False
        self.shoot_cd = random.random() * 2

        self.speed = 4
        self.vel_x = 0
        self.vel_y = 0
        self.move_cd = 1

        self.dead_image = load_image(dead_image)
        self.is_dead = False
        self.p_groups = [particle_group, groups[-1]]

        self.left_image = pygame.transform.flip(self.image, True, False)
        self.right_image = self.image

    def shoot(self, screen, projectiles, player_pos_x, player_pos_y):
        if self.is_dead: return

        if not self.saw_player:
            return

        self.shoot_cd = 0.5

    def hurt(self, damage):
        if self.is_dead: return

        self.health -= damage
        if self.health <= 0:
            self.image = self.dead_image
            self.is_dead = True

        create_particles((self.rect.centerx, self.rect.centery), "blood.png", 40, *self.p_groups)

        return "damage"

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        if self.is_dead: return

        if not self.saw_player:
            if screen.get_rect().colliderect(self.rect):
                self.saw_player = True
            else:
                return

        if player.rect.centerx > self.rect.centerx:
            self.image = self.right_image
        else:
            self.image = self.left_image


class GunEnemy(Enemy):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(pos_x, pos_y, particle_group, PLAYER_IMAGE, "button.png", *groups)

        self.ammo = 6

        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

        self.s_shoot = pygame.mixer.Sound(load_sound("gun_shot.wav"))

    def shoot(self, screen, projectiles, player_pos_x, player_pos_y):
        super().shoot(screen, projectiles, player_pos_x, player_pos_y)

        projectiles.append(Projectile(screen, self.rect.centerx, self.rect.centery,
                                      player_pos_x, player_pos_y,
                                      25, 1, 3, "bullet"))
        self.ammo -= 1
        self.s_shoot.play()

    def reload(self):
        self.ammo = 6

    def hurt(self, damage):
        return super().hurt(damage)

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        super().update(delta_time, wall_group, screen, projectiles, player)

        if not self.saw_player: return

        self.shoot_cd -= delta_time
        if self.ammo <= 0:
            if self.shoot_cd <= 0:
                self.reload()
        else:
            self.shoot_cd -= delta_time
            if self.shoot_cd <= 0:
                self.shoot(screen, projectiles, player.rect.centerx, player.rect.centery)
                if self.ammo == 0:
                    self.shoot_cd = random.choice([2.2 + x * 0.2 for x in range(0, 8)])

        step_x = self.vel_x
        step_y = self.vel_y

        self.move_cd -= delta_time
        if self.move_cd <= 0:
            if self.vel_x != 0 or self.vel_y != 0:
                self.vel_y = 0
                self.vel_x = 0
                self.move_cd = 3
            else:
                self.vel_x = random.choice((-4, 0, 4))
                self.vel_y = random.choice((-4, 0, 4))
                self.move_cd = random.choice((0.8, 1, 1.2, 1.5, 1.7))

        if self.vel_x == 0 and self.vel_y == 0: return

        apply_x = True
        next_rect_h = self.rect.move(step_x, 0)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_h.colliderect(wall.rect):
                apply_x = False
                break

        apply_y = True
        next_rect_v = self.rect.move(0, step_y)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_v.colliderect(wall.rect):
                apply_y = False
                break

        self.rect = self.rect.move(step_x if apply_x else 0, step_y if apply_y else 0)


class ShotgunEnemy(Enemy):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(pos_x, pos_y, particle_group, "shotgun_enemy.png",
                         "shotgun_enemy_dead.png", *groups)

        self.health = 50
        self.speed = 3

        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

        self.s_shoot = pygame.mixer.Sound(load_sound("shotgun_shot.wav"))

    def shoot(self, screen, projectiles, player_pos_x, player_pos_y):
        super().shoot(screen, projectiles, player_pos_x, player_pos_y)

        for i in range(5):
            projectiles.append(Projectile(screen, self.rect.centerx, self.rect.centery,
                                          player_pos_x, player_pos_y,
                                          25, 1, 3, "bullet", additional_angle=(i - 2) * 5))
        self.shoot_cd = 1.6
        self.s_shoot.play()

    def hurt(self, damage):
        return super().hurt(damage)

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        super().update(delta_time, wall_group, screen, projectiles, player)

        if not self.saw_player: return

        self.shoot_cd -= delta_time
        if self.shoot_cd <= 0:
            self.shoot(screen, projectiles, player.rect.centerx, player.rect.centery)

        step_x = self.vel_x
        step_y = self.vel_y

        self.move_cd -= delta_time
        if self.move_cd <= 0:
            if self.vel_x != 0 or self.vel_y != 0:
                self.vel_y = 0
                self.vel_x = 0
                self.move_cd = 2
            else:
                self.vel_x = random.choice((-self.speed, 0, self.speed))
                self.vel_y = random.choice((-self.speed, 0, self.speed))
                self.move_cd = random.choice((1, 1.2, 1.5, 2))

        if self.vel_x == 0 and self.vel_y == 0: return

        apply_x = True
        next_rect_h = self.rect.move(step_x, 0)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_h.colliderect(wall.rect):
                apply_x = False
                break

        apply_y = True
        next_rect_v = self.rect.move(0, step_y)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_v.colliderect(wall.rect):
                apply_y = False
                break

        self.rect = self.rect.move(step_x if apply_x else 0, step_y if apply_y else 0)


class MinigunEnemy(Enemy):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(pos_x, pos_y, particle_group, PLAYER_IMAGE, "button.png", *groups)

        self.ammo = 0
        self.health = 100
        self.speed = 1

        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

        self.s_shoot = pygame.mixer.Sound(load_sound("minigun_loop.wav"))

    def shoot(self, screen, projectiles, player_pos_x, player_pos_y):
        if self.is_dead:
            return

        projectiles.append(Projectile(screen, self.rect.centerx, self.rect.centery,
                                      player_pos_x, player_pos_y,
                                      25, 1, 3, "bullet",
                                      additional_angle=random.choice([x for x in range(-5, 5)])))
        self.shoot_cd = 0.15
        self.ammo -= 1

    def reload(self):
        self.ammo = 50
        self.s_shoot.play()

    def hurt(self, damage):
        return super().hurt(damage)

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        super().update(delta_time, wall_group, screen, projectiles, player)

        if not self.saw_player:
            self.s_shoot.stop()
            return

        self.shoot_cd -= delta_time
        if self.ammo <= 0:
            if self.shoot_cd <= 0:
                self.reload()
        else:
            self.shoot_cd -= delta_time
            if self.shoot_cd <= 0:
                self.shoot(screen, projectiles, player.rect.centerx, player.rect.centery)
                if self.ammo == 0:
                    self.shoot_cd = 7

        step_x = self.vel_x
        step_y = self.vel_y

        self.move_cd -= delta_time
        if self.move_cd <= 0:
            self.vel_x = random.choice((-self.speed, self.speed))
            self.vel_y = random.choice((-self.speed, self.speed))
            self.move_cd = random.choice((0.8, 1, 1.2, 1.5, 1.7))

        if self.vel_x == 0 and self.vel_y == 0: return

        apply_x = True
        next_rect_h = self.rect.move(step_x, 0)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_h.colliderect(wall.rect):
                apply_x = False
                break

        apply_y = True
        next_rect_v = self.rect.move(0, step_y)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_v.colliderect(wall.rect):
                apply_y = False
                break

        self.rect = self.rect.move(step_x if apply_x else 0, step_y if apply_y else 0)


class Box(Enemy):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(pos_x, pos_y, particle_group, "box.png", "grass.png", *groups)
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        # шаг определяем как размер клетки
        self.health = 1

        self.player = None
        self.pickups = None
        self.screen = None
        self.wall_group = groups[1]

        self.dollars = 4

        self.s_damage = "box"

    def hurt(self, damage):
        if self.is_dead: return

        self.health -= 1
        self.image = self.dead_image
        self.is_dead = True
        self.kill()

        if random.randint(0, 2) == 1:
            self.pickups.append(Pickup(self.screen, self.rect.centerx, self.rect.centery,
                                       random.randint(0, 360), "heart.png"))

        for i in range(random.randint(2, 5)):
            self.pickups.append(Pickup(self.screen, self.rect.centerx, self.rect.centery,
                                       random.randint(0, 360), "ammo.png"))

        create_particles((self.rect.centerx, self.rect.centery), "box_chip.png", 20, *self.p_groups)

        return self.s_damage

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        if not self.is_dead:
            self.player = player
            self.pickups = kwargs['pickups']
            self.screen = screen


class Cactus(Enemy):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(pos_x, pos_y, particle_group, "cactus.png", "grass.png", *groups)
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        # шаг определяем как размер клетки
        self.health = 1

        self.player = None
        self.proj = None
        self.screen = None
        self.wall_group = groups[1]

        self.dollars = 0

        self.s_damage = "cactus"

    def hurt(self, damage):
        if self.is_dead: return

        self.health -= 1
        self.image = self.dead_image
        self.is_dead = True
        self.kill()

        for i in range(12):
            self.proj.append(
                Projectile(self.screen, self.rect.centerx, self.rect.centery,
                           self.rect.centerx + 10, self.rect.centery,
                           25, 30, 3, "spike", player_friendly=True, additional_angle=i * 30))

        create_particles((self.rect.centerx, self.rect.centery), "cactus_chip.png", 30, *self.p_groups)

        return self.s_damage

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        if not self.is_dead:
            self.player = player
            self.proj = projectiles
            self.screen = screen


class Plank(Enemy):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(pos_x, pos_y, particle_group, "plank.png", "grass.png", *groups)
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        # шаг определяем как размер клетки
        self.health = 1

        self.player = None
        self.screen = None
        self.wall_group = groups[1]

        self.dollars = 1

        self.s_damage = "plank"

    def hurt(self, damage):
        if self.is_dead: return

        self.health -= 1
        self.image = self.dead_image
        self.is_dead = True
        self.kill()

        create_particles((self.rect.centerx, self.rect.centery), "chip.png", 20, *self.p_groups)

        return self.s_damage

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        if not self.is_dead:
            self.player = player
            self.screen = screen
