import pygame as pg

import constants as const


def tone_change(initial_color, amendment):
    """
    Lightening or darkening the tone by a given amendment
    :param initial_color: tuple(int, int, int) - the initial color in the RGB system
    :param amendment: int - the magnitude of the tone change
    :return: tuple(int, int, int) - color of button in RGB after changing
    """
    if initial_color[0] + amendment < 256:
        r_color = initial_color[0] + amendment
    else:
        r_color = 255

    if initial_color[1] + amendment < 256:
        g_color = initial_color[1] + amendment
    else:
        g_color = 255

    if initial_color[2] + amendment < 256:
        b_color = initial_color[2] + amendment
    else:
        b_color = 255

    return r_color, g_color, b_color


def is_hovered(event, draw_box):
    """
    Checking whether the cursor is hovered over the interface element
    :param event: Pygame event object - MOUSEBOTTONDOWN or MOUSEMOTION event from queue
    :param draw_box: Pygame Rect object - position and size
    """
    pos = event.pos
    hor_match = (pos[0] > draw_box[0]) and (pos[0] < draw_box[0] + draw_box[2])
    vert_match = (pos[1] > draw_box[1]) and (pos[1] < draw_box[1] + draw_box[3])
    return hor_match and vert_match


class Button:
    """
    In-game button displayed on the screen
    """

    def __init__(self, surface, draw_box, text, key, fontsize, color):
        """
        Constructor of button
        :param surface: Pygame Surface object - target window
        :param draw_box: Pygame Rect object - position and size
        :param text: string - text on button
        :param key: string - id of button
        :param fontsize: int - font height in pixels
        :param color: tuple(int, int, int) - base color of button in RGB
        """
        self.surface = surface
        self.draw_box = draw_box
        self.text = text
        self.key = key
        self.fontsize = fontsize
        self.font = pg.font.Font(const.FONT, self.fontsize)
        self.original_color = color
        self.color = color
        self.is_selected = False

    def draw(self):
        """
        Drawing button in the current window
        """
        box = self.draw_box

        pg.draw.polygon(
            self.surface,
            tone_change(self.color, 30),
            ([box[0], box[1]],
             [box[0] + box[2], box[1]],
             [box[0] + box[2], box[1] + box[3]])
        )

        pg.draw.polygon(
            self.surface,
            tone_change(self.color, -30),
            ([box[0], box[1]],
             [box[0], box[1] + box[3]],
             [box[0] + box[2], box[1] + box[3]])
        )

        smaller_box = (
            box[0] + 0.1 * box[2],
            box[1] + 0.1 * box[3],
            0.8 * box[2],
            0.8 * box[3]
        )

        pg.draw.rect(
            self.surface,
            self.color,
            smaller_box
        )

        self.surface.blit(
            self.font.render(self.text, True, const.COLORS["white"]),
            [box[0] + 0.15 * box[2],
             box[1] + 0.4 * (box[3] - self.fontsize)]
        )

    def hover(self, event):
        """
        Checking whether the cursor is hovered over the button and changing color
        :param event: Pygame event object - MOUSEMOTION event from queue
        """
        self.is_selected = is_hovered(event, self.draw_box)
        if self.is_selected:
            self.color = tone_change(self.original_color, 20)
        else:
            self.color = self.original_color


class SimplifiedButton(Button):
    def draw(self):
        """
        Drawing button in the current window
        """
        pg.draw.rect(
            self.surface,
            tone_change(self.color, 70),
            self.draw_box
        )

        smaller_box = (
            self.draw_box[0] + 4,
            self.draw_box[1] + 4,
            self.draw_box[2] - 4,
            self.draw_box[3] - 8
        )

        pg.draw.rect(
            self.surface,
            self.color,
            smaller_box
        )

        self.surface.blit(
            self.font.render(self.text, True, const.COLORS["white"]),
            [self.draw_box[0] + 0.05 * self.draw_box[2],
             self.draw_box[1] + 0.4 * (self.draw_box[3] - self.fontsize)]
        )


