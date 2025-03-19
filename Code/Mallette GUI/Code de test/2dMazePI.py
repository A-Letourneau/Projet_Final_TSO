import PySimpleGUI as sg
from time import sleep


class mazeClass:
    def __init__(self, mazeFile, nbGate, SLAVE_ADDRESS_MAZE):
        self.mazeFile = mazeFile
        self.nbGate = nbGate
        self.SLAVE_ADDRESS_MAZE = SLAVE_ADDRESS_MAZE

    def make_winMaze():
        layout = [
                    [sg.Text('A toggle button example', key="1", text_color="blue")],
                    [sg.Text("", size=(30,25), background_color='white', text_color='black', key="mazeTxtBox", font="Monaco"),],
                    [sg.Text(key="input")],
                    [sg.Button(button_text='gateA', key='gateA')]
                ]

        return sg.Window('Toggle Button Simple Graphic', layout, return_keyboard_events=True, use_default_focus=False)

    #Brief : Une fonction qui envoit une demande de donnée à l'adresse d'un esp32 
    #Param : L'adresse i2c du esp32
    def sendRequest(slaveAdr):
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
        if DEBUG:
            print(strReceived)
        return json.loads(strReceived) #Transforme la string JSON en dict pour l'utiliser en dictionnaire

    def displayMaze(maze):
        tempMazeString = ""
        # Display the maze:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (x, y) == (playerx, playery):
                    tempMazeString += PLAYER
                elif (x, y) == (exitx, exity):
                    tempMazeString += EXIT

                elif maze[(x, y)] == WALL and (x,y) in listGatePos.values():
                    tempMazeString += CLOSED_GATE
                elif maze[(x, y)] == WALL:
                    tempMazeString += BLOCK
                elif maze[(x, y)] == EMPTY and (x,y) in listGatePos.values():
                    tempMazeString += OPEN_GATE
                elif maze[(x, y)] == EMPTY:
                    tempMazeString += EMPTY
            tempMazeString += '\n'  # Print a newline after printing the row.
        window_maze["mazeTxtBox"].update(tempMazeString)

    def changeGateState(nameGate):
        y = 0
        listGateState[nameGate] = not listGateState[nameGate] 
        listGateState[nameGate.upper()] = not listGateState[nameGate.upper()] 
        for line in lines:
            for x, character in enumerate(line.rstrip()):
                if character in listGateState:
                    if listGateState[character]:
                        maze[(x, y)] = WALL
                    else:
                        maze[(x, y)] = EMPTY
            y += 1

        for line in lines:
            WIDTH = len(line.rstrip())
            for x, character in enumerate(line.rstrip()):
                if character in listGateState:
                    if listGateState[character]:
                        maze[(x, y)] = WALL
                    else:
                        maze[(x, y)] = EMPTY
                    listGatePos[character] = (x, y)
                elif character == WALL:
                    maze[(x, y)] = character
                elif character == EMPTY:
                    maze[(x, y)] = character
                elif character == START:
                    playerx, playery = x, y
                    maze[(x, y)] = EMPTY
                elif character == EXIT:
                    exitx, exity = x, y
                    maze[(x, y)] = EMPTY
            y += 1
        HEIGHT = y


    def doMaze():
        # Maze file constants:
        WALL = '#'
        EMPTY = ' '
        START = '!'
        EXIT = '?'
        CLOSED_GATE = '█'
        OPEN_GATE = '║'

        listGateState = {'a' : 1, 'A' : 0,'b' : 1, 'B' : 0,'c' : 1, 'C' : 0,'d' : 1, 'D' : 0}
        listGatePos = {}

        PLAYER = '@'  
        BLOCK = chr(9617)  # Character 9617 is '░'

        # Load the maze from a file:

        maze = {}
        lines = self.mazeFile.readlines()
        playerx = None
        playery = None
        exitx = None
        exity = None
        HEIGHT = 0
        WIDTH = 0
        y = 0

        window_maze = make_winMaze()
        window_maze.Location = (100,100)
        event, values = window_maze.read(timeout=0)
        mazeCompleted = False
        displayMaze(maze)

        while not mazeCompleted:  # Main game loop.

            #Essaye de lire les json des esp32 et met un message d'erreur s'il n'y parvient pas
            if window_maze:
                try:
                    msg_SW = sendRequest(SLAVE_ADDRESS_MAZE)
                    SWerror = False
                    window_maze["titleSW"].update(text_color = "white")
                except:
                    window_maze["titleSW"].update(text_color = "red")
                    SWerror = True
                    if DEBUG:
                        print("SW i2c ERROR")

            while True:  # Get user move.
                displayMaze(maze)
                event, values = window_maze.read()

                if event == "gateA":
                    changeGateState('a')
                    displayMaze(maze)
                    print(listGateState)
                    print(listGatePos)

                if event != "__TIMEOUT__" and event.isalpha():
                    window_maze["input"].update(event)
                    move = event.upper()

                if move not in ['W', 'A', 'S', 'D']:
                    continue

                # Check if the player can move in that direction:
                if move == 'W' and maze[(playerx, playery - 1)] == EMPTY:
                    break
                elif move == 'S' and maze[(playerx, playery + 1)] == EMPTY:
                    break
                elif move == 'A' and maze[(playerx - 1, playery)] == EMPTY:
                    break
                elif move == 'D' and maze[(playerx + 1, playery)] == EMPTY:
                    break

                

            # Keep moving in this direction until you encounter a branch point.
            if move == 'W':
                while True:
                    playery -= 1
                    if (playerx, playery) == (exitx, exity):
                        break
                    if maze[(playerx, playery - 1)] == WALL:
                        break  # Break if we've hit a wall.
                    if (maze[(playerx - 1, playery)] == EMPTY
                        or maze[(playerx + 1, playery)] == EMPTY):
                        break  # Break if we've reached a branch point.
            elif move == 'S':
                while True:
                    playery += 1
                    if (playerx, playery) == (exitx, exity):
                        break
                    if maze[(playerx, playery + 1)] == WALL:
                        break  # Break if we've hit a wall.
                    if (maze[(playerx - 1, playery)] == EMPTY
                        or maze[(playerx + 1, playery)] == EMPTY):
                        break  # Break if we've reached a branch point.
            elif move == 'A':
                while True:
                    playerx -= 1
                    if (playerx, playery) == (exitx, exity):
                        break
                    if maze[(playerx - 1, playery)] == WALL:
                        break  # Break if we've hit a wall.
                    if (maze[(playerx, playery - 1)] == EMPTY
                        or maze[(playerx, playery + 1)] == EMPTY):
                        break  # Break if we've reached a branch point.
            elif move == 'D':
                while True:
                    playerx += 1
                    if (playerx, playery) == (exitx, exity):
                        break
                    if maze[(playerx + 1, playery)] == WALL:
                        break  # Break if we've hit a wall.
                    if (maze[(playerx, playery - 1)] == EMPTY
                        or maze[(playerx, playery + 1)] == EMPTY):
                        break  # Break if we've reached a branch point.

            if (playerx, playery) == (exitx, exity):
                displayMaze(maze)
                print('You have reached the exit! Good job!')
                mazeCompleted = True
                break

        window_maze.close()

if __name__ == "__main__":
    testClass = mazeClass(mazeFile=open("maze1.txt"), nbGate=4, SLAVE_ADDRESS_MAZE=0x09)
    testClass.doMaze()