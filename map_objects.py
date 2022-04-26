import pygame as pg
from map import TILE_SIZE

COLORS = {
    "white": (255, 255, 255)
}


class MapObject:
    """
    Any changeable map object
    """

    def __init__(self, surface, coord):
        """
        Universal basic constructor of map object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        self.surface = surface
        self.coord = coord
        self.draw_features = {
            "default": [0.0, 0.0, "def_object.png"]
        }
        self.draw_box = ((coord[0] - self.draw_features["default"][0]) * TILE_SIZE,
                         (coord[1] - self.draw_features["default"][1]) * TILE_SIZE,
                         (1 + 2 * self.draw_features["default"][1]) * TILE_SIZE,
                         (1 + self.draw_features["default"][1]) * TILE_SIZE)
        self.texture = pg.transform.scale(pg.image.load("textures/def_object.png"),
                                          ((1 + 2 * self.draw_features["default"][1]) * TILE_SIZE,
                                           (1 + self.draw_features["default"][1]) * TILE_SIZE))
        self.is_chosen = False
        self.type = "def_object"

    def choose(self, event):
        """
        Choice object be mouse click
        :param event: Pygame event object - MOUSEBOTTONDOWN event from queue
        :return: bool - is object chosen
        """
        pos = event.get_pos()
        if abs(pos[0] - self.coord[0] * TILE_SIZE) <= TILE_SIZE and abs(
                pos[1] - self.coord[1] * TILE_SIZE) <= TILE_SIZE:
            self.is_chosen = True

        return self.is_chosen

    def draw(self):
        """
        Drawing object in the current window
        """
        self.surface.blit(self.texture, self.draw_box)
        if self.is_chosen:
            pg.draw.rect(self.surface, COLORS["white"], self.draw_box, 3)

    def safe(self, file):
        """
        Writing information about an object to a save file
        :param file: TextIO object - Output stream to an external save file
        """
        file.write("type: " + self.type + ", coord: " + self.coord + " ")


class SolidObject(MapObject):
    """
    Material object with limited hit points that can only exist on the map
    """

    def __init__(self, surface, coord, hit_points):
        """
        Universal constructor of solid object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord)
        self.full_hit_points = 10
        self.hit_points = hit_points
        self.type = "def_solid_object"

    def safe(self, file):
        super().safe(file)
        file.write("hit_points: " + str(self.hit_points) + " ")

    def take_damage(self, damage):
        """
        Taking damage by creature
        :param damage: damage done to an object
        :return effect
        """
        self.hit_points -= damage
        # need to return effect


class Creature(SolidObject):
    """
    Creature that can move and proceed more complex tasks
    """

    def __init__(self, surface, coord, hit_points):
        """
        Universal constructor of creature
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.0, 0.0, "def_creation.png"],
            "up": [0.0, 0.0, "def_creation.png"],
            "down": [0.0, 0.0, "def_creation.png"],
            "left": [0.0, 0.0, "def_creation.png"],
            "right": [0.0, 0.0, "def_creation.png"]
        }
        self.texture = pg.transform.scale(pg.image.load("textures/def_creation.png"),
                                          ((1 + 2 * self.draw_features["default"][1]) * TILE_SIZE,
                                           (1 + self.draw_features["default"][1]) * TILE_SIZE))
        self.speed = 0.05  # Base value [tile/tick]
        self.damage = 1.0  # Base value [hit point]
        self.melee_cooldown = 60.0  # Base value [tick]
        self.path = []
        self.direction = [0, 0]
        self.type = "def_creation"

    def update_image(self):
        """
        Updating the texture and draw box of creature in case it was moving
        :return:
        """
        pass  # need to update texture and draw_box according to direction & draw_features

    def pathfinder(self, goal_coord, region_map, list_solid_object):
        """
        Finding the best way to the goal on the map
        :param goal_coord: list[int, int] -
        :param region_map: Map object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: list[list[int, int],...] - list of tiles to go through
        """
        pass  # need to solve the problem of finding the shortest path in the maze

    def define_direction(self, next_coord):
        """
        Moving to the next tile along the path
        :param next_coord: list[int, int] - coordinates of the next tile
        :return: [float, float] - massive of coordinates direction velocity vector
        """
        if next_coord[0] < self.coord[0]:
            if next_coord[1] < self.coord[1]:
                return [-1 / (2**0.5), -1 / (2**0.5)]
            if next_coord[1] > self.coord[1]:
                return [-1 / (2**0.5), 1 / (2**0.5)]
            return [-1, 0]

        if next_coord[0] > self.coord[0]:  # check if next_coord[x] > self.coord[x]
            if next_coord[1] < self.coord[1]:
                return [1 / (2 ** 0.5), -1 / (2 ** 0.5)]
            if next_coord[1] > self.coord[1]:
                return [1 / (2 ** 0.5), 1 / (2 ** 0.5)]
            return [1, 0]
        if next_coord[1] > self.coord[1]:
            return [0, 1]
        if next_coord[1] < self.coord[1]:
            return [0, -1]

    def move(self):
        """
        Moving to its goal
        """
        pass  # need to describe moving along the path from tile to tile

    def death(self):
        """
        Processing of death effects
        """
        effect_texture = pg.transform.scale(pg.image.load("blood.png"), (TILE_SIZE, TILE_SIZE))
        effect_lifetime = 300
        death_effect = Effect(self.surface, self.coord, effect_texture, effect_lifetime)
        return death_effect
        # need to return corpse


class Animal(Creature):
    """
    Animals controlled by AI
    """

    def __init__(self, surface, coord, hit_points):
        """
        Universal constructor of animal
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.activity_rate = 0.1  # Base value, some relative coefficient
        self.is_aggressive = False
        self.type = "def_animal"

    def decide_to_move(self):
        pass  # need to call pathfinder with random chance


