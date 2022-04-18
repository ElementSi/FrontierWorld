import pygame as pg


pg.init()
screen = pg.display.set_mode((100, 100))
finished = False


while not finished:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
        elif event.type == pg.KEYDOWN:
            print(event.key)

pg.quit()
