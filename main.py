import pygame
import game

pygame.init()
contra = game.Game()
screen = pygame.display.set_mode((contra.screen_width, contra.screen_height))
clock = pygame.time.Clock()

if __name__ == "__main__":
    while True:
        contra.get_event()
        if contra.game:
            contra.show(screen)
            if contra.lv_phase == "start":
                contra.start(screen)
            elif contra.lv_phase == "middle":
                contra.middle()
            elif contra.lv_phase == "finish":
                contra.finish()
            else:
                screen.blit(contra.text3, contra.text3_rect)
        else:
            contra.menu(screen)
        pygame.display.update()
        clock.tick(60)
