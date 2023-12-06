import pygame
import keys


class Player:

    def __init__(self, size, position_y, screen_size):
        self.size = size
        self.screen_size = screen_size
        self.y_speed = 0
        self.jump = 0
        self.double_jump = 0
        self.position_x = screen_size[0]/2
        self.position_y = position_y
        self.player = pygame.Surface(self.size)
        self.player.fill('Yellow')
        self.player_hit_box = self.player.get_rect(center=(self.position_x, self.position_y))

    def surf(self):
        return self.player

    def hit_box(self):
        return self.player_hit_box

    def movement(self, g1, g2):
        if (keys.pressed_keys()[pygame.K_a] and self.player_hit_box.left > round(self.screen_size[0]/3) and
                not ((self.player_hit_box.left <= g2.left and self.player_hit_box.bottom - 10 >= g1.top) or
                     (self.player_hit_box.left <= g1.left and self.player_hit_box.bottom - 10 >= g2.top))):
            self.player_hit_box.x -= self.screen_size[0]/200
        if ((keys.pressed_keys()[pygame.K_d] and
                self.player_hit_box.right < self.screen_size[0] - round(self.screen_size[0]/3)) and
                not ((self.player_hit_box.right >= g2.right and self.player_hit_box.bottom - 10 >= g1.top) or
                     (self.player_hit_box.right >= g1.right and self.player_hit_box.bottom - 10 >= g2.top))):
            self.player_hit_box.x += self.screen_size[0]/200
        if not keys.pressed_keys()[pygame.K_SPACE] and self.jump < 2:
            self.jump += 1
            self.double_jump = 1
        if keys.pressed_keys()[pygame.K_SPACE] and self.double_jump == 1:
            self.double_jump = 0
            self.y_speed = -self.screen_size[1]/45
            self.player_hit_box.y += self.y_speed
        if ((self.player_hit_box.bottom >= g1.top and self.player_hit_box.left + 10 <= g1.right and
            self.player_hit_box.right - 10 >= g1.left) or
                (self.player_hit_box.bottom >= g2.top and self.player_hit_box.left + 10 <= g2.right and
                 self.player_hit_box.right - 10 >= g2.left)):
            self.jump = 0
            self.y_speed = 0
            if (self.player_hit_box.bottom >= g1.top and self.player_hit_box.left + 10 <= g1.right and
                    self.player_hit_box.right - 10 >= g1.left):
                self.player_hit_box.y = g1.top - self.size[1]
            if (self.player_hit_box.bottom >= g2.top and self.player_hit_box.left + 10 <= g2.right and
                    self.player_hit_box.right - 10 >= g2.left):
                self.player_hit_box.y = g2.top - self.size[1]
        return self.player_hit_box.x, self.player_hit_box.y, self.size[0], self.size[1]

    def free_fall(self):
        self.y_speed += self.screen_size[1]/600
        self.player_hit_box.y += self.y_speed
        return self.player_hit_box
