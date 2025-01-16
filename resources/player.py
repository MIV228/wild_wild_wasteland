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
        self.speed = 3

        # изначальное направление игрока (влево)
        self.image_left = self.image
        self.image_right = pygame.transform.flip(self.image, True, False)

    def update(self, keys, wall_group) -> None:
        # нужны для определения будущей позиции игрока
        step_x = 0
        step_y = 0
        if keys[pygame.K_LEFT]:
            step_x -= self.speed
            self.image = self.image_left
        elif keys[pygame.K_RIGHT]:
            step_x += self.speed
            self.image = self.image_right
        if keys[pygame.K_UP]:
            step_y -= self.speed
        elif keys[pygame.K_DOWN]:
            step_y += self.speed

        # будущая позиция игрока
        next_rect = self.rect.move(step_x, step_y)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect.colliderect(wall.rect):
                return

        self.rect = next_rect