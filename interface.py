import pygame as pg

import features as feat


def is_hovered(event, draw_box):
    """
    Checking whether the cursor is hovered over the button
    :param event: Pygame event object - MOUSEBOTTONDOWN or MOUSEMOTION event from queue
    :param draw_box: Pygame Rect object - position and size of button
    """
    pos = event.pos
    hor_match = (pos[0] > draw_box[0]) and (pos[0] < draw_box[0] + draw_box[2])
    vert_match = (pos[1] > draw_box[1]) and (pos[1] < draw_box[1] + draw_box[3])
    return hor_match and vert_match


def tone_change(color, amendment):
    """
    Lightening or darkening the tone by a given amendment
    :param color: tuple(int, int, int) - initial color of button in RGB
    :param amendment: int - the magnitude of the tone change
    :return: tuple(int, int, int) - color of button in RGB after changing
    """
    if color[0] + amendment < 256:
        r_color = color[0] + amendment
    else:
        r_color = 255

    if color[1] + amendment < 256:
        g_color = color[1] + amendment
    else:
        g_color = 255

    if color[2] + amendment < 256:
        b_color = color[2] + amendment
    else:
        b_color = 255

    return r_color, g_color, b_color


def create_text_surface(text, fontsize):
    """
    Creating a surface with the specified text
    :param text: string - text on surface
    :param fontsize: int - size of font in pixels
    :return: Pygame Surface object - surface with text
    """
    font = pg.font.Font("fonts/Montserrat-Regular.ttf", fontsize)
    return font.render(text, True, feat.COLORS["white"])


class Button:
    """
    In-game button displayed on the screen
    """

    def __init__(self, surface, draw_box, text, fontsize, color):
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
        self.fontsize = fontsize
        self.original_color = color
        self.color = color

    def draw(self):
        """
        Drawing button in the current window
        """
        box = self.draw_box

        pg.draw.polygon(
            self.surface,
            tone_change(self.color, 10),
            ([box[0], box[1]],
             [box[0] + box[2], box[1]],
             [box[0] + box[2], box[1] + box[3]])
        )

        pg.draw.polygon(
            self.surface,
            tone_change(self.color, -10),
            ([box[0], box[1]],
             [box[0], box[1] + box[3]],
             [box[0] + box[2], box[1] + box[3]])
        )

        smaller_box = (
            box[0] + 0.1 * box[2],
            box[1] + 0.1 * box[3],
            box[0] + 0.9 * box[2],
            box[1] + 0.9 * box[3]
        )

        pg.draw.rect(
            self.surface,
            self.color,
            smaller_box
        )

        self.surface.blit(
            create_text_surface(self.text, self.fontsize),
            [box[0] + 0.2 * box[2],
             box[1] + 0.5 * (box[3] - self.fontsize)]
        )

    def hover(self, event):
        """
        Checking whether the cursor is hovered over the button and changing color
        :param event: Pygame event object - MOUSEMOTION event from queue
        """
        if is_hovered(event, self.draw_box):
            self.color = tone_change(self.color, 20)
        else:
            self.color = self.original_color

    def is_pushed(self, event):
        return is_hovered(event, self.draw_box)


class MainMenu:
    """
    Main menu with a selection of basic options
    """

    def __init__(self, surface, size):
        """
        Constructor of main menu
        :param surface: Pygame Surface object - target surface
        """
        self.surface = surface
        self.buttons = [
            Button(
                surface,
                (0.1 * size, 0.15 * size, 0.2 * size, 0.05 * size),
                "Новая игра",
                0.002 * size,
                feat.COLORS["white"]
            ),
            Button(
                surface,
                (0.1 * size, 0.25 * size, 0.2 * size, 0.05 * size),
                "Загрузить игру",
                0.002 * size,
                feat.COLORS["white"]
            ),
            Button(
                surface,
                (0.1 * size, 0.35 * size, 0.2 * size, 0.05 * size),
                "Выход",
                0.002 * size,
                feat.COLORS["white"]
            )
        ]
