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
import function

working_copy_filename = ""
drawing_copy_filename = ""

# Método encargado de realizar una copia de trabajo
# para la visualización de las distintas transformaciones
def create_working_copy(filename):
    img = PIL.Image.open(filename)
    working_copy_filename = os.path.splitext(filename)[0] + "_WC.tiff"
    print(working_copy_filename)
    img.save(working_copy_filename)
    del img
    return working_copy_filename

# Método encargado de realizar una copia de dibujo
# para la visualización del roi
def create_drawing_copy(filename):
    img = PIL.Image.open(filename)
    drawing_copy_filename = os.path.splitext(filename)[0] + "_DC.tiff"
    print(drawing_copy_filename)
    img.save(drawing_copy_filename)
    del img
    return drawing_copy_filename

# Método encargado de guardar los cambios realizados en
# una copia de la original
def save_as(saves_as_filename):
    img = PIL.Image.open(working_copy_filename)
    img.save(saves_as_filename + ".tiff")
    del img

# Método encargado de mostrar la información de la imagen
def info_imagen(filename, pixels):
    img = PIL.Image.open(filename, 'r')
    width, height = img.size
    brightness = function.brightness(img.size, pixels)
    contrast = function.contrast(img.size, brightness, pixels)
    max = function.max_value(pixels)
    min = function.min_value(pixels)
    entropy = function.entropy(img.size, function.calculate_normalized_frequencies(pixels, img.size))
    return ('Height: %s | Width: %s | Brightness: %s | Contrast: %s |  Min: %s | Max: %s | Entropy: %s' % 
    (str(height), str(width), str(round(brightness, 3)), str(round(contrast, 3)), str(min), str(max), str(round(entropy, 3))))



