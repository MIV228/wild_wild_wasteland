import pygame
import math
from constants import PROJECTILE_IMAGES
from extensions import load_image


class Projectile:
    def __init__(self, screen, x, y, mouse_x, mouse_y, speed, damage, lifetime, p_type):
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        print(self.angle)
        self.image = load_image(PROJECTILE_IMAGES[p_type])
        self.rect = self.image.get_rect().move(x, y)
        self.image = pygame.transform.rotate(self.image, 30)
        self.damage = damage
        self.lifetime = lifetime
        self.x = x
        self.y = y
        self.speed = speed
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.screen = screen
        self.x -= self.vel_x * 2
        self.y -= self.vel_y * 2

    def update(self):
        self.x -= self.vel_x
        self.y -= self.vel_y

        #self.rect.move(int(self.x), int(self.y))
        self.screen.blit(self.image, (int(self.x), int(self.y)))