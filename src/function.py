"""
    University of La Laguna - Degree in Computer Engineering
    Fourth grade - Computer vision
    2021-2022

    Authors:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    File function.py: The calculation functions used in the main program are implemented.
"""
from tkinter import constants
from typing import OrderedDict, Tuple
import matplotlib.pyplot as plt
import PIL.Image
import collections
import os.path
import utility

from numpy import Infinity, log2, sqrt

## Method for obtaining the values ​​of the images 
## of width and length
def get_pixel_values(filename):
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
        red_pix_freq = utility.correct_frequency(red_pix_freq)
        green_pix_freq = utility.correct_frequency(green_pix_freq)
        blue_pix_freq = utility.correct_frequency(blue_pix_freq)
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
        grey_pix_freq = utility.correct_frequency(grey_pix_freq)
        grey_pix_freq_ord = collections.OrderedDict(sorted(grey_pix_freq.items()))
        return grey_pix_freq_ord 

## Method that calculates the normalized histogram of the colors of the image
def  calculate_normalized_frequencies(frequencies, size):
    width, height = size
    size = width * height
    if (len(frequencies) == 3):
        for color in frequencies:
            for pixel_value, frequency in color.items():
                color.update(OrderedDict.fromkeys([pixel_value], frequency / size))
    else:
        for pixel_value, frequency in frequencies.items():
                frequencies.update(OrderedDict.fromkeys([pixel_value], frequency / size))
    return frequencies    

## Method that calculates the cumulative histogram of the colors of the image
def calculate_pixel_frequency_cumulative(pixel_frequency, rgb):
    pixel_frequency_acumulativeA = dict(pixel_frequency[0])
    pixel_frequency_acumulativeB = dict(pixel_frequency[1])
    pixel_frequency_acumulativeC = dict(pixel_frequency[2])
    pixel_frequency_acumulative = [pixel_frequency_acumulativeA, pixel_frequency_acumulativeB, pixel_frequency_acumulativeC]
    sum1 = 0
    for pixel_value, frequency in pixel_frequency_acumulative[0].items():
        sum1 += frequency
        pixel_frequency_acumulative[0].update(OrderedDict.fromkeys([pixel_value], sum1))
    sum2 = 0
    for pixel_value, frequency in pixel_frequency_acumulative[1].items():
        sum2 += frequency
        pixel_frequency_acumulative[1].update(OrderedDict.fromkeys([pixel_value], sum2))
    sum3 = 0
    for pixel_value, frequency in pixel_frequency_acumulative[2].items():
        sum3 += frequency
        pixel_frequency_acumulative[2].update(OrderedDict.fromkeys([pixel_value], sum3))
    return pixel_frequency_acumulative
    
##  Method for creating the histogram of absolute values
def draw_absolute_histogram(pixel_frequency, rgb):
    if (rgb):
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
        if(len(pixel_frequency) == 3):
            keys = pixel_frequency[0].keys()
            values = pixel_frequency[0].values()
            plt.bar(keys, values, color='black', width=1.0)
            plt.xlabel("Valor de intensidad de color")
            plt.ylabel("Frecuencia")
            plt.title("Histograma de valores absolutos")
            plt.show()
        else:
            keys = pixel_frequency.keys()
            values = pixel_frequency.values()
            plt.bar(keys, values, color='black', width=1.0)
            plt.xlabel("Valor de intensidad de color")
            plt.ylabel("Frecuencia")
            plt.title("Histograma de valores absolutos")
            plt.show()
                           
## Brightness calculation method
def brightness(size, pixel_frequency):
    sum = 0
    width, height = size
    size = width * height
    if (len(pixel_frequency) == 3):
        for color in pixel_frequency:
            for pixel_value, frequency in color.items():
                sum += (frequency * pixel_value) / 3
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
                sum += (frequency * pow(pixel_value - brightness, 2)) / 3
    else: 
        for pixel_value, frequency in pixel_frequency.items():
            sum += (frequency * pow(pixel_value - brightness, 2))
    contrast = sqrt(sum / size)
    return contrast

## Entropy calculation method
def entropy(size, pixel_frequency_normalized):
    sum = 0
    width, height = size
    size = width * height
    if (len(pixel_frequency_normalized) == 3):
        for color in pixel_frequency_normalized:
            for pixel_value, frequency in color.items():
                if(frequency != 0):
                    sum += (frequency * log2(frequency)) / 3
    else:
        for pixel_value, frequency in pixel_frequency_normalized.items():
            sum += (frequency * log2(frequency))
    return -sum

## Max calculation method
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

## Min calculation method
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

## Image difference calculation method
def image_difference(filename, second_filename):
    first_image = PIL.Image.open(filename)
    second_image = PIL.Image.open(second_filename)
    if(first_image.size != second_image.size):
        return "Cant compare two images with different sizes"
    result_image = PIL.Image.new(mode='RGB',size=first_image.size)
    first_pixels  = first_image.load()
    second_pixels = second_image.load()
    result_pixels = result_image.load()
    for i in range(first_image.size[0]):
        for j in range(first_image.size[1]):
            result_pixels[i,j] = tuple(map(lambda i, j: abs(i - j), first_pixels[i,j], second_pixels[i,j]))
    difference_filename = os.path.splitext(filename)[0] + "_diff.tiff"
    result_image.save(difference_filename)
    return difference_filename       

## Image difference draw method
def draw_image_difference(difference_filename, t):
    difference_filename = PIL.Image.open(difference_filename)
    result_pixels = difference_filename.load()
    for i in range(difference_filename.size[0]):
        for j in range(difference_filename.size[1]):
            if(result_pixels[i,j][0] >= t):
                result_pixels[i,j] = (255,0,0)
    difference_filename.show()

## Method in charge of finding the index in the histogram
def find_closest_index(original_accumulative_freq_value, pixel_frequency_si_cum):
    desired_index = 0
    for i in range(256):
        if(pixel_frequency_si_cum[0][i] <= original_accumulative_freq_value):
            desired_index = i
        else:
            return desired_index
    return desired_index
