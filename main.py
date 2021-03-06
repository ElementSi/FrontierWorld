import pygame as pg

import gameplay as gameplay
import interface as interface

pg.init()

screen = pg.display.set_mode((pg.display.Info().current_w, pg.display.Info().current_h))

menu = interface.Menu(screen)
game = gameplay.Gameplay(screen, menu)
is_finished = False
game_preset = "new_game"
is_game_ready = False

while not is_finished:
    if menu.is_active:
        is_game_ready = menu.activate()
        menu.update_menu()
        menu.draw_background()
        menu.draw()
        menu.update_display()
        is_finished = menu.is_finished

    else:
        if not is_game_ready:
            game = gameplay.Gameplay(screen, menu)
            is_game_ready = True
        game.process_input()
        game.update_interface()
        game.draw_map()
        game.draw_objects()
        game.draw_interface()
        game.create_new_animal()
        game.ai_acts()
        game.do_tasks()
        game.move_creatures()
        game.update_display()
        is_finished = game.is_finished

pg.quit()
