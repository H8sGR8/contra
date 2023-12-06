import pygame
import math


class Bullet:

    def __init__(self, screen_size, from_position, to_position, color):
        self.screen_size = screen_size
        self.to_x = to_position[0]
        self.to_y = to_position[1]
        self.from_x = from_position[0]
        self.from_y = from_position[1]
        self.from_width = from_position[2]
        self.from_height = from_position[3]
        self.speed = self.screen_size[0]/100
        self.bullet = pygame.Surface((self.screen_size[0]/100, self.screen_size[0]/100))
        self.color = color
        self.bullet.fill(self.color)
        self.bullet_hit_box = (
            self.bullet.get_rect(center=(self.from_x + self.from_width/2, self.from_y + self.from_height/2)))

    def surface(self):
        return self.bullet

    def hit_box(self):
        return self.bullet_hit_box

    def acolor(self):
        if self.color == 'Yellow':
            return 0
        return 1

    def shoot(self):
        a = self.from_x + self.from_width/2 - self.to_x
        b = self.from_y + self.from_height/2 - self.to_y
        c = math.sqrt(a**2 + b**2)
        self.bullet_hit_box.x -= a / c * self.speed
        self.bullet_hit_box.y -= b / c * self.speed
        return self.bullet_hit_box

    def __del__(self):
        pass
