import random as rnd

import pygame as pg

import constants as const


def create_draw_box(coord, draw_features, orientation):
    """
    Creating draw box according to draw features of object
    :param coord: list[float, float] - coordinates of object
    :param draw_features: dict{string: [float, float, string]} - unique draw features
    :param orientation: string - orientation of object
    :return: Pygame Rect object - rect into which the texture of the object fits
    """
    return ((coord[0] - draw_features[orientation][0]) * const.TILE_SIZE,
            (coord[1] - draw_features[orientation][1]) * const.TILE_SIZE,
            (1 + 2 * draw_features[orientation][0]) * const.TILE_SIZE,
            (1 + draw_features[orientation][1]) * const.TILE_SIZE)


def create_texture(draw_features, orientation):
    """
    Creating texture according to draw features of object
    :param draw_features:additional size that extend the image of the object beyond the limits of the tile
    :param orientation: string - orientation of object
    :return: Pygame Surface object - image of map object
    """
    return pg.transform.scale(pg.image.load("assets/textures/{}".format(draw_features[orientation][2])),
                              ((1 + 2 * draw_features[orientation][0]) * const.TILE_SIZE,
                               (1 + draw_features[orientation][1]) * const.TILE_SIZE))


def is_picked(event, coord):
    """
    Choice object be mouse click
    :param event: Pygame event object - MOUSEBOTTONDOWN event from queue
    :param coord: list[float, float] - coordinates of object
    :return: bool - is object chosen
    """
    pos = event.pos
    return abs(pos[0] - (coord[0] + 0.5) * const.TILE_SIZE) < const.TILE_SIZE / 2 and abs(
        pos[1] - (coord[1] + 0.5) * const.TILE_SIZE) < const.TILE_SIZE / 2


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
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.type = "def_object"

    def draw(self):
        """
        Drawing object in the current window
        """
        self.surface.blit(self.texture, self.draw_box)

    def safe(self, file):
        """
        Writing information about an object to a save file
        :param file: TextIO object - Output stream to an external save file
        """
        file.write("type: " + self.type + ", coord: " + self.coord + " ")


class SolidObject(MapObject):
    """
    Material object with limited hit points
    """

    def __init__(self, surface, coord, hit_points=10.0):
        """
        Universal constructor of solid object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord)
        self.full_hit_points = 10.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.is_chosen = False
        self.type = "def_solid_object"

    def choose(self, event):
        """
        Choice object be mouse click
        :param event: Pygame event object - MOUSEBOTTONDOWN event from queue
        :return: bool - is object chosen
        """
        self.is_chosen = is_picked(event, self.coord)
        return self.is_chosen

    def draw_frame(self):
        """
        Drawing frame around the chosen object
        """
        tile_box = (self.coord[0] * const.TILE_SIZE,
                    self.coord[1] * const.TILE_SIZE,
                    const.TILE_SIZE,
                    const.TILE_SIZE)
        pg.draw.rect(self.surface, const.COLORS["white"], tile_box, 3)

    def safe(self, file):
        """
        Writing information about an object to a save file
        :param file: TextIO object - Output stream to an external save file
        """
        super().safe(file)
        file.write("hit_points: " + str(self.hit_points) + " ")

    def take_damage(self, damage):
        """
        Taking damage by creature
        :param damage: damage done to an object
        :return effect
        """
        self.hit_points -= damage


class NatureObject(SolidObject):
    """
    Solid object of flora or inanimate nature, impassable
    """

    def __init__(self, surface, coord, hit_points=10.0):
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

    def __init__(self, surface, coord, hit_points=30.0):
        """
        Constructor of cliff
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.0, 0.0, "cliff.png"]
        }
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.full_hit_points = 30.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.res_type = "stone"
        self.res_quantity = 30
        self.type = "cliff"


class Plant(NatureObject):
    """
    Representative of the local flora
    """

    def __init__(self, surface, coord, hit_points=10.0):
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

    def __init__(self, surface, coord, hit_points=20.0):
        """
        Constructor of tree
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.75, 1.5, "tree.png"]
        }
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.full_hit_points = 20.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.res_quantity = 150
        self.type = "tree"


class Bush(Plant):
    """
    Low-growing plant that contains berries
    """

    def __init__(self, surface, coord, hit_points=10.0):
        """
        Constructor of tree
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.125, 0.25, "bush.png"],
            "riped": [0.125, 0.25, "bush_riped.png"]
        }
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.res_quantity = 25
        self.ripening_time = 3600
        self.time_from_harvest = rnd.randint(0, 3600)
        self.is_riped = False
        self.type = "bush"

    def harvest(self):
        """
        Harvesting berries ripened on a bush
        :return: Resources object - harvested berries
        """
        self.time_from_harvest = 0
        self.is_riped = False
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        # need to return berries

    def ripe(self):
        """
        Ripening of berries through time
        """
        if self.time_from_harvest < self.ripening_time:
            self.time_from_harvest += 1
        elif (self.time_from_harvest == self.ripening_time) and not self.is_riped:
            self.is_riped = True
            self.draw_box = create_draw_box(self.coord, self.draw_features, "riped")
            self.texture = create_texture(self.draw_features, "riped")


class Construction(SolidObject):
    """
    Constructions built by player
    """

    def __init__(self, surface, coord, hit_points=10.0):
        """
        Universal constructor of construction
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        """
        super().__init__(surface, coord, hit_points)
        self.res_type = None
        self.res_quantity = 0
        self.type = "def_construction"


