"""
    Universidad de La Laguna - Grado en Ingenería Informática
    Cuarto Curso - Visión por Computador
    2021-2022

    Autores:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    Fichero main.py: Programa principal del proyecto
"""
from tkinter import constants
from typing import OrderedDict, Tuple
import matplotlib.pyplot as plt
import PIL.Image
import collections

from numpy import Infinity, log2, sqrt

## Method for obtaining the values ​​of the images 
## of width and length
def get_pixel_values(filename):
    # img = PIL.Image.open(filename, 'r')
    img = PIL.Image.open(filename)

    pixel_values = list(img.getdata())
    del img
    return pixel_values

## Method that calculates the histogram of the colors of the image
def calculate_pixel_frequency(pixel_values):
    grey_pix_freq =  {}
    red_pix_freq =   {}
    green_pix_freq = {}
    blue_pix_freq =  {}
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
        red_pix_freq_ord = collections.OrderedDict(sorted(red_pix_freq.items()))
        green_pix_freq_ord = collections.OrderedDict(sorted(green_pix_freq.items()))
        blue_pix_freq_ord = collections.OrderedDict(sorted(blue_pix_freq.items()))
        return red_pix_freq_ord, green_pix_freq_ord, blue_pix_freq_ord
    # B&W Image
    else:                                      
        for pixel in pixel_values:
            if pixel in grey_pix_freq:
                grey_pix_freq[pixel] += 1
            else:
                grey_pix_freq[pixel] = 1
        return grey_pix_freq 

## Method that calculates the normalized histogram of the colors of the image
def  calculate_normalized_frequencies(frequencies, size):
    # print(size)
    # print(frequencies)
    # factor = 1.0/sum(frequencies.values())
    # for pixel in frequencies:
    #     frequencies[pixel] = frequencies[pixel] * factor
    width, height = size
    size = width * height
    if (len(frequencies) == 3):
        for color in frequencies:
            #color_key = color.keys()
            for pixel_value, frequency in color.items():
                color.update(OrderedDict.fromkeys([pixel_value], frequency / size))
    else:
        for pixel_value, frequency in frequencies.items():
                frequencies.update(OrderedDict.fromkeys([pixel_value], frequency / size))
    return frequencies    

##  Method for creating the histogram of absolute values
def draw_absolute_histogram(pixel_frequency):
    if (len(pixel_frequency) == 3):
        # RED
        keys = pixel_frequency[0].keys()
        values = pixel_frequency[0].values()
        plt.bar(keys, values, color='red', width=1.0)
        plt.xlabel("Valor de intensidad del color rojo")
        plt.ylabel("Frecuencia")
        plt.title("Histograma de valores absolutos")
        plt.show()
        # GREEN
        keys = pixel_frequency[1].keys()
        values = pixel_frequency[1].values()
        plt.bar(keys, values, color='green', width=1.0)
        plt.xlabel("Valor de intensidad del color verde")
        plt.ylabel("Frecuencia")
        plt.title("Histograma de valores absolutos")
        plt.show()  
        # BLUE
        keys = pixel_frequency[2].keys()
        values = pixel_frequency[2].values()
        plt.bar(keys, values, color='blue', width=1.0)
        plt.xlabel("Valor de intensidad del color azul")
        plt.ylabel("Frecuencia")
        plt.title("Histograma de valores absolutos")
        plt.show()              
    else:
        for pixel in pixel_frequency:
            keys = pixel_frequency.keys()
            values = pixel_frequency.values()
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
def brightness(size, pixel_frequency):
    sum = 0
    width, height = size
    size = width * height
    if (len(pixel_frequency) == 3):
        for color in pixel_frequency:
            for pixel_value, frequency in color.items():
                # print('pv: %s * f: %s' % (str(pv), str(f)))
                sum += (frequency * pixel_value) / 3
                # sum += frequency * pixel_value
    else:
        for pixel_value, frequency in pixel_frequency.items():
            sum += (frequency * pixel_value) 
    bright = sum / (size)
    return bright

## Contrast calculation method
def contrast(size, brightness, pixel_frequency):
    sum = 0
    width, height = size
    size = width * height
    if (len(pixel_frequency) == 3):
        for color in pixel_frequency:
            for pixel_value, frequency in color.items():
                # print('pv: %s * f: %s' % (str(pv), str(f)))
                sum += (frequency * pow(pixel_value - brightness, 2)) / 3
    else: 
        for pixel_value, frequency in pixel_frequency.items():
            sum += (frequency * pow(pixel_value - brightness, 2))
    contrast = sqrt(sum / size)
    return contrast

def entropy(size, pixel_frequency_normalized):
    sum = 0
    width, height = size
    size = width * height
    if (len(pixel_frequency_normalized) == 3):
        for color in pixel_frequency_normalized:
            for pixel_value, frequency in color.items():
                sum += (frequency * log2(frequency)) / 3
    else:
        for pixel_value, frequency in pixel_frequency_normalized.items():
            sum += (frequency * log2(frequency))
    return -sum

def max_value(pixel_frequency):
    max = -1
    if (len(pixel_frequency) == 3):
        for color in pixel_frequency:
            for pixel_value, frequency in color.items():
                if (pixel_value > max):
                    max = pixel_value
    else:
        for pixel_value, frequency in pixel_frequency.items():
            if (pixel_value > max):
                    max = pixel_value
    return max

def min_value(pixel_frequency):
    min = Infinity
    if (len(pixel_frequency) == 3):
        for color in pixel_frequency:
            for pixel_value, frequency in color.items():
                if (pixel_value < min):
                    min = pixel_value
    else:
        for pixel_value, frequency in pixel_frequency.items():
            if (pixel_value < min):
                    min = pixel_value
    return min