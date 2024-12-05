import pygame, sys
from pygame.locals import *
from game import *
import const

pygame.init()
DISPLAYSURF = pygame.display.set_mode((const.GAME_WIDTH_SIZE, const.GAME_HEIGHT_SIZE))
gameRen = Game(DISPLAYSURF, (100, 100), const.ControlType.REN )
# gameJI = Game(DISPLAYSURF, (100, 20), const.ControlType.JI )

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    gameRen.update()
    # gameJI.update()
    DISPLAYSURF.fill( (0,0,0) )
    gameRen.draw()
    # gameJI.draw()
    # if gameJI.level.level > gameRen.level.level:
    #     DISPLAYSURF.fill( (0,0,0) )
    #     image = pygame.image.load("res/lose.png")
    #     DISPLAYSURF.blit(image, image.get_rect())
    pygame.display.update()
