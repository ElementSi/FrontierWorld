import random as rnd

import numpy as np
from PIL import Image

import constants as const
import perlin as perlin


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
        self.speed_mod, self.texture = const.LANDSCAPE[type]
        self.pre_object = pre_object


def probability_tree():
    if rnd.random() >= 0.91:
        return 'tree'
    else:
        return None


def probability_bush():
    if rnd.random() >= 0.95:
        return 'bush'
    else:
        return None


def probability_cliff(field, coord, surface, rad):
    is_rock_nearby = True

    for i in range(max(coord[1] - rad, 0),
                   min(surface.get_size()[1] // const.TILE_SIZE, coord[1] + rad + 1 - const.INTERFACE_AMENDMENT)):
        for j in range(max(coord[0] - rad, 0), min(surface.get_size()[0] // const.TILE_SIZE, coord[0] + rad + 1)):
            if field[i][j].type != "rock":
                is_rock_nearby = False

    if is_rock_nearby:
        return 'cliff'
    else:
        return None


class GameMap:
    """
    GameMap consisting of tiles arranged in a grid
    """

    def __init__(self, surface, size):

        self.surface = surface
        self.size = size
        self.width = size[0] // const.TILE_SIZE
        self.height = size[1] // const.TILE_SIZE - const.INTERFACE_AMENDMENT
        self.field = []
        self.perlin_size = 100
        self.res = 40
        self.frames = 20
        self.framer = 5
        self.space_range = self.perlin_size // self.res
        self.frame_range = self.frames // self.framer

        pnf = perlin.PerlinNoiseFactory(3, octaves=4, tile=(self.space_range, self.space_range, self.frame_range))

        img = Image.new('RGB', (self.height, self.width))
        t = self.frames - 1
        for i in range(self.height):
            for j in range(self.width):
                n = pnf(i / self.res, j / self.res, t / self.framer)
                img.putpixel((i, j), int((n + 1) / 2 * 255 + 0.5))

        for i in range(self.height):
            self.field.append([])
            for j in range(self.width):
                pix = img.getpixel((i, j))
                r = np.array(pix)[0]
                if 144 > r > 116:
                    self.field[-1].append(Tile(surface, 'soil', probability_tree() or probability_bush()))
                elif 116 > r > 0:
                    self.field[-1].append(Tile(surface, 'rock', None))
                else:
                    self.field[-1].append(Tile(surface, 'sand', None))

        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j].type == "rock":
                    self.field[i][j].pre_object = probability_cliff(self.field, (j, i), self.surface, 2)

    def draw(self):
        """
        Drawing the whole map in the current window
        """
        for i in range(self.height):
            for j in range(self.width):
                tile_rect = (j * const.TILE_SIZE, i * const.TILE_SIZE, const.TILE_SIZE, const.TILE_SIZE)
                landscape_texture = self.field[i][j].texture
                self.surface.blit(landscape_texture, tile_rect)
