from cmu_graphics import *
import os, pathlib
from PIL import Image, ImageDraw

class Player:
    def __init__(self,cx,cy,map):
        #player location
        self.cx = cx
        self.cy = cy
        #player hitbox
        self.width = 25
        self.height = 80
        #initializes previous position
        self.previousSides = self.getSides()
        #Velocity
        self.dy = 0
        self.movingLeft = False
        #Acceleration
        self.ddy = 2.5
        #tracks jumps in a row
        self.jumpCount = 0
        #lives
        self.lives = 3
        #tracks map
        self.map = map
        #standing sprite
        self.image = Image.open('images/Lep.png') #Image from website: https://spritedatabase.net/file/22235
        #spritestrip
        spritestrip = Image.open('images/LepRunningStrip.png') #Image from website: https://spritedatabase.net/file/22235
        self.sprites = [ ]
        for i in range(4):
            sprite = spritestrip.crop((0 + 70*i, 0, 70+70*i, 103))
            self.sprites.append(sprite)
        self.sprites.append(self.image)
        # app.spriteCounter shows which sprite (of the list) 
        # we should currently display
        self.spriteCounter = 0

    def move(self,map,dx,dy,shouldUpdatePrev):
        if(self.isValidMove(map,dx,dy,shouldUpdatePrev)): #checks if can make both movements
            map.scrollX += dx
            self.dy = dy
            self.cy += self.dy
        elif(self.isValidMove(map,dx,0,shouldUpdatePrev)): #checks if can make x movement
            map.scrollX += dx
        elif(self.isValidMove(map,0,dy,shouldUpdatePrev)): #checks if can make y movement
            self.dy = dy
            self.cy += self.dy
        if(not self.isValidMove(map,dx,0,False)): #Gets as close to obstacle as possible
            if(dx > 0):
                self.move(map,dx-1,0,False)
            elif(dx < 0):
                self.move(map,dx+1,0,False)
        if(not self.isValidMove(map,0,dy,False)): #Gets as close to obstacle as possible
            if(dy > 0):
                self.move(map,0,dy-1,False)
            elif(dy < 0):
                self.move(map,0,dy+1,False)
    
    def getSides(self): #return sides of the player's rectangle
        top0 = self.cy - (self.height / 2)
        left0 = self.cx - (self.width / 2)
        right0 = self.cx + (self.width / 2)
        bottom0 = self.cy + (self.height / 2)
        return (left0,top0,right0,bottom0)
    
    def gravity(self,map,movingX): 
        self.dy += self.ddy #applies acceleration 
        if(not movingX): #pulls player down if not moving left or right
            self.move(map,0,self.dy,True)    

    def isValidMove(self,map,dx,dy,shouldUpdatePrev):
        #gets current player dimensions
        left0,top0,right0,bottom0 = self.getSides()
        #gets potential new player dimensions
        newLeft0,newTop0,newRight0,newBottom0 = left0+dx,top0+dy,right0+dx,bottom0+dy
        leftCol,rightCol = map.getDisplayRange() #display range
        blockWidth,blockHeight = map.getBlockSize() #block size
        newLeftCol = int((map.scrollX + dx) // blockWidth) #new display range
        newRightCol = newLeftCol + map.displayCols + 1 #new display range
        if(newLeftCol < 0 or newRightCol >= map.cols): #ensures map doesn't go out of range
            return False
        #loops through all brick blocks
        for block in map.illegalBlocks:
            if(leftCol <= block.col <= rightCol): #checks if block is on screen
                left1,top1,right1,bottom1 = block.getBlockSides(map.scrollX,blockWidth,blockHeight)
                if(self.rectIntersect(newLeft0,newTop0,newRight0,\
                                      newBottom0,left1,top1,right1,bottom1)):
                    self.dy = 0
                    self.jumpCount = 0
                    return False
        if(self.cy + dy <= 0): #checks if player is jumping too high
            return False
        if(((dy != 0 or dx != 0) and shouldUpdatePrev)): #checks if previous position should be updated
            self.previousSides = left0,top0,right0,bottom0
        return True
    
    def draw(self):
        sprite = self.sprites[self.spriteCounter]
        if(self.movingLeft):
            sprite = sprite.transpose(Image.FLIP_LEFT_RIGHT)
        drawImage(CMUImage(sprite),self.cx,self.cy,align='center',width=self.width*2,height=self.height)

    def rectIntersect(self,left0,top0,right0,bottom0,left1,top1,right1,bottom1):
        if(right1 >= left0 and right0 >= left1 and \
        bottom1 >= top0 and bottom0 >= top1): #from CS academy 3.3.5 (Intersections)
            return True
        else:
            return False
        

