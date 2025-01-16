import pygame
from pygame import Surface


class Button:
    def __init__(self, pos_x, pos_y, scale_x, scale_y, text, function_type):
        self.rect = pygame.Rect(pos_x, pos_y, scale_x, scale_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.function_type = function_type
        self.text = text
        # шаг определяем как размер клетки

    def check_clicked(self, x, y) -> bool:
        if self.pos_x >= x >= self.pos_x + self.scale_x and self.pos_y >= y >= self.pos_y + self.scale_y:
            return True
        return False