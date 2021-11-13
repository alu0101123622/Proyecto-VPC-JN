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
from PIL import Image, ImageDraw
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
roi = 0
rgb = 0
information_text = ''
roi_clicks = []

# Método encargado de convertir en bytes y la imagen cambiará
# el tamaño de una imagen si es un archivo o un objeto de base64 bytes
def convert_to_bytes(file_or_bytes, resize=None):
    if isinstance(file_or_bytes, str):
        img = Image.open(file_or_bytes)
    else:
        try:
            img = Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), Image.ANTIALIAS)
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
            
imagewc_col = [[sg.Text(size=(None,None), key='-NOMBRE_IMAGEN_RESULTANTE-',  visible = False, relief= "raised", font='Arial 10 bold')],
              [sg.Image(key='-IMAGEWC-', visible = False )],
              [sg.Text(information_text, background_color= "grey", key = '-INFO_TEXT_WC-', visible = False, relief= "raised", font='Arial 10 bold')]]

# ---------------- Layout Completo ----------------
layout = [[sg.Column(image_col, element_justification='c'),
           sg.VSeparator(),
           sg.Column(imagewc_col, element_justification='c'),
           [sg.Menu(menu_def)]]]

# ---------------- Creación de ventana ----------------
window = sg.Window('Multiple Format Image Viewer', layout, resizable=True).Finalize()
window.Maximize()


if debug == 1:
    # filename = 'C:/Users/Jorge/Documents/GitHub/Proyecto-VPC-JN/VPCIMG/4.1.04.tiff'  
    filename = 'C:/Users/Jorge/Documents/GitHub/Proyecto-VPC-JN/VPCIMG/larva.tif'
    # filename = 'C:/Users/Jorge/Documents/GitHub/Proyecto-VPC-JN/VPCIMG/7.2.01.tiff'

    # filename = 'C:/Users/Nerea/Documents/Ingenería Informática/Visión por Computador/Proyecto-VPC-JN/VPCIMG/4.1.03.tiff'
    proccessed_image = convert_to_bytes(filename, resize=new_size)
    window['-IMAGE-'].update(proccessed_image)
    window['-IMAGE-'].update(visible = True)
    window['-NOMBRE_IMAGEN-'].update(filename)
    window['-NOMBRE_IMAGEN-'].update(visible = True)

    rgb = utility.is_rgb(filename)
    working_copy_filename = utility.create_working_copy(filename)
    drawing_copy_filename = utility.create_drawing_copy(filename)

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
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

        # information_text = utility.info_imagen(filename, pixels)
        window['-INFO_TEXT-'].update(information_text)

    if event == 'Ajuste lineal del brillo y contraste':
        pixels = function.get_pixel_values(working_copy_filename)
        frequency = function.calculate_pixel_frequency(pixels)
        img = Image.open(working_copy_filename)
        brightness = function.brightness(img.size, frequency)
        contrast = function.contrast(img.size, brightness, frequency)
        new_brigthness = sg.popup_get_text('Introduce el brillo:')
        new_contrast = sg.popup_get_text('Introduce el contrate:')
        table.colour_to_linearlfit(working_copy_filename, brightness, contrast, new_brigthness, new_contrast)
        pixels = function.get_pixel_values(working_copy_filename)
        frequency = function.calculate_pixel_frequency(pixels)
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_linearlfit")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
        information_text_wc = utility.info_imagen(working_copy_filename, frequency)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)
    
    if event == 'Correción Gamma':
        pixels = function.get_pixel_values(working_copy_filename)
        frequency = function.calculate_pixel_frequency(pixels)
        img = Image.open(working_copy_filename)
        if (rgb):
            gamma_valueR = sg.popup_get_text('Introduce el valor de correción gamma (R):')
            gamma_valueG = sg.popup_get_text('Introduce el valor de correción gamma (G):')
            gamma_valueB = sg.popup_get_text('Introduce el valor de correción gamma (B):')
            table.colour_to_gamma_RGB(working_copy_filename, gamma_valueR, gamma_valueG, gamma_valueB)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GAMMA_RGB")
            # information_text = utility.info_imagen(filename, pixels)
            window['-INFO_TEXT-'].update(information_text)
        else:
            gamma_value = sg.popup_get_text('Introduce el valor de correción gamma:')
            table.colour_to_gamma(working_copy_filename, gamma_value)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GAMMA_RGB")
            # information_text = utility.info_imagen(filename, pixels)
            window['-INFO_TEXT-'].update(information_text)

    # Detección de click en imagen para crear ROI
    if event == '-IMAGE-' :
        if (len(roi_clicks) < 2):
            roi_clicks.append(input.cursor_image_pos_for_rectangle(x_pos , y_pos))
            print(roi_clicks)
            print(len(roi_clicks))
        if (roi):
            roi_clicks.clear()
            drawing_copy_filename = utility.create_drawing_copy(filename)
            image_dc = utility.open_drawing_copy(drawing_copy_filename)
            image_roi = convert_to_bytes(drawing_copy_filename, resize=new_size)
            window['-IMAGE-'].update(image_roi)
            roi = 0
        if (len(roi_clicks) == 2):
            image_dc = utility.open_drawing_copy(drawing_copy_filename)
            draw = ImageDraw.Draw(image_dc)
            real_width, real_height  = utility.image_size(filename)
            adapted_roi_clicks = []
            real_point_x = 0
            real_point_y = 0
            for point in roi_clicks:
                real_point_x = round(point[0] * real_width/img_width)
                real_point_y = round(point[1] * real_height/img_height)
                adapted_roi_clicks.append((real_point_x, real_point_y))
            print(roi_clicks)
            print(adapted_roi_clicks)
            draw.rectangle(adapted_roi_clicks, width=1, outline='pink')
            image_dc.save(drawing_copy_filename)
            image_roi = convert_to_bytes(drawing_copy_filename, resize=new_size)
            window['-IMAGE-'].update(image_roi)
            final_roi = utility.create_image_roi(adapted_roi_clicks, filename)
            final_roi.save(working_copy_filename)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)            
            roi = 1

        # print(roi_clicks)

    # Instrucciones a ejecutarse cada 25 ms
    if (input.is_cursor_over_image(x_pos , y_pos, img_height, img_width)):
        window['-MOUSE_POS-'].update(visible = True)
        window['-MOUSE_POS-'].update(input.cursor_image_pos(x_pos , y_pos))
    else:
        window['-MOUSE_POS-'].update(visible = False)
        



    
os.remove(working_copy_filename)
os.remove(drawing_copy_filename)
window.close()
