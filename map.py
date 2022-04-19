import pygame
import pygame as pg
from random import randint


TILE_SIZE = 24
WIDTH = 1920
HEIGHT = 1080

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

def probability():
    return 'tree'

class Map:
    """
    Map consisting of tiles arranged in a grid
    """
    def __init__(self, surface, size):
        self.surface = surface
        self.size = size
        self.field = [size[1]][size[0]]
        for i in range(size[1]):
            for j in range (size[0]):
                if self.field[i] == size[1]//2 and self.field[j] == size[0]/2:
                    for k in range (randint(10,100)):
                        self.field[size[1]//2+k][size[0]//2+k] = Tile(surface,'soil', probability()) #fill the middle with soil
                elif self.field[i] == 0 & self.field[j] == 0:
                    for p in range (randint(30,90)):
                        self.field[p][p] = Tile(surface, 'sand', ' ') #fill the upper left corner with sand
                elif self.field[i] == size[1] and self.field[j] == size[0]:
                    for l in range (randint(10,30)):
                        self.field[l][l] = Tile(surface, 'rock', ' ') # fill the  upper right corner with rock

        # Добавить в pre-object вероятность возникновения объекта (rock, tree, bush)
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

    def draw(self, surface):
        """
        Drawing the whole map in the current window
        """
        #pygame.draw.rect(surface, 'green', Tile(self.rect))
        pass

    def safe(self, file):
        """
        Writing information about the map to a save file
        """
        pass  # Надо записать строчку с исчерпывающей и унифицированной информацией о карте в файл
