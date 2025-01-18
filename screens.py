import pygame
from pygame import Surface

from extensions import load_image
from resources.button import Button


def start_screen(screen: Surface, button_group) -> None:
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    #fon = pygame.transform.scale(load_image('fon.jpg'), (screen.get_width(), screen.get_height()))
    #screen.blit(fon, (0, 0))
    #font = pygame.font.Font(None, 50)
    #text_coord = 50
    #for line in intro_text:
    #    string_rendered = font.render(line, 1, pygame.Color('black'))
    #    intro_rect = string_rendered.get_rect()
    #    text_coord += 10
    #    intro_rect.top = text_coord
    #    intro_rect.x = 10
    #    text_coord += intro_rect.height
    #    screen.blit(string_rendered, intro_rect)
    b_start_game = Button(30, 200, 300, 80, "start game", 2, 2)
    b_quit = Button(30, 290, 300, 80, "quit", 1)

    b_level1 = Button(30, 200, 300, 80, "grand canyon", 0, 0)
    b_level2 = Button(30, 290, 300, 80, "salt marshes", 0, 1)
    b_level_back = Button(30, 470, 300, 80, "back", 2, 1)

    button_group.append([b_start_game, b_quit])
    button_group.append([b_level1, b_level2, b_level_back])