import pygame as pg
import random as rnd
import map_objects as obj
import map as reg_map


pg.init()

FPS = 60
SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h


class Gameplay:
    """
    Gameplay itself
    """
    def __init__(self, surface):
        """
        Initialising of Gameplay
        :param surface: Pygame Surface object - target surface
        """
        self.surface = surface
        self.clock = pg.time.Clock()
        self.map = reg_map.Map(surface, [SCREEN_WIDTH, SCREEN_HEIGHT])
        self.list_solid_object = []

        for i in range(self.map.height):
            for j in range(self.map.width):
                if self.map.field[i][j].pre_object == "tree":
                    self.list_solid_object.append(obj.Tree(self.surface, [i, j], 80))

        self.list_effects = []
        self.list_loot = []
        self.chosen_map_object = None
        self.chosen_task = None
        self.finished = False

    def create_new_animal(self):
        """
        Randomly spawn new animal on the border of the map
        """

    def draw_map(self):
        """
        Drawing every map tile
        """
        self.map.draw()

    def draw_objects(self):
        """
        Drawing every object
        """
        for solid_object in self.list_solid_object:
            solid_object.draw()

    def display_update(self):
        """
        Updating display to reflect changes of objects
        """
        pg.display.update()
        self.clock.tick(FPS)

    def process_input(self):
        """
        Processing all player input
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True

            elif event.type == pg.KEYDOWN:
                if event.key == 27:  # Esk.key = 27
                    if self.chosen_map_object is None:
                        self.finished = True

            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.chosen_task is None:
                    # if TaskBar is inactive
                    for map_object in self.list_solid_object:
                        if map_object.choose(event):  # choice & saving information about it
                            self.chosen_map_object = map_object
                            # if map_object.type == "settler" need to enable TaskBar
                    # elif TaskBar was active need to check the click on the task

                elif self.chosen_task == "Move to":
                    pass  # need to use function move_to

    def move_creation(self):
        """
        Moving every creation
        """

    def ai_acts(self):
        """
        Acting of artificial intelligence of animals
        """

    def remove_solid_object(self):
        """
        Removing dead animals and settler from lists
        """
        pass

    def process_effects(self):
        """
        Increase of particle age and removing particles that are too old
        """
        pass


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game = Gameplay(screen)

while not game.finished:
    game.process_input()
    game.draw_map()
    game.draw_objects()
    game.display_update()

pg.quit()
