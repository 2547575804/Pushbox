import pygame, sys
from pygame.locals import *
from sprite import *
from const import *
from level import *

class Game(object):
    def __init__(self, surface, relativePos, controlType):
        self.surface = surface
        self.relativePos = relativePos
        self.controlType = controlType
        self.level = Level(1)
        self.loadLevel()

    @property
    def row(self):
        return self.level.row

    @property
    def col(self):
        return self.level.col
    
    @property
    def map(self):
        return self.level.GetMap()
    
    def loadLevel(self):
        self.level.LoadLevel()
        self.loadMapSprites()
        self.loadDynamicSprites()
    
    def loadMapSprites(self):
        self.mapSprites = []
        for i in range(self.row):
            mapSpriteRow = []
            for j in range(self.col):
                sType = self.map[i][j]
                res = SPRITE_RES[ sType ]
                spr = Sprite(res, i, j, self.relativePos)
                mapSpriteRow.append(spr)
            self.mapSprites.append(mapSpriteRow)

    def draw(self):
        self.drawMap()
        self.drawDynamicSprites()

    def drawMap(self):
        for i in range(self.row):
            for j in range(self.col):
                self.mapSprites[i][j].draw(self.surface)

    def loadSprites(self, sType, posList):
        spriteList = []
        for pos in posList:
            res = SPRITE_RES[ sType ]
            spr = Sprite(res, pos[0], pos[1], self.relativePos)
            spriteList.append(spr)
        return spriteList
        
    def loadDynamicSprites(self):
        self.goalSprites = self.loadSprites(const.SpriteType.GOAL, self.level.GetDynamicObjIndexes(SpriteType.GOAL))
        self.boxSprites = self.loadSprites(const.SpriteType.BOX, self.level.GetDynamicObjIndexes(SpriteType.BOX))
        self.playerSprite = self.loadSprites(const.SpriteType.PLAYER, self.level.GetDynamicObjIndexes(SpriteType.PLAYER)) [0]

    def updateDynamicSprites(self):
        goalIndexes = self.level.GetDynamicObjIndexes(SpriteType.GOAL)
        boxIndexes = self.level.GetDynamicObjIndexes(SpriteType.BOX)
        playerIndex = self.level.GetDynamicObjIndexes(SpriteType.PLAYER)[0]
        for i, goal in enumerate(self.goalSprites):
            goal.updateIdx(*goalIndexes[i])
        for i, box in enumerate(self.boxSprites):
            box.updateIdx(*boxIndexes[i])
        self.playerSprite.updateIdx(*playerIndex)

    def update(self):
        self.updateDynamicSprites()
        if self.controlType == ControlType.REN:
            self.level.KeydownHandler()
            pressed = pygame.key.get_pressed()
            if pressed[K_0]:
                self.loadLevel()
        else:
            self.level.AutoMove()
        if self.level.checkLevel():
            self.loadLevel()


    def drawDynamicSprites(self):
        for goal in self.goalSprites:
            goal.draw(self.surface)
        for box in self.boxSprites:
            box.draw(self.surface)
        self.playerSprite.draw(self.surface)

   