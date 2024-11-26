from cmu_graphics import *
from Player import Player
from Map import Map
from Ant import Ant
from Button import Button

def onAppStart(app):
    app.buttons = []
    for i in range(3):
        left = app.width/13 + i*(app.width/3.5) + i*15
        top = app.height/1.5
        width = app.width/4
        height = app.height/6
        label = f'Map {i+1}'
        app.buttons.append(Button(left,top,width,height,label))
    reset(app,1)

def reset(app,mapNum):
    app.mapNum = mapNum
    app.map = Map(app.mapNum,app.width,app.height,0)
    app.player = Player(app.width/2,app.height/2,app.map)
    app.playerMovingX = False #checks if player moving horizontally

    app.stepsPerSecond = 150
    app.stepCount = 0
    app.score = 0
#---------------------------------------------------

def start_redrawAll(app):
    drawLabel("Fighting Irish World",app.width/2,app.height/3,\
              size=100,fill='green',font='Helvetica',border='gold',borderWidth=2)
    for button in app.buttons:
        button.draw()

def start_onMousePress(app,mouseX,mouseY):
    for i in range(len(app.buttons)):
        currButton = app.buttons[i]
        if(currButton.onMousePress(mouseX,mouseY)):
            reset(app,i+1)
            setActiveScreen('game')

#---------------------------------------------------

def game_redrawAll(app):
    app.map.draw()
    app.player.draw()
    for clover in app.map.clovers:
        clover.draw(app.map)
    for ant in app.map.ants:
        ant.draw(app.map)
    drawLives(app)

def drawLives(app):
    livesCount = app.player.lives
    for i in range(livesCount):
        cx = app.width*100/112 - (i * 70)
        cy = app.height/10
        r = app.height/25
        drawCircle(cx,cy,r,fill='red')

def game_onKeyPress(app, key):
    if (key == "left"):    
        app.player.move(app.map,-4,app.player.dy,True)
        app.player.movingLeft = True
    elif (key == "right"):
        app.player.move(app.map,4,app.player.dy,True)
        app.player.movingLeft = False
    elif(key == 'up'):
        app.player.jumpCount += 1
        if(app.player.jumpCount <= 2):
            app.player.move(app.map,0,-20,True) #jumps
    elif(key == 'p'):
        setActiveScreen('pause')
    
    leftCol,rightCol = app.map.getDisplayRange()
    if(rightCol == app.map.cols - 1):
        setActiveScreen('score')

def game_onKeyHold(app,keys):
    if ("left" in keys):    
        app.player.move(app.map,-8,app.player.dy,True)
        app.playerMovingX = True
        app.player.movingLeft = True
    elif ("right" in keys): 
        app.player.move(app.map,8,app.player.dy,True)
        app.playerMovingX = True
        app.player.movingLeft = False

def game_onKeyRelease(app,key):
    app.playerMovingX = False

def game_onStep(app):
    app.player.gravity(app.map,app.playerMovingX)
    if(app.player.cy + app.player.height >= app.map.appHeight):
        setActiveScreen('dead')
    for ant in app.map.ants:
        ant.onStep(app.player)
        if(ant.isOnScreen(app.map) and ant.spriteCounter != 4):    
            checkPlayerCollision(app,ant)
            if(app.stepCount % 3 == 0):
                ant.spriteCounter = (ant.spriteCounter + 1) % 4
    for clover in app.map.clovers:
        if(clover.isOnScreen(app.map)):
            left0,top0,right0,bottom0 = app.player.getSides()
            left1,top1,right1,bottom1 = clover.getSides()
            if(rectIntersect(left0,top0,right0,bottom0,\
                             left1,top1,right1,bottom1)):
                app.map.clovers.remove(clover)
                if(app.player.lives < 3): #max player lives
                    app.player.lives = app.player.lives + 1
    if(not app.playerMovingX):
        app.player.spriteCounter = 4
    elif(app.stepCount % 3 == 0):
        app.player.spriteCounter = (app.player.spriteCounter + 1) % 4
    app.stepCount += 1

def checkPlayerCollision(app,enemy):
    #retrieves player current dimensions
    left0,top0,right0,bottom0 = app.player.getSides()
    #retrieves players old dimensions
    oldLeft0,oldTop0,oldRight0,oldBottom0 = app.player.previousSides
    #retrieves enemies current dimensions
    left1,top1,right1,bottom1 = enemy.getSides()
    #checks Rectangle intersection (Player,enemy)
    if(rectIntersect(left0,top0,right0,bottom0,\
                     left1,top1,right1,bottom1)): 
        if(not enemy.collided):
            print("Previous:",app.player.previousBottom)
            print("Current:",bottom0)
            print("ANT:",top1)
            if(app.player.previousBottom < top1): #intersected through top (kills enemy)
                if(isinstance(enemy,Ant)):
                    app.map.ants.remove(enemy) #ant dies
                    app.score += 10 #score increases
            else: #intersected through side (player loses life)
                app.player.lives -= 1
                if(enemy.movingLeft):
                    app.player.move(app.map,-60,-25,True) #knockback
                else:
                    app.player.move(app.map,60,-25,True) #knockback
                if(app.player.lives == 0):
                    setActiveScreen('dead')
            enemy.collided = True
    else:
        enemy.collided = False

def rectIntersect(left0,top0,right0,bottom0,left1,top1,right1,bottom1):
    if(right1 >= left0 and right0 >= left1 and \
       bottom1 >= top0 and bottom0 >= top1):
        return True
    else:
        return False
        

#---------------------------------------------------

#pause screen implement here
def pause_redrawAll(app):
    app.map.draw()
    app.player.draw()
    for ant in app.map.ants:
        ant.draw(app.map)
    drawRect(0,0,app.width,app.height,fill='gray',opacity=50)
    drawLabel('Game Paused',app.width/2,app.height/2)

def pause_onKeyPress(app,key):
    if(key == 'p'):
        setActiveScreen('game')

#---------------------------------------------------

#pause screen implement here
def dead_redrawAll(app):
    app.map.draw()
    app.player.draw()
    for ant in app.map.ants:
        ant.draw(app.map)
    drawRect(0,0,app.width,app.height,fill='gray',opacity=50)
    drawLabel('YOU DIED',app.width/2,app.height/2,size=40,fill='red')

def dead_onKeyPress(app,key):
    if(key == 'r'):
        reset(app,app.mapNum)
        setActiveScreen('game')

#---------------------------------------------------

def score_redrawAll(app):
    drawRect(app.width/2,app.height/2,app.width * 3/4,app.height*3/5,\
             fill='green',border='gold',borderWidth = 20,align='center')
    drawLabel('GAME OVER',app.width/2,app.height/3,size=70,fill = 'white')
    drawLabel(f'Congrats, You Won! Score: {app.score}',app.width/2,\
              app.height/2,size=34,fill = 'white')
    drawLabel("Press 'h' to return to start screen",app.width/2,\
              app.height*2/3,size = 25,fill='white')
    drawLabel("Press 'r' to restart current game",app.width/2,\
              app.height*5/7,size = 25,fill='white')
    
def score_onKeyPress(app,key):
    if key == 'h':
        setActiveScreen('start')
    elif key == 'r':
        reset(app,app.mapNum)
        setActiveScreen('game')

#---------------------------------------------------

def main():
    runAppWithScreens(initialScreen='start',width=1000,height=660)

main()