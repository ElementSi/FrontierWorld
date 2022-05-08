import pygame as pg

import constants as const


class Background(pg.sprite.Sprite):
    def __init__(self, surface, image_file, location):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image_file)
        self.rect = pg.Rect(location[0], location[1], surface.get_size()[0], surface.get_size()[1])


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
        :param color: tuple(int, int, int) - base color of button in RGB
        """
        self.surface = surface
        self.draw_box = draw_box
        self.text = text
        self.key = key
        self.fontsize = fontsize
        self.font = pg.font.Font("fonts/Montserrat-Regular.ttf", self.fontsize)
        self.original_color = color
        self.color = color

    def tone_change(self, amendment):
        """
        Lightening or darkening the tone by a given amendment
        :param amendment: int - the magnitude of the tone change
        :return: tuple(int, int, int) - color of button in RGB after changing
        """
        if self.color[0] + amendment < 256:
            r_color = self.color[0] + amendment
        else:
            r_color = 255

        if self.color[1] + amendment < 256:
            g_color = self.color[1] + amendment
        else:
            g_color = 255

        if self.color[2] + amendment < 256:
            b_color = self.color[2] + amendment
        else:
            b_color = 255

        return r_color, g_color, b_color

    def draw(self):
        """
        Drawing button in the current window
        """
        box = self.draw_box

        pg.draw.polygon(
            self.surface,
            self.tone_change(20),
            ([box[0], box[1]],
             [box[0] + box[2], box[1]],
             [box[0] + box[2], box[1] + box[3]])
        )

        pg.draw.polygon(
            self.surface,
            self.tone_change(-20),
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
            [box[0] + 0.2 * box[2],
             box[1] + 0.5 * (box[3] - self.fontsize)]
        )

    def is_hovered(self, event):
        """
        Checking whether the cursor is hovered over the button
        :param event: Pygame event object - MOUSEBOTTONDOWN or MOUSEMOTION event from queue
        """
        pos = event.pos
        hor_match = (pos[0] > self.draw_box[0]) and (pos[0] < self.draw_box[0] + self.draw_box[2])
        vert_match = (pos[1] > self.draw_box[1]) and (pos[1] < self.draw_box[1] + self.draw_box[3])
        return hor_match and vert_match

    def hover(self, event):
        """
        Checking whether the cursor is hovered over the button and changing color
        :param event: Pygame event object - MOUSEMOTION event from queue
        """
        if self.is_hovered(event):
            self.color = self.tone_change(30)
        else:
            self.color = self.original_color


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
        self.buttons = [
            Button(
                surface,
                (0.1 * self.size[0], 0.15 * self.size[1], 0.2 * self.size[0], 0.05 * self.size[1]),
                "Новая игра",
                "main_menu_new_game",
                int(0.02 * self.size[1]),
                const.COLORS["brown"]
            ),
            Button(
                surface,
                (0.1 * self.size[0], 0.25 * self.size[1], 0.2 * self.size[0], 0.05 * self.size[1]),
                "Загрузить игру",
                "main_menu_download_game",
                int(0.002 * self.size[1]),
                const.COLORS["brown"]
            ),
            Button(
                surface,
                (0.1 * self.size[0], 0.35 * self.size[1], 0.2 * self.size[0], 0.05 * self.size[1]),
                "Выход",
                "main_menu_exit",
                int(0.002 * self.size[1]),
                const.COLORS["brown"]
            )
        ]
        self.menu_mod = "main_menu"
        self.is_active = True  # активировано ли меню отнсительно геймплея
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
                    if button.is_hovered(event):
                        if button.key == "main_menu_new_game":
                            self.is_active = False
                        elif button.key == "main_menu_download_game":
                            self.menu_mod = "download_menu"
                        elif button.key == "main_menu_exit":
                            self.is_finished = True

    def update_state(self):
        if self.menu_mod == "main_menu":
            self.buttons = [
                Button(
                    self.surface,
                    (0.1 * self.size[0], 0.15 * self.size[1], 0.2 * self.size[0], 0.05 * self.size[1]),
                    "Новая игра",
                    "main_menu_new_game",
                    int(0.02 * self.size[1]),
                    const.COLORS["brown"]
                ),
                Button(
                    self.surface,
                    (0.1 * self.size[0], 0.25 * self.size[1], 0.2 * self.size[0], 0.05 * self.size[1]),
                    "Загрузить игру",
                    "main_menu_download_game",
                    int(0.02 * self.size[1]),
                    const.COLORS["brown"]
                ),
                Button(
                    self.surface,
                    (0.1 * self.size[0], 0.35 * self.size[1], 0.2 * self.size[0], 0.05 * self.size[1]),
                    "Выход",
                    "main_menu_exit",
                    int(0.02 * self.size[1]),
                    const.COLORS["brown"]
                )
            ]

        elif self.menu_mod == "download_menu":
            self.buttons = [
                Button(
                    self.surface,
                    (0.1 * self.size[0], 0.15 * self.size[1], 0.2 * self.size[0], 0.05 * self.size[1]),
                    "Назад",
                    "main_menu_back",
                    int(0.002 * self.size[1]),
                    const.COLORS["brown"]
                )
            ]

    def draw(self):
        for button in self.buttons:
            button.draw()

    def update_menu(self):
        """
        Updating display to reflect changes of objects
        """
        pg.display.update()
        self.clock.tick(const.FPS)
