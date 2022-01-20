"""
    University of La Laguna - Degree in Computer Engineering
    Fourth grade - Computer vision
    2021-2022

    Authors:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    File table.py: LUTs and functions where they are used are defined
"""
from re import X
import PIL.Image
import function
import numpy as np
import math

## LUT of grayscale
def make_grayscale_table():
    grayscaleLUT = [
        [r * 0.299 for r in range(256)],
        [g * 0.587 for g in range(256)],
        [b * 0.114 for b in range(256)],
    ]
    return grayscaleLUT

## LUT of linearfit
def make_linearfit_table(brightness, contrast, new_brightness, new_contrast):
    brightness = round(float(brightness[0]), 3)
    contrast = round(float(contrast[0]), 3)
    new_brightness = round(float(new_brightness), 3)
    new_contrast = round(float(new_contrast), 3)
    if (contrast == new_contrast):
        A = 1
    else:
        A = new_contrast / contrast
    B = new_brightness - A * brightness
    
    linearfitLUT = [
        [(r * A + B) for r in range(256)],
        [(g * A + B) for g in range(256)],
        [(b * A + B) for b in range(256)],
    ]
    return linearfitLUT

def make_linearfit_table_RGB(brightness, contrast, new_brightness, new_contrast):
    A = [0, 0, 0]
    B = [0, 0, 0]
    brightness = [round(float(brightness[0]), 3), round(float(brightness[1]), 3), round(float(brightness[2]), 3)]
    contrast = [round(float(contrast[0]), 3), round(float(contrast[1]), 3), round(float(contrast[2]), 3)]
    new_brightness = [round(float(new_brightness[0]), 3), round(float(new_brightness[1]), 3), round(float(new_brightness[2]), 3)]
    new_contrast = [round(float(new_contrast[0]), 3), round(float(new_contrast[1]), 3), round(float(new_contrast[2]), 3)]
    if (contrast == new_contrast):
        A = [1, 1, 1]
    else:
        for color in range(3):
            A[color] = new_contrast[color] / contrast[color]
    for color in range(3):
        B[color] = new_brightness[color] - A[color] * brightness[color]
    
    linearfitLUT = [
        [(r * A[0] + B[0]) for r in range(256)],
        [(g * A[1] + B[1]) for g in range(256)],
        [(b * A[2] + B[2]) for b in range(256)],
    ]
    return linearfitLUT

## LUT of gamma in B&W img
def make_gamma_table(gamma_value):
    gamma_value = round(float(gamma_value), 3)
    gammaLUT = [
        [(pow((r / 255), gamma_value) * 255)  for r in range(256)],
        [(pow((g / 255), gamma_value) * 255) for g in range(256)],
        [(pow((b / 255), gamma_value) * 255) for b in range(256)]
    ]
    return gammaLUT

## LUT of gamma in color img
def make_gamma_table_RGB(gamma_valueR, gamma_valueG, gamma_valueB):
    gamma_valueR = round(float(gamma_valueR), 3)
    gamma_valueG = round(float(gamma_valueG), 3)
    gamma_valueB = round(float(gamma_valueB), 3)
    gammaLUT = [
        [(pow((r / 255), gamma_valueR) * 255)  for r in range(256)],
        [(pow((g / 255), gamma_valueG) * 255) for g in range(256)],
        [(pow((b / 255), gamma_valueB) * 255) for b in range(256)]
    ]
    return gammaLUT

## LUT of sections
def make_sections_table(array_points, array_slopes):
    array_points.pop(0)
    color_array = []
    color_array_aux = []
    for point, (i, j) in enumerate(array_points):
        if (point == 0):
            color = [(array_slopes[point] * (c - i) + j) for c in range(i + 1)]
        else:
            color = [(array_slopes[point] * (c - i) + j) for c in range((i - array_points[point - 1][0]))]
        color_array.append(color)
    for color in color_array:
        color_array_aux += color
    return color_array_aux

## LUT of equalization
def make_equalization_table_RGB(pixels_frequencies_abs, size):
    k_value = size / 256
    equalizationLUT = [
        [(max(0, round(pixels_frequencies_abs[0][r] / k_value) - 1)) for r in range(256)],
        [(max(0, round(pixels_frequencies_abs[1][g] / k_value) - 1)) for g in range(256)],
        [(max(0, round(pixels_frequencies_abs[2][b] / k_value) - 1)) for b in range(256)]
    ]
    return equalizationLUT

