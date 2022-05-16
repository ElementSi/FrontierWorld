import pygame as pg
import numpy as np
import random as rnd

import constants as const
import map_objects as objects
import dijkstra as dijkstra


class Task:
    """
    Task for the colonist
    """

    def __init__(self, task_type):
        self.task_type = task_type
        self.is_started = False
        self.is_finished = False


class ObjectTask(Task):
    """
    Task whose purpose is to interact with an object
    """

    def __init__(self, task_type, target_object):
        super().__init__(task_type)
        self.target_object = target_object


class TileTask(Task):
    """
    Task whose goal is a tile
    """

    def __init__(self, task_type, target_tile):
        super().__init__(task_type)
        self.target_tile = target_tile


class Creature(objects.SolidObject):
    """
    Creature that can move and proceed more complex tasks
    """

    def __init__(self, surface, coord, hit_points=10.0):
        """
        Universal constructor of creature
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.0, 0.0, "def_creature_west.png"],
            "north": [0.0, 0.0, "def_creature_north.png"],
            "south": [0.0, 0.0, "def_creature_south.png"],
            "west": [0.0, 0.0, "def_creature_west.png"],
            "east": [0.0, 0.0, "def_creature_east.png"]
        }
        self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "default")
        self.texture = objects.create_texture(self.draw_features, "default")
        self.speed = 0.1  # Base value [tile/tick]
        self.damage = 1.0  # Base value [hit point]
        self.melee_cooldown = 60.0  # Base value [tick]
        self.path = []
        self.direction = [0, 0]
        self.task = None
        self.type = "def_creature"

    def update_image(self):
        """
        Updating the texture and draw box of creature in case it was moving
        """
        if self.direction[0] < 0:
            self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "west")
            self.texture = objects.create_texture(self.draw_features, "west")

        elif self.direction[0] > 0:
            self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "east")
            self.texture = objects.create_texture(self.draw_features, "east")

        elif self.direction[1] < 0:
            self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "north")
            self.texture = objects.create_texture(self.draw_features, "north")

        elif self.direction[1] > 0:
            self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "south")
            self.texture = objects.create_texture(self.draw_features, "south")

        else:
            self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "default")
            self.texture = objects.create_texture(self.draw_features, "default")

    def pathfinder(self, goal_coord, region_map, list_solid_object):
        """
        Finding the best way to the goal on the map
        :param goal_coord: list[int, int] - coordinates' of target cell
        :param region_map: GameMap object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: list[list[float, float],...] - list of tiles to go through
        """
        path = dijkstra.dijkstra_logic([int(self.coord[0]),
                                        int(self.coord[1])],
                                       goal_coord,
                                       region_map,
                                       list_solid_object)
        return path

    def define_direction(self, next_coord):
        """
        Moving to the next tile along the path
        :param next_coord: list[int, int] - coordinates of the next tile
        :return: [float, float] - massive of coordinates direction velocity unit vector
        """
        if next_coord[0] < self.coord[0]:
            if next_coord[1] < self.coord[1]:
                return [-1 / (2 ** 0.5), -1 / (2 ** 0.5)]
            if next_coord[1] > self.coord[1]:
                return [-1 / (2 ** 0.5), 1 / (2 ** 0.5)]
            return [-1, 0]

        elif next_coord[0] > self.coord[0]:
            if next_coord[1] < self.coord[1]:
                return [1 / (2 ** 0.5), -1 / (2 ** 0.5)]
            if next_coord[1] > self.coord[1]:
                return [1 / (2 ** 0.5), 1 / (2 ** 0.5)]
            return [1, 0]

        elif next_coord[1] > self.coord[1]:
            return [0, 1]

        elif next_coord[1] < self.coord[1]:
            return [0, -1]

    def move(self, region_map):
        """
        Changing coordinates of the creature due to its movement
        :param region_map: GameMap object - map of the game region
        """
        if len(self.path) > 0:
            if self.direction == [0, 0]:
                self.direction = self.define_direction(self.path[0])

            max_shift = self.speed * region_map.field[int(self.coord[1] + 0.5)][int(self.coord[0] + 0.5)].speed_mod
            #                        checking speed modifier of current tile

            next_tile_dist = ((self.coord[0] - self.path[0][0]) ** 2 + (self.coord[1] - self.path[0][1]) ** 2) ** 0.5

            if max_shift >= next_tile_dist:
                self.coord[0] = self.path[0][0]
                self.coord[1] = self.path[0][1]
                self.path.pop(0)
                if len(self.path) > 0:
                    self.direction = self.define_direction(self.path[0])

            else:
                self.coord[0] += max_shift * self.direction[0]
                self.coord[1] += max_shift * self.direction[1]

        if len(self.path) == 0:
            self.direction = [0, 0]

        self.update_image()

    def go_to(self, region_map, list_solid_object):
        """
        Moving to a given tile along a suitable path
        :param region_map: GameMap object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        """
        if not self.task.is_started:
            if len(self.path) > 0:
                self.path = [self.path[0]] + self.pathfinder(self.task.target_tile, region_map, list_solid_object)
            else:
                self.path = self.pathfinder(self.task.target_tile, region_map, list_solid_object)
            self.task.is_started = True

        if len(self.path) == 0:
            self.task.is_finished = True

    def attack(self):
        pass  # approach a specific creature and beat it

    def death(self):
        """
        Processing of death effects
        :return: Effect object - some kind of effect accompanying death
                 Corpse object - corpse of dead creature
        """
        effect_texture = pg.transform.scale(pg.image.load("blood.png"), (const.TILE_SIZE, const.TILE_SIZE))
        effect_lifetime = 300
        death_effect = objects.Effect(self.surface, self.coord, effect_texture, effect_lifetime)
        return death_effect
        # need to return corpse


class Animal(Creature):
    """
    Animals controlled by AI
    """

    def __init__(self, surface, coord, hit_points=10.0, was_attacked=False):
        """
        Universal constructor of animal
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.activity_rate = 0.1  # Base value, some relative coefficient
        self.was_attacked = was_attacked
        self.type = "def_animal"

    def decide_to_move(self, game_map):
        if rnd.random() < 0.01 and len(self.path) == 0:
            self.task = TileTask("go_to", [rnd.randint(0, game_map.width - 1), rnd.randint(0, game_map.height - 1)])

    def decide_to_attack(self):
        pass  # need to create task "attack" if animal was attacked


