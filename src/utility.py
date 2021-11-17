"""
    University of La Laguna - Degree in Computer Engineering
    Fourth grade - Computer vision
    2021-2022

    Authors:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    File utility.py: Functional functions
"""
import os.path
import PIL.Image
from pyautogui import size
import function

working_copy_filename = ""
drawing_copy_filename = ""

## Method in charge of checking if an image is in color
def is_rgb(filename):
    img = PIL.Image.open(filename)
    pix = img.load()
    if type(pix[0,0]) == tuple: 
        return 1
    return 0

## Method in charge of making a working copy
## for the visualization of the different transformations
def create_working_copy(filename):
    global working_copy_filename 
    global drawing_copy_filename
    img = PIL.Image.open(filename)
    rgbimg = PIL.Image.new('RGB', img.size)
    rgbimg.paste(img)
    working_copy_filename = os.path.splitext(filename)[0] + "_WC.tiff"
    rgbimg.save(working_copy_filename)
    del img
    return working_copy_filename

## Method responsible for making a drawing copy
## for roi display
def create_drawing_copy(filename):
    global working_copy_filename 
    global drawing_copy_filename
    img = PIL.Image.open(filename)
    rgbimg = PIL.Image.new('RGB', img.size)
    rgbimg.paste(img)
    drawing_copy_filename = os.path.splitext(filename)[0] + "_DC.tiff"
    rgbimg.save(drawing_copy_filename)
    del img
    return drawing_copy_filename

## Method responsible for making a drawing copy
## for roi display
def create_drawing_copy_wc(filename):
    global working_copy_filename 
    global drawing_copy_filename
    global drawing_copy_filename_wc

    img = PIL.Image.open(filename)
    rgbimg = PIL.Image.new('RGB', img.size)
    rgbimg.paste(img)
    drawing_copy_filename_wc = os.path.splitext(filename)[0] + "_WCDC.tiff"
    rgbimg.save(drawing_copy_filename_wc)
    del img
    return drawing_copy_filename_wc

## Method responsible for opening the drawing copy
## for roi display
def open_drawing_copy(filename):
    img = PIL.Image.open(filename)
    return img

## Method in charge of saving the changes made in
## a copy of the original
def save_as(saves_as_filename):
    global working_copy_filename 
    global drawing_copy_filename
    img = PIL.Image.open(working_copy_filename)
    img.save(saves_as_filename + ".tiff")
    del img

## Method responsible for displaying image information
def info_imagen(filename, pixels):
    img = PIL.Image.open(filename)
    width, height = img.size
    brightness = function.brightness(img.size, pixels)
    contrast = function.contrast(img.size, brightness, pixels)
    max = function.max_value(pixels)
    min = function.min_value(pixels)
    entropy = function.entropy(img.size, function.calculate_normalized_frequencies(pixels, img.size))
    return ('Height: %s | Width: %s | Brightness: %s | Contrast: %s |  Min: %s | Max: %s | Entropy: %s' % 
    (str(height), str(width), str(round(brightness, 3)), str(round(contrast, 3)), str(min), str(max), str(round(entropy, 3))))

## Method in charge of calculating the size of the image
def image_size(filename):
    img = PIL.Image.open(filename)
    width, height = img.size   
    return (width, height) 

## Method responsible for creating the roi image
def create_image_roi(roi_points, filename):
    img = PIL.Image.open(filename)
    base_image = PIL.Image.new('RGB', img.size)
    base_image.paste(img)
    region = base_image.crop((roi_points[0][0], roi_points[0][1], roi_points[1][0], roi_points[1][1]))
    return region

def calculate_slope(pointA, pointB):
    slope = round((pointB[1] - pointA[1]) / (pointB[0] - pointA[0]), 2)
    return slope

def calculate_array_slope(array_points):
    array_slopes = []
    for point, (i, j) in enumerate(array_points):
        if ((point + 1) < len(array_points)):
            slope = calculate_slope(array_points[point], array_points[point + 1])
            array_slopes.append(slope)
    return array_slopes

def correct_frequency(pixel_frequency):
    color_array = [ r for r in range(256)]
    for color in color_array:
        if color not in pixel_frequency.keys():
            pixel_frequency[color] = 0
    return pixel_frequency