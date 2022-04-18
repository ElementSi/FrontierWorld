import pygame as pg


TILE_SIZE = 24

LANDSCAPE = {
    "soil": [0.9, pg.transform.scale(pg.image.load("textures/soil.png"), (TILE_SIZE, TILE_SIZE))],
    "sand": [0.5, pg.transform.scale(pg.image.load("textures/sand.png"), (TILE_SIZE, TILE_SIZE))],
    "rock": [0.7, pg.transform.scale(pg.image.load("textures/rock.png"), (TILE_SIZE, TILE_SIZE))],
    "rocky_soil": [0.8, pg.transform.scale(pg.image.load("textures/rocky_soil.png"), (TILE_SIZE, TILE_SIZE))]
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


class Map:
    """
    Map consisting of tiles arranged in a grid
    """
    def __init__(self, surface, size):
        self.surface = surface
        self.size = size
        self.field = [[Tile("soil", self.surface, None) for _ in range(self.size[0])] for _ in range(self.size[1])]
        # Главная и сложная задача - написать интересную случайную генерацию карты,
        # которая будет распределять по ней типы поверхности, а затем объекты, наследующие классу NaturalObjects.

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
        pass  # Надо нарисовать все тайлы на экране

    def safe(self, file):
        """
        Writing information about the map to a save file
        """
        pass  # Надо записать строчку с исчерпывающей и унифицированной информацией о карте в файл