class Settler(Creature):
    """
    Settler controlled by player
    """

    def __init__(self, surface, coord, hit_points=20.0):
        """
        Constructor of settler
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.0, 0.5, "settler_south.png"],
            "north": [0.0, 0.5, "settler_north.png"],
            "south": [0.0, 0.5, "settler_south.png"],
            "west": [0.0, 0.5, "settler_west.png"],
            "east": [0.0, 0.5, "settler_east.png"]
        }
        self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "default")
        self.texture = objects.create_texture(self.draw_features, "default")
        self.full_hit_points = 20.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.damage = 2.0
        self.type = "settler"

    def draw(self):
        if len(self.path) > 0:
            transparent_surface = pg.Surface(
                (self.surface.get_size()),
                pg.SRCALPHA
            )

            array_path = np.array(self.path, float)
            array_path = np.insert(array_path, 0, [self.coord], axis=0)
            pg.draw.aalines(
                transparent_surface,
                const.COLORS["white"] + (120,),
                False,
                array_path * const.TILE_SIZE + 12
            )

            self.surface.blit(transparent_surface, (0, 0))

        super().draw()

    def chop(self):
        pass  # approach a specific tree/bush and cut it down

    def harvest_berries(self):
        pass  # approach a specific riped bush and pick berries

    def construct(self):
        pass
        # check if there are enough resources in the inventory;
        # if there are enough resources, go to a specific tile and create a structure there,
        # if not, find more resources on the map

    def pick_up_loot(self):
        pass  # approach a specific loot item and take all the resources from it

    def dig(self):
        pass  # approach a specific cliff and dig it

    def death(self):
        """
        Processing of death effects especially for settler
        """
        super().death()
        #  maybe need to add smth like drop of resources from the inventory


class Deer(Animal):
    """
    Large herbivore animal
    """

    def __init__(self, surface, coord, hit_points=30.0):
        """
        Constructor of deer
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.5, 0.5, "deer_west.png"],
            "north": [0.0, 0.5, "deer_north.png"],
            "south": [0.0, 0.5, "deer_south.png"],
            "west": [0.5, 0.5, "deer_west.png"],
            "east": [0.5, 0.5, "deer_east.png"]
        }
        self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "default")
        self.texture = objects.create_texture(self.draw_features, "default")
        self.full_hit_points = 30.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.speed = 0.05
        self.damage = 0.5
        self.melee_cooldown = 120.0
        self.type = "deer"


class Wolf(Animal):
    """
    Medium size predatory animal
    """

    def __init__(self, surface, coord, hit_points=16.0):
        """
        Constructor of wolf
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.25, 0.0, "wolf_west.png"],
            "north": [0.0, 0.0, "wolf_north.png"],
            "south": [0.0, 0.0, "wolf_south.png"],
            "west": [0.25, 0.0, "wolf_west.png"],
            "east": [0.25, 0.0, "wolf_east.png"]
        }
        self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "default")
        self.texture = objects.create_texture(self.draw_features, "default")
        self.speed = 0.7
        self.full_hit_points = 16.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.damage = 3.0
        self.type = "wolf"


class Turtle(Animal):
    """
    Small herbivore in a shell
    """

    def __init__(self, surface, coord, hit_points=10.0):
        """
        Constructor of turtle
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.0, 0.0, "turtle_west.png"],
            "north": [0.0, 0.0, "turtle_north.png"],
            "south": [0.0, 0.0, "turtle_south.png"],
            "west": [0.0, 0.0, "turtle_west.png"],
            "east": [0.0, 0.0, "turtle_east.png"]
        }
        self.draw_box = objects.create_draw_box(self.coord, self.draw_features, "default")
        self.texture = objects.create_texture(self.draw_features, "default")
        self.speed = 0.2
        self.damage = 0.5
        self.melee_cooldown = 80.0
        self.type = "turtle"
