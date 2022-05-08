import pygame as pg
import random as rnd
from game_map import TILE_SIZE
import cmath
import heapq

import constants as const


def create_draw_box(coord, draw_features, orientation):
    """
    Creating draw box according to draw features of object
    :param coord: list[float, float] - coordinates of object
    :param draw_features: dict{string: [float, float, string]} - unique draw features
    :param orientation: string - orientation of object
    :return: Pygame Rect object - rect into which the texture of the object fits
    """
    return ((coord[0] - draw_features[orientation][0]) * TILE_SIZE,
            (coord[1] - draw_features[orientation][1]) * TILE_SIZE,
            (1 + 2 * draw_features[orientation][0]) * TILE_SIZE,
            (1 + draw_features[orientation][1]) * TILE_SIZE)


def create_texture(draw_features, orientation):
    """
    Creating texture according to draw features of object
    :param draw_features:additional size that extend the image of the object beyond the limits of the tile
    :param orientation: string - orientation of object
    :return: Pygame Surface object - image of map object
    """
    return pg.transform.scale(pg.image.load("assets/textures/{}".format(draw_features[orientation][2])),
                              ((1 + 2 * draw_features[orientation][0]) * TILE_SIZE,
                               (1 + draw_features[orientation][1]) * TILE_SIZE))


def is_picked(event, coord):
    """
    Choice object be mouse click
    :param event: Pygame event object - MOUSEBOTTONDOWN event from queue
    :param coord: list[float, float] - coordinates of object
    :return: bool - is object chosen
    """
    pos = event.pos
    return abs(pos[0] - (coord[0] + 0.5) * TILE_SIZE) < TILE_SIZE / 2 and abs(
        pos[1] - (coord[1] + 0.5) * TILE_SIZE) < TILE_SIZE / 2


class Task:
    """
    Task for the colonist
    """

    def __init__(self, task_type):
        self.task_type = task_type


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
        self.target_object = target_tile  # FIXME


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
        tile_box = (self.coord[0] * TILE_SIZE,
                    self.coord[1] * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE)
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


