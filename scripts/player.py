import random

import pygame

from constants import TILE_WIDTH, TILE_HEIGHT
from extensions import load_image, AnimatedSprite, load_sound
from scripts.projectile import Projectile
from scripts.particles import create_particles


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(*groups)

        # анимации
        self.a_idle = AnimatedSprite(load_image("player_idle.png"), 5, 1, pos_x, pos_y, groups[-1])
        self.a_idle_spin = AnimatedSprite(load_image("player_idle_spin.png"), 5, 1, pos_x, pos_y, groups[-1])
        self.a_run = AnimatedSprite(load_image("player_run.png"), 2, 1, pos_x, pos_y, groups[-1])
        self.a_run_spin = AnimatedSprite(load_image("player_run_spin.png"), 2, 1, pos_x, pos_y, groups[-1])

        self.curr_anim = self.a_idle
        self.image = self.curr_anim.image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)

        # шаг определяем как размер клетки
        self.speed = 5
        self.spin_seconds = 0
        self.max_health = 5
        self.health = 5
        self.dead_timer = 2
        self.ammo = 20
        self.ammo_refill_cd = 5

        self.facing_right = True
        self.moved_last_update = False
        self.spin_last_update = False

        self.p_groups = [particle_group, groups[-1]]

        self.shoot_cd = 0

        self.s_shotgun = pygame.mixer.Sound(load_sound("shotgun_shot.wav"))

        self.curr_weapon = "shotgun"
        self.ammo_requirement = 10

    def shoot(self, screen, projectiles):
        if self.ammo <= 0: return
        self.ammo -= 1

        if self.spin_seconds == 0:
            return
        if 0 < self.spin_seconds < 0.16:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                15, 5, 0.8, "steel_ball", 2, True)
        elif 0.16 <= self.spin_seconds < 0.33:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 10, 0.9, "steel_ball", 2, True)
        elif 0.33 <= self.spin_seconds < 0.5:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 10, 1, "steel_ball", 2, True)

        elif 0.5 <= self.spin_seconds < 0.8:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 20, 2, "spin_ball", 3, True)
        elif 0.8 <= self.spin_seconds < 1.2:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                23, 25, 2, "spin_ball", 3, True)
        elif 1.2 <= self.spin_seconds < 1.5:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                25, 30, 2, "spin_ball", 3, True)

        elif 1.5 <= self.spin_seconds < 2.4:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                35, 30, 1, "spin_ball", 3, True, True)
        elif 2.4 <= self.spin_seconds < 3.3:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                45, 40, 1, "spin_ball", 3, True, True)
        elif 3.3 <= self.spin_seconds < 3.5:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                60, 100, 0.8, "spin_ball", 3, True, True, True)

        elif 3.5 <= self.spin_seconds < 5.33:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                45, 50, 1, "spin_ball", 3, True, True)
        elif 5.33 <= self.spin_seconds < 6.66:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                40, 60, 1, "spin_ball", 3, True, True)
        elif 6.66 <= self.spin_seconds < 8:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                35, 70, 1, "spin_ball", 3, True, True)

        elif 8 <= self.spin_seconds < 10:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                30, 75, 2, "tornado", 2, True, True, True, dont_rotate=True)
        elif 10 <= self.spin_seconds < 12:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                28, 80, 3, "tornado", 2, True, True, True, dont_rotate=True)
        elif 12 <= self.spin_seconds < 14:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                26, 85, 4, "tornado", 2, True, True, True, dont_rotate=True)
        else:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                25, 90, 8, "tornado", 2, True, True, True, dont_rotate=True)
        projectiles.append(bullet)
        self.spin_seconds = 0

        if self.moved_last_update:
            self.change_animation(self.a_run)
        else:
            self.change_animation(self.a_idle)

    def shotgun(self, screen, projectiles):
        if self.curr_weapon == "shotgun":
            self.ammo -= 10

            for i in range(5):
                projectiles.append(Projectile(screen, self.rect.centerx, self.rect.centery,
                                              pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                              40, 15, 1, "bullet", additional_angle=(i - 2) * 3,
                                              player_friendly=True))

            self.s_shotgun.play()
            self.shoot_cd = 0.5
        elif self.curr_weapon == "minigun":
            self.ammo -= 1

            projectiles.append(Projectile(screen, self.rect.centerx, self.rect.centery,
                                          pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                          50, 20, 1, "bullet",
                                          additional_angle=random.randint(-1, 1),
                                          player_friendly=True))

            self.s_shotgun.play()
            self.shoot_cd = 0.075

    def hurt(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.image = load_image("player_dead.png")

        create_particles((self.rect.centerx, self.rect.centery), "blood.png", 30, *self.p_groups)

    def change_animation(self, anim):
        self.curr_anim.reset()
        self.curr_anim = anim

    def update(self, keys, mousebuttons, delta_time, wall_group,
               screen: pygame.Surface, projectiles) -> None:
        if self.health <= 0:
            self.dead_timer -= delta_time
            return

        if self.shoot_cd > 0:
            self.shoot_cd -= delta_time

        if self.ammo > 0:
            self.ammo_refill_cd = 5
            # спин - вращение
            # 0-0.5 сек - первый уровень (белый), 0.5-1.5 - 2 голубой, 1.5-3.5 - 3 золотой,
            # 3.5-8 - 4 оранжевый, 8-14 - 5 красный
            if 0 <= self.spin_seconds < 0.5:
                self.speed = 5
            elif 0.5 <= self.spin_seconds < 1.5:
                self.speed = 6
            elif 1.5 <= self.spin_seconds < 3.5:
                self.speed = 7
            elif 3.5 <= self.spin_seconds < 8:
                self.speed = 8
            else:
                self.speed = 9

            if mousebuttons[2]:
                if self.ammo >= self.ammo_requirement and self.shoot_cd <= 0:
                    self.shotgun(screen, projectiles)
        else:
            self.ammo_refill_cd -= delta_time
            if self.ammo_refill_cd <= 0:
                self.ammo += 1
                self.ammo_refill_cd = 5
            self.speed = 5

        if self.health > 0:
            self.curr_anim.update()
            self.image = self.curr_anim.image

            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

        step_x = 0
        step_y = 0
        if keys[pygame.K_a]:
            step_x -= self.speed
            if self.facing_right:
                self.facing_right = not self.facing_right
        elif keys[pygame.K_d]:
            step_x += self.speed
            if not self.facing_right:
                self.facing_right = not self.facing_right
        if keys[pygame.K_w]:
            step_y -= self.speed
        elif keys[pygame.K_s]:
            step_y += self.speed

        # будущая позиция игрока
        apply_x = True
        next_rect_h = self.rect.move(step_x, 0)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_h.colliderect(wall.rect):
                apply_x = False
                break

        apply_y = True
        next_rect_v = self.rect.move(0, step_y)
        # перебираем все спрайты стен и проверяем, есть ли столкновение
        for wall in wall_group:
            if next_rect_v.colliderect(wall.rect):
                apply_y = False
                break

        self.rect = self.rect.move(step_x if apply_x else 0, step_y if apply_y else 0)
        for p in projectiles:
            if apply_x: p.x -= step_x
            if apply_y: p.y -= step_y

        if mousebuttons[0]:
            if not self.spin_last_update:
                if (apply_x and step_x != 0) or (apply_y and step_y != 0):
                    self.change_animation(self.a_run_spin)
                else:
                    self.change_animation(self.a_idle_spin)
            self.spin_seconds += delta_time
            if self.spin_seconds > 14:
                self.shoot(screen, projectiles)
        else:
            if self.spin_seconds != 0:
                self.shoot(screen, projectiles)

        if (apply_x and step_x != 0) or (apply_y and step_y != 0):  # пошел
            if not self.moved_last_update:
                if self.spin_seconds > 0:
                    self.change_animation(self.a_run_spin)
                else:
                    self.change_animation(self.a_run)
                self.moved_last_update = True
        else:
            if self.moved_last_update:
                if self.spin_seconds > 0:
                    self.change_animation(self.a_idle_spin)
                else:
                    self.change_animation(self.a_idle)
                self.moved_last_update = False

        self.moved_last_update = (apply_x and step_x != 0) or (apply_y and step_y != 0)
        self.spin_last_update = mousebuttons[0]
