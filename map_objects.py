import pygame as pg
import random as rnd
import pygame.time
from map import TILE_SIZE


class MapObject:
    """
    Все объекты, размещённые на карте
    """
    def __init__(self, surface, coord):
        """
        Универсальный базовый конструктор объектов
        :param surface: Pygame Surface object - Окно, в котором отображается объект.
        :param coord: list[float, float] - Координаты верхнего левого угла объекта.
        """
        self.surface = surface
        self.is_alive = 1
        self.is_chosen = 0
        self.coord = coord
        self.draw_box = (coord[0] * TILE_SIZE, coord[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.texture = pg.transform.scale(pg.image.load("textures/default.png"), (TILE_SIZE, TILE_SIZE))
        self.type = "def_object"

    def draw(self):
        """
        Отрисовка любого объекта на карте
        """
        self.surface.blit(self.texture, self.draw_box)


class Creation(MapObject):
    """
    Живые существа, размещённые на карте
    """
    def __init__(self, surface, coord):
        """
        Универсальный конструктор живых существ
        :param surface: Pygame Surface object - Окно, в котором отображается объект.
        :param coord: list[float, float] - Координаты верхнего левого угла объекта.
        """
        super().__init__(surface, coord)
        self.hit_points = 10
        self.type = "def_creation"

    def taking_damage(self):
        """
        Получение урона живым существом
        """
        # rood = Object(self.surface, "blood.png", [10, 10])  # найти и спользовать фотографию крови
        # rood.draw()
        # # pygame.display.update()
        # # clock.tick(1)
        # self.live -= 1


class Animal(Creation):
    """
    Животные (управляемые ИИ), размещённые на карте
    """
    def __init__(self, surface, coord):
        """
        Универсальный конструктор животных
        :param surface: Pygame Surface object - Окно, в котором отображается объект.
        :param coord: list[float, float] - Координаты верхнего левого угла животного.
        """
        super().__init__(self, surface, coord)
        self.type = "animal"

    def death(self):
        """
        Processing of death effects
        """
        self.texture = "died_animal.png"  # найти и спользовать фотографию мертвого животного

    def move(self, obj):
        """
        перемещение животного
        """
        self.vx = rnd.choice([-10, 0, 10])
        self.vy = rnd.choice([-10, 0, 10])
        self.x += self.vx
        self.y += self.vy
        if self.hit_test(obj):
            self.vx *= -1
        pass

    def doing_something(self):
        """
        выполнение какаих-то действий
        """
        pass


class Man(Creation):
    """
    конструктор человека
    """

    def __init__(self, surface, texture, size, x, y):
        """
        :param surface: экран, где рисуем
        :param texture: изображение человека
        :param size: размеры существа
        :param x: местоположение сущесвта по ОХ
        :param y: местоположение существа по ОУ
        """
        super().__init__(surface, texture, size, x, y)
        self.type = "man"

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
