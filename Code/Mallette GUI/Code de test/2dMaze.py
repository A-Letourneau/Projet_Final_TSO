import PySimpleGUI as sg
from time import sleep

sg.theme('NeonGreen1')
layout = [
            [sg.Text('A toggle button example', key="1", text_color="lightgreen")],
            [sg.Text("", size=(30,25), background_color='white', text_color='black', key="mazeTxtBox", font="Monaco"),],
            [sg.Text(key="input")],
            [sg.Button(button_text='gateA', key='gateA')]
         ]

window = sg.Window('Toggle Button Simple Graphic', layout, return_keyboard_events=True, use_default_focus=False)

window.Location = (100,100)


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
    window["mazeTxtBox"].update(tempMazeString)

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


# Load the maze from a file:
mazeFile = open("maze1.txt")
maze = {}
lines = mazeFile.readlines()
playerx = None
playery = None
exitx = None
exity = None
HEIGHT = 0
WIDTH = 0
y = 0

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

event, values = window.read(timeout=0)

mazeCompleted = False
displayMaze(maze)
move = ''

while not mazeCompleted:  # Main game loop.
    
    while True:  # Get user move.
        displayMaze(maze)
        event, values = window.read()

        if event == "gateA":
            changeGateState('a')
            displayMaze(maze)
            print(listGateState)
            print(listGatePos)

        if event != "__TIMEOUT__" and event.isalpha():
            window["input"].update(event)
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

window.close()