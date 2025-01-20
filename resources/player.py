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

        # изначальное направление игрока (влево)
        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

    def shoot(self, screen, projectiles):

        if 0 <= self.spin_seconds < 0.5:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 20, 3, "bullet")
            bullet.speed = 10
            bullet.damage = 5
            bullet.lifetime = 1
        elif 0.5 <= self.spin_seconds < 2:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                            20, 20, 3, "bullet")
        elif 2 <= self.spin_seconds < 4:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 20, 3, "bullet")
            bullet.speed = 40
            bullet.damage = 40
            if 3.8 <= self.spin_seconds < 4:
                bullet.speed = 60
                bullet.damage = 100
        elif 4 <= self.spin_seconds < 8:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 20, 3, "bullet")
            bullet.speed = 30
            bullet.damage = 60
            bullet.lifetime = 5
        else:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 20, 3, "bullet")
            bullet.speed = 5
            bullet.damage = 80
            bullet.lifetime = 10
        projectiles.append(bullet)
        self.spin_seconds = 0

    def update(self, keys, mousebuttons, delta_time, wall_group, screen, projectiles) -> None:
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
                self.spin_seconds = 0
                self.shoot(screen, projectiles)

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
        next_rect = self.rect.move(step_x, step_y)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect.colliderect(wall.rect):
                return

        self.rect = next_rect