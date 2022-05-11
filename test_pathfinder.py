import pygame as pg

import constants as const
import map_objects as objects
import game_map as game_map
import interface as interface


pg.init()

SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GameMap = game_map.Map(screen, [SCREEN_WIDTH, SCREEN_HEIGHT])

ListSolidObject = []

for i in range(GameMap.height):
    for j in range(GameMap.width):
        if GameMap.field[i][j].pre_object == "tree":
            ListSolidObject.append(objects.Tree(screen, [j, i]))
        elif GameMap.field[i][j].pre_object == "bush":
            ListSolidObject.append(objects.Bush(screen, [j, i]))
        elif GameMap.field[i][j].pre_object == "cliff":
            ListSolidObject.append(objects.Cliff(screen, [j, i]))

Settler = objects.Settler(screen, [0, 0])

GameMap.draw()
for SolidObject in ListSolidObject:
    SolidObject.draw()

pg.display.update()
pg.time.wait(3000)

print(Settler.pathfinder([9, 9], GameMap, ListSolidObject))
