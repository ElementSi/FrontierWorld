import math
import random as rnd
import pygame
import pygame.draw as dr


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


class Person:
    """
    конструктор живых существ
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.live = 1
        self.x = rnd.randint(0, WIDTH - 100)
        self.y = rnd.randint(0, HEIGHT - 100)
        self.v = 10
        self.vx = self.v * rnd.random()
        self.r = 10
        direction_y = rnd.random()
        if direction_y != 0:
            direction_y /= abs(direction_y)
        self.vy = (self.v ** 2 - self.vx ** 2) ** (1 / 2) * direction_y

    def hit_test(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с объектом obj.
        :param obj: Обьект, с которым проверяется столкновение.
        :return: Возвращает True в случае столкновения объектов. В противном случае возвращает False.
        """
        if self.r + obj.r >= ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1 / 2):
            return True
        return False
