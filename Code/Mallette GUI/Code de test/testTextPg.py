import PySimpleGUI as sg

layout = [
            [sg.Text('A toggle button example', key="1", text_color="blue")],
            [sg.Text("123", background_color='white', key="mazeTxtBox")],
            [sg.Input()],
         ]

window = sg.Window('Toggle Button Simple Graphic', layout)

window.Location = (100,100)

while True:  # Main game loop.
    event, values = window.read(timeout=100)