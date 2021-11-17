from tkinter import constants
import PIL.Image
import function
import numpy as np

def make_grayscale_table():
    grayscaleLUT = [
        [r * 0.299 for r in range(256)],
        [g * 0.587 for g in range(256)],
        [b * 0.114 for b in range(256)],
    ]
    return grayscaleLUT

def make_linearfit_table(brightness, contrast, new_brightness, new_contrast):
    brightness = round(float(brightness), 3)
    constants = round(float(contrast), 3)
    new_brightness = round(float(new_brightness), 3)
    new_contrast = round(float(new_contrast), 3)
    if (contrast == new_contrast):
        A = 1
    else:
        A = new_contrast / constants
    if (brightness == new_brightness):
        B = new_brightness - A * brightness
    else:
        B = new_brightness - A * brightness
    linearfitLUT = [
        [(r * A + B) for r in range(256)],
        [(g * A + B) for g in range(256)],
        [(b * A + B) for b in range(256)],
    ]
    return linearfitLUT

def make_gamma_table(gamma_value):
    gamma_value = round(float(gamma_value), 3)
    gammaLUT = [
        [(pow((r / 255), gamma_value) * 255)  for r in range(256)],
        [(pow((g / 255), gamma_value) * 255) for g in range(256)],
        [(pow((b / 255), gamma_value) * 255) for b in range(256)]
    ]
    return gammaLUT

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

def make_sections_table(array_points, array_slopes):
    array_points.pop(0)
    # sectionsLUT = []
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
    
    # for color in range(3):
    #     sectionsLUT.append(color_array_aux[color])
    return color_array_aux

def make_equalization_table(pixels_frequencies_abs, size):
    k_value = size / 256
    equalizationLUT = [
        [(max(0, round(pixels_frequencies_abs[0][r] / k_value) - 1)) for r in range(256)],
        [(max(0, round(pixels_frequencies_abs[1][g] / k_value) - 1)) for g in range(256)],
        [(max(0, round(pixels_frequencies_abs[2][b] / k_value) - 1)) for b in range(256)]
    ]
    return equalizationLUT

def make_specification_table(pixel_frequency_wc_cum, pixel_frequency_si_cum):
    #print(pixels_frequencies_si)
    specificationLUT = [c for c in range(256)]
    for color in range(256):
        fg1 = pixel_frequency_wc_cum[0][color]
        g2 =  function.find_closest_index(fg1, pixel_frequency_si_cum)
        specificationLUT[color] = g2
    # print(specificationLUT)
    return specificationLUT    



# Método encargado de realizar la transformación de la imagen
# a una imagen en escala de grises
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

def colour_to_linearlfit(working_copy_filename, brightness, contrast, new_brigthness, new_contrast):
    img  = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    linearfitLUT = make_linearfit_table(brightness, contrast, new_brigthness, new_contrast)
    if type(pixs[0,0]) == tuple: 
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
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                linearfit_valueR = linearfitLUT[0][pixs[i,j]]
                linearfit_valueB = linearfitLUT[2][pixs[i,j]]
                linearfit_valueR = round(linearfit_valueR)
                linearfit_valueB = round(linearfit_valueB)
                pixs[i,j] = linearfit_valueR
    img.save(working_copy_filename)
    del img


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

def colour_equalization(working_copy_filename, pixels_frequencies_abs, rgb):
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    width, height = img.size
    size = width * height
    equalizationLUT = make_equalization_table(pixels_frequencies_abs, size)
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

def color_specification(working_copy_filename, pixel_frequency_wc_cum, pixel_frequency_si_cum, rgb):
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    specificationLUT = make_specification_table(pixel_frequency_wc_cum, pixel_frequency_si_cum)
    if (rgb):
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                specification_valueR = round(specificationLUT[pixs[i,j][0]])
                specification_valueG = round(specificationLUT[pixs[i,j][1]])
                specification_valueB = round(specificationLUT[pixs[i,j][2]])
                pixs[i,j] = (specification_valueR, specification_valueG, specification_valueB)
        img.save(working_copy_filename)
        img.show()
        del img
    else:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                specification_value = round(specificationLUT[pixs[i,j][0]])
                pixs[i,j] = (specification_value, specification_value, specification_value)
        img.save(working_copy_filename)
        img.show()
        del img