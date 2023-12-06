import pygame
import sys
import player
import world
import bullets
import bad_guys
import time


def screen_creator(width, height):
    return pygame.display.set_mode((width, height))


b = 0
shoot_player = 0
shoot_enemy = 0
bullet_list = []
enemy_list = []
bullet = None
screen_width = 1200
screen_height = 900
hero_width = screen_width/18
hero_height = screen_height/9
screen = screen_creator(screen_width, screen_height)
clock = pygame.time.Clock()
hero = player.Player((hero_width, hero_height), screen_height*2/3-hero_height/2,
                     (screen_width, screen_height))

ground1 = world.Background((screen_width, screen_height), hero.hit_box(), (screen_width/2, screen_height*5/6),
                           (screen_width*2, screen_height/2.25), 200, 'graphics/ground.png')
ground2 = world.Background((screen_width, screen_height), hero.hit_box(), (screen_width*5/2, screen_height*11/12),
                           (screen_width*2, screen_height/2.25), 200, 'graphics/ground.png')
forest1 = world.Background((screen_width, screen_height), hero.hit_box(), (screen_width/2, screen_height/2),
                           (screen_width*2, screen_height*2/3), 400, 'graphics/forest.png')
forest2 = world.Background((screen_width, screen_height), hero.hit_box(), (screen_width*5/2, screen_height/2),
                           (screen_width*2, screen_height*2/3), 400, 'graphics/forest.png')
sky1 = world.Background((screen_width, screen_height), hero.hit_box(), (screen_width/2, screen_height/2),
                        (screen_width*2, screen_height), 600, 'graphics/sky.png')
sky2 = world.Background((screen_width, screen_height), hero.hit_box(), (screen_width*5/2, screen_height/2),
                        (screen_width*2, screen_height), 600, 'graphics/sky.png')
enemy = bad_guys.BadGuy((screen_width, screen_height), hero.hit_box(), (2000, 575))

while True:

    if pygame.mouse.get_pressed() == (False, False, False) and b == 0:
        b = 1
    if b == 1 and pygame.mouse.get_pressed() == (True, False, False) and shoot_player == 0:
        bullet_list.append(time.time())
        bullet_list[-1] = (
            bullets.Bullet((screen_height, screen_width), (hero.hit_box()), (pygame.mouse.get_pos()), 'Yellow'))
        b = 0
        shoot_player = 50
    if shoot_player > 0:
        shoot_player -= 2
    screen.blit(sky1.surf(), sky1.hit_box())
    screen.blit(sky2.surf(), sky2.hit_box())
    screen.blit(forest1.surf(), forest1.hit_box())
    screen.blit(forest2.surf(), forest2.hit_box())
    screen.blit(ground1.surf(), ground1.hit_box())
    screen.blit(ground2.surf(), ground2.hit_box())
    try:
        screen.blit(enemy.surf(), enemy.hit_box())
        enemy.hit_box().update(enemy.move())
        if shoot_enemy == 0:
            bullet_list.append(time.time())
            bullet_list[-1] = enemy.shoot()
            shoot_enemy = 100
        if shoot_enemy > 0:
            shoot_enemy -= 2
    except NameError:
        pass

    for i in bullet_list:
        screen.blit(i.surface(), i.hit_box())
        i.hit_box().update(i.shoot())
        try:
            if i.hit_box().colliderect(enemy.hit_box()) and i.acolor() == 0:
                del enemy
                bullet_list.pop(bullet_list.index(i))
                del i
        except NameError:
            pass
        try:
            if i.hit_box().x < 0 or i.hit_box().x > screen_width or i.hit_box().y < 0 or i.hit_box().y > screen_height:
                bullet_list.pop(bullet_list.index(i))
                del i
        except NameError:
            pass
    screen.blit(hero.surf(), hero.hit_box())
    hero.hit_box().update(hero.movement(ground1.hit_box(), ground2.hit_box()))
    sky1.hit_box().update(sky1.move())
    sky2.hit_box().update(sky2.move())
    forest1.hit_box().update(forest1.move())
    forest2.hit_box().update(forest2.move())
    ground1.hit_box().update(ground1.move())
    ground2.hit_box().update(ground2.move())
    hero.hit_box().update(hero.free_fall())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(60)
