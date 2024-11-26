from cmu_graphics import *
import os, pathlib
from PIL import Image, ImageDraw

class Ant:
    def __init__(self,col,enemyY,map):
        self.col = col #tracks enemy sprite's column on map
        self.cx = 0 #tracks enemies sprite's movement from column
        self.enemyY = enemyY #tracks change in Y
        self.movingLeft = True
        #enemy hitbox
        self.width = 50
        self.height = 30
        self.map = map
        #Velocity
        self.dy = 0
        #Acceleration
        self.ddy = 5
        #tracks if player is currently in ant
        self.collided = False
        #sprite
        spritestrip = Image.open('images/Enemies.png') #Image from website: https://spritedatabase.net/file/22357
        self.sprites = [ ]
        for i in range(5):
            sprite = spritestrip.crop((0 + 76*i, 0, 76+76*i, 44))
            self.sprites.append(sprite)
        self.spriteCounter = 0

    def draw(self,map):
        if(self.isOnScreen(map)):
            blockWidth,blockHeight = map.getBlockSize()
            #calculates cx on canvas
            drawX = (self.col * blockWidth) + self.cx - map.scrollX 
            sprite = self.sprites[self.spriteCounter]
            if(not self.movingLeft):
                 sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
            drawImage(CMUImage(sprite),drawX,self.enemyY,align='center',width=self.width,height=self.height)
            
    def isOnScreen(self,map):
        leftCol,rightCol = map.getDisplayRange()
        return leftCol <= self.col <= rightCol

    def move(self,dx,dy):
        if(self.isValidMove(self.map,dx,dy)): #tries to make both movements
            self.cx += dx
            self.dy = dy
            self.enemyY += self.dy
        if(self.isValidMove(self.map,dx,0)): #tries to just make x movement
            self.cx += dx
        elif(self.isValidMove(self.map,0,dy)): #tries to just make y movement
            self.dy = dy
            self.enemyY += self.dy
        if(not self.isValidMove(self.map,dx,0)): #Gets as close to obstacle
            if(dx > 0):
                self.move(dx-1,0)
            elif(dx < 0):
                self.move(dx+1,0)
        if(not self.isValidMove(self.map,0,dy)): #Gets as close to obstacle
            if(dy > 0):
                self.move(0,dy-1)
            elif(dy < 0):
                self.move(0,dy+1)

    def isValidMove(self,map,dx,dy):
        blockWidth,blockHeight = map.getBlockSize()
        left0,top0,right0,bottom0 = self.getSides()
        leftCol,rightCol = map.getDisplayRange()
        for block in map.illegalBlocks:
            if(leftCol <= block.col <= rightCol): #checks if block is on screen
                left1,top1,right1,bottom1 = block.getBlockSides(map.scrollX,blockWidth,blockHeight)
                if(right1 >= left0 + dx and right0 + dx >= left1 \
                and bottom1 >= top0 + dy and bottom0 + dy >= top1): #from CS academy 3.3.5 (Intersections)
                    return False
        return True
    
    def getSides(self): #return sides of the ant
        blockWidth,blockHeight = self.map.getBlockSize()
        top0 = self.enemyY - (self.height / 2)
        canvasX = (self.col * blockWidth) + self.cx - self.map.scrollX
        left0 = canvasX - (self.width / 2)
        right0 = canvasX + (self.width / 2)
        bottom0 = self.enemyY + (self.height / 2)
        return (left0,top0,right0,bottom0)

    def onStep(self,player):
        #update column position on map
        blockWidth,blockHeight = self.map.getBlockSize()
        dcol = self.cx // blockWidth
        self.col += dcol
        self.cx = self.cx % blockWidth
        #AI pathing movements
        if(self.isOnScreen(self.map)):
            canvasX = (self.col * blockWidth) + self.cx - self.map.scrollX
            if(self.collided):
                pass
            elif(player.cx - canvasX < -player.width/2): #if player left of ant
                self.move(-1,0)
                self.movingLeft = True
            elif(player.cx - canvasX > player.width/2): #if player right of ant
                self.move(1,0)
                self.movingLeft = False
            self.move(0,5) #gravity
            
        