#--------------------------------#
# Aminov Renat 8th October 2020  #
#                                #
# v 0.0.2                        #
#--------------------------------#

'''
                                 To Do:
- Не все точки имеют одинаковый цвет (хотя он одинаков для глаз)
- Ходить не по пикселям
'''

from PIL import Image
import pygame
from pygame.draw import *
import sys

class MAP():
    def __init__(self, pic):
        self.color_map = pic
        self.size = (len(pic[0]), len(pic))
        self.make_conturs()

    def find_contur(self, x0, y0):
        color = self.color(x0, y0)
        x, y = (x0, y0)
        dots = []
        dots.append((x, y))

        step = 1
        while step == 1:
            step = 0
            for d in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                x_ = x + d[0]
                y_ = y + d[1]
                if not self.is_inner(x_, y_, color) and self.in_map(x_, y_) and self.color(x_, y_) == color:
                    if not (x_, y_) in dots:
                        x, y = (x_, y_)
                        dots.append((x, y))
                        step = 1
                        break

        contur = dict()
        contur['dots'] = dots
        contur['color'] = color
        return contur

    def is_inner(self, x0, y0, color):
        for d in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x, y = (x0 + d[0], y0 + d[1])
            if not self.in_map(x, y) or self.color(x, y) != color:
                return False
        return True

    def in_map(self, x, y):
        return 0 <= x < self.size[0] and 0 <= y < self.size[1]

    def make_conturs(self):
        self.conturs = []
        mark_map = self.get_mark_map()

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if mark_map[y][x] == 0:
                    self.conturs.append(self.find_contur(x, y))
                    mark_map = self.get_mark_map()
        self.conturs = sorted(self.conturs, key = lambda x: min(x['dots'])[0] - max(x['dots'])[0])

    def color(self, x, y):
        return self.color_map[y][x]

    def get_mark_map(self):
        mark_map = [[0 for x in range(self.size[0])] for y in range(self.size[1])]
        for contur in self.conturs:
            mark = 0
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    if (x, y) in contur['dots'] and mark == 0:
                        mark = 1
                    if self.color(x, y) != contur['color'] and mark == 1:
                        mark = 0
                    if mark_map[y][x] != 1:
                        mark_map[y][x] = mark
        return mark_map

def display_dots(a):
    b = [[0 for x in range(32)] for y in range(32)]

    for dot in a:
        b[dot[1]][dot[0]] = 1

    for l in b:
        print(l)
    print()

im = Image.open('pic.png')
im.load()
pygame.init()
FPS = 30
screen = pygame.display.set_mode(im.size)

print(im.format, im.size, im.mode)

pic = [[im.getpixel((x, y))[:3] for x in range(im.size[0])] for y in range(im.size[1])]
#pic = [[0 for x in range(im.size[0])] for y in range(im.size[1])]

'''
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
'''

mp = MAP(pic)

for contur in mp.conturs:
    if len(contur['dots']) > 1:
        print(contur['dots'])
        print(contur['color'])
        display_dots(contur['dots'])
        polygon(screen, contur['color'], contur['dots'])



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()



