# 实现一个pygame的精灵类
# 图片资源由传参决定
# 并且传入 rowIdx 和 colIdx 代表处于哪个方格

import pygame
import const

class Sprite(pygame.sprite.Sprite):
    def __init__(self, imgPath, rowIdx, colIdx, relativePos):
        super(Sprite, self).__init__()
        self.image = pygame.image.load(imgPath)
        # 将图片大小改为 wxh
        self.image = pygame.transform.scale(self.image, (const.SPRITE_SIZE_W, const.SPRITE_SIZE_H))
        self.rect = self.image.get_rect()
        self.relativePos = relativePos
        self.updateRowIdx(rowIdx)
        self.updateColIdx(colIdx)
    
    def updateRowIdx(self, rowIdx):
        self.rowIdx = rowIdx
        self.rect.y = self.relativePos[0] + rowIdx * self.rect.height

    def updateColIdx(self, colIdx):
        self.colIdx = colIdx
        self.rect.x = self.relativePos[1] + colIdx * self.rect.width
    
    def updateIdx(self, rowIdx, colIdx):
        self.updateRowIdx(rowIdx)
        self.updateColIdx(colIdx)
    
    # 实现一个图片的渲染函数
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        