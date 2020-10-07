#--------------------------------#
# Aminov Renat 7th October 2020  #
#                                #
# v 0.0.1                        #
#--------------------------------#

#
#
# Делит пикчу на области одного цвета и делает из них контуры
#
#


'''
                                 To Do:
- Отсортировать точки из контура так, чтоб можно было натянуть полигон
- Решить проблему с полостями внутри контура (как вобще это сделать?
 * * * * * * * *
 *             *
 *    * * *    *
 *    *   *    *
 *    * * *    *
 *             *
 * * * * * * * *

- Не все точки имеют одинаковый цвет (хотя он одинаков для глаз)
- Сделать нерекурсивное нахождение окрестности
- Ходить не по пикселям
- Сделать нормальные типы данных (сделать area и contur словарями)
'''

from PIL import Image
import pygame
from pygame.draw import *
import sys

# надо
sys.setrecursionlimit(100000)

# Класс работает с двумя обьетками
# areas - множество точек имеющих один цвет и из любой точки можно пройти в другую не выходя за рамки area
# area = [[точки], цвет]
# areas = [area]
#
# conturs - точки area, имеющих хотя бы одного соседа не того же цвета
# contur = [[точки], цвет]
# conturs = [contur]
class MAP():

    #
    # color_map - двумерный массив с цветом в каждом пикселе
    #
    def __init__(self, color_map):
        self.color_map = color_map
        self.size = (len(color_map[0]), len(color_map))
        self._get_areas()
        self._get_conturs()

    #
    # Принадлежит ли точка какой нибудь области?
    #
    def _is_dot_reg(self, x, y):
        for area in self.areas:
            if (x, y) in area[0]:
                return True
        return False

    #
    # Принадлежит ли точка рисунку?
    #
    def _is_dot_inside(self, x, y):
        return 0 <= x <= self.size[0] - 1 and 0 <= y <= self.size[1] - 1

    #
    # Принадлежит ли точка множеству dots и принадлежит ли точка рисунку?
    #
    def _is_dot_nice(self, x, y, dots):
        return not (x, y) in dots and self._is_dot_inside(x, y)

    #
    # Уфф, это дерьмо
    # из за особенностей рекурсии приходиться так колхозить
    #
    def get_area(self, x0, y0):
        color = self.color_map[y0][x0]
        dots = []
        self._fill_area(x0, y0, color, dots)
        return (sorted(dots), color)


    #
    # Лазает по соседям и ищет такого же цвета
    #
    def _fill_area(self, x, y, color, dots):
        dots.append((x, y))
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if self._is_dot_nice(x + d[0], y + d[1], dots) and self.color_map[y + d[1]][x + d[0]] == color:
                self._fill_area(x + d[0], y + d[1], color, dots)

    #
    # Уфф, это дерьмо
    # из за особенностей рекурсии приходиться так колхозить
    #
    def _get_areas(self):
        self.areas = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if not self._is_dot_reg(x, y):
                    self.areas.append(self.get_area(x, y))
    #
    # делает контур из area
    #
    #
    def _get_contur(self, area):
        contur = []
        for dot in area[0]:
            a = False
            for d in[(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if not self._is_dot_inside(dot[0] + d[0], dot[1] + d[1]) or self.color_map[dot[1] + d[1]][dot[0] + d[0]] != area[1]:
                    a = True
            if a:
                contur.append(dot)
        return (contur, area[1])

    #
    # делает все контуры
    #
    def _get_conturs(self):
        self.conturs = [self._get_contur(area) for area in self.areas]


im = Image.open('pic.png')
im.load()
pygame.init()
FPS = 30
screen = pygame.display.set_mode(im.size)

print(im.format, im.size, im.mode)

pic = [[0 for x in range(im.size[0])] for y in range(im.size[1])]

#без этого не все красиво
for y in range(im.size[1]):
    for x in range(im.size[0]):
        r = im.getpixel((x, y))[0]
        g = im.getpixel((x, y))[1]
        b = im.getpixel((x, y))[2]
        if r + g + b > 570:
            pic[y][x] = (255, 255, 255)
        else:
            pic[y][x] = (0, 0, 0)

mp = MAP(pic)
areas = mp.areas
print(areas)

for ar in areas:
    b = [[0 for i in range(len(pic[0]))] for j in range(len(pic))]

    for dot in ar[0]:
        b[dot[1]][dot[0]] = 1

    for l in b:
        print(l)
    print()


for area in mp.conturs:
    for dot in area[0]:
        screen.set_at(dot, area[1])


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()