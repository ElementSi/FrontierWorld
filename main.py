import pygame as pg

import constants as const
import map_objects as objects
import creature as creature
import game_map as game_map
import interface as interface

pg.init()

SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h


def pixels2tiles(pixel_coords):
    return [pixel_coords[0] // const.TILE_SIZE, pixel_coords[1] // const.TILE_SIZE]


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
        self.interface = interface.InGameInterface(surface)
        self.game_map = game_map.Map(surface, [SCREEN_WIDTH, SCREEN_HEIGHT])
        self.settler = creature.Settler(self.surface, [0, 0])
        self.list_solid_object = []

        for i in range(self.game_map.height):
            for j in range(self.game_map.width):
                if self.game_map.field[i][j].pre_object == "tree":
                    self.list_solid_object.append(objects.Tree(self.surface, [j, i]))
                elif self.game_map.field[i][j].pre_object == "bush":
                    self.list_solid_object.append(objects.Bush(self.surface, [j, i]))
                elif self.game_map.field[i][j].pre_object == "cliff":
                    self.list_solid_object.append(objects.Cliff(self.surface, [j, i]))

        self.list_effects = []
        self.list_loot = []
        self.chosen_map_object = None
        self.picked_task = None
        self.is_finished = False

    def create_new_animal(self):
        """
        Randomly spawn new animal on the border of the map
        """
        pass

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

    def process_input(self):
        """
        Processing all player input
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_finished = True

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.chosen_map_object is None:
                        self.is_finished = True
                    else:
                        self.chosen_map_object.is_chosen = False
                        self.chosen_map_object = None

            elif event.type == pg.MOUSEMOTION:
                self.interface.activate(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in self.interface.buttons:
                    if interface.is_hovered(event, button.draw_box):
                        if button.key == "interface_go_to":
                            self.picked_task = "go_to"

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

                    self.interface.is_in_need_of_update = True

                else:
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
                            self.picked_task = None

                    else:
                        object_interferes = False

                        for solid_object in self.list_solid_object:
                            if objects.is_picked(event, solid_object.coord):
                                object_interferes = True
                                break

                        if not object_interferes:
                            print(pixels2tiles(event.pos))
                            self.settler.task = creature.TileTask(self.picked_task, pixels2tiles(event.pos))

                        else:
                            self.picked_task = None

    def update_interface(self):
        if self.chosen_map_object is None:
            self.interface.interface_mod = "default"

        else:
            self.interface.interface_mod = self.chosen_map_object.type

        self.interface.update_interface()

    def do_tasks(self):
        if self.settler.task is not None:
            getattr(self.settler, self.settler.task.task_type)(self.game_map, self.list_solid_object)
            self.settler.task = None

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


menu = interface.Menu(screen)
game = Gameplay(screen)
is_finished = False
game_preset = "new_game"
is_game_ready = False


while not is_finished:
    if menu.is_active:
        game_preset = menu.activate()
        menu.update_menu()
        menu.draw_background()
        menu.draw()
        menu.update_display()
        is_finished = menu.is_finished
    else:
        if (game_preset == "new_game") and (not is_game_ready):
            game = Gameplay(screen)
            is_game_ready = True
        elif not is_game_ready:
            game = Gameplay(screen)
            is_game_ready = True
        game.process_input()
        game.update_interface()
        game.draw_interface()
        game.draw_map()
        game.draw_objects()
        game.do_tasks()
        game.move_creatures()
        game.update_display()
        is_finished = game.is_finished

pg.quit()
