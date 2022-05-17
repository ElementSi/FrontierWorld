import pygame as pg
import random as rnd

import constants as const
import interface as interface
import game_map as game_map
import map_objects as objects
import creature as creature


def pixels2tiles(pixel_coords):
    """
    Converting pixel coordinates to tile coordinates
    :param pixel_coords: list[int, int] - coordinates in pixels [x, y]
    :return: list[int, int] - coordinates in tiles [x, y]
    """
    return [pixel_coords[0] // const.TILE_SIZE, pixel_coords[1] // const.TILE_SIZE]


def find_safe_tile(list_solid_object, spawn_box, mode="anywhere"):
    """
    Spawn creatures in a random guaranteed suitable tile
    :param list_solid_object: list[SolidObject object,...] - list of all solid objects
    :param spawn_box: list[int, int] - the size of the area where spawn is allowed
    :param mode: string - spawn mod (everywhere or only at the border)
    :return: list[int, int] - coordinates of suitable tile
    """
    suitable_tile = [0, 0]
    is_found = False

    while not is_found:
        is_found = True
        rnd_coord = [rnd.randint(0, spawn_box[0]), rnd.randint(0, spawn_box[1])]

        if mode == "border":
            if (rnd_coord[0] * rnd_coord[1] != 0) and (rnd_coord[0] != spawn_box[0]) and (rnd_coord[1] != spawn_box[1]):
                is_found = False

        for obj in list_solid_object:
            if (int(obj.coord[0]) == rnd_coord[0]) and (int(obj.coord[1]) == rnd_coord[1]):
                is_found = False

        suitable_tile = rnd_coord

    return suitable_tile


class Gameplay:
    """
    Gameplay itself
    """

    def __init__(self, surface, main_menu):
        """
        Constructor of gameplay
        :param surface: Pygame Surface object - target surface
        """
        self.surface = surface
        self.main_menu = main_menu
        self.clock = pg.time.Clock()
        self.interface = interface.InGameInterface(surface)
        self.game_map = game_map.GameMap(surface, surface.get_size())
        self.list_solid_object = []

        for i in range(self.game_map.height):
            for j in range(self.game_map.width):
                if self.game_map.field[i][j].pre_object == "tree":
                    self.list_solid_object.append(objects.Tree(self.surface, [j, i]))
                elif self.game_map.field[i][j].pre_object == "bush":
                    self.list_solid_object.append(objects.Bush(self.surface, [j, i]))
                elif self.game_map.field[i][j].pre_object == "cliff":
                    self.list_solid_object.append(objects.Cliff(self.surface, [j, i]))
                elif self.game_map.field[i][j].pre_object == "deer":
                    self.list_solid_object.append(creature.Deer(self.surface, [j, i]))
                elif self.game_map.field[i][j].pre_object == "wolf":
                    self.list_solid_object.append(creature.Wolf(self.surface, [j, i]))
                elif self.game_map.field[i][j].pre_object == "turtle":
                    self.list_solid_object.append(creature.Turtle(self.surface, [j, i]))

        self.settler = creature.Settler(self.surface, find_safe_tile(
            self.list_solid_object,
            [self.game_map.width - 1, self.game_map.height - 1],
        ))
        self.list_effects = []
        self.list_loot = []
        self.number_of_animals = 0
        self.scan_time = 0
        self.interface_mod = "default"
        self.chosen_map_object = None
        self.picked_task = None
        self.is_finished = False

    def create_new_animal(self):
        """
        Randomly spawn new animal on the border of the map
        """
        if (pg.time.get_ticks() > self.scan_time + 1000) and (self.number_of_animals < const.ANIMALS_LIMIT):
            rand_num = rnd.random()
            if rand_num < 0.1:
                new_dear = creature.Deer(
                    self.surface,
                    find_safe_tile(self.list_solid_object,
                                   [self.game_map.width - 1, self.game_map.height - 1],
                                   "border"),
                )
                self.list_solid_object.append(new_dear)
                new_dear.path = new_dear.pathfinder(
                    find_safe_tile(self.list_solid_object,
                                   [self.game_map.width - 1, self.game_map.height - 1]),
                    self.game_map,
                    self.list_solid_object
                )
                self.number_of_animals += 1

            elif rand_num < 0.2:
                new_wolf = creature.Wolf(
                    self.surface,
                    find_safe_tile(self.list_solid_object,
                                   [self.game_map.width - 1, self.game_map.height - 1],
                                   "border"),
                )
                self.list_solid_object.append(new_wolf)
                new_wolf.path = new_wolf.pathfinder(
                    find_safe_tile(self.list_solid_object,
                                   [self.game_map.width - 1, self.game_map.height - 1]),
                    self.game_map,
                    self.list_solid_object
                )
                self.number_of_animals += 1

            elif rand_num < 0.3:
                new_turtle = creature.Turtle(
                    self.surface,
                    find_safe_tile(self.list_solid_object,
                                   [self.game_map.width - 1, self.game_map.height - 1],
                                   "border"),
                )
                self.list_solid_object.append(new_turtle)
                new_turtle.path = new_turtle.pathfinder(
                    find_safe_tile(self.list_solid_object,
                                   [self.game_map.width - 1, self.game_map.height - 1]),
                    self.game_map,
                    self.list_solid_object
                )
                self.number_of_animals += 1

            self.scan_time = pg.time.get_ticks()

    def draw_interface(self):
        """
        Drawing in-game interface
        """
        self.interface.draw()

    def draw_map(self):
        """
        Drawing every map tile
        """
        self.game_map.draw()

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

    def update_display(self):
        """
        Updating display to reflect changes of objects
        """
        pg.display.update()
        self.clock.tick(const.FPS)

    def _process_quit(self, event):
        """
        Processing window close button press
        :param event: PyGame event object - pg.QUIT object from queue
        """
        self.is_finished = True

    def _process_keydown(self, event):
        """
        Processing any button from keyboard press
        :param event: PyGame event object - pg.KEYDOWN object from queue
        """
        if event.key == pg.K_ESCAPE:
            if self.chosen_map_object is None:
                self.is_finished = True
            else:
                self.chosen_map_object.is_chosen = False
                self.chosen_map_object = None

    def _process_interface(self, event):
        """
        Processing click on the interface buttons
        :param event: PyGame event object - pg.MOUSEBUTTONDOWN object from queue
        :return: bool - was interface used
        """
        is_interface_used = False

        for button in self.interface.buttons:
            if interface.is_hovered(event, button.draw_box):
                is_interface_used = True
                if button.key == "interface_go_to":
                    self.picked_task = "go_to"
                elif button.key == "interface_menu":
                    self.interface_mod = "menu"
                elif button.key == "interface_main_menu":
                    self.main_menu.is_active = True

        for frame in self.interface.frames:
            if interface.is_hovered(event, frame.draw_box):
                is_interface_used = True

        return is_interface_used

    def _process_if_no_picked_task(self, event):
        """
        Processing click on the game map if task for settler is not picked
        :param event: PyGame event object - pg.MOUSEBUTTONDOWN object from queue
        """
        none_is_chosen = True

        for solid_object in self.list_solid_object:
            if solid_object.choose(event):
                none_is_chosen = False
                self.chosen_map_object = solid_object

        for loot_item in self.list_loot:
            if loot_item.choose(event):
                none_is_chosen = False
                self.chosen_map_object = loot_item

        if self.settler.choose(event):
            none_is_chosen = False
            self.chosen_map_object = self.settler

        if none_is_chosen:
            self.chosen_map_object = None
            self.interface_mod = "default"

        else:
            self.interface_mod = self.chosen_map_object.type

    def _process_if_picked_task(self, event):
        """
        Processing click on the game map if some task for settler is picked
        :param event: PyGame event object - pg.MOUSEBUTTONDOWN object from queue
        """
        if const.TASKS[self.picked_task] == "object_task":
            target_object = None

            for solid_object in self.list_solid_object:
                if objects.is_picked(event, solid_object.coord):
                    target_object = solid_object
                    break

            for loot_item in self.list_loot:
                if objects.is_picked(event, loot_item.coord):
                    target_object = loot_item
                    break

            if target_object is not None:
                self.settler.task = creature.ObjectTask(self.picked_task, target_object)

        else:
            object_interferes = False

            for solid_object in self.list_solid_object:
                if objects.is_picked(event, solid_object.coord):
                    object_interferes = True
                    break

            if not object_interferes:
                self.settler.task = creature.TileTask(self.picked_task, pixels2tiles(event.pos))

        self.picked_task = None

    def process_input(self):
        """
        Processing all player input
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._process_quit(event)

            elif event.type == pg.KEYDOWN:
                self._process_keydown(event)

            elif event.type == pg.MOUSEMOTION:
                self.interface.activate(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                if self._process_interface(event):
                    continue

                if self.picked_task is None:
                    self._process_if_no_picked_task(event)
                else:
                    self._process_if_picked_task(event)

    def update_interface(self):
        """
        Updating the mod of interface according to chosen object
        """
        if (self.interface_mod == "menu") and (self.interface.interface_mod != "menu"):
            self.interface.update_interface("menu")

        elif (self.interface_mod == "default") and (self.interface.interface_mod != "default"):
            self.interface.update_interface("default")

        elif (self.chosen_map_object is not None) and (self.interface.interface_mod != self.chosen_map_object.type):
            self.interface.update_interface(self.chosen_map_object.type)

    def do_tasks(self):
        """
        Execution of tasks by creatures in accordance with the name of the tasks
        """
        if self.settler.task is not None:
            getattr(self.settler, self.settler.task.task_type)(self.game_map, self.list_solid_object)
            if self.settler.task.is_finished:
                self.settler.task = None

        for solid_object in self.list_solid_object:
            if hasattr(solid_object, 'task'):
                if solid_object.task is not None:
                    getattr(solid_object, solid_object.task.task_type)(self.game_map, self.list_solid_object)
                    if solid_object.task.is_finished:
                        solid_object.task = None

    def move_creatures(self):
        """
        Moving every creation
        """
        for solid_object in self.list_solid_object:
            if hasattr(solid_object, 'move'):
                solid_object.move(self.game_map)

        self.settler.move(self.game_map)

    def ai_acts(self):
        """
        Acting of artificial intelligence of animals
        """
        for solid_object in self.list_solid_object:
            if hasattr(solid_object, 'decide_to_move'):
                solid_object.decide_to_move(self.game_map)
            if hasattr(solid_object, 'decide_to_attack'):
                solid_object.decide_to_attack()
