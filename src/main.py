"""
    University of La Laguna - Degree in Computer Engineering
    Fourth grade - Computer vision
    2021-2022

    Authors:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    File main.py: Main program file
"""
from tkinter import wantobjects
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

new_size = int(600), int(600)
filename = ""
debug = 1
roi = 0
roi_wc = 0
rgb = 0
information_text = ''
information_text_wc = ''
roi_clicks = []
roi_clicks_wc = []

working_copy_filename = ''
drawing_copy_filename = ''
# drawing_copy_filename_wc = ''

## Method in charge of converting into bytes and the image will resize an image 
## if it is a file or an object of base64 bytes
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

## ---------------- Definition of Layout ---------------- ##
sg.theme('GreenMono')
menu_def = [['Imagen', ['Abrir','Guardar', 'Salir',]],
            ['Información', ['Histogramas', ['Histograma absoluto Original', 'Histograma absoluto Working Copy', 'Histograma absoluto acumulado Original', 'Histograma absoluto acumulado Working Copy']],],
            ['Operaciones Lineales', ['Transformaciones lineales por tramos', 'Ajuste lineal del brillo y contraste', 'Escala de grises']],
            ['Operaciones No Lineales', ['Ecualización del histograma', 'Especificación del histograma', 'Correción Gamma', 'Diferencia entre dos imagenes']],
            ['Operaciones Geométricas', ['Espejo vertical', 'Espejo horizontal', 'Traspuesta de una imagen', 'Rotaciones múltiplo de 90º']],
            ['Transformaciones', ['Transformación de Escalado', 'Transformación de Rotación']]

            ]

image_col = [[sg.Text(size=(None,None), key='-NOMBRE_IMAGEN-', visible = False, relief= "raised", font='Arial 12 bold')],
              [sg.Image(key='-IMAGE-', visible = False, enable_events= True)],
              [sg.Text(information_text ,background_color= "light blue", key = '-INFO_TEXT-',  visible = False, relief= "raised", font='Arial 10 bold')],
              [sg.Text(information_text ,background_color= "light green", key = '-MOUSE_POS-',  visible = False, relief= "raised", font='Arial 14 bold')]]
            
imagewc_col = [[sg.Text(size=(None,None), key='-NOMBRE_IMAGEN_RESULTANTE-',  visible = False, relief= "raised", font='Arial 12 bold')],
              [sg.Image(key='-IMAGEWC-', visible = False, enable_events= True )],
              [sg.Text(information_text, background_color= "light blue", key = '-INFO_TEXT_WC-', visible = False, relief= "raised", font='Arial 10 bold')],
              [sg.Text(information_text ,background_color= "light green", key = '-MOUSE_POS_WC-',  visible = False, relief= "raised", font='Arial 14 bold')]]

## ---------------- Full Layout  ---------------- ##
layout = [[sg.Column(image_col, element_justification='c'),
           sg.VSeparator(),
           sg.Column(imagewc_col, element_justification='c'),
           [sg.Menu(menu_def)]]]


##---------------- Window creation ---------------- ##
window = sg.Window('Multiple Format Image Viewer', layout, resizable=True).Finalize()
window.Maximize()

filename = 'C:/Users/Nerea/Documents/Ingenería Informática/Visión por Computador/Proyecto-VPC-JN/VPCIMG/lena-std_WC.tiff'
# filename = 'C:/Users/Nerea/Documents/Ingenería Informática/Visión por Computador/Proyecto-VPC-JN/VPCIMG/5.3.01.tiff'
rgb = utility.is_rgb(filename)
proccessed_image = convert_to_bytes(filename, resize=new_size)
window['-IMAGE-'].update(proccessed_image)
window['-NOMBRE_IMAGEN-'].update(filename)
window['-NOMBRE_IMAGEN-'].update(visible= True)
window['-IMAGE-'].update(visible = True)

working_copy_filename = utility.create_working_copy(filename)
drawing_copy_filename = utility.create_drawing_copy(filename)
# drawing_copy_filename_wc = utility.create_drawing_copy_wc(filename)
pixels = function.get_pixel_values(filename)
pixel_frequency = function.calculate_pixel_frequency(pixels)

information_text = utility.info_imagen(filename, pixel_frequency, rgb)
window['-INFO_TEXT-'].update(information_text)
window['-INFO_TEXT-'].update(visible = True)

window['-IMAGEWC-'].update(proccessed_image)
window['-IMAGEWC-'].update(visible = True)
window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
pixels_wc = function.get_pixel_values(working_copy_filename)    
pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
information_text = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
window['-INFO_TEXT_WC-'].update(information_text)
window['-INFO_TEXT_WC-'].update(visible = True)