class Settler(Creature):
    """
    Settler controlled by player
    """

    def __init__(self, surface, coord, hit_points):
        """
        Constructor of settler
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_box = (coord[0] * TILE_SIZE, coord[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.texture = pg.transform.scale(pg.image.load("textures/settler.png"), (TILE_SIZE, TILE_SIZE))
        self.hit_points = 20.0
        self.damage = 2.0
        self.type = "settler"

    def death(self):
        """
        Processing of death effects especially for settler
        """
        super().death()
        return


class Deer(Animal):
    """
    Large herbivore animal
    """

    def __init__(self, surface, coord, hit_points):
        """
        Constructor of deer
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        # self.draw_box
        self.texture = pg.transform.scale(pg.image.load("textures/deer.png"), (TILE_SIZE, TILE_SIZE))
        self.hit_points = 30.0
        self.speed = 0.8
        self.damage = 0.5
        self.melee_cooldown = 120.0
        self.type = "deer"


class Wolf(Animal):
    """
    Medium size predatory animal
    """

    def __init__(self, surface, coord, hit_points):
        """
        Constructor of wolf
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        # self.draw_box
        self.texture = pg.transform.scale(pg.image.load("textures/wolf.png"), (TILE_SIZE, TILE_SIZE))
        self.speed = 0.7
        self.hit_points = 16.0
        self.damage = 3.0
        self.type = "wolf"


class Turtle(Animal):
    """
    Small herbivore in a shell
    """

    def __init__(self, surface, coord, hit_points):
        """
        Constructor of turtle
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        # self.draw_box
        self.texture = pg.transform.scale(pg.image.load("textures/turtle.png"), (TILE_SIZE, TILE_SIZE))
        self.speed = 0.2
        self.damage = 0.5
        self.melee_cooldown = 80.0
        self.type = "turtle"


class NatureObject(SolidObject):
    """
    Solid object of flora or inanimate nature, impassable
    """

    def __init__(self, surface, coord, hit_points):
        """
        Universal constructor of nature object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.res_type = None
        self.res_quantity = 0
        self.type = "def_nature_object"

    def destroy(self):
        """
        Destruction triggered from the outside
        :return: Resources object - resources obtained when an object is destroyed
        """
        pass  # need to create loot & (possibly) effects in place of destroyed object


class Cliff(NatureObject):
    """
    Part of the rock that rises above the map
    """

    def __init__(self, surface, coord, hit_points):
        """
        Constructor of cliff
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.texture = pg.transform.scale(pg.image.load("textures/cliff.png"), (TILE_SIZE, TILE_SIZE))
        self.res_type = "stone"
        self.res_quantity = 30
        self.type = "cliff"


class Plant(NatureObject):
    """
    Representative of the local flora
    """

    def __init__(self, surface, coord, hit_points):
        """
        Universal constructor of plant
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.res_type = "wood"
        self.type = "def_plant"


class Tree(Plant):
    """
    Large plant, contains a lot of wood
    """

    def __init__(self, surface, coord, hit_points):
        """
        Constructor of tree
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        # self.draw_box
        self.texture = pg.transform.scale(pg.image.load("textures/tree.png"), (TILE_SIZE, TILE_SIZE))
        self.res_quantity = 150
        self.type = "tree"


class Effect(MapObject):
    """
    Intangible effect that exists for a limited time
    """

    def __init__(self, surface, coord, texture, lifetime):
        """
        Constructor of any effect
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.texture = texture
        self.lifetime = lifetime
        self.age = 0
