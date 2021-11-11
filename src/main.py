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
import table
import input

new_size = int(600), int(600) # Ajusto un tamaño fijo para cualquier imagen de 800x800
filename = ""
debug = 1
information_text = ''

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
            ['Herramientas', ['Región de interés']],
            ['Operaciones Lineales', ['Transformaciones lineales por tramos', 'Ajuste lineal del brillo y contraste']],
            ['Operaciones No Lineales', ['Ecualización del histograma', 'Especificación del histograma', 'Correción Gamma', 'Diferencia entre dos imagenes']],
            ['Transformación', ['Escala de grises'],]]

# Por ahora solo mostrará el nombre del archivo que se eligió
image_col = [[sg.Text(size=(None,None), key='-NOMBRE_IMAGEN-', visible = False, relief= "raised", font='Arial 10 bold')],
              [sg.Image(key='-IMAGE-', visible = False, enable_events= True)],
              [sg.Text(information_text ,background_color= "light blue", key = '-INFO_TEXT-',  visible = False, relief= "raised", font='Arial 10 bold')],
              [sg.Text(information_text ,background_color= "light green", key = '-MOUSE_POS-',  visible = False, relief= "raised", font='Arial 12 bold')]]
            
imagewc_col = [[sg.Text(size=(None,None), key='-NOMBRE_IMAGEN_RESULTANTE-',  visible = False)],
              [sg.Image(key='-IMAGEWC-', visible = False )],
              [sg.Text(information_text, background_color= "grey", key = '-INFO_TEXT-', visible = False)]]

# ---------------- Layout Completo ----------------
layout = [[sg.Column(image_col, element_justification='c'),
           sg.VSeparator(),
           sg.Column(imagewc_col, element_justification='c'),
           [sg.Menu(menu_def)]]]

# ---------------- Creación de ventana ----------------
window = sg.Window('Multiple Format Image Viewer', layout, resizable=True).Finalize()
window.Maximize()


if debug == 1:
    # filename = 'C:/Users/Jorge/Documents/GitHub/Proyecto-VPC-JN/VPCIMG/4.1.03.tiff'  
    #filename = 'C:/Users/Jorge/Documents/GitHub/Proyecto-VPC-JN/VPCIMG/larva.tif'

    filename = 'C:/Users/Nerea/Documents/Ingenería Informática/Visión por Computador/Proyecto-VPC-JN/VPCIMG/4.1.03.tiff'
    proccessed_image = convert_to_bytes(filename, resize=new_size)
    window['-IMAGE-'].update(proccessed_image)
    window['-IMAGE-'].update(visible = True)
    window['-NOMBRE_IMAGEN-'].update(filename)
    window['-NOMBRE_IMAGEN-'].update(visible = True)

    working_copy_filename = utility.create_working_copy(filename)
    pixels = function.get_pixel_values(filename)
    pixel_frequency = function.calculate_pixel_frequency(pixels)
    # function.draw_absolute_histogram(pixel_frequency)
    # normalizated_frequency = function.calculate_normalized_frequencies(pixel_frequency, len(pixels))
    information_text = utility.info_imagen(filename, pixel_frequency)
    window['-INFO_TEXT-'].update(information_text)
    window['-INFO_TEXT-'].update(visible = True)

# ---------------- Bucle de eventos ----------------
while True:
    event, values = window.read(timeout=500)
    # print(event, values)

    x_pos = window['-IMAGE-'].Widget.winfo_rootx()
    y_pos = window['-IMAGE-'].Widget.winfo_rooty()
    img_height = window['-IMAGE-'].Widget.winfo_height()
    img_width  = window['-IMAGE-'].Widget.winfo_width()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    # Opciones de la barra superior principal
    if event == 'Abrir':
        # sg.popup('About this program', 'Version 1.0', 'PySimpleGUI rocks...') #--> PARA LA INFORMACION DE LA IMAGEN      
        filename = sg.popup_get_file("Selecciona la imagen a cargar")
        proccessed_image = convert_to_bytes(filename, resize=new_size)
        window['-IMAGE-'].update(proccessed_image)
        window['-NOMBRE_IMAGEN-'].update(filename)
        working_copy_filename = utility.create_working_copy(filename)
        pixels = function.get_pixel_values(filename)
        frequency = function.frequency(pixels)
        utility.info_imagen(filename, pixels)


    if event == 'Guardar':
        new_filename = sg.popup_get_file("Guardar como", save_as= True)
        utility.save_as(new_filename)
    
    # Opciones de edición
    if event == 'Escala de grises':
        table.colour_to_grayscale(working_copy_filename)
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + " GREYSCALE")
        # information_text = utility.info_imagen(filename, pixels)
        window['-INFO_TEXT-'].update(information_text)

    if event == 'Ajuste lineal del brillo y contraste':
        pixels = function.get_pixel_values(working_copy_filename)
        frequency = function.calculate_pixel_frequency(pixels)
        img = PIL.Image.open(working_copy_filename, 'r')
        brightness = function.brightness(img.size, frequency)
        contrast = function.contrast(img.size, brightness, frequency)
        new_brigthness = sg.popup_get_text('Introduce el brillo:')
        new_contrast = sg.popup_get_text('Introduce el contrate:')
        table.colour_to_linearlfit(working_copy_filename, brightness, contrast, new_brigthness, new_contrast)
    # Detección de click en imagen para crear ROI
    if event == '-IMAGE-' :
        position = input.cursor_image_pos(x_pos , y_pos, img_height, img_width)
    
    # Instrucciones a ejecutarse cada 25 ms
    if (input.is_cursor_over_image(x_pos , y_pos, img_height, img_width)):
        window['-MOUSE_POS-'].update(visible = True)
        window['-MOUSE_POS-'].update(input.cursor_image_pos(x_pos , y_pos, img_height, img_width))
    else:
        window['-MOUSE_POS-'].update(visible = False)
        if event == 'Región de interés':
            position = input.cursor_image_pos(x_pos , y_pos, img_height, img_width)
            print("hola")
            print("HOLA")
            positionA = position
            position = input.cursor_image_pos(x_pos , y_pos, img_height, img_width)
            positionB = position
            print(positionA)
            print(positionB)


    
os.remove(working_copy_filename)
window.close()