## ---------------- Event loop ---------------- ##
while True:
    event, values = window.read(timeout=150)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    x_pos = window['-IMAGE-'].Widget.winfo_rootx()
    y_pos = window['-IMAGE-'].Widget.winfo_rooty()
    img_height = window['-IMAGE-'].Widget.winfo_height()
    img_width  = window['-IMAGE-'].Widget.winfo_width()

    x_pos_wc = window['-IMAGEWC-'].Widget.winfo_rootx()
    y_pos_wc = window['-IMAGEWC-'].Widget.winfo_rooty()
    img_height_wc = window['-IMAGEWC-'].Widget.winfo_height()
    img_width_wc  = window['-IMAGEWC-'].Widget.winfo_width()


    if event == 'Abrir':
        filename = sg.popup_get_file("Selecciona la imagen a cargar")
        rgb = utility.is_rgb(filename)
        proccessed_image = convert_to_bytes(filename, resize=new_size)
        window['-IMAGE-'].update(proccessed_image)
        window['-NOMBRE_IMAGEN-'].update(filename)
        window['-NOMBRE_IMAGEN-'].update(visible= True)
        window['-IMAGE-'].update(visible = True)


        working_copy_filename = utility.create_working_copy(filename)
        drawing_copy_filename = utility.create_drawing_copy(filename)
        # drawing_copy_filename_wc = utility.create_drawing_copy_wc(filename)
        pixels = function.get_pixel_values(filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)

        information_text = utility.info_imagen(filename, pixel_frequency, rgb)
        window['-INFO_TEXT-'].update(information_text)
        window['-INFO_TEXT-'].update(visible = True)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
        pixels_wc = function.get_pixel_values(working_copy_filename)    
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        information_text = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text)
        window['-INFO_TEXT_WC-'].update(visible = True)

    if event == 'Guardar':
        new_filename = sg.popup_get_file("Guardar como", save_as= True)
        utility.save_as(new_filename)
    
    if event == 'Transformaciones lineales por tramos':
        number_sections = int(sg.popup_get_text('Número de tramos: '))
        array_points = []
        for i in range(number_sections + 1):
            pointA = int(sg.popup_get_text('Introduce la coordenada x del punto %s:' % str(i)))
            pointB = int(sg.popup_get_text('Introduce la coordenada y del punto %s:' % str(i)))
            point = (pointA, pointB)
            array_points.append(point)
        array_slopes = utility.calculate_array_slope(array_points)
        if (rgb):
            table.colour_by_sections_RGB(working_copy_filename, array_points, array_slopes)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_SECTIONS_RGB")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

            pixels_wc = function.get_pixel_values(working_copy_filename)
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            information_text = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text)
            window['-INFO_TEXT_WC-'].update(visible = True)

        else:
            table.colour_by_sections(working_copy_filename, array_points, array_slopes)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_SECTIONS_B&W")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

            pixels_wc = function.get_pixel_values(working_copy_filename)
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text_wc)
            window['-INFO_TEXT_WC-'].update(visible = True)

    if event == 'Escala de grises':
        table.colour_to_grayscale(working_copy_filename)
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

        pixels_wc = function.get_pixel_values(working_copy_filename)    
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)

    if event == 'Ajuste lineal del brillo y contraste':
        img = Image.open(working_copy_filename)
        pixels = function.get_pixel_values(working_copy_filename)    
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        brightness = function.brightness(img.size, pixel_frequency)
        contrast = function.contrast(img.size, brightness, pixel_frequency)

        if(brightness[0]!=brightness[1]):
            new_brigthness = []
            new_contrast = []
            for color in range(3):
                nb = sg.popup_get_text('Introduce el brillo:')
                new_brigthness.append(nb)
            for color in range(3):
                nc = sg.popup_get_text('Introduce el contrate:')
                new_contrast.append(nc)

            table.colour_to_linearlfit(working_copy_filename, brightness, contrast, new_brigthness, new_contrast)
            pixels_wc = function.get_pixel_values(working_copy_filename)
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)

            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_linearlfit")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

            information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text_wc)
            window['-INFO_TEXT_WC-'].update(visible = True)
        else:
            new_brigthness = sg.popup_get_text('Introduce el brillo:')
            new_contrast = sg.popup_get_text('Introduce el contrate:')
            table.colour_to_linearlfit(working_copy_filename, brightness, contrast, new_brigthness, new_contrast)

            pixels_wc = function.get_pixel_values(working_copy_filename)
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)

            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_linearlfit")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

            information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text_wc)
            window['-INFO_TEXT_WC-'].update(visible = True)
    
    if event == 'Correción Gamma':
        img = Image.open(working_copy_filename)
        pixels_wc = function.get_pixel_values(working_copy_filename)
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        if (rgb):
            gamma_valueR = sg.popup_get_text('Introduce el valor de correción gamma (R):')
            gamma_valueG = sg.popup_get_text('Introduce el valor de correción gamma (G):')
            gamma_valueB = sg.popup_get_text('Introduce el valor de correción gamma (B):')
            table.colour_to_gamma_RGB(working_copy_filename, gamma_valueR, gamma_valueG, gamma_valueB)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GAMMA_RGB")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
            information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text_wc)
            window['-INFO_TEXT_WC-'].update(visible = True)
        else:
            gamma_value = sg.popup_get_text('Introduce el valor de correción gamma:')
            table.colour_to_gamma(working_copy_filename, gamma_value)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GAMMA_B&W")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
            information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text)
            window['-INFO_TEXT_WC-'].update(visible = True)

    if event == 'Histograma absoluto Original':
        pixels = function.get_pixel_values(filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        function.draw_absolute_histogram(pixel_frequency, rgb)

    if event == 'Histograma absoluto Working Copy':
        pixels_wc = function.get_pixel_values(working_copy_filename)
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        function.draw_absolute_histogram(pixel_frequency_wc, rgb)
    
    if event == 'Histograma absoluto acumulado Original':
        pixels = function.get_pixel_values(filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        pixel_frequency_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency, rgb)
        function.draw_absolute_histogram(pixel_frequency_cum, rgb)

    if event == 'Histograma absoluto acumulado Working Copy':
        pixels_wc = function.get_pixel_values(working_copy_filename)
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        if(rgb == 0):
            pixel_frequency_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, 2)
        else:
            pixel_frequency_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, rgb)
        if(rgb == 0):
            function.draw_absolute_histogram(pixel_frequency_cum, 2)
        else:
            function.draw_absolute_histogram(pixel_frequency_cum, rgb)

    if event == 'Ecualización del histograma':
        pixels_wc = function.get_pixel_values(working_copy_filename)
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        function.draw_absolute_histogram(pixel_frequency, rgb)
        if(rgb == 0):
            pixel_frequency_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, 2)
            table.colour_equalization_BW(working_copy_filename, pixel_frequency_cum, rgb)
            pixels_wc = function.get_pixel_values(working_copy_filename)
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            function.draw_absolute_histogram(pixel_frequency, rgb)
        else:
            pixel_frequency_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, rgb)
            table.colour_equalization(working_copy_filename, pixel_frequency_cum, rgb)
            pixels_wc = function.get_pixel_values(working_copy_filename)
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            function.draw_absolute_histogram(pixel_frequency, rgb)

        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_ECUALIZACION")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)    

    if event == 'Especificación del histograma':
        img_wc = Image.open(working_copy_filename)
        si_filename = sg.popup_get_file("Selecciona la imagen a cargar")
        img_si = Image.open(si_filename)
        working_copy_filename_si = utility.create_working_copy(si_filename)

        pixels_wc = function.get_pixel_values(working_copy_filename)
        pixels_si = function.get_pixel_values(working_copy_filename_si)
        
        if(rgb == 0):
            pixel_frequency_si = function.calculate_pixel_frequency(pixels_si)
            pixel_frequency_si_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_si, 2)
            pixel_frequency_si_cum_norm = function.calculate_normalized_frequencies(pixel_frequency_si_cum, img_si.size, 2)

            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            pixel_frequency_wc_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, 2)
            pixel_frequency_wc_cum_norm = function.calculate_normalized_frequencies(pixel_frequency_wc_cum, img_wc.size, 2)
        else:
            pixel_frequency_si = function.calculate_pixel_frequency(pixels_si)
            pixel_frequency_si_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_si, rgb)
            pixel_frequency_si_cum_norm = function.calculate_normalized_frequencies(pixel_frequency_si_cum, img_si.size, rgb)

            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            pixel_frequency_wc_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, rgb)
            pixel_frequency_wc_cum_norm = function.calculate_normalized_frequencies(pixel_frequency_wc_cum, img_wc.size, rgb)

        table.color_specification(working_copy_filename, pixel_frequency_wc_cum_norm, pixel_frequency_si_cum_norm, rgb)

        proccessed_image = convert_to_bytes(si_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(si_filename + "_ESPECIFICACIÓN")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
        information_text_si = utility.info_imagen(si_filename, pixel_frequency_si , rgb)
        window['-INFO_TEXT_WC-'].update(information_text_si)
        window['-INFO_TEXT_WC-'].update(visible = True)

    if event == 'Diferencia entre dos imagenes':
        second_filename = sg.popup_get_file("Selecciona la segunda imagen a cargar")
        working_copy_second_filename = utility.create_working_copy(second_filename)
        second_proccessed_image = convert_to_bytes(working_copy_second_filename, resize=new_size)
        window['-IMAGEWC-'].update(second_proccessed_image)
        window['-IMAGEWC-'].update(visible = True)

        difference_filename = function.image_difference(working_copy_filename, working_copy_second_filename)
        pixels_difference = function.get_pixel_values(difference_filename)
        pixel_frequency_difference = function.calculate_pixel_frequency(pixels_difference)

        function.draw_absolute_histogram(pixel_frequency_difference, rgb)
        umbral = int(sg.popup_get_text("Selecciona el umbral:"))
        function.draw_image_difference(difference_filename, umbral)

        proccessed_image = convert_to_bytes(second_filename, resize=new_size)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_difference,rgb)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(second_filename + "_SEGUNDA_IMAGEN")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)

