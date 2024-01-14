import pygame
import sys
from random import randint
import player
import world
import bad_guys
import hud
import bonus
import buttons
import keys


class Game:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 900
        self.game = False
        self.current_points = 0
        self.max_points = 0
        self.alpha = 255
        self.level = 0
        self.lv_phase = ''
        self.game_outcome = 'NEW GAME'

        self.speed = self.screen_width / 6
        self.hp_bar_position = (self.screen_width / 9, self.screen_height / 70 * 8)
        self.hp_bar_size = (self.screen_width / 30, self.screen_height / 30)
        self.hero_width = self.screen_width / 10
        self.hero_height = self.screen_height / 7

        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.hp_points = pygame.sprite.Group()
        self.fixed_hud = pygame.sprite.Group()
        self.heroes = pygame.sprite.Group()
        self.add_amo = pygame.sprite.Group()
        self.add_hp = pygame.sprite.Group()

        self.hero = player.Player((self.hero_width, self.hero_height), -self.hero_height,
                             (self.screen_width, self.screen_height), self.speed)
        self.ground1 = world.Background((self.screen_width, self.screen_height), self.hero.rect, (self.screen_width / 2, self.screen_height * 5 / 6),
                                   (self.screen_width * 2, self.screen_height / 2.25), self.speed, 'graphics/ground.png')
        self.ground2 = world.Background((self.screen_width, self.screen_height), self.hero.rect,
                                   (self.screen_width * 5 / 2, self.screen_height * 11/12),
                                   (self.screen_width * 2, self.screen_height / 2.25), self.speed, 'graphics/ground.png')
        self.forest1 = world.Background((self.screen_width, self.screen_height), self.hero.rect, (self.screen_width / 2, self.screen_height / 2),
                                   (self.screen_width * 2, self.screen_height * 2 / 3), self.speed * 2, 'graphics/forest.png')
        self.forest2 = world.Background((self.screen_width, self.screen_height), self.hero.rect, (self.screen_width * 5 / 2, self.screen_height / 2),
                                   (self.screen_width * 2, self.screen_height * 2 / 3), self.speed * 2, 'graphics/forest.png')
        self.sky1 = world.Background((self.screen_width, self.screen_height), self.hero.rect, (self.screen_width / 2, self.screen_height / 2),
                                (self.screen_width * 2, self.screen_height), self.speed * 3, 'graphics/sky.png')
        self.sky2 = world.Background((self.screen_width, self.screen_height), self.hero.rect, (self.screen_width * 5 / 2, self.screen_height / 2),
                                (self.screen_width * 2, self.screen_height), self.speed * 3, 'graphics/sky.png')
        self.bar = hud.HUD((self.hp_bar_position[0] + self.hero.hp / 2 * self.hp_bar_size[0] - self.screen_width / 60, self.hp_bar_position[1]),
                      (self.hp_bar_size[0] * self.hero.hp + self.hp_bar_size[0] / 3, self.hp_bar_size[1] + self.hp_bar_size[1] / 3),
                      'graphics/bar.png')
        self.hp_points.add(self.bar)
        self.heart = hud.HUD((self.hp_bar_position[0] - self.screen_height / 25, self.hp_bar_position[1]),
                        (self.hp_bar_size[0] + self.screen_height / 30, self.hp_bar_size[1] + self.screen_width / 30), 'graphics/heart.png')
        self.fixed_hud.add(self.heart)
        self.amo = hud.Counter((self.screen_width * 0.7, self.screen_height / 70 * 8),
                          (self.hp_bar_size[0] + self.screen_height / 30, self.hp_bar_size[1] + self.screen_width / 30), 'graphics/amo.png')
        self.fixed_hud.add(self.amo)
        self.points = hud.Counter((self.screen_width * 0.3, self.screen_height / 70 * 8),
                             (self.hp_bar_size[0] + self.screen_height / 30, self.hp_bar_size[1] + self.screen_width / 30),
                             'graphics/skull.png')
        self.fixed_hud.add(self.points)

        self.font = pygame.font.Font(None, int(self.screen_width / 40))
        self.text3 = self.font.render('GAME PAUSED', False, 'White')
        self.text3 = pygame.transform.scale(self.text3, (self.screen_width / 3, self.screen_height / 6))
        self.text3_rect = self.text3.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.text4 = None
        self.text4_rect = self.text3_rect
        self.lv_end = pygame.surface.Surface((self.screen_width, self.screen_height))
        self.lv_end.fill((0, 0, 0))
        self.start_but = buttons.Button((self.screen_width, self.screen_height), 'START GAME', self.font,
                                   (self.screen_width / 4, self.screen_height / 3))
        self.exit_but = buttons.Button((self.screen_width, self.screen_height), 'EXIT GAME', self.font,
                                  (self.screen_width / 4, self.screen_height * 2 / 3))

    def hp_position(self):
        """
        creating hp in hp bar
        """
        for j in range(self.hero.hp):
            hp_point = hud.HUD((self.hp_bar_position[0] + self.hp_bar_size[0] * j, self.hp_bar_position[1]),
                               (self.hp_bar_size[0], self.hp_bar_size[1]), 'graphics/hp.png')
            self.hp_points.add(hp_point)

    def hp_change(self):
        """
        creating hp bar
        """
        self.hp_points.empty()
        self.hp_points.add(self.bar)
        self.hp_position()

    def enemy_shoot_kill(self):
        """
        enemies shooting
        changing hp of enemies while hit
        creating bonuses after killing enemies
        """
        for e in self.enemies:
            if e.gun_reload == 0:
                enemy_bullet = e.shoot()
                self.enemy_bullets.add(enemy_bullet)
            if pygame.sprite.spritecollide(e, self.player_bullets, True):
                e.hp -= 1
                if e.hp == 0:
                    e.kill()
                    self.current_points += 1
                    random = randint(0, 100)
                    if random <= 30:
                        bon = bonus.Bonus((self.screen_width, self.screen_height), self.hero.rect,
                                          e.rect, 'graphics/amo.png', self.speed)
                        self.add_amo.add(bon)
                    if random >= 70:
                        bon = bonus.Bonus((self.screen_width, self.screen_height), self.hero.rect,
                                          e.rect, 'graphics/heart.png', self.speed)
                        self.add_hp.add(bon)

    def hp_amo_change(self):
        """
        picking bonuses
        checking if player got hit
        """
        if pygame.sprite.spritecollide(self.hero, self.add_amo, True):
            self.hero.whole_ammunition += 5
        if pygame.sprite.spritecollide(self.hero, self.add_hp, True) and self.hero.hp < self.hero.max_hp:
            self.hero.hp += 1
        if pygame.sprite.groupcollide(self.heroes, self.enemy_bullets, False, True):
            self.hero.hp -= 1
        if self.hero.hp == 0:
            self.heroes.empty()

    def show(self, screen):
        """
        showing all elements on a screen
        """
        screen.blit(self.sky1.element, self.sky1.element_hit_box)
        screen.blit(self.sky2.element, self.sky2.element_hit_box)
        screen.blit(self.forest1.element, self.forest1.element_hit_box)
        screen.blit(self.forest2.element, self.forest2.element_hit_box)
        screen.blit(self.ground1.element, self.ground1.element_hit_box)
        screen.blit(self.ground2.element, self.ground2.element_hit_box)
        self.enemy_bullets.draw(screen)
        self.player_bullets.draw(screen)
        self.add_amo.draw(screen)
        self.add_hp.draw(screen)
        if len(self.heroes) > 0:
            screen.blit(self.hero.gun.surf, self.hero.gun.rect)
            self.heroes.draw(screen)
            screen.blit(self.hero.hand.surf, self.hero.hand.rect)
        self.enemies.draw(screen)
        self.hp_points.draw(screen)
        self.fixed_hud.draw(screen)
        text1, text1_fit_box = self.amo.amount((self.hero.current_ammunition, self.hero.whole_ammunition), self.font)
        screen.blit(text1, text1_fit_box)
        text2, text2_fit_box = self.points.amount((self.current_points, self.max_points), self.font)
        screen.blit(text2, text2_fit_box)
        screen.blit(self.lv_end, (0, 0))
        self.lv_end.set_alpha(self.alpha)

    def movement(self):
        """
        updating positions of all elements
        """
        self.player_bullets.update()
        self.enemies.update(self.ground1.element_hit_box, self.ground2.element_hit_box)
        self.enemy_bullets.update()
        self.add_amo.update()
        self.add_hp.update()
        self.heroes.update(self.ground1.element_hit_box, self.ground2.element_hit_box, pygame.mouse.get_pos())
        self.sky1.element_hit_box.update(self.sky1.move())
        self.sky2.element_hit_box.update(self.sky2.move())
        self.forest1.element_hit_box.update(self.forest1.move())
        self.forest2.element_hit_box.update(self.forest2.move())
        self.ground1.element_hit_box.update(self.ground1.move())
        self.ground2.element_hit_box.update(self.ground2.move())

    def get_event(self):
        """
        shooting bullets by player
        reloading a gun while r key clicked or an ammunition is equal to zero
        stopping a game
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game:
                if self.lv_phase == 'middle':
                    if (pygame.mouse.get_pressed() == (True, False, False) and self.hero.gun_reload == 0 and
                            self.hero.current_ammunition > 0 and len(self.heroes) > 0):
                        bullet = self.hero.shoot()
                        self.player_bullets.add(bullet)
                    if len(self.heroes) > 0 and keys.pressed_keys()[pygame.K_r] or not self.hero.current_ammunition:
                        self.hero.reload()
                if keys.pressed_keys()[pygame.K_ESCAPE]:
                    if self.lv_phase == 'middle':
                        self.lv_phase = 'stopped'
                    elif self.lv_phase == 'stopped':
                        self.lv_phase = 'middle'

    def create_enemies(self, enemies_number):
        """
        creating enemies
        """
        self.max_points = 0
        for i in range(enemies_number):
            enemy = (bad_guys.BadGuy((self.screen_width, self.screen_height),
                                     (self.hero_width, self.hero_height), self.hero.rect,
                                     (self.screen_width * 10 / 12 + self.screen_width * (i + 1),
                                      self.screen_height * 0.57 - self.hero_height/2), self.speed))
            self.enemies.add(enemy)
            self.max_points += 1

    def game_prep(self):
        """
        resetting a game to prepare it for a new level
        """
        self.ground1.element_hit_box.center = (self.screen_width / 2, self.screen_height * 5 / 6)
        self.ground2.element_hit_box.center = (self.screen_width * 5 / 2, self.screen_height * 0.95)
        self.forest1.element_hit_box.center = (self.screen_width / 2, self.screen_height / 2)
        self.forest2.element_hit_box.center = (self.screen_width * 5 / 2, self.screen_height / 2)
        self.sky1.element_hit_box.center = (self.screen_width / 2, self.screen_height / 2)
        self.sky2.element_hit_box.center = (self.screen_width * 5 / 2, self.screen_height / 2)
        self.hero.rect.center = (self.screen_width / 2, -self.hero_height)
        self.hero.hand.rect.center = (self.screen_width / 2, -self.hero_height)
        self.hero.gun.rect.center = (self.screen_width / 2, -self.hero_height)
        self.hero.hp = self.hero.max_hp
        self.add_hp.empty()
        self.add_amo.empty()
        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.hero.reload()
        self.hero.whole_ammunition = 60

    def set_menu(self, screen):
        """
        creating a menu
        """
        self.ground1.element_hit_box.center = (self.screen_width / 2, self.screen_height * 5 / 6)
        self.forest1.element_hit_box.center = (self.screen_width / 2, self.screen_height / 2)
        self.sky1.element_hit_box.center = (self.screen_width / 2, self.screen_height / 2)
        text5 = self.font.render(self.game_outcome, False, 'Black')
        text5 = pygame.transform.scale(text5, (self.screen_width / 5, self.screen_height / 7))
        text5_rect = text5.get_rect(center=(self.screen_width / 2, self.screen_height / 5))
        screen.blit(self.sky1.element, self.sky1.element_hit_box)
        screen.blit(self.forest1.element, self.forest1.element_hit_box)
        screen.blit(self.ground1.element, self.ground1.element_hit_box)
        screen.blit(self.start_but.but, self.start_but.but_rect)
        screen.blit(self.start_but.text, self.start_but.text_rect)
        screen.blit(self.exit_but.but, self.exit_but.but_rect)
        screen.blit(self.exit_but.text, self.exit_but.text_rect)
        screen.blit(self.lv_end, (0, 0))
        screen.blit(text5, text5_rect)
        self.start_but.hovered()
        self.exit_but.hovered()
        self.lv_end.set_alpha(self.alpha)

    def start(self, screen):
        """
        start phase of a game
        """
        if self.alpha == 255:
            self.game_prep()
            self.text4 = self.font.render('LEVEL ' + str(self.level), False, 'White')
            self.text4 = pygame.transform.scale(self.text4, (self.screen_width / 3, self.screen_height / 6))
            self.current_points = 0
            self.create_enemies(3 * self.level)
        screen.blit(self.text4, self.text4_rect)
        self.alpha -= 3
        if self.alpha == 0:
            self.lv_phase = 'middle'

    def middle(self):
        """
        middle phase of a game
        """
        if len(self.heroes) > 0:
            self.movement()
        else:
            self.alpha += 3
            if self.alpha == 255:
                self.game_outcome = 'LOSE'
                self.game = False
        self.enemy_shoot_kill()
        self.hp_amo_change()
        self.hp_change()
        if self.current_points == self.max_points:
            self.hero.level_complete()
            if self.hero.rect.bottom < 0:
                self.lv_phase = 'finish'

    def finish(self):
        """
        finish phase of a game
        """
        self.alpha += 3
        if self.alpha == 255:
            if self.level == 3:
                self.game_outcome = 'WIN'
                self.game = False
            else:
                self.level += 1
                self.lv_phase = 'start'

    def menu(self, screen):
        """
        menu
        """
        self.set_menu(screen)
        if self.start_but.clicked() and self.alpha == 0:
            self.level = 1
            self.lv_phase = 'start'
            self.heroes.add(self.hero)
            self.enemies.empty()
        if self.exit_but.clicked() and self.alpha == 0:
            pygame.quit()
            sys.exit()
        if self.lv_phase == 'start':
            self.alpha += 3
        elif self.lv_phase != 'start' and self.alpha > 0:
            self.alpha -= 3
        if self.alpha == 255 and self.lv_phase == 'start':
            self.game = True
