import keyboard
import time
from random import randint
import sys
from colorama import Fore, Back, Style
class snake:
        posx: int
        posy: int
        directionx: int
        directiony: int
        maxx: int
        maxy: int
        g = 0
        fields = []
        multiplier: int
        multiplierCountdown: int
        magnetism: bool
        magnetismCountdown: int
        adding: int
        score: int
        hasEaten: int
        movedSinceMovementUpdate: bool
        invis: bool
        inviscountdown: int
        
        def __init__(self, ga, x, y, length):
            length += 5
            self.directionx, self.directiony = 0, 1
            self.posx, self.posy = round(x/2), round(y/2)+round(length/2)
            self.g = ga
            self.maxx = x
            self.maxy = y
            self.fields = []
            for i in range(length):
                self.fields.append([self.posy-i, self.posx])
            self.multiplier = 1
            self.multiplierCountdown = 0
            self.magnetism = False
            self.magnetismCountdown = 0
            self.adding = 0
            self.score = 0
            self.hasEaten = 0
            self.movedSinceMovementUpdate = True
            self.invis = False
            self.inviscountdown = 0
        
        def replace(self, x, y, length):
            length += 5
            self.posx, self.posy = round(x/2), round(y/2)+round(length/2)
            self.maxx = x
            self.maxy = y
            self.fields = []
            for i in range(length):
                self.fields.append([self.posy-i, self.posx])

        def move(self):
            self.movedSinceMovementUpdate = True
            if self.g.field[self.posx][self.posy] == "g":
                self.g.killSnake("You have been catched by a ghost")
            if(self.multiplierCountdown==0):
                self.multiplier = 1
            else:
                self.multiplierCountdown -= 1
            if(self.magnetismCountdown==0):
                self.magnetism = False
            else:
                self.magnetismCountdown -= 1
            if(self.inviscountdown==0):
                self.invis = False
            else:
                self.inviscountdown -= 1
            if(self.posx + (self.directionx*self.multiplier) < 0 or self.posx + (self.directionx*self.multiplier) > self.maxx-1):
                 self.g.killSnake("You ran into a wall")
            elif(self.posy + (self.directiony*self.multiplier) < 0 or self.posy + (self.directiony*self.multiplier) > self.maxy-1):
                 self.g.killSnake("You ran into a Wall")
            elif([self.posy+(self.directiony*self.multiplier), self.posx+(self.directionx*self.multiplier)] in self.fields):
                 self.g.killSnake("You ran into yourself")
            else:
                self.posx += (self.directionx*self.multiplier)
                self.posy += (self.directiony*self.multiplier)
                for i in range(len(self.fields)-1, 0, -1):
                    self.fields[i] = self.fields[i-1]
                self.fields[0] = [self.posy, self.posx]
                if self.g.field[self.posx][self.posy] == "#":
                    #self.fields.append(self.fields[len(self.fields)-1])
                    self.adding += 1
                    self.hasEaten += 2
                    self.g.field[self.posx][self.posy] = " "
                    self.g.newSpot()
                if self.g.field[self.posx][self.posy] == "x":
                    self.g.killSnake("You ran into a wall")
                if self.g.field[self.posx][self.posy] == "~":
                    self.g.field[self.posx][self.posy] = " "
                    self.multiplier = 2
                    self.multiplierCountdown += 10
                    self.magnetism = True
                    self.magnetismCountdown += 10
                if self.g.field[self.posx][self.posy] == "m":
                    self.g.field[self.posx][self.posy] = " "
                    self.magnetism = True
                    self.magnetismCountdown += 20
                if self.g.field[self.posx][self.posy] == "i":
                    self.g.field[self.posx][self.posy] = " "
                    self.invis = True
                    self.inviscountdown += 10
                if self.g.field[self.posx][self.posy] == "t":
                    possiblePos = self.g.getTeleports().copy()
                    del possiblePos[possiblePos.index([self.posx, self.posy])]
                    newPos = possiblePos[randint(0,len(possiblePos)-1)]
                    self.posx, self.posy = newPos[0], newPos[1]
                if self.magnetism:
                    if(self.posx > 0):
                        if self.g.field[self.posx-1][self.posy] == "#":
                            #self.fields.append(self.fields[len(self.fields)-1])
                            self.adding += 1
                            self.hasEaten += 2
                            self.g.field[self.posx-1][self.posy] = " "
                            self.g.newSpot()
                    if(self.posx < self.maxx -1):
                        if self.g.field[self.posx+1][self.posy] == "#":
                            #self.fields.append(self.fields[len(self.fields)-1])
                            self.adding += 1
                            self.hasEaten += 2
                            self.g.field[self.posx+1][self.posy] = " "
                            self.g.newSpot()
                    if(self.posy > 0):
                        if self.g.field[self.posx][self.posy-1] == "#":
                            #self.fields.append(self.fields[len(self.fields)-1])
                            self.adding += 1
                            self.hasEaten += 2
                            self.g.field[self.posx][self.posy-1] = " "
                            self.g.newSpot()
                    if(self.posy < self.maxy -1):
                        if self.g.field[self.posx][self.posy+1] == "#":
                            #self.fields.append(self.fields[len(self.fields)-1])
                            self.adding += 1
                            self.hasEaten += 2
                            self.g.field[self.posx][self.posy+1] = " "
                            self.g.newSpot()
                if self.adding > 0:
                    self.hasEaten -= 1
                    self.fields.append(self.fields[len(self.fields)-1])
                    self.adding -= 1
                    if(self.hasEaten > 2):
                        self.score += 1
                    if(self.hasEaten > 4):
                        self.score += 1 
                    self.score += 1
        
        def dirU(self):
            if(self.directionx == 0 and self.movedSinceMovementUpdate):
                self.directionx = -1
                self.directiony = 0
                self.movedSinceMovementUpdate = False
        def dirD(self):
            if(self.directionx == 0 and self.movedSinceMovementUpdate):
                self.directionx = 1
                self.directiony = 0
                self.movedSinceMovementUpdate = False
        def dirL(self):
            if(self.directiony == 0 and self.movedSinceMovementUpdate):
                self.directiony = -1
                self.directionx = 0
                self.movedSinceMovementUpdate = False
        def dirR(self):
            if(self.directiony == 0 and self.movedSinceMovementUpdate):
                self.directiony = 1
                self.directionx = 0
                self.movedSinceMovementUpdate = False
        
        def getCooldownMagn(self):
            return self.magnetismCountdown
        def getCooldownMulti(self):
            return self.multiplierCountdown
        def getScore(self):
            return self.score
        def getDir(self):
            if(self.directionx == 1 and self.directiony == 0):
                return "down"
            if(self.directionx == -1 and self.directiony == 0):
                return "up"
            if(self.directionx == 0 and self.directiony == 1):
                return "right"
            if(self.directionx == 0 and self.directiony == -1):
                return "left"
        def resetScore(self):
            self.score = 0
        def resetDir(self):
            self.directionx, self.directiony = 0,1
        def resetEffects(self):
            self.multiplierCountdown, self.magnetismCountdown, self.magnetism, self.multiplier = 0, 0, False, 1
            self.movedSinceMovementUpdate = True
            self.invis = False
            self.inviscountdown = 0
        def getX(self):
            return self.posx
        def getY(self):
            return self.posy
        def getCooldownInvis(self):
            return self.inviscountdown

