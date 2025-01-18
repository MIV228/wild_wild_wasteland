import pygame

from constants import PLAYER_IMAGE, TILE_WIDTH, TILE_HEIGHT
from extensions import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = load_image(PLAYER_IMAGE)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)
        # шаг определяем как размер клетки
        self.speed = 5
        self.spin_seconds = 0

        # изначальное направление игрока (влево)
        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

    def update(self, keys, mousebuttons, delta_time, wall_group) -> None:
        # нужны для определения будущей позиции игрока
        if 0 <= self.spin_seconds < 1:
            self.speed = 5
        elif 1 <= self.spin_seconds < 2:
            self.speed = 6
        elif 2 <= self.spin_seconds < 3:
            self.speed = 7
        elif 3 <= self.spin_seconds < 5:
            self.speed = 8
        else:
            self.speed = 10

        if mousebuttons[0]:
            self.spin_seconds += delta_time
        else:
            if self.spin_seconds != 0:
                self.spin_seconds = 0
                pass

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