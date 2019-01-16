import pygame
import numpy as np


class World:
    def __init__(self, typ="standard"):  # на будущее
        self.table = np.zeros(1000000, dtype=int)  # заполняем воздухом
        self.table[500000:] = np.ones(500000, dtype=int)  # добавляем землю
        self.table = self.table.reshape(1000, 1000)  # превращаем ее в двумерный массив
        self.lst_objects = []  # на будущее
        self.border = self.table[
                      int(500 - (360 + 20) / 20) // 1: int(500 + (360 - 20) / 20) // 1,
                      # Та часть мира которая будет прорисововатся
                      int(500 - 640 / 20)//1: int(500 + 640 / 20)//1
                      ]

    def update(self, x, y):
        self.border = self.table[
                      int(int(500 - (360 + 20) / 20) // 1 - y // 20): int(int(500 + (360 - 20) / 20) // 1 - y // 20),
                      # Ее изменение
                      int(x//20+int(500 - 640 / 20)//1): int(x//20+int(500 + 640 / 20)//1)
                      ]

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
    # функция получения модуля с избытком вида ov_mod(1.1) = 2
    if n // 1 == n:
        return int(n)
    else:
        if n < 0:
            return int(n // 1) - 1
        else:
            return int(n // 1) + 1


# создание мира
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen.fill((0, 0, 0))
main_char = Character(0, 0)
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
world1 = World()
world1.append(main_char)
running = True
world1.table[500][500] = 2
# запуск
while running:
    # проверка на то что игрок стоит на земле или же в воздухе
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
            # его вертикальное ускорение = g
            main_char.a_v = 0 - 9.8 * 20
    except IndexError:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # при нажатии его горизонтальное ускорение изменятся
            if event.key == pygame.K_d:
                main_char.a_h = 100
            if event.key == pygame.K_a:
                main_char.a_h = -100
            if event.key == pygame.K_SPACE:
                # если он стоит на земле то при нажатии на пробел его вертикальная скорость приравнивается 200
                if main_char.status == "on_ground":
                    main_char.v_v = 200
        if event.type == pygame.KEYUP:
            # при отжатии в горизонтальные переменные = 0
            if event.key == pygame.K_d:
                main_char.v_h = 0
                main_char.a_h = 0
            if event.key == pygame.K_a:
                main_char.v_h = 0
                main_char.a_h = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = int(500 - 360 / 20) // 1 + int(event.pos[1] / 20), int(event.pos[0]/20) + int(500 - 640 / 20)//1
            if world1.table[cell[0], cell[1]] == 0:
                world1.table[cell[0], cell[1]] = 1
    try:
        if main_char.a_h != 0 or main_char.v_h != 0:
            # ограничение в скорости 40 метров в секунду или 800 пикселей в с
            if abs(main_char.v_h) >= 800:
                pass
            else:
                # уравнение движение по горизонтальной оси
                main_char.v_h = main_char.v_h + main_char.a_h * clock.get_time()/1000
            # уравнение горизонтальной скорости
            main_char.x = main_char.x + main_char.v_h * clock.get_time()/1000 +\
                (main_char.a_h * ((clock.get_time()/1000) ** 2)) / 2
            # изменение границ мира
            world1.update(main_char.x, main_char.y)
        # тоже самое только для вертикальной оси
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
    # для упрошения кода
    w, h = pygame.display.get_surface().get_size()
    ch_w = main_char.weight
    ch_h = main_char.height
    # прорисовка мира
    for index, row in enumerate(world1.border):
        for jandex, block in enumerate(row):
            if block == 1:
                pygame.draw.rect(screen, pygame.Color("dark green"),
                                 ((-main_char.x % 20) + jandex * 20, ((main_char.y % 20) + index * 20), 20, 20))
            elif block == 0:
                pygame.draw.rect(screen, pygame.Color("light blue"),
                                 ((-main_char.x % 20) + jandex * 20, ((main_char.y % 20) + index * 20), 20, 20))
            else:  # это было сделано для того чтоб понимать если что то будет не так с первой и следюующим кадром
                pygame.draw.rect(screen, pygame.Color("red"),
                                 ((-main_char.x % 20) + jandex * 20, ((main_char.y % 20) + index * 20), 20, 20))
            pygame.draw.rect(screen, pygame.Color("black"),
                             ((-main_char.x % 20) + jandex * 20, ((main_char.y % 20) + index * 20), 20, 20), 1)
    # отрисовка персонажа
    pygame.draw.rect(screen, main_char.color, (w // 2 - ch_w // 2, h // 2 - ch_h // 2, ch_w, ch_h))
    pygame.display.flip()
    # лог для проверки достоверности того что мы видем
    print(clock.get_time(), main_char.y, main_char.x, main_char.v_v, main_char.v_h, main_char.a_v, main_char.status,
          main_char.hp)
    clock.tick(60)
pygame.quit()