def make_equalization_table_BW(pixels_frequencies_abs, size):
    k_value = size / 256
    equalizationLUT = [
        [(max(0, round(pixels_frequencies_abs[0][r] / k_value) - 1)) for r in range(256)],
    ]
    return equalizationLUT

## LUT of specification
def make_specification_table(pixel_frequency_wc_cum, pixel_frequency_si_cum):
    specificationLUT = [
        [c for c in range(256)],
        [c for c in range(256)],
        [c for c in range(256)]
    ]
    for color in range(256):
        fg1 = pixel_frequency_wc_cum[0][color]
        g2 =  function.find_closest_index(fg1, pixel_frequency_si_cum)
        specificationLUT[0][color] = g2
    return specificationLUT

def make_specification_table_RGB(pixel_frequency_wc_cum, pixel_frequency_si_cum):
    specificationLUT = [
        [c for c in range(256)],
        [c for c in range(256)],
        [c for c in range(256)]
    ]
    for color in range(256):
        fg1 = pixel_frequency_wc_cum[0][color]
        g2 =  function.find_closest_index_RGB(fg1, pixel_frequency_si_cum, 0)
        specificationLUT[0][color] = g2
    for color in range(256):
        fg2 = pixel_frequency_wc_cum[1][color]
        g3 =  function.find_closest_index_RGB(fg2, pixel_frequency_si_cum, 1)
        specificationLUT[1][color] = g3
    for color in range(256):
        fg3 = pixel_frequency_wc_cum[2][color]
        g4 =  function.find_closest_index_RGB(fg3, pixel_frequency_si_cum, 2)
        specificationLUT[2][color] = g4
    return specificationLUT   

#############################################################################################
#############################################################################################
#############################################################################################

## Method in charge of performing the image transformation
## to a grayscale image
def colour_to_grayscale(working_copy_filename):
    grayscaleLUT = make_grayscale_table()
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    grey_value = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            for k in range(3):
                grey_value += grayscaleLUT[k][pixs[i,j][k]]
                grey_value = round(grey_value)
            pixs[i,j] = (grey_value, grey_value, grey_value)
            grey_value = 0
    img.save(working_copy_filename)
    del img

## Method in charge of making the linear adjustment of the brightness and contrast of the image
def colour_to_linearlfit(working_copy_filename, brightness, contrast, new_brigthness, new_contrast):
    img  = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    if brightness[0] != brightness[1]:
        linearfitLUT = make_linearfit_table_RGB(brightness, contrast, new_brigthness, new_contrast) 
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                linearfit_valueR = linearfitLUT[0][pixs[i,j][0]]
                linearfit_valueG = linearfitLUT[1][pixs[i,j][1]]
                linearfit_valueB = linearfitLUT[2][pixs[i,j][2]]
                linearfit_valueR = round(linearfit_valueR)
                linearfit_valueG = round(linearfit_valueG)
                linearfit_valueB = round(linearfit_valueB)
                pixs[i,j] = (linearfit_valueR, linearfit_valueG, linearfit_valueB)
    else:
        linearfitLUT = make_linearfit_table(brightness, contrast, new_brigthness, new_contrast)
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                linearfit_value = linearfitLUT[1][pixs[i,j][1]]
                linearfit_value = round(linearfit_value)
                pixs[i,j] = (linearfit_value, linearfit_value, linearfit_value)
    img.save(working_copy_filename)
    del img

## Method responsible for gamma correction of a color image
def colour_to_gamma_RGB(working_copy_filename, gamma_valueR, gamma_valueG, gamma_valueB):
    gammaLUT = make_gamma_table_RGB(gamma_valueR, gamma_valueG, gamma_valueB)
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            gamma_valueR = round(gammaLUT[0][pixs[i,j][0]])
            gamma_valueG = round(gammaLUT[1][pixs[i,j][1]])
            gamma_valueB = round(gammaLUT[2][pixs[i,j][2]])
            pixs[i,j] = (gamma_valueR, gamma_valueG, gamma_valueB)
    img.save(working_copy_filename)
    del img

## Method responsible for gamma correction of a B&W image
def colour_to_gamma(working_copy_filename, gamma_value):
    gammaLUT = make_gamma_table(gamma_value)
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            gamma_value = round(gammaLUT[0][pixs[i,j][0]])
            pixs[i,j] = (gamma_value, gamma_value, gamma_value)
    img.save(working_copy_filename)
    del img