#############################################################################################
#############################################################################################
#############################################################################################

    if event == 'Espejo horizontal':
        table.horizontal_mirror(working_copy_filename)
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

        pixels_wc = function.get_pixel_values(working_copy_filename)    
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)

    if event == 'Espejo vertical':
        table.vertical_mirror(working_copy_filename)
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

        pixels_wc = function.get_pixel_values(working_copy_filename)    
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True) 
    
    if event == 'Traspuesta de una imagen':
        table.trasp_mirror(working_copy_filename)
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

        pixels_wc = function.get_pixel_values(working_copy_filename)    
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)

    if event == 'Rotaciones múltiplo de 90º':
        rotation_angle = sg.popup_get_text('Introduce el ángulo de rotación (+/-(90, 180, 270))')
        if rotation_angle not in {'90' , '-90', '180', '-180', '270', '-270'}:
            print('Angulo de rotación no multiplo de 90')
        else:
            table.rotate(working_copy_filename, rotation_angle)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

            pixels_wc = function.get_pixel_values(working_copy_filename)    
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text_wc)
            window['-INFO_TEXT_WC-'].update(visible = True)  

    if event == 'Transformación de Escalado':
        mode = sg.popup_get_text('Introduce 0 para modo escalado VMP o 1 para modo escalado bilineal')
        mode = int(mode)
        if (mode == 0):
            sg.popup('El tamaño de la seleccion de trabajo actual es %i x %i' % (img_width_wc, img_height_wc))
            new_width = sg.popup_get_text('Introduce el nuevo ancho de la imagen:')
            new_height = sg.popup_get_text('Introduce el nuevo alto de la imagen:')
            table.scale_vmp(working_copy_filename, new_width, new_height)
        elif (mode == 1):
            sg.popup('El tamaño de la seleccion de trabajo actual es %i x %i' % (img_width_wc, img_height_wc))
            new_width = sg.popup_get_text('Introduce el nuevo ancho de la imagen:')
            new_height = sg.popup_get_text('Introduce el nuevo alto de la imagen:')
            table.scale_bilineal(working_copy_filename, new_width, new_height)

        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

        pixels_wc = function.get_pixel_values(working_copy_filename)    
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)  

    if event == 'Transformación de Rotación':
        # sg.popup('Seleccione el ángulo de rotación.\nSi desea que se rote hacia la izquierda incluya un simbolo (-) delante del valor')
        # rotation_angle = sg.popup_get_text('Introduce el ángulo de rotación de la imagen:')

        # table.rotate_paint(working_copy_filename, rotation_angle)
        table.rotate_ti(working_copy_filename, '211')

        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GREYSCALE")
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)

        pixels_wc = function.get_pixel_values(working_copy_filename)    
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
        window['-INFO_TEXT_WC-'].update(information_text_wc)
        window['-INFO_TEXT_WC-'].update(visible = True)  


