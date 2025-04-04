import PySimpleGUI as sg
from time import sleep
#from smbus2 import SMBus, i2c_msg   #Pour la communication i2c
import json                         #Pour la manipulation des json

class mazeClass:
    def __init__(self, mazeFile, nbGate, SLAVE_ADDRESS_MAZE, DEBUG, strip = None):
        self.mazeFile = mazeFile
        self.nbGate = nbGate
        self.SLAVE_ADDRESS_MAZE = SLAVE_ADDRESS_MAZE
        self.DEBUG = DEBUG
        self.mazeError = False
        self.windowMaze = None
        self.strip = strip
        self.HEIGHT = 0
        self.WIDTH = 0
        self.maze = {}
        self.lines = self.mazeFile.readlines()
        self.playerx = 0
        self.playery = 0
        self.exitx = 0
        self.exity = 0
        
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

        self.window_maze = None

        
    def make_winMaze(self):
        layout = [
                    [sg.Text('A maze', text_color="white", key="title_Maze")],
                    [sg.Text("", size=(30,25), background_color='white', text_color='black', key="mazeTxtBox", font="Monaco"),],
                    [sg.Text(key="input")],
                    [sg.Button(button_text='gateA', key='gateA')]
                ]

        return sg.Window('Toggle Button Simple Graphic', layout, return_keyboard_events=True, use_default_focus=False)

    #Brief : Une fonction qui envoit une demande de donnée à l'adresse d'un esp32 
    #Param : L'adresse i2c du esp32
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
        mazeCompleted = False
        self.displayMaze(self.maze)

        while not mazeCompleted:  # Main game loop.

            #Essaye de lire les json des esp32 et met un message d'erreur s'il n'y parvient pas
            """if self.window_maze:
                try:
                    msgMaze = self.getMazeJSON(self.SLAVE_ADDRESS_MAZE)
                    self.mazeError = False
                    self.window_maze["title_Maze"].update(text_color = "white")
                except:
                    self.window_maze["title_Maze"].update(text_color = "red")
                    self.mazeError = True
                    if self.DEBUG:
                        print("Maze i2c ERROR")"""

            while True:  # Get user move.
                self.displayMaze(self.maze)
                event, values = self.window_maze.read()

                if event == "gateA":
                    self.changeGateState('a')
                    self.displayMaze(self.maze)
                    if self.DEBUG:
                        print(self.listGateState)
                elif event == sg.WIN_CLOSED:
                    self.window_maze.close()
                    mazeCompleted = True
                    move = ''
                    break
                elif event != "__TIMEOUT__" and event.isalpha():
                    self.window_maze["input"].update(event)
                    move = event.upper()
                    if move not in ['W', 'A', 'S', 'D']:
                        continue
                elif event != "__TIMEOUT__" and not event.isalpha():
                    move = ''
                    
                # Check if the player can move in that direction:
                if move == 'W' and self.maze[(self.playerx, self.playery - 1)] == self.EMPTY:
                    break
                elif move == 'S' and self.maze[(self.playerx, self.playery + 1)] == self.EMPTY:
                    break
                elif move == 'A' and self.maze[(self.playerx - 1, self.playery)] == self.EMPTY:
                    break
                elif move == 'D' and self.maze[(self.playerx + 1, self.playery)] == self.EMPTY:
                    break

            # Keep moving in this direction until you encounter a branch point.
            if move == 'W':
                while True:
                    self.playery -= 1
                    if (self.playerx, self.playery) == (self.exitx, self.exity):
                        break
                    if self.maze[(self.playerx, self.playery - 1)] == self.WALL:
                        break  # Break if we've hit a wall.
                    if (self.maze[(self.playerx - 1, self.playery)] == self.EMPTY
                        or self.maze[(self.playerx + 1, self.playery)] == self.EMPTY):
                        break  # Break if we've reached a branch point.
            elif move == 'S':
                while True:
                    self.playery += 1
                    if (self.playerx, self.playery) == (self.exitx, self.exity):
                        break
                    if self.maze[(self.playerx, self.playery + 1)] == self.WALL:
                        break  # Break if we've hit a wall.
                    if (self.maze[(self.playerx - 1, self.playery)] == self.EMPTY
                        or self.maze[(self.playerx + 1, self.playery)] == self.EMPTY):
                        break  # Break if we've reached a branch point.
            elif move == 'A':
                while True:
                    self.playerx -= 1
                    if (self.playerx, self.playery) == (self.exitx, self.exity):
                        break
                    if self.maze[(self.playerx - 1, self.playery)] == self.WALL:
                        break  # Break if we've hit a wall.
                    if (self.maze[(self.playerx, self.playery - 1)] == self.EMPTY
                        or self.maze[(self.playerx, self.playery + 1)] == self.EMPTY):
                        break  # Break if we've reached a branch point.
            elif move == 'D':
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
                mazeCompleted = True
                break

        self.window_maze.close()

if __name__ == "__main__":
    DEBUG = True
    #testClass = mazeClass(mazeFile=open("/home/pi/Desktop/programMallette/maze1.txt"), nbGate=4, SLAVE_ADDRESS_MAZE=0x0a, DEBUG=DEBUG)
    testClass = mazeClass(mazeFile=open("maze1.txt"), nbGate=4, SLAVE_ADDRESS_MAZE=0x0a, DEBUG=DEBUG)
    testClass.make_winMaze()
    testClass.startMaze()
    


