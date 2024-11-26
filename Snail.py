from cmu_graphics import *

class Snail:
    def __init__(self,col,enemyY,map):
        self.col = col #tracks enemy sprite's column on map
        self.cx = 0 #tracks enemies sprite's movement from column
        self.enemyY = enemyY
        #enemy hitbox
        self.width = 30
        self.height = 30
        self.map = map
        #Velocity
        self.dy = 0
        #Acceleration
        self.ddy = 5
        #tracks enemy state
        self.collided = False
        self.jumpedOn = False

    def draw(self,map):
        if(self.isOnScreen(map)):
            leftCol,rightCol = map.getDisplayRange()
            blockWidth,blockHeight = map.getBlockSize()
            drawX = (self.col * blockWidth) + self.cx - map.scrollX
            drawRect(drawX,self.enemyY,self.width,self.height,\
                     fill='blue',align='center')
            
    def isOnScreen(self,map):
        leftCol,rightCol = map.getDisplayRange()
        return leftCol <= self.col <= rightCol

    def move(self,dx,dy):
        if(self.isValidMove(self.map,dx,dy)): #tries to make both movements
            self.cx += dx
            self.dy = dy
            self.enemyY += self.dy
        elif(self.isValidMove(self.map,dx,0)): #tries to just make x movement
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
                and bottom1 >= top0 + dy and bottom0 + dy >= top1): #checks Rectangle intersection
                    self.dy = 0
                    self.jumpCount = 0
                    return False
        #need to check off screen y movement
        return True
    
    def getSides(self): #return sides of the ant
        blockWidth,blockHeight = self.map.getBlockSize()
        top0 = self.enemyY - (self.height / 2)
        canvasX = (self.col * blockWidth) + self.cx - self.map.scrollX
        left0 = canvasX - (self.width / 2)
        right0 = canvasX + (self.width / 2)
        bottom0 = self.enemyY + (self.height / 2)
        return (left0,top0,right0,bottom0)

    def onStep(self):
        #update column
        blockWidth,blockHeight = self.map.getBlockSize()
        dcol = self.cx // blockWidth
        self.col += dcol
        self.cx = self.cx % blockWidth
        #AI pathing movements
        if(self.isOnScreen(self.map)):
            #self.move(-2,0) #hardcoded AI
            self.move(0,5) #gravity