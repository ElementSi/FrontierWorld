from random import random

import PIL
import numpy as np
import pygame as pg
from PIL import Image

from perlin import PerlinNoiseFactory

TILE_SIZE = 24

LANDSCAPE = {
    "soil": [0.9, pg.transform.scale(pg.image.load("assets/textures/soil.png"), (TILE_SIZE, TILE_SIZE))],
    "sand": [0.5, pg.transform.scale(pg.image.load("assets/textures/sand.png"), (TILE_SIZE, TILE_SIZE))],
    "rock": [0.7, pg.transform.scale(pg.image.load("assets/textures/rock.png"), (TILE_SIZE, TILE_SIZE))],
    "rocky_soil": [0.8, pg.transform.scale(pg.image.load("assets/textures/rocky_soil.png"), (TILE_SIZE, TILE_SIZE))]
}


class Tile:
    """
    Tile that contains information about its surface type and prescribed for spawn objects
    """

    def __init__(self, surface, type, pre_object):
        """
        Constructor of tile
        :param type: string - the key of the corresponding landscape
        :param pre_object: string - the key of the corresponding map object
        """
        self.surface = surface
        self.type = type
        self.speed_mod = LANDSCAPE[type][0]
        self.texture = LANDSCAPE[type][1]
        self.pre_object = pre_object


def probability_tree():
    t = random()
    if t >= 0.91:
        return 'tree'
    else:
        return None


def probability_bush():
    b = random()
    if b >= 0.4:
        return 'bush'
    else:
        return None


def probability_cliff():
    r = random()
    if r >= 0.12:
        return 'cliff'
    else:
        return None


class Map:
    """
    Map consisting of tiles arranged in a grid
    """

    def __init__(self, surface, size):

        self.surface = surface
        self.size = size
        self.width = size[0] // TILE_SIZE
        self.height = size[1] // TILE_SIZE
        self.field = []
        self.perlin_size = 100
        self.res = 40
        self.frames = 20
        self.frameres = 5
        self.space_range = self.perlin_size // self.res
        self.frame_range = self.frames // self.frameres

        pnf = PerlinNoiseFactory(3, octaves=4, tile=(self.space_range, self.space_range, self.frame_range))

        img = PIL.Image.new('RGB', (self.height, self.width))
        t = self.frames - 1
        for i in range(self.height):
            for j in range(self.width):
                n = pnf(i / self.res, j / self.res, t / self.frameres)
                img.putpixel((i, j), int((n + 1) / 2 * 255 + 0.5))

        for i in range(self.height):
            self.field.append([])
            for j in range(self.width):
                pix = img.getpixel((i, j))
                r = np.array(pix)[0]
                if 144 > r > 116:
                    self.field[-1].append(Tile(surface, 'soil', probability_tree() or probability_bush()))
                elif 116 > r > 0:
                    self.field[-1].append(Tile(surface, 'rock', probability_cliff()))
                else:
                    self.field[-1].append(Tile(surface, 'sand', None))

    def get_pre_object(self, coord):
        """
        Request for the prescribed object to spawn
        :param coord: list[int, int] - coordinates of the tile of interest
        :return: string - description of the prescribed object
        """
        return self.field[coord[0]][coord[1]].pre_object

    def get_speed_mod(self, coord):
        """
        Request for the speed modifier of tile
        :param coord: list[int, int] - coordinates of the tile of interest
        :return: float - value of speed modifier
        """
        return self.field[coord[0]][coord[1]].speed_mod

    def draw(self):
        """
        Drawing the whole map in the current window
        """
        for i in range(self.size[1] // TILE_SIZE):
            for j in range(self.size[0] // TILE_SIZE):
                tile_rect = (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                landscape_texture = LANDSCAPE[self.field[i][j].type][1]
                self.surface.blit(landscape_texture, tile_rect)

    def safe(self, file):
        """
        Writing information about the map to a save file
        """
        pass  # Надо записать строчку с исчерпывающей и унифицированной информацией о карте в файл
