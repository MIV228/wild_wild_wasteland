import pygame

from constants import TILE_WIDTH, TILE_HEIGHT
from extensions import load_image, AnimatedSprite
from resources.projectile import Projectile
from resources.particles import create_particles


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, particle_group, *groups):
        super().__init__(*groups)

        # анимации
        self.a_idle = AnimatedSprite(load_image("player_idle.png"), 5, 1, pos_x, pos_y, groups[-1])
        self.a_idle_spin = AnimatedSprite(load_image("player_idle_spin.png"), 5, 1, pos_x, pos_y, groups[-1])
        self.a_run = AnimatedSprite(load_image("player_run.png"), 4, 1, pos_x, pos_y, groups[-1])

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

        self.p_groups = [particle_group, groups[-1]]

        self.shoot_cd = 0

    def shoot(self, screen, projectiles):
        if self.ammo <= 0: return
        self.ammo -= 1

        if self.spin_seconds == 0:
            return
        if 0 < self.spin_seconds < 0.16:
            bullet = Projectile(screen, self.rect.centerx, self.rect.centery,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                15, 5, 0.8, "steel_ball", True)
        elif 0.16 <= self.spin_seconds < 0.33:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 10, 0.9, "steel_ball", True)
        elif 0.33 <= self.spin_seconds < 0.5:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 10, 1, "steel_ball", True)

        elif 0.5 <= self.spin_seconds < 0.8:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 20, 2, "steel_ball", True)
        elif 0.8 <= self.spin_seconds < 1.2:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                23, 25, 2, "steel_ball", True)
        elif 1.2 <= self.spin_seconds < 1.5:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                25, 30, 2, "steel_ball", True)

        elif 1.5 <= self.spin_seconds < 2.4:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                35, 30, 1, "steel_ball", True, True)
        elif 2.4 <= self.spin_seconds < 3.3:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                45, 40, 1, "steel_ball", True, True)
        elif 3.3 <= self.spin_seconds < 3.5:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                60, 100, 0.8, "steel_ball", True, True, True)

        elif 3.5 <= self.spin_seconds < 5.33:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                45, 50, 1, "steel_ball", True, True)
        elif 5.33 <= self.spin_seconds < 6.66:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                40, 60, 1, "steel_ball", True, True)
        elif 6.66 <= self.spin_seconds < 8:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                35, 70, 1, "steel_ball", True, True)

        elif 8 <= self.spin_seconds < 10:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                30, 75, 2, "tornado", True, True, True)
        elif 10 <= self.spin_seconds < 12:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                20, 80, 3, "tornado", True, True, True)
        elif 12 <= self.spin_seconds < 14:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                10, 85, 4, "tornado", True, True, True)
        else:
            bullet = Projectile(screen, self.rect.x - 10, self.rect.y,
                                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                5, 90, 8, "tornado", True, True, True)
        projectiles.append(bullet)
        self.spin_seconds = 0

    def shotgun(self, screen, projectiles):
        self.ammo -= 10

        for i in range(5):
            projectiles.append(Projectile(screen, self.rect.x - 10, self.rect.y,
                                          pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
                                          40, 15, 1, "bullet", additional_angle=(i - 2) * 3,
                                          player_friendly=True))
        self.shoot_cd = 1

    def hurt(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.image = pygame.transform.scale_by(load_image("box.png"), 4)

        create_particles((self.rect.centerx, self.rect.centery), "blood.png", 30, *self.p_groups)

    def change_animation(self, anim):
        self.curr_anim.reset()
        self.curr_anim = anim

    def update(self, keys, mousebuttons, delta_time, wall_group,
               screen:pygame.Surface, projectiles) -> None:
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
                if self.ammo >= 10 and self.shoot_cd <= 0:
                    self.shotgun(screen, projectiles)
        else:
            self.ammo_refill_cd -= delta_time
            if self.ammo_refill_cd <= 0:
                self.ammo += 1
                self.ammo_refill_cd = 5
            self.speed = 5

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
            self.spin_seconds += delta_time
            if self.spin_seconds > 14:
                self.shoot(screen, projectiles)
            self.change_animation(self.a_idle_spin)
        else:
            if self.spin_seconds != 0:
                self.shoot(screen, projectiles)
            self.change_animation(self.a_idle)

        if apply_x or apply_y:  # пошел
            if not self.moved_last_update:
                self.change_animation(self.a_run)
        else:
            if self.moved_last_update:
                self.change_animation(self.a_idle)

        self.moved_last_update = apply_x or apply_y