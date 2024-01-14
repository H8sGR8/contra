import pygame
import keys


class Bonus(pygame.sprite.Sprite):
    def __init__(self, screen_size, hero_position, position, image, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (hero_position[2]/2, hero_position[3]/2))
        self.hero_position = hero_position
        self.screen_size = screen_size
        self.speed = speed
        self.rect = self.image.get_rect(center=(position[0]+position[2]/2, position[1]+position[3]*2/3))

    def update(self):
        """
        movement of bonuses while a or d key pressed
        destroying while out of screen
        """
        if (keys.pressed_keys()[pygame.K_a] and self.hero_position[0]
                <= round(self.screen_size[0] / 3) and not keys.pressed_keys()[pygame.K_d]):
            self.rect.x += self.screen_size[0] / self.speed
        if (keys.pressed_keys()[pygame.K_d] and self.hero_position[0] + self.hero_position[2] >= self.screen_size[0] -
                round(self.screen_size[0] / 3) and not keys.pressed_keys()[pygame.K_a]):
            self.rect.x -= self.screen_size[0] / self.speed
        if self.rect.right < 0 or self.rect.left > self.screen_size[0]:
            self.kill()
