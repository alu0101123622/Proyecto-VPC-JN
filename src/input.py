"""
    Universidad de La Laguna - Grado en Ingenería Informática
    Cuarto Curso - Visión por Computador
    2021-2022

    Autores:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    Fichero main.py: Programa principal del proyecto
"""
import pyautogui

def is_cursor_over_image(img_x_pos , img_y_pos, img_height, img_width):
    cursor_pos = pyautogui.position()
    if (img_x_pos <= cursor_pos[0] <= (img_x_pos + img_width)):
        if(img_y_pos <= cursor_pos[1] <= (img_y_pos + img_height)):
            return 1
    return 0

def cursor_image_pos(img_x_pos , img_y_pos, img_height, img_width):
    cursor_pos = pyautogui.position()
    x = cursor_pos[0] - img_x_pos
    y = cursor_pos[1] - img_y_pos
    return ([x, y])