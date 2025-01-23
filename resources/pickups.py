import pygame
import math
from constants import PROJECTILE_IMAGES
from extensions import load_image


class Pickup:
    def __init__(self, screen, x, y, angle, image):
        self.angle = angle
        self.image = load_image(image)
        self.image = pygame.transform.scale_by(self.image, 2)
        self.image = pygame.transform.rotate(self.image, self.angle * 1.275 * -45)
        self.rect = self.image.get_rect().move(x, y)
        self.x = x
        self.y = y
        self.speed = 20
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.screen = screen
        self.going_towards_player = False
        self.p_type = image

    def update(self, player_x, player_y):
        if self.going_towards_player:
            if self.speed < 20: self.speed += 1
            self.angle = math.atan2(self.y - player_y, self.x - player_x)
            self.vel_x = math.cos(self.angle) * self.speed
            self.vel_y = math.sin(self.angle) * self.speed
            #self.image = pygame.transform.rotate(self.image, self.angle * 1.275 * -45)
        else:
            self.speed -= 1
            if self.speed <= 0:
                self.speed = 0
                self.going_towards_player = True

        self.x -= self.vel_x
        self.y -= self.vel_y

        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, (int(self.x), int(self.y)))