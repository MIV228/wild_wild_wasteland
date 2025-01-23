import pygame

from constants import TILE_WIDTH, TILE_HEIGHT, TILE_IMAGES
from extensions import load_image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, *groups):
        super().__init__(*groups)
        self.image = load_image(TILE_IMAGES[tile_type])
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)