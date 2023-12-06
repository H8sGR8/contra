import pygame
import keys
from random import randint


class Background:

    def __init__(self, screen_size, hero_position, element_position, size, speed, image):
        self.hero_position = hero_position
        self.screen_size = screen_size
        self.speed = speed
        self.ground = 0
        self.size = size
        self.element = pygame.image.load(image)
        self.element = pygame.transform.scale(self.element, (self.size[0], self.size[1]))
        if image == 'graphics/ground.png':
            self.ground = 1
        self.element_hit_box = self.element.get_rect(center=(element_position[0], element_position[1]))

    def surf(self):
        return self.element

    def hit_box(self):
        return self.element_hit_box

    def move(self):
        if (keys.pressed_keys()[pygame.K_a] and self.hero_position[0] -
                self.hero_position[2]/2 <= round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_d]):
            self.element_hit_box.x += self.screen_size[0]/self.speed
        if (keys.pressed_keys()[pygame.K_d] and self.hero_position[0] + self.hero_position[2] >= self.screen_size[0] -
                round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_a]):
            self.element_hit_box.x -= self.screen_size[0]/self.speed
        if self.element_hit_box.left >= self.screen_size[0]*2:
            self.element_hit_box.x = -self.screen_size[0]*2
            if self.ground == 1:
                self.element_hit_box.y += randint(-round(self.screen_size[1]/24), round(self.screen_size[1]/24))
        if self.element_hit_box.right <= -self.screen_size[0]:
            self.element_hit_box.x = self.screen_size[0]
            if self.ground == 1:
                self.element_hit_box.y = randint(round(self.screen_size[1]*19/24),
                                                 round(self.screen_size[1]*23/24)) - self.size[1]/2
        return self.element_hit_box
