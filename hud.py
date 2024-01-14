import pygame


class HUD(pygame.sprite.Sprite):
    def __init__(self, position, size, image):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.size = size
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(self.position[0], self.position[1]))


class Counter(HUD):
    def amount(self, numbers, font):
        """
        creating a counter of amount of resources
        """
        text = font.render('x ' + str(numbers[0]) + '/' + str(numbers[1]), False, 'Black')
        text = pygame.transform.scale(text, (self.size[0]*4, self.size[1]/2))
        text_hit_box = text.get_rect(center=(self.position[0]+200, self.position[1]))
        return text, text_hit_box
