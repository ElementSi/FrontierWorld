import pygame as pg

import features as feat
import map_objects as obj
import map as reg_map

pg.init()

SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h


def pixels2tiles(pixel_coords):
    return [int(pixel_coords[0]), int(pixel_coords[1])]


class Menu:
    """
    Main menu and other pre-game features
    """

    def __init__(self, surface):
        """
        Constructor of menu
        :param surface: Pygame Surface object - target surface
        """
        self.surface = surface
        self.mod = "main_menu"


class Gameplay:
    """
    Gameplay itself
    """

    def __init__(self, surface):
        """
        Constructor of gameplay
        :param surface: Pygame Surface object - target surface
        """
        self.surface = surface
        self.clock = pg.time.Clock()
        self.map = reg_map.Map(surface, [SCREEN_WIDTH, SCREEN_HEIGHT])
        self.settler = obj.Settler(self.surface, [40, 20], 20)
        self.list_solid_object = []

        for i in range(self.map.height):
            for j in range(self.map.width):
                if self.map.field[i][j].pre_object == "tree":
                    self.list_solid_object.append(obj.Tree(self.surface, [j, i]))
                elif self.map.field[i][j].pre_object == "bush":
                    self.list_solid_object.append(obj.Bush(self.surface, [j, i]))
                elif self.map.field[i][j].pre_object == "cliff":
                    self.list_solid_object.append(obj.Cliff(self.surface, [j, i]))

        self.list_effects = []
        self.list_loot = []
        self.chosen_map_object = None
        self.picked_task = None
        self.finished = False

    def create_new_animal(self):
        """
        Randomly spawn new animal on the border of the map
        """
        pass

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

        for loot_item in self.list_loot:
            loot_item.draw()

        for effect in self.list_effects:
            effect.draw()

        self.settler.draw()

        if self.chosen_map_object is not None:
            self.chosen_map_object.draw_frame()

    def display_update(self):
        """
        Updating display to reflect changes of objects
        """
        pg.display.update()
        self.clock.tick(feat.FPS)

    def process_input(self):
        """
        Processing all player input
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.chosen_map_object is None:
                        self.finished = True
                    else:
                        self.chosen_map_object.is_chosen = False
                        self.chosen_map_object = None

            elif event.type == pg.MOUSEBUTTONDOWN:
                # First, clicking on the interface buttons is checked

                # Then, clicking on the objects is checked
                if self.picked_task is None:

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

                    if none_is_chosen:
                        self.chosen_map_object = None

                else:
                    if feat.TASKS[self.picked_task] == "object_task":
                        target_object = None

                        for solid_object in self.list_solid_object:
                            if obj.is_picked(event, solid_object.coord):
                                target_object = solid_object
                                continue

                        for loot_item in self.list_loot:
                            if obj.is_picked(event, loot_item.coord):
                                target_object = loot_item
                                continue

                        if target_object is not None:
                            self.settler.task = obj.ObjectTask(self.picked_task, target_object)

                        else:
                            pass  # need to send an error message "no object selected" to the interface

                    else:
                        object_interferes = False

                        for solid_object in self.list_solid_object:
                            if obj.is_picked(event, solid_object.coord):
                                object_interferes = True
                                continue

                        for loot_item in self.list_loot:
                            if obj.is_picked(event, loot_item.coord):
                                object_interferes = True
                                continue

                        if not object_interferes:
                            self.settler.task = obj.TileTask(self.picked_task, pixels2tiles(event.pos))

    def move_creatures(self):
        """
        Moving every creation
        """
        for solid_object in self.list_solid_object:
            if hasattr(solid_object, 'move'):
                solid_object.move(self.map)

        self.settler.move(self.map)

    def ai_acts(self):
        """
        Acting of artificial intelligence of animals
        """
        for solid_object in self.list_solid_object:
            if hasattr(solid_object, 'decide_to_move'):
                solid_object.decide_to_move()
            if hasattr(solid_object, 'decide_to_attack'):
                solid_object.decide_to_attack()

    def remove_solid_object(self):
        """
        Removing dead animals and settler, destroyed constructions and nature objects from lists
        """
        for solid_object in self.list_solid_object:
            if solid_object.hit_points < 0:
                self.list_solid_object.remove(solid_object)

    def remove_effects(self):
        """
        Removing effects that are too old
        """
        for effect in self.list_effects:
            if effect.age > effect.lifetime:
                self.list_effects.remove(effect)


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game = Gameplay(screen)

while not game.finished:
    game.draw_map()
    game.draw_objects()
    game.process_input()
    game.move_creatures()
    game.display_update()

pg.quit()
