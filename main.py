import pygame
import numpy as np
import math


class World:
    def __init__(self, typ="standard"):
        self.table = np.zeros(1000000, dtype=int)
        self.table[500000:] = np.ones(500000, dtype=int)
        self.table = self.table.reshape(1000, 1000)
        self.lst_objects = []
        self.border = self.table[int(500 - (360 + 15) / 20)//1: int(500 + (360 - 15) / 20)//1,
                                 int(500 - 640 / 20)//1: int(500 + 640 / 20)//1]

    def update(self, x, y):
        self.border = self.table[int(500 - (360 + 15) / 20 - y/20)//1: int(500 + (360 - 15) / 20 - y/20)//1,
                                 int(x/20 + 500 - 640 / 20)//1: int(x/20 + 500 + 640 / 20)//1]

    def append(self, obj):
        self.lst_objects.append(obj)


class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v_v = 0
        self.a_h = 0
        self.a_v = 0
        self.v_h = 0


class Character(Object):
    def __init__(self, x, y):
        super(Character, self).__init__(x, y)
        self.hp = 10
        self.height = 30
        self.weight = 10
        self.color = (245, 245, 220)
        self.effects = []
        self.status = "in_air"


def ov_mod(n):
    if n // 1 == n:
        return int(n)
    else:
        if n < 0:
            return int(n // 1) - 1
        else:
            return int(n // 1) + 1


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
    try:
        if world1.table[500 - ov_mod(main_char.y / 20)][int(main_char.x / 20) + 500] == 1:
            main_char.status = "on_ground"
            main_char.a_v = 0
            main_char.v_v = 0
            main_char.hp -= main_char.v_v // 40
            if main_char.hp < 0:
                main_char.hp = 0
        elif world1.table[500 - ov_mod(main_char.y / 20)][int(main_char.x / 20) + 500] == 0:
            main_char.status = "in_air"
            main_char.a_v = 0 - 9.8 * 20
    except IndexError:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                main_char.a_h = 100
            if event.key == pygame.K_a:
                main_char.a_h = -100
            if event.key == pygame.K_SPACE:
                if main_char.status == "on_ground":
                    main_char.v_v = 200
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                main_char.v_h = 0
                main_char.a_h = 0
            if event.key == pygame.K_a:
                main_char.v_h = 0
                main_char.a_h = 0
    try:
        if main_char.a_h != 0 or main_char.v_h != 0:
            if abs(main_char.v_h) >= 800:
                pass
            else:
                main_char.v_h = main_char.v_h + main_char.a_h * clock.get_time()/1000
            main_char.x = main_char.x + main_char.v_h * clock.get_time()/1000 +\
                (main_char.a_h * ((clock.get_time()/1000) ** 2)) / 2
            world1.update(main_char.x, main_char.y)
        if main_char.a_v != 0 or main_char.v_v != 0:
            if abs(main_char.v_v) >= 800:
                pass
            else:
                main_char.v_v = main_char.v_v + main_char.a_v * clock.get_time() / 1000
            main_char.y = main_char.y + main_char.v_v * clock.get_time() / 1000 + \
                (main_char.a_v * ((clock.get_time() / 1000) ** 2)) / 2
            world1.update(main_char.x, main_char.y)
    except IndexError:
        pass
    w, h = pygame.display.get_surface().get_size()
    ch_w = main_char.weight
    ch_h = main_char.height
    for index, row in enumerate(world1.border):
        for jandex, block in enumerate(row):
            if block == 1:
                pygame.draw.rect(screen, pygame.Color("dark green"), ((main_char.x % 20) + jandex * 20, ((main_char.y % 20) + index * 20), 20, 20))
            else:
                pygame.draw.rect(screen, pygame.Color("light blue"), ((main_char.x % 20) + jandex * 20, ((main_char.y % 20) + index * 20), 20, 20))
            pygame.draw.rect(screen, pygame.Color("black"), ((main_char.x % 20) + jandex * 20, ((main_char.y % 20) + index * 20), 20, 20), 1)
    pygame.draw.rect(screen, main_char.color, (w // 2 - ch_w // 2, h // 2 - ch_h // 2, ch_w, ch_h))
    pygame.display.flip()
    print(clock.get_time(), main_char.y, main_char.x, main_char.v_v, main_char.v_h, main_char.a_v, main_char.status)
    clock.tick(60)
pygame.quit()
