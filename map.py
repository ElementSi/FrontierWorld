from random import random, randint

import PIL
import pygame as pg
from PIL import Image, ImageDraw
from perlin import PerlinNoiseFactory
import typing as tp
import numpy as np

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


def probability():
    p = random()
    if p >= 0.9:
        return 'tree'
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

        res = 40
        frames = 20
        frameres = 5
        space_range = size // res
        frame_range = frames // frameres

        pnf = PerlinNoiseFactory(3, octaves=4, tile=(space_range, space_range, frame_range))

        for t in range(frames):
            img = PIL.Image.new('L', (size, size))
            for x in range(size):
                for y in range(size):
                    n = pnf(x / res, y / res, t / frameres)
                    img.putpixel((x, y), int((n + 1) / 2 * 255 + 0.5))
            pix: tp.Optional[np.array] = img.load()  # All pixels from background

            draw = ImageDraw.Draw(img)
            for i in range(self.height):
                for j in range (self.width):
                     rand_num = randint(0, 255)
                     draw.point((i, j), (rand_num, rand_num, rand_num))
            for i in range(self.height):
                for j in range(self.width):
                     r = pix[i, j][0]
                     g = pix[i, j][1]
                     b = pix[i, j][2]

                     if r > 100 and g > 100 and b > 100:
                          self.field[i][j] = Tile(surface, 'soil', probability())
                     elif (45 < r < 101 ) and (45 < r < 101)  and (45 < r < 101):
                          self.field[i][j] = Tile(surface, 'sand', ' ')
                     else:
                          self.field[i][j] = Tile(surface, 'rock', ' ')



        # for i in range(self.height):
        #     self.field.append([])
        #     for j in range(self.width):
        #         self.field[-1].append(Tile(surface, 'soil', probability()))
        # im1 = Image.new("RGB", (self.height, self.width))  # create new picture
        # pix: tp.Optional[np.array] = im1.load()  # All pixels from background
        # if pix is not None:
        #     pix = im1.load()
        #
        # draw = ImageDraw.Draw(im1)
        # for i in range(self.height):
        #     for j in range (self.width):
        #         rand_num = randint(0, 255)
        #         draw.point((i, j), (rand_num, rand_num, rand_num))
        # for i in range(self.height):
        #     for j in range(self.width):
        #         r = pix[i, j][0]
        #         g = pix[i, j][1]
        #         b = pix[i, j][2]
        #
        #         if r > 100 and g > 100 and b > 100:
        #              self.field[i][j] = Tile(surface, 'soil', probability())
        #         elif (45 < r < 101 ) and (45 < r < 101)  and (45 < r < 101):
        #              self.field[i][j] = Tile(surface, 'sand', ' ')
        #         else:
        #              self.field[i][j] = Tile(surface, 'rock', ' ')


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