## Method in charge of transforming a color image by sections
def colour_by_sections_RGB(working_copy_filename, array_points, array_slopes):
    sectionsLUT = make_sections_table(array_points, array_slopes)
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            gamma_valueR = round(sectionsLUT[pixs[i,j][0]])
            gamma_valueG = round(sectionsLUT[pixs[i,j][1]])
            gamma_valueB = round(sectionsLUT[pixs[i,j][2]])
            pixs[i,j] = (gamma_valueR, gamma_valueG, gamma_valueB)
    img.save(working_copy_filename)
    del img

## Method in charge of transforming a B&W image by sections
def colour_by_sections(working_copy_filename, array_points, array_slopes):
    sectionsLUT = make_sections_table(array_points, array_slopes)
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            gamma_value = round(sectionsLUT[pixs[i,j][0]])
            pixs[i,j] = (gamma_value, gamma_value, gamma_value)
    img.save(working_copy_filename)
    del img

## Method in charge of performing the equalization of an image
def colour_equalization(working_copy_filename, pixels_frequencies_abs, rgb):
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    width, height = img.size
    size = width * height
    equalizationLUT = make_equalization_table_RGB(pixels_frequencies_abs, size)
    if (rgb):
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                equalization_valueR = round(equalizationLUT[0][pixs[i,j][0]])
                equalization_valueG = round(equalizationLUT[1][pixs[i,j][1]])
                equalization_valueB = round(equalizationLUT[2][pixs[i,j][2]])
                pixs[i,j] = (equalization_valueR, equalization_valueG, equalization_valueB)
        img.save(working_copy_filename)
        del img
    else:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                equalization_value = round(equalizationLUT[0][pixs[i,j][0]])
                pixs[i,j] = (equalization_value, equalization_value, equalization_value)
        img.save(working_copy_filename)
        del img

def colour_equalization_BW(working_copy_filename, pixels_frequencies_abs, rgb):
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    width, height = img.size
    size = width * height
    equalizationLUT = make_equalization_table_BW(pixels_frequencies_abs, size)
    if (rgb):
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                equalization_valueR = round(equalizationLUT[0][pixs[i,j][0]])
                equalization_valueG = round(equalizationLUT[1][pixs[i,j][1]])
                equalization_valueB = round(equalizationLUT[2][pixs[i,j][2]])
                pixs[i,j] = (equalization_valueR, equalization_valueG, equalization_valueB)
        img.save(working_copy_filename)
        del img
    else:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                equalization_value = round(equalizationLUT[0][pixs[i,j][0]])
                pixs[i,j] = (equalization_value, equalization_value, equalization_value)
        img.save(working_copy_filename)
        del img

## Method responsible for specifying an image
def color_specification(working_copy_filename, pixel_frequency_wc_cum, pixel_frequency_si_cum, rgb):
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    if (rgb):
        specificationLUT = make_specification_table_RGB(pixel_frequency_wc_cum, pixel_frequency_si_cum)
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                specification_valueR = round(specificationLUT[0][pixs[i,j][0]])
                specification_valueG = round(specificationLUT[1][pixs[i,j][1]])
                specification_valueB = round(specificationLUT[2][pixs[i,j][2]])
                pixs[i,j] = (specification_valueR, specification_valueG, specification_valueB)
        img.save(working_copy_filename)
        img.show()
        del img
    else:
        specificationLUT = make_specification_table(pixel_frequency_wc_cum, pixel_frequency_si_cum)
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                specification_value = round(specificationLUT[0][pixs[i,j][0]])
                pixs[i,j] = (specification_value, specification_value, specification_value)
        img.save(working_copy_filename)
        img.show()
        del img

#############################################################################################
#############################################################################################
#############################################################################################

## Method in charge of performing the image transformation
## to a grayscale image
def horizontal_mirror(working_copy_filename):
    img = PIL.Image.open(working_copy_filename)
    result_img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    result_pixs = result_img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            result_pixs[i,  (img.size[1] - 1) - j] = pixs[i, j]
    result_img.save(working_copy_filename)
    del img

def vertical_mirror(working_copy_filename):
    img = PIL.Image.open(working_copy_filename)
    result_img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    result_pixs = result_img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            result_pixs[(img.size[0] - 1) - i, j] = pixs[i, j]
    result_img.save(working_copy_filename)
    del img

