"""
    University of La Laguna - Degree in Computer Engineering
    Fourth grade - Computer vision
    2021-2022

    Authors:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    File main.py: Main program file
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

working_copy_filename = ''
drawing_copy_filename = ''
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
sg.theme('GreenMono')
menu_def = [['Imagen', ['Abrir','Guardar', 'Salir',]],
            ['Información', ['Imprimir datos', 'Histogramas', ['Histograma absoluto Original', 'Histograma absoluto Working Copy', 'Histograma absoluto acumulado Original', 'Histograma absoluto acumulado Working Copy']],],
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

# ---------------- Bucle de eventos ----------------
while True:
    event, values = window.read(timeout=500)
    # print(event, values)


    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    x_pos = window['-IMAGE-'].Widget.winfo_rootx()
    y_pos = window['-IMAGE-'].Widget.winfo_rooty()
    img_height = window['-IMAGE-'].Widget.winfo_height()
    img_width  = window['-IMAGE-'].Widget.winfo_width()

    # Opciones de la barra superior principal
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
        pixels = function.get_pixel_values(filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        information_text = utility.info_imagen(filename, pixel_frequency)
        window['-INFO_TEXT-'].update(information_text)
        window['-INFO_TEXT-'].update(visible = True)
#     working_copy_filename = utility.create_working_copy(filename)
#     img_wc = Image.open(working_copy_filename)
#     drawing_copy_filename = utility.create_drawing_copy(filename)


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
            # information_text = utility.info_imagen(filename, pixels)
            window['-INFO_TEXT-'].update(information_text)
        else:
            table.colour_by_sections(working_copy_filename, array_points, array_slopes)
            proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
            window['-IMAGEWC-'].update(proccessed_image)
            window['-IMAGEWC-'].update(visible = True)
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_SECTIONS_B&W")
            # information_text = utility.info_imagen(filename, pixels)
            window['-INFO_TEXT-'].update(information_text)

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
            window['-NOMBRE_IMAGEN_RESULTANTE-'].update(working_copy_filename + "_GAMMA_B&W")
            # information_text = utility.info_imagen(filename, pixels)
            window['-INFO_TEXT-'].update(information_text)

    if event == 'Histograma absoluto Original':
        pixels = function.get_pixel_values(filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        function.draw_absolute_histogram(pixel_frequency, rgb)

    if event == 'Histograma absoluto Working Copy':
        pixels = function.get_pixel_values(working_copy_filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        function.draw_absolute_histogram(pixel_frequency, rgb)
    
    if event == 'Histograma absoluto acumulado Original':
        pixels = function.get_pixel_values(filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        pixel_frequency_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency, rgb)
        function.draw_absolute_histogram(pixel_frequency_cum, rgb)

    if event == 'Histograma absoluto acumulado Working Copy':
        pixels = function.get_pixel_values(working_copy_filename)
        pixel_frequency = function.calculate_pixel_frequency(pixels)
        pixel_frequency_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency, rgb)
        function.draw_absolute_histogram(pixel_frequency_cum, rgb)

    if event == 'Ecualización del histograma':
        pixels_wc = function.get_pixel_values(working_copy_filename)
        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        # function.draw_absolute_histogram(pixel_frequency, rgb)
        pixels_frequencies_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, rgb)
        table.colour_equalization(working_copy_filename, pixels_frequencies_cum, rgb)
        proccessed_image = convert_to_bytes(working_copy_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
    
    if event == 'Especificación del histograma':
        img_wc = Image.open(working_copy_filename)
        si_filename = sg.popup_get_file("Selecciona la imagen a cargar")
        img_si = Image.open(si_filename)
        working_copy_filename_si = utility.create_working_copy(si_filename)

        pixels_wc = function.get_pixel_values(working_copy_filename)
        pixels_si = function.get_pixel_values(working_copy_filename_si)

        pixel_frequency_si = function.calculate_pixel_frequency(pixels_si)
        pixel_frequency_si_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_si, rgb)
        pixel_frequency_si_cum_norm = function.calculate_normalized_frequencies(pixel_frequency_si_cum, img_si.size)

        pixel_frequency_wc = function.calculate_pixel_frequency(pixels_wc)
        pixel_frequency_wc_cum = function.calculate_pixel_frequency_cumulative(pixel_frequency_wc, rgb)
        pixel_frequency_wc_cum_norm = function.calculate_normalized_frequencies(pixel_frequency_wc_cum, img_wc.size)

        table.color_specification(working_copy_filename, pixel_frequency_wc_cum_norm, pixel_frequency_si_cum_norm, rgb)

        proccessed_image = convert_to_bytes(si_filename, resize=new_size)
        window['-IMAGEWC-'].update(proccessed_image)
        window['-IMAGEWC-'].update(visible = True)
        window['-NOMBRE_IMAGEN_RESULTANTE-'].update(si_filename)


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
        function.draw_image_difference(difference_filename, 30)

    # Detección de click en imagen para crear ROI
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
            roi = 1

    # Instrucciones a ejecutarse cada 25 ms
    if (input.is_cursor_over_image(x_pos , y_pos, img_height, img_width)):
        window['-MOUSE_POS-'].update(visible = True)
        window['-MOUSE_POS-'].update(input.cursor_image_pos(x_pos , y_pos))
    else:
        window['-MOUSE_POS-'].update(visible = False)
        
    if event == '-IMAGEWC-':
        if (len(roi_clicks) < 2):
            roi_clicks.append(input.cursor_image_pos_for_rectangle(x_pos , y_pos))


    
os.remove(working_copy_filename)
os.remove(drawing_copy_filename)
window.close()
