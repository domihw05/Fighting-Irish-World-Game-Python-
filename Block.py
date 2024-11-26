from cmu_graphics import *

class Block:
    def __init__(self,row,col,material):
        self.row = row
        self.col = col
        #2 == ant and 3 == clover and 4 == pot of gold
        if material == 0 or material == 2 or material == 3 or material == 4:
            self.color = 'deepSkyBlue' #air
            self.border = None
        elif material == 1:
            self.color = 'sienna' #dirt
            self.border = 'tan'
    
    def draw(self,scrollX,width,height):
        blockLeft,blockTop = self.getBlockLeftTop(scrollX,width,height)
        drawRect(blockLeft,blockTop,width,height,fill=self.color,border=self.border)

    def getBlockLeftTop(self,scrollX,width,height):
        blockLeft = (width * self.col) - scrollX #converts col to center screen again
        blockTop = height * self.row
        return (blockLeft,blockTop)
    
    def getBlockSides(self,scrollX,width,height):
        left1,top1 = self.getBlockLeftTop(scrollX,width,height)
        right1 = left1 + width
        bottom1 = top1 + height
        return(left1,top1,right1,bottom1)