def trasp_mirror(working_copy_filename):
    img = PIL.Image.open(working_copy_filename)
    new_height,new_width = img.size
    result_img = PIL.Image.new(mode="RGB", size=(new_width, new_height))
    pixs = img.load()
    result_pixs = result_img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            result_pixs[j, i] = pixs[i, j]
    result_img.save(working_copy_filename)
    del img

def rotate(working_copy_filename, rotation_angle):
    rotation_times = int(int(rotation_angle) / 90)
    if (rotation_times < 0 ):
        if (rotation_times == -1):
            rotation_times = 3
        elif (rotation_times == -2):
            rotation_times = 2
        elif (rotation_times == -3):
            rotation_times = 1
    for times in range(rotation_times):
        img = PIL.Image.open(working_copy_filename)
        new_height,new_width = img.size
        result_img = PIL.Image.new(mode="RGB", size=(new_width, new_height))
        pixs = img.load()
        result_pixs = result_img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                result_pixs[(img.size[1] - 1) - j, i] = pixs[i, j]
        result_img.save(working_copy_filename)
    del img


def scale_vmp(working_copy_filename, new_width, new_height):
    new_width, new_height = int(new_width), int(new_height)
    img = PIL.Image.open(working_copy_filename)
    result_img = PIL.Image.new(mode="RGB", size=(new_width, new_height))
    pixs = img.load()
    result_pixs = result_img.load()
    original_width, original_height = img.size
    width_correlation = new_width / original_width
    height_correlation = new_height / original_height
    for i in range(result_img.size[0]):
        for j in range(result_img.size[1]):
            x_pos_translation = i / width_correlation
            y_pos_translation = j / height_correlation
            result_pixs[i,j] = pixs[int(np.floor(x_pos_translation)), int(np.floor(y_pos_translation))]
    result_img.save(working_copy_filename)
    del img    

def scale_bilineal(working_copy_filename, new_width, new_height):
    new_width, new_height = int(new_width), int(new_height)
    img = PIL.Image.open(working_copy_filename)
    old_width, old_height = img.size
    result_img = PIL.Image.new(mode="RGB", size=(new_width, new_height))
    pixs = img.load()
    result_pixs = result_img.load()
    width_correlation = new_width / old_width
    height_correlation = new_height / old_height
    P = []
    for i in range(result_img.size[0]):
        for j in range(result_img.size[1]):
            x_pos_translation = i / width_correlation # x
            y_pos_translation = j / height_correlation # y
            p, q = x_pos_translation - np.floor(x_pos_translation), y_pos_translation - np.floor(y_pos_translation)
            x_pos_translation = int(x_pos_translation)
            y_pos_translation = int(y_pos_translation)
            if (x_pos_translation == img.size[0] - 1):
                x_pos_translation = x_pos_translation - 1
                p = 0
            if (y_pos_translation == img.size[1] - 1):
                y_pos_translation = y_pos_translation - 1
                q = 0
            A = pixs[x_pos_translation, y_pos_translation + 1]
            B = pixs[x_pos_translation + 1, y_pos_translation + 1]        
            C = pixs[x_pos_translation, y_pos_translation]
            D = pixs[x_pos_translation + 1, y_pos_translation]
            for pos in range(3):
                Q = A[pos] + ((B[pos] - A[pos]) * p)
                R = C[pos] + ((D[pos] - C[pos]) * q)
                # pos_P = (C[pos] + ((D[pos] - C[pos]) * p) + ((A[pos] - C[pos]) * q) + ((B[pos] + C[pos] - A[pos] - D[pos]) * p * q))
                pos_P = R + ((Q - R) * q)
                P.append(int(pos_P))
            result_pixs[i, j] = (P[0], P[1], P[2])
            P.clear()
    result_img.save(working_copy_filename)
    del img 

