from pygame.locals import *
from const import *
import pygame
from utils import *
from pather import *

class Level(object):
    def __init__(self, level):
        self.map = []
        self.dynamicObjIndexes = {
            SpriteType.GOAL: [],
            SpriteType.BOX: [],
            SpriteType.PLAYER: []
        }
        self.row = 1
        self.col = 1
        self.level = level
        self.pressTime = {}
        self.pather = Pather()
        self.LoadLevel()

    def LoadLevel(self):
        self.map = []
        goalIndexes = []
        boxIndexes = []
        playerIndexes = []
        with open ('data/level/' + str(self.level) + '.x', 'r') as f:
            lines = f.readlines()
            r, c = lines[0].split(' ')
            self.row = int(r)
            self.col = int(c)
            r = 0
            for line in lines[1:]:
                mapRow = []
                for c in range(self.col):
                    if line[c] == SpriteType.BOX:
                        mapRow.append(SpriteType.FLOOR)
                        boxIndexes.append( [r, c] )
                    elif line[c] == SpriteType.PLAYER:
                        mapRow.append(SpriteType.FLOOR)
                        playerIndexes.append( [r, c] )
                    elif line[c] == SpriteType.GOAL:
                        mapRow.append(SpriteType.FLOOR)
                        goalIndexes.append( (r, c) )
                    else:
                        mapRow.append(line[c])

                self.map.append(mapRow)
                r += 1
        self.dynamicObjIndexes = {
            SpriteType.GOAL: goalIndexes,
            SpriteType.BOX: boxIndexes,
            SpriteType.PLAYER: playerIndexes
        }
        self.pather.StartRecord(self.level)
        self.autoMoveIndex = 0
        self.lastAutoMoveTime = getCurrentTime()
        
    def GetMap(self):
        return self.map
    
    def GetDynamicObjIndexes(self, sType):
        return self.dynamicObjIndexes[sType]
    
    def checkAndSetPressTime(self, key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 150:
            ret = True
            self.pressTime[key] = getCurrentTime()
        return ret
    
    def KeydownHandler(self):
        pressed = pygame.key.get_pressed()
        for i, key in enumerate(DIR_KEY):
            if pressed[key] and self.checkAndSetPressTime(key):
                self.move(i)

    def move(self, i):
        playerIndex = self.GetDynamicObjIndexes(SpriteType.PLAYER)[0]
        r, c = playerIndex[0], playerIndex[1]
        nr = r + DIR[i][0]
        nc = c + DIR[i][1]
        if self.isFloor(nr, nc):
            self.setPlayerIndex( nr, nc )
            self.pather.AddRecord(i)
        elif self.isBox(nr, nc):
            if self.canPush(nr, nc, i):
                self.pushBox(nr, nc, i)
                self.pather.AddRecord(i)
                
    def AutoMove(self):
        import random
        if getCurrentTime() - self.lastAutoMoveTime > random.randint(200, 500):
            self.lastAutoMoveTime = getCurrentTime()
            if self.autoMoveIndex < len(self.pather.getRecords()):
                self.move(self.pather.getRecords()[self.autoMoveIndex])
                self.autoMoveIndex += 1
            else:
                self.move(random.randint(0, 3))

    def setPlayerIndex(self, r, c):
        playerPos = self.GetDynamicObjIndexes(SpriteType.PLAYER)
        playerPos[0] = (r, c)    

    def isFloor(self, r, c):
        if r < 0 or c < 0:
            return False
        if r >= self.row or c >= self.col:
            return False
        if self.map[r][c] == SpriteType.WALL:
            return False
        for box in self.GetDynamicObjIndexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                return False
        return True
    
    def isBox(self, r, c):
        for box in self.GetDynamicObjIndexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                return True
        return False

    def canPush(self, r, c, d):
        nr = r + DIR[d][0]
        nc = c + DIR[d][1]
        return self.isFloor(nr, nc)
    
    def pushBox(self, r, c, d):
        for box in self.GetDynamicObjIndexes(SpriteType.BOX):
            if box[0] == r and box[1] == c:
                nr = r + DIR[d][0]
                nc = c + DIR[d][1]
                if self.isFloor(nr, nc):
                    box[0] = nr
                    box[1] = nc
                    self.setPlayerIndex( r, c )
    
    def checkFinish(self):
        for box in self.GetDynamicObjIndexes(SpriteType.BOX):
            find = False
            for goal in self.GetDynamicObjIndexes(SpriteType.GOAL):
                if box[0] == goal[0] and box[1] == goal[1]:
                    find = True
                    break
            if find == False:
                return False
        return True
    
    def checkLevel(self):
        if self.checkFinish():
            self.pather.DumpRecord()
            self.level += 1
            self.LoadLevel()
            return True
        return False