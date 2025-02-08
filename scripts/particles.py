import pygame
from constants import WIDTH, HEIGHT
from extensions import load_image
import random

screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, image, dx, dy, *groups):
        super().__init__(*groups)
        self.image = load_image(image)
        self.image = pygame.transform.scale_by(self.image, random.randint(3, 7))
        self.image = pygame.transform.rotate(self.image, random.randint(0, 359))
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, image, count, *groups):
    if not screen_rect.collidepoint(position):
        return
    numbers = range(-12, 12)
    for _ in range(count):
        Particle(position, image, random.choice(numbers), random.choice(numbers), *groups)