class ghost:
    posx: int
    posy: int
    before: str
    def __init__(self, x, y):
        self.posx, self.posy = x,y

    def move(self, snakex, snakey):
        if(snakey > self.posy and snakey > self.posy+1 and self.posx == snakex):
            self.posy += 2
        elif(snakey > self.posy):
            self.posy += 1
        elif(self.posy < snakey and snakey < self.posy-1 and self.posx == snakex):
            self.posy -= 2
        elif(self.posy > snakey):
            self.posy -= 1
        
        if(snakex > self.posx and snakex > self.posx+1 and self.posy == snakey):
            self.posx += 2
        elif(snakex > self.posx):
            self.posx += 1
        elif(snakex < self.posx and snakex < self.posx-1 and self.posy == snakey):
            self.posx -= 2
        elif(self.posx > snakex):
            self.posx -= 1
    
    def getX(self):
        return self.posx
    def getY(self):
        return self.posy
    def setBefore(self, bef):
        self.before = bef
    def getBefore(self):
        return self.before
    
             
class game:
    s: snake
    field = []
    mapNum: int
    living: bool
    wallgenerating = [0, 5, 10, 15, 20, 25, 30, 35, 39, 42, 44, 45]
    curspot = 0
    winning: bool
    countdown: int
    colored: bool
    cause: str
    teleports = []
    ghosts = []
    ghostcountdown: int
    ghostMoveCountdown: int
    oldPos = []
    def __init__(self):
        self.mapNum = 0
        self.buildfield()
        self.s = snake(self, len(self.field), len(self.field[0]), self.mapNum)
        self.colored = True
    
    def startlvl(self):
        self.teleports = []
        self.oldPos = []
        self.s.replace(len(self.field), len(self.field[0]), self.mapNum)
        self.mapNum += 1
        self.s.resetScore()
        self.s.resetEffects()
        self.buildmap()
        self.living = True
        self.winning = False
        self.countdown = 0
        self.curspot = 0
        self.s.resetDir()
        self.ghostcountdown = 0
        self.ghostMoveCountdown = 2
        self.ghosts = []
        
    
    def restartlvl(self):
        self.buildfield(11, 36+(self.mapNum*2))
        self.s.replace(len(self.field), len(self.field[0]), self.mapNum)
        self.s.resetScore()
        self.s.resetEffects()
        for i in self.oldPos:
            self.field[i[0]][i[1]] = i[2]
        self.living = True
        self.winning = False
        self.countdown = 0
        self.curspot = 0
        self.s.resetDir()
        self.ghostcountdown = 0
        self.ghostMoveCountdown = 2
        self.ghosts = []
        
        
    def buildfield(self, num_of_rows=11, num_of_columns=36):
        #num_of_rows = 13 is MAX and recommended
        #num_of_columns = 36 Can be extended
        self.field = []
        for _ in range(num_of_rows):
            row = []
            for p in range(num_of_columns):
                row.append(" ")
            self.field.append(row)

    def buildmap(self):
            self.buildfield(11, 36+(self.mapNum*2))
            self.s.replace(len(self.field), len(self.field[0]), self.mapNum)
            for y in range(len(self.field)):
                for x in range(len(self.field[y])):
                    if(y == 12):
                        pass
                    if(y == 0):
                        pass
                print(" ",end="")
                r = 40
                fullrows = r%len(self.field)
                for _ in range(fullrows):
                    print("|", end="")
                r-=fullrows*len(self.field)
                if r>y:
                    print("|", end="")
                else:
                    print(" ", end="")
                print(" ", end="")
            numOfPlus = 30/self.mapNum
            while(numOfPlus > 0):
                y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                while([y,x]in self.s.fields or self.field[y][x] != " "):
                    y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                self.field[y][x] = "#"
                numOfPlus-=1
                self.oldPos.append([y,x,"#"])
            numOfMulti = 4/self.mapNum
            while(numOfMulti > 0):
                y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                while([y,x]in self.s.fields or self.field[y][x] != " "):
                    y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                self.field[y][x] = "~"
                numOfMulti-=1
                self.oldPos.append([y,x,"~"])
            numOfMagne = 4/self.mapNum
            while(numOfMagne > 0):
                y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                while([y,x]in self.s.fields or self.field[y][x] != " "):
                    y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                self.field[y][x] = "m"
                self.oldPos.append([y,x,"m"])
                numOfMagne-=1
            numOfWalls = self.mapNum
            while(numOfWalls > 0):
                y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                xpos = self.s.posx
                ypos = self.s.posy
                xdist = xpos-x
                ydist = ypos-y
                while([y,x]in self.s.fields or self.field[y][x] != " " or (xdist*xdist+ydist*ydist < 9)):
                    y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                    xdist = xpos-x
                    ydist = ypos-y
                self.field[y][x] = "x"
                self.oldPos.append([y,x,"x"])
                numOfWalls-=1
            numOfTeleports = round(len(self.field[0])/12)
            while(numOfTeleports > 0):
                y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                while([y,x]in self.s.fields or self.field[y][x] != " "):
                    y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                self.teleports.append([y,x])
                self.field[y][x] = "t"
                self.oldPos.append([y,x,"t"])
                numOfTeleports-=1
            numOfInvis = 4/self.mapNum
            while(numOfInvis > 0):
                y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                while([y,x]in self.s.fields or self.field[y][x] != " "):
                    y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                self.field[y][x] = "i"
                self.oldPos.append([y,x,"i"])
                numOfInvis-=1
            
    def addGhost(self):
        g = ghost(0,0)
        self.ghosts.append(g)
        g.setBefore(self.field[0][0])
        self.field[0][0] = "g"


    def update(self):
        if(keyboard.is_pressed("a")):
            self.s.dirL()
        if(keyboard.is_pressed("d")):
            self.s.dirR()
        if(keyboard.is_pressed("w")):
            self.s.dirU()
        if(keyboard.is_pressed("s")):
            self.s.dirD()
        if(self.ghostcountdown == 0):
            self.ghostcountdown = 1000
            self.addGhost()
        else:
            self.ghostcountdown -= 1
        if(self.countdown == 0):
            if self.curspot < len(self.wallgenerating)-1:
                if(self.wallgenerating[self.curspot+1] <= self.s.getScore()):
                    self.curspot += 1
                    if(self.curspot == len(self.wallgenerating)-1):
                        pass
                    else:
                        numOfWalls = self.mapNum
                        while(numOfWalls > 0):
                            y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                            xpos = self.s.posx
                            ypos = self.s.posy
                            xdist = xpos-x
                            ydist = ypos-y
                            while([y,x]in self.s.fields or self.field[y][x] != " " or (xdist*xdist+ydist*ydist < 12)):
                                y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
                                xdist = xpos-x
                                ydist = ypos-y
                            self.field[y][x] = "x"
                            numOfWalls-=1
            else:
                self.winning = True
        
            self.s.move()
            self.countdown = 100
            if(self.ghostMoveCountdown == 0 and not self.s.invis):
                for i in self.ghosts:
                    self.field[i.getY()][i.getX()] = i.getBefore()
                    i.move(self.s.getY(), self.s.getX())
                    i.setBefore(self.field[i.getY()][i.getX()])
                    self.field[i.getY()][i.getX()] = "g"
            self.ghostMoveCountdown -= 1
            if(self.ghostMoveCountdown < 0):
                self.ghostMoveCountdown = 3
        else:
            self.countdown -= 10
        if(self.living and self.countdown % 40 == 0):
            self.display()
        
    
    def newSpot(self):
        y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
        while([y,x]in self.s.fields or self.field[y][x] != " "):
            y, x = randint(0, len(self.field)-1), randint(0, len(self.field[0])-1)
        self.field[y][x] = "#"
        
    
    def display(self):
        for _ in range(len(self.field[0])+2):
            print(Back.RED+" ", end="")
        print(Style.RESET_ALL)
        for x, row in enumerate(self.field):
            print(Back.RED + " " + Style.RESET_ALL, end="")
            for i in range(len(row)):
                if([i,x] in self.s.fields):
                    got = False
                    for gho in self.ghosts:
                        if(gho.getX() == i and gho.getY() == x):
                            print(Back.WHITE + " ", end = "")
                            got = True
                    if not got:
                        print(Back.CYAN, end="")
                        if(self.s.posy == i and self.s.posx == x):
                            if(self.s.getDir() == "left"):
                                print("←", end="")
                            elif(self.s.getDir() == "up"):
                                print("↑", end="")
                            elif(self.s.getDir() == "right"):
                                print("→", end="")
                            elif(self.s.getDir() == "down"):
                                print("↓", end="")
                        else:
                            print(" ", end="")
                    print(Style.RESET_ALL, end="")
                else:
                    if(self.colored):
                        if(row[i] == "g"):
                            print(Back.WHITE + " ", end = "")
                        elif(row[i] == "x"):
                            print(Back.RED + " ", end = "")
                        elif(row[i] == "#"):
                            print(Back.GREEN + " ", end = "")
                        elif(row[i] == "m"):
                            print(Back.BLUE + " ", end = "")
                        elif(row[i] == "~"):
                            print(Back.MAGENTA + " ", end = "")
                        elif(row[i] == "t"):
                            print(Back.YELLOW + " ", end = "")
                        elif(row[i] == "i"):
                            print(Back.LIGHTBLACK_EX + " ", end = "")    
                        else:
                            print(row[i], end = "")
                        print(Style.RESET_ALL, end="")
                    else:
                        print(row[i], end = "")
            print(Back.RED + " " + Style.RESET_ALL, end="")
            print(" ",end="")
            r = self.s.getCooldownMagn()
            fullrows, rest = divmod(r, len(self.field)-1)
            for _ in range(fullrows):
                print(Back.BLUE +" ", end="")
                print(Style.RESET_ALL, end="")
            if rest>x:
                print(Back.BLUE + " ", end="")
                print(Style.RESET_ALL, end="")
            else:
                print(Style.RESET_ALL, end="")
                print(" ", end="")
            if(r>0):
                if x == len(self.field)-1:
                    print("magnetism", end="")
                    print(Style.RESET_ALL, end="")
                else:
                    print("         ", end="")
                print("    ", end="")
            r = self.s.getCooldownMulti()
            fullrows, rest = divmod(r, len(self.field))
            for _ in range(fullrows):
                print(Back.MAGENTA+" ", end="")
                print(Style.RESET_ALL, end="")
            if rest>x:
                print(Back.MAGENTA+" ", end="")
                print(Style.RESET_ALL, end="")
            else:
                print(" ", end="")
            if(r>0):
                if x == len(self.field)-1:
                    print("speed    ", end="")
                    print(Style.RESET_ALL, end="")
                else:
                    print("         ", end="")
                print("    ", end="")
            r = self.s.getCooldownInvis()
            fullrows, rest = divmod(r, len(self.field))
            for _ in range(fullrows):
                print(Back.LIGHTBLACK_EX+" ", end="")
                print(Style.RESET_ALL, end="")
            if rest>x:
                print(Back.LIGHTBLACK_EX+" ", end="")
                print(Style.RESET_ALL, end="")
            else:
                print(" ", end="")
            if(r>0):
                if x == len(self.field)-1:
                    print("invis    ", end="")
                    print(Style.RESET_ALL, end="")
                else:
                    print("         ", end="")
                print("    ", end="")
            if x == len(self.field)-1:
                print("Progression: "+ str(round((self.s.getScore()/45)*100) if round((self.s.getScore()/45)*100) < 100 else 100 ) + "%", end="")
            print("")
        for _ in range(len(self.field[0])+2):
                print(Back.RED+" ", end="")
                print(Style.RESET_ALL, end="")
        print("")
    
    def killSnake(self, cause):
        self.living = False
        self.cause = cause 
    def isLiving(self):
        return self.living
    def isWinning(self):
        return self.winning
    def setLvl(self, lvl):
        self.mapNum = lvl
    def getLvlNum(self):
        return self.mapNum
    def resetScore(self):
        self.s.resetScore()
    def getCause(self):
        return self.cause
    def getTeleports(self):
        return self.teleports

