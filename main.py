import pygame
import numpy as np


class World:
    def __init__(self, typ="standard"):
        self.table = np.zeros(10000, dtype=int)
        self.table[5000:] = np.ones(5000, dtype=int)
        self.table = self.table.reshape(100, 100)
        self.lst_objects = []

    def append(self, obj):
        self.lst_objects.append(obj)


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_v = 0
        self.v_h = 0

    def fall(self):
        self.y = self.v_v * (1 / 60) + (9.8 * (1 / 60) ** 2) / 2
        self.v_v = self.v_v - 9.8 * 20 * (1 / 60)


class Character(Object):
    def __init__(self, x, y):
        super(Character, self).__init__(x, y)
        self.hp = 10
        self.height = 30
        self.weight = 10
        self.color = (245, 245, 220)
        self.effects = []
        self.status = "in_air"


pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill((0, 0, 0))
main_char = Character(0, 0)
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
world1 = World()
world1.append(main_char)
running = True
while running:
    if pygame.event.wait().type == pygame.QUIT:
        running = False
    w, h = pygame.display.get_surface().get_size()
    ch_w = main_char.weight
    ch_h = main_char.height
    if main_char.status == "in_air":
        if world1.table[int(main_char.y) + 50, int(main_char.x) + 50] == 1:
            main_char.status = "on_ground"
            main_char.hp -= main_char.v_v // 40
            if main_char.hp < 0:
                main_char.hp = 0
        else:
            main_char.fall()
    pygame.draw.rect(screen, main_char.color, (w // 2 - ch_w // 2, h // 2 - ch_h // 2, ch_w, ch_h))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