#############################################################################################
#############################################################################################
#############################################################################################


## Detection of click on image to create ROI
    if event == '-IMAGE-' :
        if (len(roi_clicks) < 2):
            roi_clicks.append(input.cursor_image_pos_for_rectangle(x_pos , y_pos))
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
            draw.rectangle(adapted_roi_clicks, width=1, outline='pink')
            image_dc.save(drawing_copy_filename)
            image_roi = convert_to_bytes(drawing_copy_filename, resize=new_size)
            window['-IMAGE-'].update(image_roi)
            final_roi = utility.create_image_roi(adapted_roi_clicks, filename)
            final_roi.save(working_copy_filename)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True) 
            pixels_wc = function.get_pixel_values(working_copy_filename)
            pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
            information_text_wc = utility.info_imagen(working_copy_filename, pixel_frequency_wc, rgb)
            window['-INFO_TEXT_WC-'].update(information_text_wc)
            window['-INFO_TEXT_WC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_ROI")
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(visible= True)           
            roi = 1

    # if event == '-IMAGEWC-' :
    #     print('s')
    #     if (len(roi_clicks_wc) < 2):
    #         roi_clicks_wc.append(input.cursor_image_pos_for_rectangle(x_pos_wc , y_pos_wc))
    #     if (roi_wc):
    #         roi_clicks_wc.clear()
    #         drawing_copy_filename_wc = utility.create_drawing_copy_wc(drawing_copy_filename_wc)
    #         wc_image_dc = utility.open_drawing_copy(drawing_copy_filename_wc)
    #         wc_image_roi = convert_to_bytes(drawing_copy_filename_wc, resize=new_size)
    #         window['-IMAGEWC-'].update(wc_image_roi)
    #         roi_wc = 0
    #     if (len(roi_clicks_wc) == 2):
    #         wc_image_dc = utility.open_drawing_copy(drawing_copy_filename_wc)
    #         draw = ImageDraw.Draw(wc_image_dc)
    #         real_width, real_height  = utility.image_size(filename)
    #         adapted_roi_clicks_wc = []
    #         real_point_x = 0
    #         real_point_y = 0
    #         for point in roi_clicks_wc:
    #             real_point_x = round(point[0] * real_width/img_width)
    #             real_point_y = round(point[1] * real_height/img_height)
    #             adapted_roi_clicks_wc.append((real_point_x, real_point_y))
    #         draw.rectangle(adapted_roi_clicks_wc, width=1, outline='pink')
    #         wc_image_dc.save(drawing_copy_filename_wc)
    #         wc_image_roi = convert_to_bytes(drawing_copy_filename_wc, resize=new_size)
    #         window['-IMAGEWC-'].update(wc_image_roi)
    #         final_roi = utility.create_image_roi(adapted_roi_clicks_wc, working_copy_filename)
    #         final_roi.save(working_copy_filename)
    #         proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
    #         window['-IMAGEWC-'].update(proccessed_image)
    #         window['-IMAGEWC-'].update(visible = True)            
    #         roi_wc = 1



## Instructions to be executed every 25 ms
    if (input.is_cursor_over_image(x_pos , y_pos, img_height, img_width)):
        real_width, real_height  = utility.image_size(filename)
        window['-MOUSE_POS-'].update(visible = True)
        img = Image.open(filename)
        pixs = img.load()
        point = input.cursor_image_pos(x_pos , y_pos)
        real_point_x = round(point[0] * real_width/img_width)
        real_point_y = round(point[1] * real_height/img_height)
        window['-MOUSE_POS-'].update(str(input.cursor_image_pos(x_pos , y_pos)) + ' ' + str(pixs[real_point_x, real_point_y]))
    else:
        window['-MOUSE_POS-'].update(visible = False)
    
    if(input.is_cursor_over_image(x_pos_wc , y_pos_wc, img_height_wc, img_width_wc)):
        window['-MOUSE_POS_WC-'].update(visible = True)
        real_width_wc, real_height_wc  = utility.image_size(working_copy_filename)
        img_wc = Image.open(working_copy_filename)
        pixs_wc = img_wc.load()
        point_wc = input.cursor_image_pos(x_pos_wc , y_pos_wc)
        real_point_x_wc = round(point_wc[0] * real_width_wc/img_width_wc)
        real_point_y_wc = round(point_wc[1] * real_height_wc/img_height_wc)
        window['-MOUSE_POS_WC-'].update(str(input.cursor_image_pos(x_pos_wc , y_pos_wc)) + ' ' + str(pixs_wc[real_point_x_wc, real_point_y_wc]))       
    else:
        window['-MOUSE_POS_WC-'].update(visible = False)


os.remove(working_copy_filename)
os.remove(drawing_copy_filename)
# os.remove(drawing_copy_filename_wc)
window.close()
