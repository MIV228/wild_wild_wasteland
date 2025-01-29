import pygame

from constants import TILE_WIDTH, TILE_HEIGHT, WIDTH, HEIGHT
from extensions import load_image


class Sign(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, text, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale_by(load_image("sign.png"), 4)
        self.hint_bg = pygame.transform.scale_by(load_image("interface_bg.png"), 12)
        self.rect = self.image.get_rect().move(
            TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.hint_pos = (WIDTH // 2 - self.hint_bg.get_rect().w // 2, HEIGHT // 2 + 200)
        self.text = text
        self.font = pygame.font.Font("www_font.ttf", 60)

    def update(self, x, y, screen:pygame.Surface):
        if self.rect.x - 200 <= x <= self.rect.x + 300 and self.rect.y - 200 <= y <= self.rect.y + 300:
            screen.blit(self.hint_bg, self.hint_pos)
            text = self.font.render(self.text, 1, (40, 24, 7))
            text_rect = text.get_rect()
            text_rect.x = self.hint_pos[0] + self.hint_bg.get_rect().centerx - text_rect.w // 2
            text_rect.y = self.hint_pos[1] + self.hint_bg.get_rect().centery - text_rect.h // 2 + 5
            screen.blit(text, text_rect)