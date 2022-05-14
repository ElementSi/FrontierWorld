import pygame as pg

import features as feat


pg.init()

class Button:
    """
    In-game button displayed on the screen
    """

    def __init__(self, surface, pos, draw_box, text, fontsize, color):
        """
        Constructor of button
        :param surface: Pygame Surface object - target window
        :param draw_box: Pygame Rect object - position and size
        :param text: string - text on button
        :param color: tuple(int, int, int) - base color of button in RGB
        """
        self.surface = surface
        self.draw_box = draw_box
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text = text
        self.fontsize = fontsize
        self.original_color = color
        self.color = color
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def is_hovered(self, event):
        if event[0] in range(self.rect.left, self.rect.right) and event[1] in range(self.rect.top,
                                                                                    self.rect.bottom):
            return True
        return False

    def colour_change(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = self.fontsize.render(self.text, True, self.original_color)
        else:
            self.text = self.fontsize.render(self.text, True, self.color)

    def update(self, screen):
        if self.surface is not None:
            screen.blit(self.surface, self.rect)
        screen.blit(self.text, self.text_rect)

    def get_font(size):  # Returns Press-Start-2P in the desired size
        return pg.font.Font("Textures/menu/font.ttf", size)

    def main_menu(SCREEN, flag):
        SCREEN.blit(background, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(960, 150))

        PLAY_BUTTON = Button(surface=pg.image.load("Textures/.png"), pos=(960, 375),
                             text_input="PLAY", fontsize=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pg.image.load("Textures/menu/Options Rect.png"), pos=(960, 600),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pg.image.load("Textures/menu/Quit Rect.png"), pos=(960, 825),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SURFACE.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.is_hovered(MENU_MOUSE_POS):
                    flag = 1
                    SCREEN.fill((0, 0, 0, 0))
                if OPTIONS_BUTTON.is_hovered(MENU_MOUSE_POS):
                    pg.quit()
                if QUIT_BUTTON.is_hovered(MENU_MOUSE_POS):
                    pg.quit()
        return flag
