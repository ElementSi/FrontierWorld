import pygame as pg
import random as rnd
import pygame.time
from map import TILE_SIZE


class MapObject:
    """
    Any changeable map object
    """
    def __init__(self, surface, coord):
        """
        Universal basic constructor of map object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of upper left corner of object (tile coordinates)
        """
        self.surface = surface
        self.coord = coord
        self.draw_box = (coord[0] * TILE_SIZE, coord[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.texture = pg.transform.scale(pg.image.load("textures/default.png"), (TILE_SIZE, TILE_SIZE))
        self.is_chosen = False
        self.type = "def_object"

    def chose(self, event):
        """
        Choice object be mouse click
        :param event: Pygame event object - any event from queue
        :return: bool - is object chosen
        """
        pass  # Надо провести аккуратную и быструю (!) проверку на то, попал ли игрок курсором на объект

    def draw(self):
        """
        Drawing object in the current window
        """
        self.surface.blit(self.texture, self.draw_box)
        if self.is_chosen:
            pass  # Надо нарисовать белую рамку вокруг объекта, если он выбран

    def safe(self, file):
        """
        Writing information about an object to a save file
        :param file: TextIO object - Output stream to an external save file
        """
        pass  # Надо записать строчку с исчерпывающей и унифицированной информацией об объекте в файл


class SolidObject(MapObject):
    """
    Material object with limited hit points that can only exist on the map
    """
    def __init__(self, surface, coord):
        """
        Universal constructor of solid object
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of upper left corner of object (tile coordinates)
        """
        super().__init__(surface, coord)
        self.hit_points = 10
        self.type = "def_solid_object"


class Creation(SolidObject):
    """
    Creature that can move and proceed more complex tasks
    """
    def __init__(self, surface, coord):
        """
        Universal constructor of creature
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of upper left corner of object (tile coordinates)
        """
        super().__init__(surface, coord)
        self.speed = 0.05  # Base value [tile/tick]
        self.damage = 1  # Base value [hit point]
        self.melee_cooldown = 60  # Base value [tick]
        self.type = "def_creation"

    def take_damage(self, damage):
        """
        Taking damage by creature
        """
        # rood = Object(self.surface, "blood.png", [10, 10])  # Найти и использовать фотографию крови
        # rood.draw()
        # # pygame.display.update()
        # # clock.tick(1)
        # self.live -= 1

    def pathfinder(self, goal_coord, region_map):
        """

        :param goal_coord:
        :param region_map:
        :return:
        """


class Animal(Creation):
    """
    Animals controlled by AI
    """
    def __init__(self, surface, coord):
        """
        Universal constructor of animal
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of upper left corner of object (tile coordinates)
        """
        super().__init__(surface, coord)
        self.activity_rate = 0.1  # Base value, some relative coefficient
        self.type = "def_animal"

    def death(self):
        """
        Processing of death effects
        """
        pass

    def move(self):
        """
        Moving to its goal
        """
        pass


class Settler(Creation):
    """
    Settler controlled by player
    """

    def __init__(self, surface, coord):
        """
        Universal constructor of animal
        :param surface: Pygame Surface object - target window
        :param coord: list[float, float] - coordinates of upper left corner of object (tile coordinates)
        """
        super().__init__(surface, coord)
        self.activity_rate = 0.1  # Base value, some relative coefficient
        self.type = "def_animal"

    def death(self):
        """
        Processing of death effects
        """
        RED = (255, 0, 0)
        font = pygame.font.Font(None, 100)
        message = font.render("Game over", True, RED)
        place = message.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        self.surface.blit(message, place)
        pygame.display.update()
        clock.tick(1)
        self.texture = "died_man.png"  # найти и спользоват фотогорафию мертовго чела

        # по идее выход из игры + вывод счетчика очков

    def move(self):
        """
        перемещение человека
        """
        pass

    def doing_something(self):
        """
        выполнение какаих-то действий
        """
        pass

    def find_good_road(self):
        """
        поиск короткого пути и перемещение по нему
        """
        pass

    def choose_men(self):
        """
        :return: True если им можно управлять, else False
        """
        if self.controllability % 2 == 0:
            return True
        else:
            return False

    def event_command(self, event):
        """
        обработка команд с клавиатуры
        :param event: команда которую нужно обработать
        """
        pass
