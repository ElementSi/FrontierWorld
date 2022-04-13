import random as rnd
import pygame as pg
import pygame.time

clock = pygame.time.Clock()

ARROWS = [1073741903, 1073741904, 1073741905, 1073741906]
WASD = [100, 97, 115, 119]
TAB = 9
LEFT_SHIFT = 1073742049
RIGHT_SHIFT = 1073742053
ZX = [122, 120]
Q, E = 113, 101
SQUARE_BRACKETS = [91, 93]
ONE_TO_FIVE = [49, 50, 51, 52, 53]
SIX_TO_ZERO = [54, 55, 56, 57, 48]

WIDTH = 1000
HEIGHT = 750

size_cell = 10  # тут нужно в качестве числа передать сторону клетки


def hit_test(lhs_coordinate, rhs_coordinate):
    """
    Функция проверяет сталкивалкивается ли данный обьект с объектом obj.
    :param lhs_coordinate: координата левого тела
    :param rhs_coordinate: координаата пправого тела
    :return: Возвращает True в случае столкновения объектов. В противном случае возвращает False
    """
    if size_cell >= (lhs_coordinate - rhs_coordinate):
        return True
    return False

class Object:
    """
    конструктор объектов игры
    """

    def __init__(self, surface, texture, size):
        """
        :param surface: экран, где рисуем
        :param texture: изображение объекта
        :param size: массив с размерами по ОХ и ОУ
        """
        self.surface = surface
        self.live = 1
        self.x = rnd.randint(0, WIDTH - 100)
        self.y = rnd.randint(0, HEIGHT - 100)
        self.vx = 0
        self.vy = 0
        self.size = size
        self.texture = pg.transform.scale(pg.image.load(texture), (self.x, self.y))
        self.type = "object"
        self.controllability = 1

    def hit_test(self, obj):
        """
        Функция проверяет сталкивалкивается ли данный обьект с объектом obj.
        :param obj: Обьект, с которым проверяется столкновение.
        :return: Возвращает True в случае столкновения объектов. В противном случае возвращает False
        """
        if size_cell >= ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** (1 / 2):
            return True
        return False

    def draw(self):
        """
        Drawing a Particle
        """
        if self.live > 0:
            rect_draw_box = (self.x - self.size[0] / 2,
                             self.y - self.size[1] / 2,
                             self.size[0],
                             self.size[1])
            self.surface.blit(self.texture, rect_draw_box)


class Creation(Object):
    """
    конструктор живых существ игры
    """

    def __init__(self, surface, texture, size, x, y):
        """
        :param surface: экран, где рисуем
        :param texture: изображение существа
        :param size: размеры существа
        :param x: местоположение сущесвта по ОХ
        :param y: местоположение существа по ОУ
        """
        super().__init__(surface, texture, size)
        self.x = x
        self.y = y
        self.type = "creation"

    def taking_damage(self):
        """
        Processing of damage effects
        """
        rood = Object(self.surface, "blood.png", [10, 10])  # найти и спользовать фотографию крови
        rood.draw()
        pygame.display.update()
        clock.tick(1)
        self.live -= 1


class Animal(Creation):
    """
    конструктор животного
    """

    def __init__(self, surface, texture, size, x, y):
        """
        :param surface: экран, где рисуем
        :param texture: изображение животное
        :param size: размеры существа
        :param x: местоположение сущесвта по ОХ
        :param y: местоположение существа по ОУ
        """
        super().__init__(surface, texture, size, x, y)
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
