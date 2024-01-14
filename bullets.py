import pygame
import math
import keys


class Bullet(pygame.sprite.Sprite):

    def __init__(self, screen_size, hero_position, from_position, to_position, color, speed):
        pygame.sprite.Sprite.__init__(self)
        self.screen_size = screen_size
        self.hero_position = hero_position
        self.to_x = to_position[0]
        self.to_y = to_position[1]
        self.from_x = from_position[0]
        self.from_y = from_position[1]
        self.from_width = from_position[2]
        self.from_height = from_position[3]
        self.velocity = self.screen_size[0]/70
        self.image = pygame.Surface((self.screen_size[0]/100, self.screen_size[0]/100))
        self.color = color
        self.speed = speed
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(self.from_x + self.from_width/2, self.from_y + self.from_height/2))

    def update(self):
        """
        setting x and y velocity
        moving while a or d key pressed
        """
        a = self.from_x + self.from_width/2 - self.to_x
        b = self.from_y + self.from_height/2 - self.to_y
        c = math.sqrt(a**2 + b**2)
        self.rect.x -= a / c * self.velocity
        self.rect.y -= b / c * self.velocity
        if (keys.pressed_keys()[pygame.K_a] and self.hero_position[0]
                <= round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_d]):
            self.rect.x += self.screen_size[0]/self.speed
        if (keys.pressed_keys()[pygame.K_d] and self.hero_position[0] + self.hero_position[2] >= self.screen_size[0] -
                round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_a]):
            self.rect.x -= self.screen_size[0]/self.speed
        if (self.rect.bottom < 0 or self.rect.right < 0 or
                self.rect.top > self.screen_size[1] or self.rect.left > self.screen_size[0]):
            self.kill()
