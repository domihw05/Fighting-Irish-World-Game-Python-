from cmu_graphics import *
from Block import Block
from Ant import Ant
from Clover import Clover
from PotOfGold import PotOfGold

class Map:
    def __init__(self,mapNum,appWidth,appHeight,scrollX):
        self.appWidth = appWidth
        self.appHeight = appHeight
        #keeps track of ants and clovers and gold
        self.ants = []
        self.clovers = []
        self.gold = []
        #unpacks map,dirt blocks,ants,clovers,gold
        self.map,self.illegalBlocks = self.unloadMapFile(mapNum) #creates a 2D list of block objects and a set with all illegal blocks
        self.rows,self.cols = len(self.map),len(self.map[0])
        self.displayCols = 30
        self.scrollX = scrollX
    
    def draw(self):
        #draws dirt blocks
        blockWidth,blockHeight = self.getBlockSize()
        leftCol,rightCol = self.getDisplayRange()
        for row in range(self.rows):
            for col in range(leftCol,rightCol+1):
                currBlock = self.map[row][col]
                currBlock.draw(self.scrollX,blockWidth,blockHeight)

    def getDisplayRange(self):
        blockWidth,blockHeight = self.getBlockSize()
        leftCol = int(self.scrollX // blockWidth)
        rightCol = leftCol + self.displayCols + 1
        return (leftCol,rightCol)
    
    def getBlockSize(self):
        blockWidth = self.appWidth / self.displayCols
        blockHeight = self.appHeight / self.rows
        return (blockWidth,blockHeight)
    
    def unloadMapFile(self,mapNum): # Opens CSV file AND converts to a 2D List
        if(mapNum == 1):
            filename = 'FightingIrishWorldMap1.csv'
        elif(mapNum == 2):
            filename = 'FightingIrishWorldMap2.csv'
        elif(mapNum == 3):
            filename = 'FightingIrishWorldMap3.csv'
        with open(filename, encoding='utf-8') as f:
            fileString = f.read()
        map = []
        illegalBlocks = set()
        rowIdx = 0
        groundLevelY = self.appHeight * 0.6431
        for line in fileString.splitlines():
            row = []
            colIdx = 0
            for num in line.split(','):
                material = int(num)
                if(material == 2):
                    self.ants.append(Ant(colIdx,groundLevelY,self))
                elif(material == 3):
                    self.clovers.append(Clover(colIdx,groundLevelY,self))
                elif(material == 4):
                    self.gold.append(PotOfGold(colIdx,rowIdx,self))
                newBlock = Block(rowIdx,colIdx,material)
                row.append(newBlock)
                if(material == 1):
                    illegalBlocks.add(newBlock)
                colIdx += 1
            map.append(row)
            rowIdx += 1
        
        return (map,illegalBlocks)
