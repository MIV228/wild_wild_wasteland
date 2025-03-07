import os
import sys

import pygame
from pygame import Surface


def load_sound(name) -> str:
    fullname = os.path.join('audio', name)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл со звуком '{fullname}' не найден")
        sys.exit()

    return fullname

def load_image(name, scale_x=0, scale_y=0, color_key=None) -> Surface:
    fullname = os.path.join('data', name)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if scale_x != 0:
        image = pygame.transform.scale(image, (scale_x, scale_y))

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


def load_level(filename):
    filename = "maps/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '#'), level_map))


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, *groups):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.cd_update = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self) -> bool:
        self.cd_update += 1
        if self.cd_update >= 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.cd_update = 0
            return True
        return False

    def scale(self, scale):
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale_by(self.frames[i], scale)
        self.image = self.frames[self.cur_frame]

    def rotate(self, angle):
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.rotate(self.frames[i], angle * 1.275 * -45)
        self.image = self.frames[self.cur_frame]

    def reset(self):
        self.cd_update = 0
        self.cur_frame = 0


def get_sheet_image(x, y, width, height, sprite_sheet, color_key=None):
    image = pygame.Surface.subsurface(sprite_sheet, (x, y, width, height))
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image
