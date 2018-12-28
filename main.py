import pygame


class Character:
    def __init__(self, x, y):
        self.height = 30
        self.weight = 10
        self.color = (245, 245, 220)
        self.x = x
        self.y = y
        self.v = 0


pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill((0, 0, 0))
main_char = Character(0, 0)
screen.fill((255, 255, 255))
while pygame.event.wait().type != pygame.QUIT:
    w, h = pygame.display.get_surface().get_size()
    ch_w = main_char.weight
    ch_h = main_char.height
    pygame.draw.rect(screen, main_char.color, (w // 2 - ch_w // 2, h // 2 - ch_h // 2, ch_w, ch_h))
    pygame.display.flip()
pygame.quit()
