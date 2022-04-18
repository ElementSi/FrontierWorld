import pygame as pg


class Cell:
    """

    """

    def __init__(self, cell_type, owner_id=0):
        self.cell_type = cell_type
        self.owner_id = owner_id

        self.player = cell_type == 1
        self.trace = cell_type == 2
        self.rock = cell_type == 3
        self.plant = cell_type == 4
        self.wall = cell_type == 5
        self.empty = cell_type == 0

#field = [[Cell(0) for _ in range(board_size.y)] for _ in range(board_size.x)]

    def is_player(self):
        return self.player

    def is_rock(self):
        return self.rock

    def is_plant(self):
        return self.plant

    def is_trace(self):
        return self.trace