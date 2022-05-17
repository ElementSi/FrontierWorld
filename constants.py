import pygame as pg

FPS = 60
TILE_SIZE = 24
FONT = "fonts/Montserrat-Medium.ttf"
INTERFACE_AMENDMENT = 3
ANIMALS_LIMIT = 5

COLORS = {
    "white": (255, 255, 255),
    "cream": (191, 133, 57),
    "brown": (77, 53, 48),
    "light_blue": (80, 82, 148),
    "dark_blue": (13, 14, 41)
}

LANDSCAPE = {
    "soil": [0.9, pg.transform.scale(pg.image.load("assets/textures/soil.png"), (TILE_SIZE, TILE_SIZE))],
    "sand": [0.5, pg.transform.scale(pg.image.load("assets/textures/sand.png"), (TILE_SIZE, TILE_SIZE))],
    "rock": [0.7, pg.transform.scale(pg.image.load("assets/textures/rock.png"), (TILE_SIZE, TILE_SIZE))],
}

TASKS = {
    "chop": "object_task",
    "harvest_berries": "object_task",
    "attack": "object_task",
    "construct": "tile_task",
    "go_to": "tile_task",
    "pick_up_loot": "object_task",
    "dig": "object_task"
}
