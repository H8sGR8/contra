import pygame
import keys
import bullets


class BadGuy(pygame.sprite.Sprite):

    def __init__(self, screen_size, size, hero_position, position, speed):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.screen_size = screen_size
        self.hero_position = hero_position
        self.image = pygame.image.load('graphics/enemy.png')
        self.image = pygame.transform.scale(self.image, size)
        self.speed = speed
        self.bullet = None
        self.rotate = 0
        self.hp = 3
        self.gun_reload = 2
        self.rect = self.image.get_rect(center=(self.position[0], self.position[1]))

    def shoot(self):
        """
        create a bullet which will be shot by enemy
        :return:
        """
        self.bullet = (
            bullets.Bullet(self.screen_size, self.hero_position, self.rect,
                           (self.hero_position[0] - self.hero_position[2]/2,
                            self.hero_position[1] + self.hero_position[3]/2), 'Red', self.speed))
        self.gun_reload = 100
        return self.bullet

    def update(self, g1, g2):
        """"
        movement of enemies while a or d keys pressed
        rotating enemies to face a player
        reloading of a gun
        gravity for enemies
        """
        if (keys.pressed_keys()[pygame.K_a] and self.hero_position[0]
                <= round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_d]):
            self.rect.x += self.screen_size[0]/self.speed
        if (keys.pressed_keys()[pygame.K_d] and self.hero_position[0] + self.hero_position[2] >= self.screen_size[0] -
                round(self.screen_size[0]/3) and not keys.pressed_keys()[pygame.K_a]):
            self.rect.x -= self.screen_size[0]/self.speed
        if self.hero_position[0] < self.rect.x and self.rotate == 0:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate = 1
        if self.hero_position[0] > self.rect.x and self.rotate == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rotate = 0
        if self.screen_size[0] * 1.2 < self.rect.x < -self.screen_size[0]*0.2:
            self.rect.bottom = self.screen_size[1]*0.57
        if self.screen_size[0]*1.2 > self.rect.x > -self.screen_size[0]*0.2:
            if self.gun_reload > 0:
                self.gun_reload -= 2
            if not self.rect.colliderect(g1) and not self.rect.colliderect(g2):
                self.rect.y += self.screen_size[1] / 150
