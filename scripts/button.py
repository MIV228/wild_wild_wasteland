import pygame
from pygame import Surface
from extensions import load_image


class Button:
    def __init__(self, pos_x, pos_y, text, function_type, par=0):
        self.image = load_image('button.png')
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.function_type = function_type
        self.text = text
        self.par = par

    def check_clicked(self, x, y) -> bool:
        return self.rect.collidepoint(x, y)