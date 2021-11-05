"""
    Universidad de La Laguna - Grado en Ingenería Informática
    Cuarto Curso - Visión por Computador
    2021-2022

    Autores:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    Fichero main.py: Programa principal del proyecto
"""
from typing import Tuple
import matplotlib.pyplot as plt
import PIL.Image

## Method for obtaining the values ​​of the images 
## of width and length
def get_pixel_values(filename):
    img = PIL.Image.open(filename, 'r')
    #width, height = img.size
    pixel_values = list(img.getdata())
    #print('Los datos de la imagen son widht: %s, height: %s' % (str(width), str(height)))
    #print(pixel_values)
    del img
    return pixel_values

## Method that calculates the histogram of the colors of the image
## He cambiado el nombre a calculate_pixel_frequency ya que representa mejor lo que hace la función
def calculate_pixel_frequency(pixel_values):
    grey_pix_freq =  {}
    red_pix_freq =   {}
    green_pix_freq = {}
    blue_pix_freq =  {}
#    print(type(pixel_values[0]))
    if type(pixel_values[0]) == tuple:   # Color image
        # RED
        for pixel in pixel_values:
            if pixel[0] in red_pix_freq:
                red_pix_freq[pixel[0]] += 1
            else:
                red_pix_freq[pixel[0]] = 1
      # GREEN
        for pixel in pixel_values:
            if pixel[1] in green_pix_freq:
                green_pix_freq[pixel[1]] += 1
            else:
                green_pix_freq[pixel[1]] = 1
        # BLUE
        for pixel in pixel_values:
            if pixel[2] in blue_pix_freq:
                blue_pix_freq[pixel[2]] += 1
            else:
                blue_pix_freq[pixel[2]] = 1
        return red_pix_freq, green_pix_freq, blue_pix_freq
    # B&W Image
    else:                                      
        for pixel in pixel_values:
            if pixel in grey_pix_freq:
                grey_pix_freq[pixel] += 1
            else:
                grey_pix_freq[pixel] = 1
        return grey_pix_freq 

## Method that calculates the normalized histogram of the colors of the image
## He cambiado el nombre a calculate_normalized_frequencies ya que representa mejor lo que hace la función
def  calculate_normalized_frequencies(frequencies, size):
    # print(size)
    # print(frequencies)
    # factor = 1.0/sum(frequencies.values())
    # for pixel in frequencies:
    #     frequencies[pixel] = frequencies[pixel] * factor
    normalized_frequencies = frequencies
    for pixel in frequencies:
        normalized_frequencies[pixel] = frequencies[pixel] /size
    return normalized_frequencies    
    
##  Method for creating the histogram of absolute values
def draw_absolute_histogram(array):
    keys = array.keys()
    values = array.values()
    plt.bar(keys, values, color='black')
    plt.xlabel("Valor de intensidad de color")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de valores absolutos")
    plt.show()

## Method for creating the histogram of cumulative values
def draw_cumulative_histogram(array):
    plt.hist(array, 256, range=[0, 255], histtype='bar', color = "grey", edgecolor= "black", cumulative = True)
    plt.xlabel("Valor de intensidad de color")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de valores acumulativos")
    plt.show()


## Brightness calculation method
def brightness(size, pixels):
    sum = 0
    for pixel in pixels:
        sum += int(pixel)
    width, height = size
    size = width * height
    bright = sum / size
    return bright

## Contrast calculation method
def contrast(size, bright, pixels):
    print(bright)
    print("HOLA")