if __name__ == "__main__":
    g: game = game()
    print("Welcome to Snake\nTo start press 'enter'. To stop the game press 'ctrl'+'c'\nInstructions/Rules\n     "+Back.RED+" "+ Style.RESET_ALL+" is a Wall, means Death"+
        "\n     "+ Back.BLUE + " "+ Style.RESET_ALL+ " is Magnetism, you attrack nearby food, has cooldown" +
        "\n     " + Back.MAGENTA + " "+ Style.RESET_ALL+ " is Speed, you are faster and get magnetism for that time, has cooldown"+
        "\n     "+ Back.LIGHTBLACK_EX + " "+ Style.RESET_ALL+ " is invisibility, while being invis, ghosts don't follow you, has cooldown" +
        "\n     "+ Back.GREEN + " " + Style.RESET_ALL+ " is food, increases your size, eat as many as fast as possible" + 
        "\n     "+ Back.YELLOW + " "+ Style.RESET_ALL+ " is a teleport, teleports you to a random other teleport" +
        "\n     "+ Back.WHITE + " "+ Style.RESET_ALL+ " are ghosts. Once they hit your head, you are dead" +
        "\n  "+Back.CYAN+"   →"+Style.RESET_ALL+" are you, arrow shows direction you are moving in, "+Back.CYAN+"    "+Style.RESET_ALL+" is your body"+
        "\n       You move yourself with 'w','a','s','d'. Don't drive into Walls and into yourself, be careful: you are constantly moving"+
        "\n             Once typed, you can only change, if you moved"+
        "\n       You have three lives, complete as many levels as you can (completion is 100% on score down left)"+
        "Good Luck")
    won = True
    while(True):
        live = 3
        print("New Game has started. Press 'enter' to start Level")
        while(live > 0):
            print("Waiting...")
            while(not keyboard.is_pressed("enter")):
                time.sleep(0.01)
            if(won):
                g.startlvl()
            else:
                g.restartlvl()
            sleeping: float = 0.05
            while(g.isLiving() and not g.isWinning()):
                g.update()
                time.sleep(sleeping)
            g.resetScore()
            if(g.isWinning()):
                print("Press 'enter' to continue with the next Level. Next Level is " + str(g.getLvlNum()+1))
                won = True
            else:
                won = False
                print(g.getCause())
                live -= 1
                if(live > 0):
                    print("Press 'enter' to retry this level")
        print("All lives lost, restart Game. You got to level "+ str(g.getLvlNum()))
        g.setLvl(0)