import pygame

from constants import PLAYER_IMAGE, TILE_WIDTH, TILE_HEIGHT
from extensions import load_image
from resources.projectile import Projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = load_image(PLAYER_IMAGE)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)
        # шаг определяем как размер клетки
        self.speed = 5
        self.spin_seconds = 0
        self.max_health = 5
        self.health = 5
        self.dead_timer = 2
        self.ammo = 20
        self.ammo_refill_cd = 5

        # изначальное направление игрока (влево)
        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

    def shoot(self, screen, projectiles):
        if self.ammo <= 0: return
        self.ammo -= 1

        if self.spin_seconds == 0:
            return
        if 0 < self.spin_seconds < 0.16:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                10, 1, 0.8, "steel_ball", True)
        elif 0.16 <= self.spin_seconds < 0.33:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                10, 3, 0.9, "steel_ball", True)
        elif 0.33 <= self.spin_seconds < 0.5:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                10, 5, 1, "steel_ball", True)

        elif 0.5 <= self.spin_seconds < 1:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                15, 15, 2, "steel_ball", True)
        elif 1 <= self.spin_seconds < 1.5:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 20, 2, "steel_ball", True)
        elif 1.5 <= self.spin_seconds < 2:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                25, 25, 2, "steel_ball", True)

        elif 2 <= self.spin_seconds < 2.9:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                35, 30, 1, "steel_ball", True)
        elif 2.9 <= self.spin_seconds < 3.8:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                45, 40, 1, "steel_ball", True)
        elif 3.8 <= self.spin_seconds < 4:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                60, 100, 1, "steel_ball", True, True)

        elif 4 <= self.spin_seconds < 5.33:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                45, 50, 1, "steel_ball", True, True)
        elif 5.33 <= self.spin_seconds < 6.66:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                40, 60, 1, "steel_ball", True, True)
        elif 6.66 <= self.spin_seconds < 8:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                35, 70, 1, "steel_ball", True, True)

        elif 8 <= self.spin_seconds < 10:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                30, 75, 5, "tornado", True, True)
        elif 10 <= self.spin_seconds < 12:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 80, 5, "tornado", True, True)
        elif 12 <= self.spin_seconds < 14:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                10, 85, 5, "tornado", True, True)
        else:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 90, 5, "tornado", True, True)
        projectiles.append(bullet)
        self.spin_seconds = 0

    def hurt(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.image = pygame.transform.scale_by(load_image("box.png"), 4)

    def update(self, keys, mousebuttons, delta_time, wall_group,
               screen:pygame.Surface, projectiles) -> None:
        if self.health <= 0:
            self.dead_timer -= delta_time
            return

        if self.ammo > 0:
            self.ammo_refill_cd = 5
            # спин - вращение
            # 0-0.5 сек - первый уровень (белый), 0.5-2 - 2 голубой, 2-4 - 3 золотой,
            # 4-8 - 4 оранжевый, 8-14 - 5 красный
            if 0 <= self.spin_seconds < 0.5:
                self.speed = 5
            elif 0.5 <= self.spin_seconds < 2:
                self.speed = 6
            elif 2 <= self.spin_seconds < 4:
                self.speed = 7
            elif 4 <= self.spin_seconds < 8:
                self.speed = 8
            else:
                self.speed = 7

            if mousebuttons[0]:
                self.spin_seconds += delta_time
                if self.spin_seconds > 14:
                    self.shoot(screen, projectiles)
            else:
                if self.spin_seconds != 0:
                    self.shoot(screen, projectiles)
        else:
            self.ammo_refill_cd -= delta_time
            if self.ammo_refill_cd <= 0:
                self.ammo += 1
                self.ammo_refill_cd = 5
            self.speed = 5

        step_x = 0
        step_y = 0
        if keys[pygame.K_a]:
            step_x -= self.speed
            self.image = self.image_left
        elif keys[pygame.K_d]:
            step_x += self.speed
            self.image = self.image_right
        if keys[pygame.K_w]:
            step_y -= self.speed
        elif keys[pygame.K_s]:
            step_y += self.speed

        # будущая позиция игрока
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
        for p in projectiles:
            if apply_x: p.x -= step_x
            if apply_y: p.y -= step_y