class Wall(Construction):
    """
    Basic impassable construction
    """

    def __init__(self, surface, coord, hit_points, res_type):
        """
        Constructor of wall
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        :param res_type: string - type of resource the wall is made up of
        """
        super().__init__(surface, coord, hit_points)
        self.draw_features = {
            "default": [0.0, 0.0, "wall.png"]
        }
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.res_type = res_type
        self.res_quantity = 20
        self.type = "wall"


class Door(Construction):
    """
    Basic passable construction
    """

    def __init__(self, surface, coord, hit_points, res_type, list_solid_object):
        """
        Constructor of door
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of object
        :param hit_points: int - current object hit points
        :param res_type: string - type of resource the door is made up of
        """
        super().__init__(surface, coord, hit_points)

        is_wall_n_or_s_ward = False  # is there a wall south or north of the door

        for solid_object in list_solid_object:
            if solid_object.type == "wall" or solid_object.type == "door":
                if abs(int(solid_object.coord[1]) - int(self.coord[1])) == 1:
                    is_wall_n_or_s_ward = True

        if is_wall_n_or_s_ward:
            self.draw_features = {
                "closed": [0.0, 0.0, "door_n2s_closed.png"],
                "opened": [0.0, 0.0, "door_n2s_opened.png"]
            }

        else:
            self.draw_features = {
                "closed": [0.0, 0.0, "door_e2w_closed.png"],
                "opened": [0.0, 0.0, "door_e2w_opened.png"]
            }

        self.draw_box = create_draw_box(self.coord, self.draw_features, "closed")
        self.texture = create_texture(self.draw_features, "closed")
        self.res_type = res_type
        self.res_quantity = 10
        self.is_opened = False
        self.type = "door"

    def open(self):
        """
        Opening for the settler
        """
        self.is_opened = True
        self.draw_box = create_draw_box(self.coord, self.draw_features, "opened")
        self.texture = create_texture(self.draw_features, "opened")

    def close(self):
        """
        Closing for the settler
        """
        self.is_opened = False
        self.draw_box = create_draw_box(self.coord, self.draw_features, "closed")
        self.texture = create_texture(self.draw_features, "closed")


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
        self.type = "effect"

    def aging(self):
        self.age += 1


class Loot(MapObject):
    """
    Indestructible material object that can be taken into inventory
    """

    def __init__(self, surface, coord):
        """
        Universal constructor of loot
        :param surface: Pygame Surface object - target window
        :param coord: list[int, int] - coordinates of object
        """
        super().__init__(surface, coord)
        self.is_chosen = False
        self.type = "def_loot"

    def choose(self, event):
        """
        Choice object be mouse click
        :param event: Pygame event object - MOUSEBOTTONDOWN event from queue
        :return: bool - is object chosen
        """
        self.is_chosen = is_picked(event, self.coord)
        return self.is_chosen

    def draw_frame(self):
        """
        Drawing frame around the chosen object
        """
        tile_box = (self.coord[0] * const.TILE_SIZE,
                    self.coord[1] * const.TILE_SIZE,
                    const.TILE_SIZE,
                    const.TILE_SIZE)
        pg.draw.rect(self.surface, const.COLORS["white"], tile_box, 3)


class Corpse(Loot):
    """
    Corpse that remains after the death of a living creature
    """

    def __init__(self, surface, coord, creature_type):
        """
        Constructor of corpse
        :param surface: Pygame Surface object - target window
        :param coord: list[int, int] - coordinates of object
        :param creature_type: string - type of dead creature
        """
        super().__init__(surface, coord)
        self.draw_features = {
            "settler": [0.0, 0.5, "corpse_settler.png"],
            "deer": [0.25, 0.0, "corpse_deer.png"],
            "wolf": [0.5, 0.5, "corpse_wolf.png"],
            "turtle": [0.0, 0.0, "corpse_turtle.png"]
        }
        self.draw_box = create_draw_box(self.coord, self.draw_features, creature_type)
        self.texture = create_texture(self.draw_features, creature_type)
        self.entrails_features = {
            "settler": 125,
            "deer": 200,
            "wolf": 75,
            "turtle": 25
        }
        self.meat_quantity = self.entrails_features[creature_type]
        self.creation_type = creature_type
        self.type = "corpse"


class Resources(Loot):
    """
    Resources that remain after the destruction of a natural object or structure
    """

    def __init__(self, surface, coord, resource_type, res_quantity):
        """
        Constructor of corpse
        :param surface: Pygame Surface object - target window
        :param coord: list[int, int] - coordinates of object
        :param resource_type: string - type of dropped resource
        :param res_quantity: int - type of dropped resources
        """
        super().__init__(surface, coord)
        self.draw_features = {
            "wood": [0.0, 0.0, "resources_wood.png"],
            "stone": [0.0, 0.0, "resources_stone.png"],
            "berries": [0.0, 0.0, "resources_berries.png"],
            "meet": [0.0, 0.0, "resources_meet.png"]
        }
        self.draw_box = create_draw_box(self.coord, self.draw_features, resource_type)
        self.texture = create_texture(self.draw_features, resource_type)
        self.full_res_quantity = 75
        self.res_quantity = res_quantity
        self.resource_type = resource_type
        self.type = "resources"

    def draw(self):
        super().draw()
        # need to draw the quantity of resources in this stack

    def take(self, res_quantity):
        """
        Taking a certain quantity of resources from stack
        :param res_quantity: int - quantity of taken resources
        :return int - how many resources of this type still need to be obtained
        """
        self.res_quantity -= res_quantity
        if self.res_quantity >= 0:
            return 0
        else:
            return -self.res_quantity
