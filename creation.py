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
        self.vx = 2 * self.v * (rnd.random() - 0.5)
        direction_y = rnd.random() - 0.5
        if direction_y != 0:
            direction_y /= abs(direction_y)
        self.vy = (self.v ** 2 - self.vx ** 2) ** (1 / 2) * direction_y