class Frame:
    """
    Empty space used to highlight important buttons
    """

    def __init__(self, surface, draw_box, colors):
        """
        Constructor of frame
        :param surface: Pygame Surface object - target window
        :param draw_box: Pygame Rect object - position and size
        :param colors: list[tuple(int, int, int)x2] - colors of frame in RGB
        """
        self.surface = surface
        self.draw_box = draw_box
        self.colors = colors

    def draw(self):
        """
        Drawing button in the current window
        """
        pg.draw.rect(
            self.surface,
            self.colors[0],
            self.draw_box
        )

        smaller_box = (
            self.draw_box[0] + 4,
            self.draw_box[1] + 4,
            self.draw_box[2] - 8,
            self.draw_box[3] - 8
        )

        pg.draw.rect(
            self.surface,
            self.colors[1],
            smaller_box
        )


class Menu:
    """
    Main menu with a selection of basic options
    """

    def __init__(self, surface):
        """
        Constructor of main menu
        :param surface: Pygame Surface object - target surface
        """
        self.surface = surface
        self.clock = pg.time.Clock()
        self.size = surface.get_size()
        self.background = pg.transform.scale(pg.image.load("assets/menu_background.png"),
                                             (self.size[0],
                                              self.size[1]))
        self.frames = []
        self.buttons = [
            Button(
                surface,
                (0.1 * self.size[0],
                 0.15 * self.size[1],
                 0.2 * self.size[0],
                 0.05 * self.size[1]),
                "Новая игра",
                "main_menu_new_game",
                int(0.02 * self.size[1]),
                const.COLORS["cream"]
            ),
            Button(
                surface,
                (0.1 * self.size[0],
                 0.25 * self.size[1],
                 0.2 * self.size[0],
                 0.05 * self.size[1]),
                "Загрузить игру",
                "main_menu_download_game",
                int(0.02 * self.size[1]),
                const.COLORS["cream"]
            ),
            Button(
                surface,
                (0.1 * self.size[0],
                 0.35 * self.size[1],
                 0.2 * self.size[0],
                 0.05 * self.size[1]),
                "Выход",
                "main_menu_exit",
                int(0.02 * self.size[1]),
                const.COLORS["cream"]
            )
        ]
        self.menu_mod = "main_menu"
        self.is_background_drawn = False
        self.is_in_need_of_update = False
        self.is_active = True
        self.is_finished = False

    def activate(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_finished = True

            elif event.type == pg.MOUSEMOTION:
                for button in self.buttons:
                    button.hover(event)

            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if is_hovered(event, button.draw_box):
                        if button.key == "main_menu_new_game":
                            self.is_active = False
                            return "new_game"
                        elif button.key == "main_menu_download_game":
                            self.menu_mod = "download_menu"
                            self.is_in_need_of_update = True
                        elif button.key == "main_menu_exit":
                            self.is_finished = True
                        elif button.key == "download_menu_back":
                            self.menu_mod = "main_menu"
                            self.is_in_need_of_update = True

    def update_menu(self):
        if self.is_in_need_of_update:
            if self.menu_mod == "main_menu":
                self.frames.clear()
                self.buttons.clear()
                self.buttons = [
                    Button(
                        self.surface,
                        (0.1 * self.size[0],
                         0.15 * self.size[1],
                         0.2 * self.size[0],
                         0.05 * self.size[1]),
                        "Новая игра",
                        "main_menu_new_game",
                        int(0.02 * self.size[1]),
                        const.COLORS["cream"]
                    ),
                    Button(
                        self.surface,
                        (0.1 * self.size[0],
                         0.25 * self.size[1],
                         0.2 * self.size[0],
                         0.05 * self.size[1]),
                        "Загрузить игру",
                        "main_menu_download_game",
                        int(0.02 * self.size[1]),
                        const.COLORS["cream"]
                    ),
                    Button(
                        self.surface,
                        (0.1 * self.size[0],
                         0.35 * self.size[1],
                         0.2 * self.size[0],
                         0.05 * self.size[1]),
                        "Выход",
                        "main_menu_exit",
                        int(0.02 * self.size[1]),
                        const.COLORS["cream"]
                    )
                ]
                self.is_in_need_of_update = False

            elif self.menu_mod == "download_menu":
                self.frames.clear()
                self.buttons.clear()
                self.frames = [
                    Frame(
                        self.surface,
                        (0.05 * self.size[0],
                         0.05 * self.size[0],
                         0.3 * self.size[0],
                         0.6 * self.size[1]),
                        [const.COLORS["light_blue"], const.COLORS["dark_blue"]]
                    )
                ]
                self.buttons = [
                    Button(
                        self.surface,
                        (0.1 * self.size[0],
                         0.15 * self.size[1],
                         0.2 * self.size[0],
                         0.05 * self.size[1]),
                        "Назад",
                        "download_menu_back",
                        int(0.02 * self.size[1]),
                        const.COLORS["cream"]
                    )
                ]
                self.is_in_need_of_update = False

    def draw_background(self):
        if (not self.is_background_drawn) or (not self.is_in_need_of_update):
            self.surface.blit(self.background, (0, 0, self.size[0], self.size[1]))
            self.is_background_drawn = True

    def draw(self):
        for frame in self.frames:
            frame.draw()
        for button in self.buttons:
            button.draw()

    def update_display(self):
        """
        Updating display to reflect changes of objects
        """
        pg.display.update()
        self.clock.tick(const.FPS)


class InGameInterface:
    """
    The interface that the player sees during gameplay
    """

    def __init__(self, surface):
        """
        Constructor of in-game interface
        :param surface: Pygame Surface object - target surface
        """
        self.surface = surface
        self.clock = pg.time.Clock()
        self.size = surface.get_size()
        self.frames = [
            Frame(
                self.surface,
                (0,
                 self.size[1] - const.TILE_SIZE * const.INTERFACE_AMENDMENT,
                 self.size[0],
                 const.TILE_SIZE * const.INTERFACE_AMENDMENT),
                [const.COLORS["light_blue"], const.COLORS["dark_blue"]]
            )
        ]
        self.buttons = [
            SimplifiedButton(
                surface,
                (self.size[0] - 0.15 * self.size[0],
                 self.size[1] - const.TILE_SIZE * const.INTERFACE_AMENDMENT,
                 0.15 * self.size[0] + 1,
                 const.TILE_SIZE * const.INTERFACE_AMENDMENT),
                "Меню",
                "in-game_interface_menu",
                int(0.02 * self.size[1]),
                const.COLORS["dark_blue"]
            ),
            Button(
                surface,
                (self.size[0] - 23.8 * self.size[0] // const.TILE_SIZE,
                 self.size[1] - 0.9 * const.TILE_SIZE * const.INTERFACE_AMENDMENT,
                 0.08 * self.size[0] + 1,
                 0.8 * const.TILE_SIZE * const.INTERFACE_AMENDMENT),
                "Идти",
                "interface_go_to",
                int(0.02 * self.size[1]),
                const.COLORS["light_blue"]
            ),
        ]
        self.interface_mod = "default"
        self.is_in_need_of_update = False
        self.is_active = True
        self.is_finished = False

    def draw(self):
        for frame in self.frames:
            frame.draw()
        for button in self.buttons:
            button.draw()

    def activate(self, event):
        if event.type == pg.MOUSEMOTION:
            for button in self.buttons:
                button.hover(event)

    def update_interface(self):
        if self.interface_mod == "default":
            pass
        #олжна быть кнопка меню + фрейм
        # селф.мод сеттлер == баттон идти
