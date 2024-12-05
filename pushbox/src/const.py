from pygame.locals import *

GAME_WIDTH_SIZE = 1200
GAME_HEIGHT_SIZE = 800

SPRITE_SIZE_W = 64
SPRITE_SIZE_H = 64

DIR = (
    (-1, 0), # up
    (0, 1),  # right
    (1, 0),  # down
    (0, -1)  # left
)

DIR_KEY = (K_UP, K_RIGHT, K_DOWN, K_LEFT)

class SpriteType:
    FLOOR = '.'
    WALL = '#'
    BOX = 'o'
    GOAL = 'O'
    PLAYER = 'I'

SPRITE_RES = {
    SpriteType.FLOOR: 'res/floor.png',
    SpriteType.WALL: 'res/wall.png',
    SpriteType.BOX: 'res/box.png',
    SpriteType.GOAL: 'res/goal.png',
    SpriteType.PLAYER: 'res/player.png'
}

class ControlType:
    REN = 0
    JI = 1