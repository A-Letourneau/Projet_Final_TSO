# import PySimpleGUIWeb as sg
# import PySimpleGUIQt as sg
import PySimpleGUI as sg
import math
from random import randint

SIZE_X = 200
SIZE_Y = 100
NUMBER_MARKER_FREQUENCY = 25

def draw_axis():
    graph.draw_line((-SIZE_X,0), (SIZE_X, 0))                # axis lines
    graph.draw_line((0,-SIZE_Y), (0,SIZE_Y))

    for x in range(-SIZE_X, SIZE_X+1, NUMBER_MARKER_FREQUENCY):
        graph.draw_line((x,-3), (x,3))                       # tick marks
        if x != 0:
            graph.draw_text( str(x), (x,-10), color='green', font='Algerian 10')      # numeric labels

    for y in range(-SIZE_Y, SIZE_Y+1, NUMBER_MARKER_FREQUENCY):
        graph.draw_line((-3,y), (3,y))
        if y != 0:
            graph.draw_text( str(y), (-10,y), color='blue')

sg.theme('DarkAmber')  # let's add a little color

# Create the graph that will be put into the window
graph = sg.Graph(canvas_size=(400, 400),
          graph_bottom_left=(-(SIZE_X+5), -(SIZE_Y+5)),
          graph_top_right=(SIZE_X+5, SIZE_Y+5),
          background_color='white',
          key='graph')
# Window layout 
# f(x)=a*sin(p(x−pX))+pY 
# a = amplitude, p = periode (2pi / p), pX et pY = position x et y de la sine

layout = [[sg.Text('Example of Using Math with a Graph', justification='center', size=(50,1), relief=sg.RELIEF_SUNKEN)],
          [graph],
          [sg.Text('y = sin(x / x2 * x1)', font='Algerian 18')],
          [sg.Text('a'),sg.Slider((0,200), orientation='h', enable_events=True,key='amplitude')],
          [sg.Text('p'),sg.Slider((0,50), orientation='h', enable_events=True,key='periode')],
          [sg.Text('pX'),sg.Slider((1,200), orientation='h', enable_events=True,key='posX')],
          [sg.Text('pY'),sg.Slider((-100,100), orientation='h', enable_events=True,key='posY')],
          ]

window = sg.Window('Graph of Sine Function', layout)

correctSin = True
margins = 3

while True:
    event, values = window.read()
    if event is None:
        break
    graph.erase()
    draw_axis()

    if correctSin:
        sg.popup_auto_close("Find the corresponding sine wave")
        amplitudeGoal = randint(0,50)
        periodeGoal = randint(10,25)
        posXGoal = randint(1,10)
        posYGoal = randint(-10,-10)
        print(amplitudeGoal, periodeGoal, posXGoal, posYGoal)
        correctSin = False

    prev_x = prev_y = None
    for x in range(int(-SIZE_X/2),int(SIZE_X/2)):
        #f(x)=a*sin(p(x−pX))+pY
        y = values['amplitude'] * math.sin((values['periode']/100)*(x - values['posX'])) + int(values['posY'])
        if prev_x is not None:
            graph.draw_line((prev_x, prev_y), (x,y), color='red')
        prev_x, prev_y = x, y
        if amplitudeGoal-margins <= values['amplitude'] <= amplitudeGoal+margins and periodeGoal-margins <= values['periode'] <= periodeGoal+margins and posXGoal-margins <= values['posX'] <= posXGoal+margins and posYGoal-margins <= values['posY'] <= posYGoal+margins:
            correctSin = True

    prev_x_goal = prev_y_goal = None
    for x in range(int(-SIZE_X/2),int(SIZE_X/2)):
        #f(x)=a*sin(p(x−pX))+pY
        #y = math.sin(x)
        y = amplitudeGoal * math.sin((periodeGoal/100)*(x - posXGoal)) + posYGoal
        if prev_x_goal is not None:
            graph.draw_line((prev_x_goal, prev_y_goal), (x,y), color='black')
        prev_x_goal, prev_y_goal = x, y

