from tkinter import constants
import PIL.Image
import function

def make_grayscale_table():

    grayscaleLUT = [
        [r * 0.299 for r in range(256)],
        [g * 0.587 for g in range(256)],
        [b * 0.114 for b in range(256)],
    ]
    return grayscaleLUT

def make_linearfit_table(brightness, contrast, new_brightness, new_contrast):
    if (constants == new_contrast):
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

def make_equalization_table(frequency):
    # FORMULA: vout = max(0, round[(ho(Vin)/size)*M]-1)
    print(frequency)

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
            #grey_value = round(0.222 * pixs[i,j][0] + 0.707 * pixs[i,j][1] + 0.071 * pixs[i,j][2])
                grey_value += grayscaleLUT[k][pixs[i,j][k]]
                grey_value = round(grey_value)
            pixs[i,j] = (grey_value, grey_value, grey_value)
            grey_value = 0
    img.save(working_copy_filename)
    del img

def colour_to_linearlfit(working_copy_filename, pixels):
    img  = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    brightness = function.brightness(working_copy_filename.size, pixels)
    contrast = function.contrast(working_copy_filename.size, pixels)
    linearfitLUT = make_linearfit_table(brightness, contrast, 150, 50)
    linearfit_value = 0
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            for k in range(3):
                linearfit_value += linearfitLUT[k][pixs[i,j][k]]
                linearfit_value = round(linearfit_value)
            pixs[i,j] = (linearfit_value, linearfit_value, linearfit_value)
            linearfit_value = 0
    img.save(working_copy_filename)
    del img
