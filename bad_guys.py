import pygame
import keys
import bullets


class BadGuy:

    def __init__(self, screen_size, hero_position, position):
        self.position = position
        self.screen_size = screen_size
        self.hero_position = hero_position
        self.enemy = pygame.Surface((self.screen_size[0]/18, self.screen_size[1]/9))
        self.enemy.fill('Red')
        self.bullet = 0
        self.enemy_hit_box = self.enemy.get_rect(center=(self.position[0], self.position[1]))

    def surf(self):
        return self.enemy

    def hit_box(self):
        return self.enemy_hit_box

    def move(self):
        if (keys.pressed_keys()[pygame.K_a] and self.hero_position[0] -
                self.hero_position[2]/2 <= round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_d]):
            self.enemy_hit_box.x += self.screen_size[0]/200
        if (keys.pressed_keys()[pygame.K_d] and self.hero_position[0] + self.hero_position[2] >= self.screen_size[0] -
                round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_a]):
            self.enemy_hit_box.x -= self.screen_size[0]/200
        return self.enemy_hit_box

    def shoot(self):
        self.bullet = bullets.Bullet(self.screen_size, self.enemy_hit_box, self.hero_position, 'Red')
        return self.bullet

    def __del__(self):
        pass
