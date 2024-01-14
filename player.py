import pygame
import keys
import bullets
import math


class Player(pygame.sprite.Sprite):

    def __init__(self, size, position_y, screen_size, speed):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.screen_size = screen_size
        self.speed = speed
        self.y_speed = 0
        self.single_jump = 0
        self.rotate = 0
        self.double_jump = 0
        self.max_current_ammunition = 30
        self.current_ammunition = self.max_current_ammunition
        self.whole_ammunition = 60
        self.max_hp = 3
        self.hp = self.max_hp
        self.gun_reload = 0
        self.bullet = None
        self.frames = []
        self.frame = 0
        self.position_x = screen_size[0]/2
        self.position_y = position_y
        self.frames.append(pygame.image.load('graphics/hero_frame_1.png'))
        self.frames.append(pygame.image.load('graphics/hero_frame_2.png'))
        self.frames.append(pygame.image.load('graphics/hero_frame_3.png'))
        self.frames.append(pygame.image.load('graphics/hero_frame_4.png'))
        self.image = self.frames[0]
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=(self.position_x, self.position_y))
        self.hand = HandGun('graphics/hero_hand.png', self.rect)
        self.gun = HandGun('graphics/hero_gun.png', self.rect)

    def shoot(self):
        """
        creating a bullet to be shot by player
        """
        self.bullet = bullets.Bullet(self.screen_size, self.rect,
                                     (self.rect.center[0], self.rect.center[1], 0, 0),
                                     pygame.mouse.get_pos(), 'Yellow', self.speed)
        self.current_ammunition -= 1
        self.gun_reload = 50
        return self.bullet

    def reload(self):
        """
        reloading a gun
        """
        missing_amo = self.max_current_ammunition - self.current_ammunition
        if self.whole_ammunition < missing_amo:
            missing_amo = self.whole_ammunition
        self.whole_ammunition -= missing_amo
        self.current_ammunition += missing_amo

    def rotation(self, mouse):
        """
        rotate a player to face a mouse pointer
        """
        if mouse[0] < self.rect.x + self.size[0]/2 and self.rotate == 0:
            self.image = pygame.transform.flip(self.image, 1, False)
            self.hand.surf = pygame.transform.flip(self.hand.surf, 1, False)
            self.gun.surf = pygame.transform.flip(self.gun.surf, 1, False)
            self.rotate = 1
        if mouse[0] > self.rect.x + self.size[0]/2 and self.rotate == 1:
            self.image = pygame.transform.flip(self.image, 1, False)
            self.hand.surf = pygame.transform.flip(self.hand.surf, 1, False)
            self.gun.surf = pygame.transform.flip(self.gun.surf, 1, False)
            self.rotate = 0

    def movement(self, g1, g2):
        """
        moving and changing frames while a or d key pressed
        """
        self.rotate = 0
        if ((keys.pressed_keys()[pygame.K_a] or keys.pressed_keys()[pygame.K_d]) and
                (self.rect.colliderect(g1) or self.rect.colliderect(g2))):
            self.frame += 0.2
            if int(self.frame) > len(self.frames) - 1:
                self.frame = 0
            self.image = self.frames[int(self.frame)]
            self.image = pygame.transform.scale(self.image, self.size)
            self.hand.show()
            self.gun.show()
        else:
            self.frame = 0
            self.image = self.frames[int(self.frame)]
            self.image = pygame.transform.scale(self.image, self.size)
            self.hand.show()
            self.gun.show()
        if (keys.pressed_keys()[pygame.K_a] and self.rect.left > round(self.screen_size[0] / 3) and
                not ((self.rect.left <= g2.left and self.rect.bottom - 10 >= g1.top) or
                     (self.rect.left <= g1.left and self.rect.bottom - 10 >= g2.top))):
            self.rect.x -= self.screen_size[0] / self.speed
        if ((keys.pressed_keys()[pygame.K_d] and
             self.rect.right < self.screen_size[0] - round(self.screen_size[0] / 3)) and
                not ((self.rect.right >= g2.right and self.rect.bottom - 10 >= g1.top) or
                     (self.rect.right >= g1.right and self.rect.bottom - 10 >= g2.top))):
            self.rect.x += self.screen_size[0] / self.speed

    def jump(self):
        """
        jump or double jump when space key clicked
        """
        if not keys.pressed_keys()[pygame.K_SPACE] and self.single_jump < 2:
            self.single_jump += 1
            self.double_jump = 1
        if keys.pressed_keys()[pygame.K_SPACE] and self.double_jump == 1:
            self.double_jump = 0
            self.y_speed = -self.screen_size[1]/45
            self.rect.y += self.y_speed

    def environment_interaction(self, g1, g2):
        """
        correcting a position of a player after fall
        checking collision with a side of a ground
        """
        if ((self.rect.bottom >= g1.top and self.rect.left + 10 <= g1.right and
             self.rect.right - 10 >= g1.left) or
                (self.rect.bottom >= g2.top and self.rect.left + 10 <= g2.right and
                 self.rect.right - 10 >= g2.left)):
            self.single_jump = 0
            self.y_speed = 0
            if (self.rect.bottom >= g1.top and self.rect.left + 10 <= g1.right and
                    self.rect.right - 10 >= g1.left):
                self.rect.y = g1.top - self.size[1]
            if (self.rect.bottom >= g2.top and self.rect.left + 10 <= g2.right and
                    self.rect.right - 10 >= g2.left):
                self.rect.y = g2.top - self.size[1]

    def level_complete(self):
        """
        flying out of screen while level completed
        """
        if self.rect.bottom >= 0:
            self.y_speed = 0
            self.rect.y -= 10

    def update(self, g1, g2, mouse):
        """
        executing all functions above
        """
        if self.gun_reload > 0:
            self.gun_reload -= 2
        self.movement(g1, g2)
        self.rotation(mouse)
        self.jump()
        self.environment_interaction(g1, g2)
        self.y_speed += self.screen_size[1]/(self.speed * 3)
        self.rect.y += self.y_speed
        self.hand.rotation(mouse, self.rotate)
        self.gun.rotation(mouse, self.rotate)


class HandGun:

    def __init__(self, image, hero_position):
        self.image = image
        self.surf = pygame.image.load(self.image)
        self.hero_position = hero_position
        self.rect = self.surf.get_rect(center=(-100, -100))

    def show(self):
        """
        showing and scaling a hand and a gun
        """
        self.surf = pygame.image.load(self.image)
        self.surf = pygame.transform.scale(self.surf, (self.hero_position[2] * 1.4, self.hero_position[3] * 10/23))

    def rotation(self, mouse, rotate):
        """
        rotate a hand and a gun to point a mouse pointer
        """
        if mouse[0] - self.rect.center[0] != 0:
            angle = math.atan((self.rect.center[1] - mouse[1]) / (mouse[0] - self.rect.center[0]))*180/math.pi
            self.surf = pygame.transform.rotate(self.surf, angle)
        if rotate == 0:
            self.rect = (
                self.surf.get_rect(center=(self.hero_position[0] + self.hero_position[2] * 4/12,
                                           self.hero_position[1] + self.hero_position[3] * 4/12)))
        else:
            self.rect = self.surf.get_rect(
                center=(self.hero_position[0] + self.hero_position[2] * 8/12,
                        self.hero_position[1] + self.hero_position[3] * 4/12))
