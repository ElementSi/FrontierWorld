import pygame as pg
from map import TILE_SIZE


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
        self.draw_box = (coord[0] * TILE_SIZE, coord[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.texture = pg.transform.scale(pg.image.load("textures/default.png"), (TILE_SIZE, TILE_SIZE))
        self.is_chosen = False
        self.type = "def_object"

    def choose(self, event):
        """
        Choice object be mouse click
        :param event: Pygame event object - MOUSEBOTTONDOWN event from queue
        :return: bool - is object chosen
        """
        pos = event.get_pos()
        if abs(pos[0] - self.coord[0]*TILE_SIZE) <= TILE_SIZE and abs(pos[1] - self.coord[1]*TILE_SIZE) <= TILE_SIZE:
            self.is_chosen = True
        else:
            self.is_chosen = True

        return self.is_chosen

    def draw(self):
        """
        Drawing object in the current window
        """
        self.surface.blit(self.texture, self.draw_box)
        if self.is_chosen:
            white = (255, 255, 255)
            pg.draw.rect(self.surface, white, self.draw_box, 3)

    def safe(self, file):
        """
        Writing information about an object to a save file
        :param file: TextIO object - Output stream to an external save file
        """
        file.write("type: " + self.type + ", coord: " + self.coord)


class SolidObject(MapObject):
    """
    Material object with limited hit points that can only exist on the map
    """
    def __init__(self, surface, coord):
        """
        Universal constructor of solid object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.hit_points = 10
        self.type = "def_solid_object"

    def safe(self, file):
        super().safe(file)
        file.write("hit_points: " + str(self.hit_points))

    def take_damage(self, damage):
        """
        Taking damage by creature
        :param damage: damage done to an object
        :return effect
        """
        self.hit_points -= damage
        # return effect


class Creature(SolidObject):
    """
    Creature that can move and proceed more complex tasks
    """
    def __init__(self, surface, coord):
        """
        Universal constructor of creature
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.speed = 0.05  # Base value [tile/tick]
        self.damage = 1.0  # Base value [hit point]
        self.melee_cooldown = 60.0  # Base value [tick]
        self.type = "def_creation"

    def update_draw_box(self):
        self.draw_box = (self.coord[0] * TILE_SIZE, self.coord[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def pathfinder(self, goal_coord, region_map, list_solid_object):
        """
        Finding the best way to the goal on the map
        :param goal_coord: list[int, int] -
        :param region_map: Map object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: list[list[int, int],...] - list of tiles to go through
        """
        pass  # Надо решить задачу поиска кратчайшего пути в лабиринте


class Animal(Creature):
    """
    Animals controlled by AI
    """
    def __init__(self, surface, coord):
        """
        Universal constructor of animal
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.activity_rate = 0.1  # Base value, some relative coefficient
        self.type = "def_animal"

    def death(self):
        """
        Processing of death effects
        """
        # return effect

    def move(self):
        """
        Moving to its goal
        """
        pass


class Settler(Creature):
    """
    Settler controlled by player
    """
    def __init__(self, surface, coord):
        """
        Constructor of settler
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.texture = pg.transform.scale(pg.image.load("textures/settler.png"), (TILE_SIZE, TILE_SIZE))
        self.hit_points = 20.0
        self.damage = 2.0
        self.type = "settler"

    def death(self):
        """
        Processing of death effects
        """
        # RED = (255, 0, 0)
        # font = pg.font.Font(None, 100)
        # message = font.render("Game over", True, RED)
        # place = message.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        # self.surface.blit(message, place)
        # return effect



class Deer(Animal):
    """
    Large herbivore animal
    """
    def __init__(self, surface, coord):
        """
        Constructor of deer
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
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
    def __init__(self, surface, coord):
        """
        Constructor of wolf
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.texture = pg.transform.scale(pg.image.load("textures/wolf.png"), (TILE_SIZE, TILE_SIZE))
        self.speed = 0.7
        self.hit_points = 16.0
        self.damage = 3.0
        self.type = "wolf"


class Turtle(Animal):
    """
    Small herbivore in a shell
    """
    def __init__(self, surface, coord):
        """
        Constructor of turtle
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.texture = pg.transform.scale(pg.image.load("textures/turtle.png"), (TILE_SIZE, TILE_SIZE))
        self.speed = 0.2
        self.damage = 0.5
        self.melee_cooldown = 80.0
        self.type = "turtle"


class NatureObject(SolidObject):
    """
    Solid object of flora or inanimate nature, impassable
    """
    def __init__(self, surface, coord):
        """
        Universal constructor of nature object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.res_type = None
        self.res_quantity = 0
        self.type = "def_nature_object"

    def destroy(self):
        """
        Destruction triggered from the outside
        :return: Resources object - resources obtained when an object is destroyed
        """
        pass


class Cliff(NatureObject):
    """
    Part of the rock that rises above the map
    """
    def __init__(self, surface, coord):
        """
        Constructor of cliff
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        """
        super().__init__(surface, coord)
        self.res_type = "stone"
        self.res_quantity = 30
        self.type = "def_nature_object"


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
