import PySimpleGUI as sg
# import PySimpleGUIQt as sg
import os.path
import PIL.Image
from pathlib import Path
import io
import base64

new_size = int(800), int(800) # Ajusto un tamaño fijo para cualquier imagen de 800x800
filename = ""
working_copy_filename = ""

def create_working_copy(filename):
    img = PIL.Image.open(filename)
    working_copy_filename = os.path.splitext(filename)[0] + "WC.tiff"
    print(working_copy_filename)
    img.save(working_copy_filename)
    del img
    return working_copy_filename

def save_as(saves_as_filename):
    img = PIL.Image.open(working_copy_filename)
    img.save(saves_as_filename + ".tiff")
    del img

def get_pixel_values(filename):
    img = PIL.Image.open(filename, 'r')
    width, height = img.size
    pixel_values = list(img.getdata())
    print('Los datos de la imagen son widht: %s, height: %s' % (str(width), str(height)))
    print(pixel_values[0])

def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()


# --------------------------------- Define Layout ---------------------------------

sg.theme('Dark Grey 3')
menu_def = [['Imagen', ['Abrir','Guardar', 'Salir',]],
            ['Información', ['Imprimir datos'],],
            ['Herramientas',]]

# First the window layout...2 columns

left_col = [[sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
            [sg.Text('Resize to'), sg.In(key='-W-', size=(5,1)), sg.In(key='-H-', size=(5,1))]]

# For now will only show the name of the file that was chosen
images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(None,None), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')]]

# ----- Full layout -----
# layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(images_col, element_justification='c')], [sg.Menu(menu_def)]]
layout = [[sg.Column(images_col, element_justification='c')], [sg.Menu(menu_def)]]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('Multiple Format Image Viewer', layout, resizable=True, location=(50,50), size =(800,800))

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    # Opciones del menú
    if event == 'Abrir':
    
        # sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...') --> PARA LA INFORMACION DE LA IMAGEN      
        filename = sg.popup_get_file("Selecciona la imagen a cargar")
        proccessed_image = convert_to_bytes(filename, resize=new_size)
        window['-IMAGE-'].update(proccessed_image)
        working_copy_filename = create_working_copy(filename)
        get_pixel_values(filename)
    
    if event == 'Guardar':
        new_filename = sg.popup_get_file("Guardar como", save_as= True)
        print(new_filename)
        save_as(new_filename)

# --------------------------------- Close & Exit ---------------------------------
os.remove(working_copy_filename)
window.close()