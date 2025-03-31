import PySimpleGUI as sg
import Minesweeper
sg.Window._move_all_windows = True

def title_bar(title, text_color, background_color):
    """
    Creates a "row" that can be added to a layout. This row looks like a titlebar
    :param title: The "title" to show in the titlebar
    :type title: str
    :param text_color: Text color for titlebar
    :type text_color: str
    :param background_color: Background color for titlebar
    :type background_color: str
    :return: A list of elements (i.e. a "row" for a layout)
    :rtype: List[sg.Element]
    """
    bc = background_color
    tc = text_color
    font = 'Helvetica 12'

    return [sg.Col([[sg.T(title, text_color=tc, background_color=bc, font=font, grab=True)]], pad=(0, 0), background_color=bc),
            sg.Col([[sg.T('_', text_color=tc, background_color=bc, enable_events=True, font=font, key='-MINIMIZE-'), sg.Text('❎', text_color=tc, background_color=bc, font=font, enable_events=True, key='Exit')]], element_justification='r', key='-C-', grab=True,
                   pad=(0, 0), background_color=bc)]


def main():

    background_layout = [ title_bar('This is the titlebar', sg.theme_text_color(), sg.theme_background_color()),
                        [sg.Image(source='Desktop.png')]]
    window_background = sg.Window('Background', background_layout, no_titlebar=True, finalize=True, margins=(0, 0), element_padding=(0,0), right_click_menu=[[''], ['Exit',]])

    window_background['-C-'].expand(True, False, False)  # expand the titlebar's rightmost column so that it resizes correctly

    
    layout = [
        [sg.Button(image_source='Minesweeperlogo.png', image_subsample=5, pad=10, key="Minesweeper")],
        [sg.Button(image_source='Folder.png', image_subsample=5, pad=10)],
        [sg.Button(image_source='Folder.png', image_subsample=5, pad=10)],
        [sg.Button(image_source='Folder.png', image_subsample=5, pad=10)],
        [sg.Button(image_source='Folder.png', image_subsample=5, pad=10)],
        ]

    top_window = sg.Window('Everything bagel', layout, finalize=True, keep_on_top=True, grab_anywhere=False,  transparent_color=sg.theme_background_color(), no_titlebar=True)

    top_window.move(window_background.current_location()[0] + 10, window_background.current_location()[1] + 50)

    # window_background.send_to_back()
    # top_window.bring_to_front()

    while True:
        window, event, values = sg.read_all_windows()
        print(event, values)
        if event == "Minesweeper":
            Minesweeper.startGame()
        if event is None or event == 'Cancel' or event == 'Exit':
            print(f'closing window = {window.Title}')
            break

    top_window.close()
    window_background.close()



if __name__ == '__main__':

    main()