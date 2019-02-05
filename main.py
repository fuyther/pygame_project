import pygame
import numpy as np
import os


class World:
    def __init__(self, typ="standard"):  # на будущее
        self.table = np.zeros(1000000, dtype=int)  # заполняем воздухом
        self.table[500000:] = np.ones(500000, dtype=int)  # добавляем землю
        self.table = self.table.reshape(1000, 1000)  # превращаем ее в двумерный массив
        self.lst_objects = {}  # на будущее

    def append(self, key, obj):
        self.lst_objects[key] = obj


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
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


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


# создание мира
pygame.init()
screen = pygame.display.set_mode((1280, 720))
objects = {
    0: load_image("air.png"),
    1: load_image("dirt.png")
}
character = load_image("char.png")
screen.fill((0, 0, 0))
all_sprites = pygame.sprite.Group()
main_char = Character(0, 0)
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
world1 = World()
world1.append("main_char", (main_char, main_char.x + 500*20, - main_char.y + 500*20))
running = True
world1.table[500][490:501] = 2
# запуск
while running:
    screen.fill((0, 0, 0))
    # проверка на то что игрок стоит на земле или же в воздухе
    try:
        if world1.table[500 - int(main_char.y // 20)][int(main_char.x // 20) + 500] == 1:
            main_char.status = "on_ground"
            main_char.a_v = 0
            main_char.v_v = 0
            main_char.hp -= main_char.v_v // 40
            if main_char.hp < 0:
                main_char.hp = 0
        elif world1.table[500 - int(main_char.y // 20)][int(main_char.x // 20) + 500] == 0:
            main_char.status = "in_air"
            # его вертикальное ускорение = g
            main_char.a_v = 0 - 9.8 * 30
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
            cell = int(world1.lst_objects["main_char"][1] + event.pos[0] - 640)//20, int(world1.lst_objects["main_char"][2] + event.pos[1] - 360)//20
            if world1.table[cell[1], cell[0]] == 0:
                world1.table[cell[1], cell[0]] = 1
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
        # тоже самое только для вертикальной оси
        if main_char.a_v != 0 or main_char.v_v != 0:
            if abs(main_char.v_v) >= 800:
                pass
            else:
                main_char.v_v = main_char.v_v + main_char.a_v * clock.get_time() / 1000
            main_char.y = main_char.y + main_char.v_v * clock.get_time() / 1000 + \
                (main_char.a_v * ((clock.get_time() / 1000) ** 2)) / 2
        world1.lst_objects["main_char"] = (main_char, main_char.x + 500*20, - main_char.y + 500*20)
    except IndexError:
        pass
    # для упрошения кода
    w, h = pygame.display.get_surface().get_size()
    ch_w = main_char.weight
    ch_h = main_char.height
    # прорисовка мира
    for i in range(38):
        for j in range(66):
            cell = world1.table[ov_mod(world1.lst_objects["main_char"][2] / 20) + (i - 19)][
                int(world1.lst_objects["main_char"][1] / 20) + (j - 33)]
            if cell == 1:
                screen.blit(objects[1], (int((j - 1)*20 - main_char.x % 20), int((i - 1)*20 + main_char.y % 20)))
            else:
                screen.blit(objects[0], (int((j - 1) * 20 - main_char.x % 20), int((i - 1) * 20 + main_char.y % 20)))
    # отрисовка персонажа
        screen.blit(character, (w // 2 - ch_w // 2, h // 2 - ch_h // 2))
    pygame.display.flip()
    # лог для проверки достоверности того что мы видем
    print(clock.get_time(), main_char.y, main_char.x, main_char.v_v, main_char.v_h, main_char.a_v, main_char.status,
          main_char.hp)
    clock.tick(60)
pygame.quit()
