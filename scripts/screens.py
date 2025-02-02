import pygame
from extensions import load_sound
from scripts.button import Button


def start_screen(button_group) -> None:
    pygame.mixer.music.load(load_sound('menu_music.wav'))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)

    b_start_game = Button(64, 360, "play", 2, 2)
    b_stats = Button(64, 450, "marauder's journal", 2, 3)
    b_quit = Button(64, 630, "quit", 1)

    b_level1 = Button(64, 360, "tutorial", 0, 0)
    b_level2 = Button(64, 450, "gunpowder canyon", 0, 1)
    #b_level3 = Button(64, 540, "metal marshes", 0, 2)
    b_level_back = Button(64, 630, "back", 2, 1)

    # сейв - файл:
    # 1) total kills
    # 2) property damage
    # 3) total strongholds
    # 4) total revenue
    # 5) current level
    f = open("data/savefile.txt", mode="r", encoding="utf-8")
    lines = f.read().split("\n")
    if len(lines) < 3:
        lines = ["0", "0", "0", "0", "0"]

    b_stat_dollars = Button(64, 360, f"mission revenue:  ${lines[3]}", -1)
    b_stat_kills = Button(64, 450, f"kills:  {lines[0]}", -1)
    b_stat_pd = Button(64, 540, f"property damage:  ${lines[1]}", -1)
    b_stat_sh = Button(64, 630, f"strongholds raided:  {lines[2]}", -1)
    b_stat_back = Button(64, 740, "back", 2, 1)

    if lines[4] == "0":
        button_group.append([b_start_game, Button(64, 450, "quit", 1)])
    else:
        button_group.append([b_start_game, b_stats, b_quit])
    button_group.append([b_level1, b_level2, b_level_back])
    button_group.append([b_stat_dollars, b_stat_kills, b_stat_pd, b_stat_sh, b_stat_back])

    f.close()
