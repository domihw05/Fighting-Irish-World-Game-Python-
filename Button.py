from cmu_graphics import *

class Button:
    def __init__(self,left,top,width,height,label):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.label = label

    def draw(self):
        drawRect(self.left,self.top,self.width,self.height,fill='darkGreen',\
                 border='gold',borderWidth=5)
        centerX = self.left + self.width/2
        centerY = self.top + self.height/2
        drawLabel(self.label,centerX,centerY,size=30,fill='white')

    def onMousePress(self,mouseX,mouseY):
        left = self.left
        right = self.left + self.width
        top = self.top
        bottom = self.top + self.height
        if(left <= mouseX <= right and top <= mouseY <= bottom):
            return True
        return False
