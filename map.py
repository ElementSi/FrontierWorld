import pygame as pg


TILE_SIZE = 24


class Tile:
    """
    Tile that contains information about its surface type and prescribed for spawn objects
    """
    def __init__(self, type, prescribed_object):
        """

        :param type:
        :param prescribed_object:
        """
        self.type = type  # Строчка, например "soil", "sand"
        self.prescribed_object = prescribed_object

    def get_prescribed_object(self):
        return self.prescribed_object


class Map:
    """

    """
    def __init__(self, size):
        self.size = size
        self.field = [[Tile("soil", None) for _ in range(self.size[0])] for _ in range(self.size[1])]

    def get_prescribed_object(self, coord):
        return self.field[coord[0]][coord[1]].get_prescribed_object()

    def safe(self):
        pass