class Creature(SolidObject):
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
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.speed = 0.05  # Base value [tile/tick]
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
            self.draw_box = create_draw_box(self.coord, self.draw_features, "west")
            self.texture = create_texture(self.draw_features, "west")

        elif self.direction[0] > 0:
            self.draw_box = create_draw_box(self.coord, self.draw_features, "east")
            self.texture = create_texture(self.draw_features, "east")

        elif self.direction[1] < 0:
            self.draw_box = create_draw_box(self.coord, self.draw_features, "north")
            self.texture = create_texture(self.draw_features, "north")

        elif self.direction[1] > 0:
            self.draw_box = create_draw_box(self.coord, self.draw_features, "south")
            self.texture = create_texture(self.draw_features, "south")

        else:
            self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
            self.texture = create_texture(self.draw_features, "default")

    def time_counter(self, path_to_finish, region_map):
        """
        function count time which is necessary to overcome the path
        :param path_to_finish: list[list[float]]
        :param region_map: Map object - map of the game region
        :return: float - time
        """
        time = 0.0
        number_element = 1
        while number_element != path_to_finish.size():
            x0 = path_to_finish[number_element - 1][0]
            y0 = path_to_finish[number_element - 1][1]
            x1 = path_to_finish[number_element][0]
            y1 = path_to_finish[number_element][1]
            facet = cmath.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
            time += facet / region_map.field[y0][x0].speed_mod
        return time

    def make_grid(self, region_map, list_solid_object):
        """
        function makes cell velocity multiplier matrix
        :param region_map: Map object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: grid: list[list[float]] - velocity multiplier matrix
        """

        grid = list(list())
        first_tile = TILE_SIZE / 2
        last_tile_in_row = self.surface.get_size()[0] - TILE_SIZE / 2
        last_tile_in_column = self.surface.get_size()[1] - TILE_SIZE / 2

        for tile_coord_in_column in range(first_tile, TILE_SIZE, last_tile_in_column):

            for tile_coord_in_row in range(first_tile, TILE_SIZE, last_tile_in_row):
                row_of_speed_mood = list()
                checker_object_in_tile = 0

                for i in range(len(list_solid_object)):
                    if list_solid_object[i].get_coord[0] == tile_coord_in_row and \
                            list_solid_object[i].get_coord[1] == tile_coord_in_column:
                        checker_object_in_tile = 1

                if checker_object_in_tile == 1:
                    if 1 / region_map.field[tile_coord_in_column][tile_coord_in_row].speed_mod > 10 ** 17:
                        row_of_speed_mood.append(
                            2 / region_map.field[tile_coord_in_column][tile_coord_in_row].speed_mod)
                    else:
                        row_of_speed_mood.append(10 ** 17)

                else:
                    row_of_speed_mood.append(
                        1 / region_map.field[tile_coord_in_column][tile_coord_in_row].speed_mod)
                if tile_coord_in_row == last_tile_in_row:
                    grid.append(row_of_speed_mood)

        return grid

    def make_graph(self, region_map, list_solid_object):
        """
        Function makes a dict. The Key: velocity coefficient values at the given coordinate, value:
         velocity coefficient values around the given coordinate.
        :param region_map: Map object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: {float: list[float]} - The Key: velocity coefficient values at the given coordinate, value:
         velocity coefficient values around the given coordinate.
        """
        graph = {}
        grid = self.make_grid(region_map, list_solid_object)
        for y, row in enumerate(grid):
            for x, col in enumerate(row):
                graph[(x, y)] = graph.get((x, y), []) + self.get_next_nodes(x, y, region_map, list_solid_object)
        return graph

    def get_next_nodes(self, x, y, region_map, list_solid_object):
        """
        function finds cell coordinates around the current in a certain direction
        :param x: float - x location coordinate
        :param y: float - y location coordinate
        :param region_map: Map object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: [float, float] - coordinate around the current in a certain direction
        """
        grid = self.make_grid(region_map, list_solid_object)
        cols = self.surface.get_size()[0] // TILE_SIZE
        rows = self.surface.get_size()[1] // TILE_SIZE
        check_next_node = lambda x_element, y_element: True if 0 <= x_element < cols and \
                                                               0 <= y_element < rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1], [1, 1], [1, -1], [-1, 1], [-1, -1]
        return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def dijkstra_logic(self, goal_coord, region_map, list_solid_object):
        """
        :param self: Creature for whom we are looking for a way
        :param goal_coord: [float, float] - finish coordinate
        :param region_map: Map object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: list[list[float, float],...] - list of tiles to go through
        """
        graph = self.make_graph(region_map, list_solid_object)
        start = (self.coord[0], self.coord[1])
        goal = (goal_coord[0], goal_coord[1])
        queue_coords = []
        heapq.heappush(queue_coords, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while queue_coords:
            cur_cost, cur_node = heapq.heappop(queue_coords)
            if cur_node == goal:
                break

            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    heapq.heappush(queue_coords, (new_cost, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node

        cur_node = goal
        path = list()
        coordinates = list()
        coordinates.append(goal[0])
        coordinates.append(goal[1])
        path.append(coordinates)
        while cur_node != start:
            cur_node = visited[cur_node]
            coordinates = [cur_node[0], cur_node[1]]
            path.append(coordinates)

        path.reverse()
        return path

    def pathfinder(self, goal_coord, region_map, list_solid_object):
        """
        Finding the best way to the goal on the map
        :param goal_coord: list[int, int] - coordinates' of target cell
        :param region_map: Map object - map of the game region
        :param list_solid_object: list[MapObject object,...] - list of all objects that can block a path
        :return: list[list[float, float],...] - list of tiles to go through
        """
        map_objects_around_self = list()
        for map_object in list_solid_object:
            if abs(map_object.coord[0] - self.coord[0]) < (TILE_SIZE * cmath.sqrt(2)) and abs(
                    map_object.coord[0] - self.coord[1]) < (TILE_SIZE * cmath.sqrt(2)):
                map_objects_around_self = map_objects_around_self.append(map_object)
        if map_objects_around_self.size() == 8:
            return list()
        path = self.dijkstra_logic(goal_coord, region_map, list_solid_object)
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
        :param region_map: Map object - map of the game region
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

    def move_to(self):
        pass  # approach a specific tile

    def attack(self):
        pass  # approach a specific creature and beat it

    def do_task(self):
        pass  # do task from the self.task

    def death(self):
        """
        Processing of death effects
        :return: Effect object - some kind of effect accompanying death
                 Corpse object - corpse of dead creature
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

    def decide_to_move(self):
        pass  # need to create task "move_to" with random chance

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
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.full_hit_points = 20.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.damage = 2.0
        self.type = "settler"

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
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.full_hit_points = 30.0
        if hit_points > self.full_hit_points:
            self.hit_points = self.full_hit_points
        else:
            self.hit_points = hit_points
        self.speed = 0.8
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
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
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
        self.draw_box = create_draw_box(self.coord, self.draw_features, "default")
        self.texture = create_texture(self.draw_features, "default")
        self.speed = 0.2
        self.damage = 0.5
        self.melee_cooldown = 80.0
        self.type = "turtle"


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
            "default": [0.5, 1.5, "tree.png"]
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
        tile_box = (self.coord[0] * TILE_SIZE,
                    self.coord[1] * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE)
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
