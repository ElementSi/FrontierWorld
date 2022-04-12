import random as rnd
import pygame as pg

ARROWS = [1073741903, 1073741904, 1073741905, 1073741906]
WASD = [100, 97, 115, 119]
TAB = 9
LEFT_SHIFT = 1073742049
RIGHT_SHIFT = 1073742053
ZX = [122, 120]
Q, E = 113, 101
SQUARE_BRACKETS = [91, 93]
ONE_TO_FIVE = [49, 50, 51, 52, 53]
SIX_TO_ZERO = [54, 55, 56, 57, 48]

WIDTH = 1000
HEIGHT = 750

size_cell = 10  # тут нужно в качестве числа передать сторону клетки


class Creation:
    """
    конструктор живых существ
    """

    def __init__(self, surface, texture, size):
        """
        :param surface: экран, где рисуем
        :param texture: изображение объекта
        :param size: массив с размерами по ОХ и ОУ
        """
        self.surface = surface
        self.live = 1
        self.x = rnd.randint(0, WIDTH - 100)
        self.y = rnd.randint(0, HEIGHT - 100)
        self.vx = 0
        self.vy = 0
        self.size = size
        self.texture = pg.transform.scale(pg.image.load(texture), (self.x, self.y))
        self.type = "creation"

    def hit_test(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с объектом obj.
        :param obj: Обьект, с которым проверяется столкновение.
        :return: Возвращает True в случае столкновения объектов. В противном случае возвращает False
        """
        if size_cell >= ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1 / 2):
            return True
        return False

    def draw(self):
        """
        Drawing a Particle
        """
        rect_draw_box = (self.x - self.size[0] / 2,
                         self.y - self.size[1] / 2,
                         self.size[0],
                         self.size[1])
        self.surface.blit(self.texture, rect_draw_box)


class Person(Creation):
    def __init__(self, surface, texture, size, x, y):
        """
        :param surface: экран, где рисуем
        :param texture: изображение человека
        :param size: размеры человека
        :param x: местоположение человека по ОХ
        :param y: местоположение человека по ОУ
        """
        super().__init__(surface, texture, size)
        self.x = x
        self.y = y
        self.type = "person"

