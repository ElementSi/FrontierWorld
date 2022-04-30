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
        self.settler = obj.Settler(self.surface, [self.map.width // 2, self.map.height // 2], 20)
        self.list_solid_object = []

        for i in range(self.map.height):
            for j in range(self.map.width):
                if self.map.field[i][j].pre_object == "tree":
                    self.list_solid_object.append(obj.Tree(self.surface, [j, i], 80))

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
        self.settler.draw()

        for solid_object in self.list_solid_object:
            solid_object.draw()

        if self.chosen_map_object is not None:
            self.chosen_map_object.draw_frame()

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
                    else:
                        self.chosen_map_object.is_chosen = False
                        self.chosen_map_object = None

            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.chosen_task is None:
                    # if TaskBar is inactive

                    none_is_chosen = True

                    for solid_object in self.list_solid_object:
                        if solid_object.choose(event):  # choice of solid object & saving information about it
                            none_is_chosen = False
                            self.chosen_map_object = solid_object

                    for loot_item in self.list_loot:
                        if loot_item.choose(event):  # choice of loot item & saving information about it
                            none_is_chosen = False
                            self.chosen_map_object = loot_item

                    if self.settler.choose(event):  # choice of settler & saving information about it
                        none_is_chosen = False
                        self.chosen_map_object = self.settler
                        #  need to enable TaskBar

                    if none_is_chosen:
                        self.chosen_map_object = None

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
    game.draw_map()
    game.draw_objects()
    game.process_input()
    game.display_update()

pg.quit()
