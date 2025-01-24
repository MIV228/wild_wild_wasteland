import pygame
import math
from constants import PROJECTILE_IMAGES
from extensions import load_image


class Projectile:
    def __init__(self, screen, x, y, mouse_x, mouse_y, speed, damage, lifetime, p_type,
                 player_friendly=False, piercing=False, passes_environment=False, additional_angle=0):
        self.angle = math.atan2(y - mouse_y, x - mouse_x) + (additional_angle / 50)
        self.image = load_image(PROJECTILE_IMAGES[p_type])
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image = pygame.transform.rotate(self.image, self.angle * 1.275 * -45)
        self.rect = self.image.get_rect().move(x, y)
        self.damage = damage
        self.lifetime = lifetime
        self.x = x
        self.y = y
        self.speed = speed
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.screen = screen
        self.x -= math.cos(self.angle) * self.rect.width
        self.y -= math.sin(self.angle) * self.rect.width
        self.player_friendly = player_friendly
        self.piercing = piercing
        self.passes_env = passes_environment

    def update(self):
        self.x -= self.vel_x
        self.y -= self.vel_y

        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, (int(self.x), int(self.y)))