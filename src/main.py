"""
    Universidad de La Laguna - Grado en Ingenería Informática
    Cuarto Curso - Visión por Computador
    2021-2022

    Autores:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    Fichero main.py: Programa principal del proyecto
"""
import PySimpleGUI as sg
import os.path
import PIL.Image
from pathlib import Path
import io
import base64
import utility
import function

new_size = int(700), int(700) # Ajusto un tamaño fijo para cualquier imagen de 800x800
filename = ""
debug = 1
information_text = ''

# Método encargado de realizar la transformación de la imagen
# a una imagen en escala de grises
def colour_to_grayscale():
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            grey_value = round(0.222 * pixs[i,j][0] + 0.707 * pixs[i,j][1] + 0.071 * pixs[i,j][2])
            pixs[i,j] = (grey_value, grey_value, grey_value)
    img.save(working_copy_filename)
    del img

# Método encargado de convertir en bytes y la imagen cambiará
# el tamaño de una imagen si es un archivo o un objeto de base64 bytes
def convert_to_bytes(file_or_bytes, resize=None):
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


# ---------------- Definición de Layout ----------------
sg.theme('Light Blue 2')
menu_def = [['Imagen', ['Abrir','Guardar', 'Salir',]],
            ['Información', ['Imprimir datos'],],
            ['Herramientas', ],
            ['Transformación', ['Escala de grises'],]]

# Por ahora solo mostrará el nombre del archivo que se eligió
image_col = [[sg.Text(size=(None,None), key='-NOMBRE_IMAGEN-')],
              [sg.Image(key='-IMAGE-')],
              [sg.Text(information_text, background_color= "grey", key = '-INFO_TEXT-')]]
            
imagewc_col = [[sg.Text(size=(None,None), key='-NOMBRE_IMAGEN_RESULTANTE-')],
              [sg.Image(key='-IMAGEWC-')],
              [sg.Text(information_text, background_color= "grey", key = '-INFO_TEXT-')]]

status_bar = [[sg.Text(information_text, background_color= "grey", key = '-INFO_TEXT-')]]
# ---------------- Layout Completo ----------------
# layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(image_col, element_justification='c')], [sg.Menu(menu_def)]]
layout = [[sg.Column(image_col, element_justification='c'),
           sg.VSeparator(),
           sg.Column(imagewc_col, element_justification='c'),
           [sg.Menu(menu_def)]]]

# ---------------- Creación de ventana ----------------
window = sg.Window('Multiple Format Image Viewer', layout, resizable=True, location=(50,50), size =(800,800)).Finalize()
window.Maximize()


if debug == 1:
    filename = 'C:/Users/Nerea/Documents/Ingenería Informática/Visión por Computador/Proyecto-VPC-JN/VPCIMG/4.1.06.tiff'
    proccessed_image = convert_to_bytes(filename, resize=new_size)
    window['-IMAGE-'].update(proccessed_image)
    window['-NOMBRE_IMAGEN-'].update(filename)
    working_copy_filename = utility.create_working_copy(filename)
    pixels = function.get_pixel_values(filename)
    frequency = function.frequency(pixels)
    information_text = utility.info_imagen(filename, pixels)
    print(information_text)
    window['-INFO_TEXT-'].update(information_text)
    # function.draw_absolute_histogram(sorted(pixels))
    # function.draw_cumulative_histogram(sorted(pixels))
    

# ---------------- Bucle de eventos ----------------
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    # Opciones de la barra superior principal
    if event == 'Abrir':
        # sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...') #--> PARA LA INFORMACION DE LA IMAGEN      
        filename = sg.popup_get_file("Selecciona la imagen a cargar")
        print(filename)
        proccessed_image = convert_to_bytes(filename, resize=new_size)
        window['-IMAGE-'].update(proccessed_image)
        window['-NOMBRE_IMAGEN-'].update(filename)
        working_copy_filename = utility.create_working_copy(filename)
        pixels = function.get_pixel_values(filename)
        frequency = function.frequency(pixels)
        utility.info_imagen(filename, pixels)
        function.draw_histogram(sorted(pixels))


    if event == 'Guardar':
        new_filename = sg.popup_get_file("Guardar como", save_as= True)
        print(new_filename)
        utility.save_as(new_filename)
    
    # Opciones de edición
    if event == 'Escala de grises':
        colour_to_grayscale()
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        print(proccessed_image)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + " GREYSCALE")
        information_text = utility.info_imagen(filename, pixels)
        print(information_text)
        window['-INFO_TEXT-'].update(information_text)

os.remove(working_copy_filename)
window.close()
