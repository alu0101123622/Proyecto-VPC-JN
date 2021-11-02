"""
    Universidad de La Laguna - Grado en Ingenería Informática
    Cuarto Curso - Visión por Computador
    2021-2022

    Autores:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    Fichero utility.py: Fichero donde se definen distintos tipos de métodos
                        para el manejo de imagenes
"""
import os.path
import PIL.Image

working_copy_filename = ""

# Método encargado de realizar una copia de trabajo
# para la visualización de las distintas transformaciones
def create_working_copy(filename):
    img = PIL.Image.open(filename)
    working_copy_filename = os.path.splitext(filename)[0] + "_WC.tiff"
    print(working_copy_filename)
    img.save(working_copy_filename)
    del img
    return working_copy_filename

# Método encargado de guardar los cambios realizados en
# una copia de la original
def save_as(saves_as_filename):
    img = PIL.Image.open(working_copy_filename)
    img.save(saves_as_filename + ".tiff")
    del img

def info_imagen(filename, pixels):
    img = PIL.Image.open(filename, 'r')
    width, height = img.size
    print('Los datos de la imagen son ancho: %s, largo: %s' % (str(width), str(height)))
    print('Max:', max(pixels), 'Min:', min(pixels))
    print('Brillo:', brightness(img.size, pixels))

def brightness(size, pixels):
    sum = 0
    for pixel in pixels:
        sum += int(pixel)
    width, height = size
    size = width * height
    bright = sum / size
    return bright