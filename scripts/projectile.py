import pygame
import math
from constants import PROJECTILE_IMAGES, WIDTH, HEIGHT
from extensions import load_image, AnimatedSprite


class Projectile:
    def __init__(self, screen, x, y, mouse_x, mouse_y, speed, damage, lifetime, p_type, anim_frames=1,
                 player_friendly=False, piercing=False, passes_environment=False, additional_angle=0, dont_rotate=False):
        self.angle = math.atan2(y - mouse_y, x - mouse_x) + (additional_angle / 50)
        self.anim_sprite = AnimatedSprite(load_image(PROJECTILE_IMAGES[p_type]), anim_frames, 1, x, y)
        self.anim_sprite.scale(4)
        if not dont_rotate:
            self.anim_sprite.rotate(self.angle)
        self.anim_sprite.update()
        self.image = self.anim_sprite.image
        self.damage = damage
        self.lifetime = lifetime
        self.x = x - (self.image.get_width() // 2)
        self.y = y - (self.image.get_height() // 2)
        self.rect = self.image.get_rect().move(x, y)
        self.speed = speed
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.screen = screen
        self.x -= math.cos(self.angle) * self.rect.width / 2
        self.y -= math.sin(self.angle) * self.rect.width / 2
        self.player_friendly = player_friendly
        self.piercing = piercing
        self.passes_env = passes_environment

    def update(self):
        self.anim_sprite.update()
        self.image = self.anim_sprite.image

        self.x -= self.vel_x
        self.y -= self.vel_y

        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, (int(self.x), int(self.y)))
