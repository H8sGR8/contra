import pygame


class Button:
    def __init__(self, screen_size, message, font, position):
        self.font = font
        self.message = message
        self.screen_size = screen_size
        self.text = self.font.render(message, False, (50, 50, 50))
        self.text = pygame.transform.scale(self.text, (self.screen_size[0] / 7, self.screen_size[1] / 10))
        self.text_rect = self.text.get_rect(center=(position[0], position[1]))
        self.but = pygame.surface.Surface((self.text_rect[2]*1.2, self.text_rect[3]*1.2))
        self.but_rect = self.but.get_rect(center=(position[0], position[1]))

    def hovered(self):
        """"
        changing color while hovered and not hovered
        """
        if self.but_rect.collidepoint(pygame.mouse.get_pos()):
            self.but.fill((50, 50, 50))
            self.text = self.font.render(self.message, False, (25, 25, 25))
            self.text = pygame.transform.scale(self.text, (self.screen_size[0] / 7, self.screen_size[1] / 10))
        else:
            self.but.fill((100, 100, 100))
            self.text = self.font.render(self.message, False, (50, 50, 50))
            self.text = pygame.transform.scale(self.text, (self.screen_size[0] / 7, self.screen_size[1] / 10))

    def clicked(self):
        """"
        checking if clicked
        """
        if self.but_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed() == (True, False, False):
            return True
        return False
