import PIL.Image

def make_grayscale_table():
    grayscaleLUT = [
        [r * 0.299 for r in range(256)],
        [g * 0.587 for g in range(256)],
        [b * 0.114 for b in range(256)],
    ]
    return grayscaleLUT

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