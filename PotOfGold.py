from cmu_graphics import *
from PIL import Image, ImageDraw

class PotOfGold:
    def __init__(self,col,row,map):
        self.col = col #tracks sprite's column on map
        self.row = row
        self.cx = 15 #tracks sprite's movement from column
        self.cy = 0 #tracks change in Y
        #pot of gold hitbox
        self.width = 50
        self.height = 50
        self.map = map
        #sprite
        self.sprite = Image.open('images/PotOfGold.png') #Image from website: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.stockio.com%2Ffree-clipart%2Fpot-of-gold&psig=AOvVaw3Q7tUaLZ1tHO_3vtkrPdIo&ust=1701895565664000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIiQspeV-YIDFQAAAAAdAAAAABAn
    
    def getSides(self): #return sides of the clover
        blockWidth,blockHeight = self.map.getBlockSize()
        canvasX = (self.col * blockWidth) + self.cx - self.map.scrollX
        canvasY = (self.row * blockHeight) + self.cy + (blockHeight / 2)
        top0 = canvasY - (self.height / 2)
        left0 = canvasX - (self.width / 2)
        right0 = canvasX + (self.width / 2)
        bottom0 = canvasY + (self.height / 2)
        return (left0,top0,right0,bottom0)

    def draw(self,map):
        if(self.isOnScreen(map)):
            blockWidth,blockHeight = map.getBlockSize()
            drawX = (self.col * blockWidth) + self.cx - map.scrollX
            drawY = (self.row * blockHeight) + self.cy + (blockHeight / 2)
            drawImage(CMUImage(self.sprite),drawX,drawY,align='center',width=self.width,height=self.height)

    def isOnScreen(self,map):
        leftCol,rightCol = map.getDisplayRange()
        return leftCol <= self.col <= rightCol
