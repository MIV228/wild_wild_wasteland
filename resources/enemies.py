import random

import pygame

from constants import PLAYER_IMAGE, TILE_WIDTH, TILE_HEIGHT
from extensions import load_image
from resources.projectile import Projectile
from resources.pickups import Pickup


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image, dead_image, *groups):
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

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        if self.is_dead: return

        if not self.saw_player:
            if screen.get_rect().colliderect(self.rect):
                self.saw_player = True
            else:
                return


class GunEnemy(Enemy):
    def __init__(self, pos_x, pos_y, *groups):
        super().__init__(pos_x, pos_y, PLAYER_IMAGE, "button.png", *groups)

        self.ammo = 6

        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

    def shoot(self, screen, projectiles, player_pos_x, player_pos_y):
        super().shoot(screen, projectiles, player_pos_x, player_pos_y)

        bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                            player_pos_x, player_pos_y,
                            25, 1, 3, "bullet")
        projectiles.append(bullet)
        self.ammo -= 1

    def reload(self):
        self.ammo = 6

    def hurt(self, damage):
        super().hurt(damage)

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
                    self.shoot_cd = 3

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
    def __init__(self, pos_x, pos_y, *groups):
        super().__init__(pos_x, pos_y, "player_idle.png", "button.png", *groups)

        self.health = 50
        self.speed = 3

        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

    def shoot(self, screen, projectiles, player_pos_x, player_pos_y):
        super().shoot(screen, projectiles, player_pos_x, player_pos_y)

        for i in range(5):
            projectiles.append(Projectile(screen, self.rect.x - 10, self.rect.y,
                                          player_pos_x, player_pos_y,
                                          25, 1, 3, "bullet", additional_angle=(i - 2) * 2))
        self.shoot_cd = 2

    def hurt(self, damage):
        super().hurt(damage)

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
                self.vel_x = random.choice((-4, 0, 4))
                self.vel_y = random.choice((-4, 0, 4))
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


class Box(Enemy):
    def __init__(self, pos_x, pos_y, *groups):
        super().__init__(pos_x, pos_y, "box.png", "grass.png", *groups)
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        # шаг определяем как размер клетки
        self.health = 1

        self.player = None
        self.pickups = None
        self.screen = None
        self.wall_group = groups[1]

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

    def update(self, delta_time, wall_group, screen: pygame.Surface, projectiles, player, **kwargs) -> None:
        if not self.is_dead:
            self.player = player
            self.pickups = kwargs['pickups']
            self.screen = screen
