import PySimpleGUI as sg
from time import sleep
from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import json                         #Pour la manipulation des json
from rpi_ws281x import PixelStrip, Color
import moduleDEL

class mazeClass:
    def __init__(self, mazeFile, nbGate, SLAVE_ADDRESS_MAZE, DEBUG, DEL_ACTIVE, strip = None):
        self.mazeFile = mazeFile
        self.nbGate = nbGate
        self.SLAVE_ADDRESS_MAZE = SLAVE_ADDRESS_MAZE
        self.mazeError = False

        self.strip = strip
        self.HEIGHT = 0
        self.WIDTH = 0
        self.maze = {}
        self.lines = self.mazeFile.readlines()
        self.playerx = 0
        self.playery = 0
        self.exitx = 0
        self.exity = 0
       
        self.DEBUG = DEBUG
        self.DEL_ACTIVE = DEL_ACTIVE       
       
        # Maze file constants:
        self.WALL = '#'
        self.EMPTY = ' '
        self.START = '!'
        self.EXIT = '?'
        self.CLOSED_GATE = '█'
        self.OPEN_GATE = '║'
        self.PLAYER = '@'  
        self.BLOCK = chr(9617)  # Character 9617 is '░'


        self.listGateState = {'a' : 1, 'A' : 0,'b' : 1, 'B' : 0,'c' : 1, 'C' : 0,'d' : 1, 'D' : 0}
        self.listGatePos = {}

        self.puzzleSolved = False
        self.window_maze = None

        self.minDEL = 36
        self.maxDEL = 53

    """
    Brief : Cree une fenetre qui contient le labyrinthe
    Para : self.
    Return : les information pour cree une fenetre labyrinthe dans une variable
    
    """
    def make_winMaze(self):
        layout = [
                [sg.VPush()],
                [sg.Push(), sg.Text('Résoudre le labyrinthe\navec les touches du clavier et les interrupteurs', size=(50,2), key="title_Maze", font='Algerian 20', justification = "center"),sg.Push(),],
                [sg.Push(),sg.Text("", size=(25,25), background_color='white', text_color='black', key="mazeTxtBox", font="FreeMono 20"),sg.Push()],
                [sg.Push(), sg.Text(key="input"), sg.Push(),],
                [sg.VPush()]
            ]
        return sg.Window('Une fenetre de labyrinthe', layout, return_keyboard_events=True, use_default_focus=False)

    """
    Brief : Une fonction qui envoit une demande de donnée à l'adresse d'un esp32
    Param : slaveAdr = L'adresse i2c du esp32
    """
    def getMazeJSON(self, slaveAdr):
        strReceived = ''
        #Demande le json du esp32 et reçoit une liste de byte
        with SMBus(1) as bus:
            msg = i2c_msg.read(slaveAdr, 125) #Demande 125 bytes à l'addresse du sub
            bus.i2c_rdwr(msg) #retourne par pointer la liste de byte dans msg
        #Transforme la ligne de byte en string
        for value in msg:
            if(value == 0x00): #Signifie la fin de la string
                break
            else:
                strReceived += chr(value) #Accumule les caractères pour faire un string Json complet
        if self.DEBUG:
            print(strReceived)
        return json.loads(strReceived) #Transforme la string JSON en dict pour l'utiliser en dictionnaire


    """
    Brief : Met les information d'un dictionnaire de caractere dans la boite de texte sur la fenetre windowMaze
    Param : maze = un dictionnaire de caractere dont l'index est la position et la valeur est soit un mur, un espace vide ou une porte ouverte ou ferme
    """    
    def displayMaze(self, maze):
        if self.DEBUG:
            print(self.maze)
            print(self.HEIGHT)
            print(self.WIDTH)
        tempMazeString = ""
        # Display the maze:
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if (x, y) == (self.playerx, self.playery):
                    tempMazeString += self.PLAYER
                elif (x, y) == (self.exitx, self.exity):
                    tempMazeString += self.EXIT


                elif maze[(x, y)] == self.WALL and (x,y) in self.listGatePos.values():
                    tempMazeString += self.CLOSED_GATE
                elif maze[(x, y)] == self.WALL:
                    tempMazeString += self.BLOCK
                elif maze[(x, y)] == self.EMPTY and (x,y) in self.listGatePos.values():
                    tempMazeString += self.OPEN_GATE
                elif maze[(x, y)] == self.EMPTY:
                    tempMazeString += self.EMPTY
            tempMazeString += '\n'  # Print a newline after printing the row.
        self.window_maze["mazeTxtBox"].update(tempMazeString)

    """
    Brief : Change l'etat d'une des paires de portes et reconstruit le labyrinthe
    Param : nameGate = une lettre en miniscule
    """  
    def changeGateState(self, nameGate):
        y = 0
        self.listGateState[nameGate] = not self.listGateState[nameGate]
        self.listGateState[nameGate.upper()] = not self.listGateState[nameGate.upper()]

        for line in self.lines:
            self.WIDTH = len(line.rstrip())
            for x, character in enumerate(line.rstrip()):
                if character in self.listGateState:
                    if self.listGateState[character]:
                        self.maze[(x, y)] = self.WALL
                    else:
                        self.maze[(x, y)] = self.EMPTY
                    self.listGatePos[character] = (x, y)
                elif character == self.WALL:
                    self.maze[(x, y)] = character
                elif character == self.EMPTY:
                    self.maze[(x, y)] = character
                elif character == self.PLAYER:
                    self.playerx, self.playery = x, y
                    self.maze[(x, y)] = self.EMPTY
                elif character == self.START:
                    self.maze[(x, y)] = self.EMPTY
                elif character == self.EXIT:
                    self.maze[(x, y)] = self.EMPTY
            y += 1
        self.HEIGHT = y


    """
    Brief : Commence l'interface graphique du labyrinthe. Prend les touches du clavier directement pour se deplacer dans le labyrinthe
    """  
    def startMaze(self):
        # Load the maze from a file:
        y = 0
        for line in self.lines:
            if self.DEBUG:
                print(line)
            self.WIDTH = len(line.rstrip())
            for x, character in enumerate(line.rstrip()):
                if character in self.listGateState:
                    if self.listGateState[character]:
                        self.maze[(x, y)] = self.WALL
                    else:
                        self.maze[(x, y)] = self.EMPTY
                    self.listGatePos[character] = (x, y)
                elif character == self.WALL:
                    self.maze[(x, y)] = character
                elif character == self.EMPTY:
                    self.maze[(x, y)] = character
                elif character == self.START:
                    self.playerx, self.playery = x, y
                    self.maze[(x, y)] = self.EMPTY
                elif character == self.EXIT:
                    self.exitx, self.exity = x, y
                    self.maze[(x, y)] = self.EMPTY
            y += 1
        self.HEIGHT = y        

        self.window_maze = self.make_winMaze()
        self.window_maze.Location = (100,100)
        event, values = self.window_maze.read(timeout=0)
        self.displayMaze(self.maze)
        
        
    def doMaze(self):
        #Essaye de lire les json des esp32 et met un message d'erreur s'il n'y parvient pas
        if self.window_maze:
            try:
                msgMaze = self.getMazeJSON(self.SLAVE_ADDRESS_MAZE)
                self.mazeError = False
                self.window_maze["title_Maze"].update(text_color = "white")
            except:
                self.window_maze["title_Maze"].update(text_color = "red")
                self.mazeError = True
                if self.DEBUG:
                    print("Maze i2c ERROR")
        
        #------------ Verifie que les Gates 
        i = 0 
        for switch in msgMaze['JsonData']:
            if i >= self.nbGate:
                break 
            if int(msgMaze['JsonData'][switch]) == self.listGateState[chr(97 + i)]:
                self.changeGateState(chr(97 + i))
                self.displayMaze(self.maze)
            i += 1
        
        
        self.displayMaze(self.maze)
        event, values = self.window_maze.read(timeout=50)
                
        if event == sg.WIN_CLOSED or event == "Exit":
            self.window_maze = None
            self.puzzleSolved = True
            move = ''
        elif event != "__TIMEOUT__" and event.isalpha():
            self.window_maze["input"].update(event)
            move = event.upper()
            if self.DEBUG:
                print(self.listGateState)
                print(msgMaze['JsonData'])
        elif event == "__TIMEOUT__" or not event.isalpha():
            move = ''
           

        # Keep moving in this direction until you encounter a branch point.
        if move == 'W' and self.maze[(self.playerx, self.playery - 1)] == self.EMPTY:
            while True:
                self.playery -= 1
                if (self.playerx, self.playery) == (self.exitx, self.exity):
                    break
                if self.maze[(self.playerx, self.playery - 1)] == self.WALL:
                    break  # Break if we've hit a wall.
                if (self.maze[(self.playerx - 1, self.playery)] == self.EMPTY
                    or self.maze[(self.playerx + 1, self.playery)] == self.EMPTY):
                    break  # Break if we've reached a branch point.
        elif move == 'S' and self.maze[(self.playerx, self.playery + 1)] == self.EMPTY:
            while True:
                self.playery += 1
                if (self.playerx, self.playery) == (self.exitx, self.exity):
                    break
                if self.maze[(self.playerx, self.playery + 1)] == self.WALL:
                    break  # Break if we've hit a wall.
                if (self.maze[(self.playerx - 1, self.playery)] == self.EMPTY
                    or self.maze[(self.playerx + 1, self.playery)] == self.EMPTY):
                    break  # Break if we've reached a branch point.
        elif move == 'A' and self.maze[(self.playerx - 1, self.playery)] == self.EMPTY:
            while True:
                self.playerx -= 1
                if (self.playerx, self.playery) == (self.exitx, self.exity):
                    break
                if self.maze[(self.playerx - 1, self.playery)] == self.WALL:
                    break  # Break if we've hit a wall.
                if (self.maze[(self.playerx, self.playery - 1)] == self.EMPTY
                    or self.maze[(self.playerx, self.playery + 1)] == self.EMPTY):
                    break  # Break if we've reached a branch point.
        elif move == 'D' and self.maze[(self.playerx + 1, self.playery)] == self.EMPTY:
            while True:
                self.playerx += 1
                if (self.playerx, self.playery) == (self.exitx, self.exity):
                    break
                if self.maze[(self.playerx + 1, self.playery)] == self.WALL:
                    break  # Break if we've hit a wall.
                if (self.maze[(self.playerx, self.playery - 1)] == self.EMPTY
                    or self.maze[(self.playerx, self.playery + 1)] == self.EMPTY):
                    break  # Break if we've reached a branch point.

        if (self.playerx, self.playery) == (self.exitx, self.exity):
            self.displayMaze(self.maze)
            print('You have reached the exit! Good job!')
            moduleDEL.colorInBetween(self.strip, Color(0, 255, 0),self.minDEL,self.maxDEL)  # Red wipe
            moduleDEL.colorInBetween(self.strip, Color(0, 255, 0),18,35)
            self.puzzleSolved = True
            




if __name__ == "__main__":
    DEBUG = False
    DEL_ACTIVE = False
    testClass = mazeClass(mazeFile=open("maze1.txt"), nbGate=4, SLAVE_ADDRESS_MAZE=0x0a, DEBUG=DEBUG, DEL_ACTIVE=DEL_ACTIVE)
    testClass.startMaze()
    while not testClass.puzzleSolved:
        testClass.doMaze()
    if testClass.window_maze:
        testClass.window_maze.close()









