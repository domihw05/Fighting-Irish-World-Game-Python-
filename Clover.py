from cmu_graphics import *
from PIL import Image, ImageDraw

class Clover:
    def __init__(self,col,cy,map):
        self.col = col #tracks sprite's column on map
        self.cx = 0 #tracks sprite's movement from column
        self.cy = cy #tracks change in Y
        self.movingLeft = True
        #clover hitbox
        self.width = 35
        self.height = 35
        self.map = map
        #sprite
        self.sprite = Image.open('images/Clover.png') #Image from website: https://www.vhv.rs/viewpic/iTwwbwR_four-leaf-clover-symbol-hd-png-download/
    
    def getSides(self): #return sides of the clover
        blockWidth,blockHeight = self.map.getBlockSize()
        top0 = self.cy - (self.height / 2)
        canvasX = (self.col * blockWidth) + self.cx - self.map.scrollX
        left0 = canvasX - (self.width / 2)
        right0 = canvasX + (self.width / 2)
        bottom0 = self.cy + (self.height / 2)
        return (left0,top0,right0,bottom0)

    def draw(self,map):
        if(self.isOnScreen(map)):
            blockWidth,blockHeight = map.getBlockSize()
            drawX = (self.col * blockWidth) + self.cx - map.scrollX
            drawImage(CMUImage(self.sprite),drawX,self.cy,align='center',width=self.width,height=self.height)

    def isOnScreen(self,map):
        leftCol,rightCol = map.getDisplayRange()
        return leftCol <= self.col <= rightCol