def rotate_td(working_copy_filename, rotation_angle):
    img = PIL.Image.open(working_copy_filename)

    sinx = np.sin(int(rotation_angle))
    cosx = np.cos(int(rotation_angle))

    corner_E = (0,0)
    corner_F = (img.size[0] - 1, 0)
    corner_G = (img.size[0] - 1, img.size[1] - 1)
    corner_H = (0, img.size[1] - 1)

    new_corner_E = (int(corner_E[0]*cosx) - (corner_E[1]*sinx) , int(corner_E[0]*sinx) + (corner_E[1]*cosx))
    new_corner_F = (int(corner_F[0]*cosx) - (corner_F[1]*sinx) , int(corner_F[0]*sinx) + (corner_F[1]*cosx))
    new_corner_G = (int(corner_G[0]*cosx) - (corner_G[1]*sinx) , int(corner_G[0]*sinx) + (corner_G[1]*cosx))
    new_corner_H = (int(corner_H[0]*cosx) - (corner_H[1]*sinx) , int(corner_H[0]*sinx) + (corner_H[1]*cosx))

    max_x = max([new_corner_E[0], new_corner_F[0], new_corner_G[0], new_corner_H[0]])
    max_y = max([new_corner_E[1], new_corner_F[1], new_corner_G[1], new_corner_H[1]])
    min_x = min([new_corner_E[0], new_corner_F[0], new_corner_G[0], new_corner_H[0]])
    min_y = min([new_corner_E[1], new_corner_F[1], new_corner_G[1], new_corner_H[1]])

    new_size = (int(abs(np.ceil(max_x - min_x))), int(abs(np.ceil(max_y - min_y))))
    result_img = PIL.Image.new(mode="RGB",size= new_size)
    pixs = img.load()
    result_pixs = result_img.load()
    x_shift = max_x
    y_shift = max_y
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            new_i = (i*cosx) - (j*sinx) - x_shift
            new_j = (i*sinx) + (j*cosx) - y_shift
            result_pixs[new_i, new_j] = pixs[i, j]
    result_img.save(working_copy_filename)
    del img    

##############################################################################################

def rotate_ti(working_copy_filename, rotation_angle):
    img = PIL.Image.open(working_copy_filename)
    sinx = np.sin(np.deg2rad(int(rotation_angle)))
    cosx = np.cos(np.deg2rad(int(rotation_angle)))

    corner_E = (0,0)
    corner_F = (img.size[0] - 1, 0)
    corner_G = (img.size[0] - 1, img.size[1] - 1)
    corner_H = (0, img.size[1] - 1)

    new_corner_E = (corner_E[0]*cosx) - (corner_E[1]*sinx) , (corner_E[0]*sinx) + (corner_E[1]*cosx)
    new_corner_F = (corner_F[0]*cosx) - (corner_F[1]*sinx) , (corner_F[0]*sinx) + (corner_F[1]*cosx)
    new_corner_G = (corner_G[0]*cosx) - (corner_G[1]*sinx) , (corner_G[0]*sinx) + (corner_G[1]*cosx)
    new_corner_H = (corner_H[0]*cosx) - (corner_H[1]*sinx) , (corner_H[0]*sinx) + (corner_H[1]*cosx)

    max_x = max([new_corner_E[0], new_corner_F[0], new_corner_G[0], new_corner_H[0]])
    max_y = max([new_corner_E[1], new_corner_F[1], new_corner_G[1], new_corner_H[1]])
    min_x = min([new_corner_E[0], new_corner_F[0], new_corner_G[0], new_corner_H[0]])
    min_y = min([new_corner_E[1], new_corner_F[1], new_corner_G[1], new_corner_H[1]])

    new_size = (int(abs(np.ceil(max_x - min_x))), int(abs(np.ceil(max_y - min_y))))
    result_img = PIL.Image.new(mode="RGB",size= new_size)
    coordinate_matrix = PIL.Image.new(mode="RGB",size= new_size) 
    pixs = img.load()
    result_pixs = result_img.load()
    coordinate_matrix = coordinate_matrix.load()
    msinx = -1 * np.sin(np.deg2rad(int(rotation_angle)))
    mcosx = np.cos(np.deg2rad(int(rotation_angle)))
    fill_pix_counter = 0
    for indiceX in range(result_img.size[0]):
        for indiceY in range(result_img.size[1]):
            xprima = indiceX + min_x
            yprima = indiceY + min_y
            x = int((xprima * mcosx) - (yprima * msinx))
            y = int((xprima * msinx) + (yprima * mcosx))
            if ((x >= img.size[0]) or (y >= img.size[1]) or (x < 0) or (y < 0)):
                result_pixs[indiceX, indiceY] = (0, 0, 0)
                fill_pix_counter += 1 
            else:
                result_pixs[indiceX, indiceY] = pixs[x, y]
    result_img.save(working_copy_filename)
    del img
    return fill_pix_counter
