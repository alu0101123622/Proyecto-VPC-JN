import PIL.Image

def color_array():
    array = []
    array.append(0)
    color = -1
    for color in range(255):
        array.append(color + 1)
    return array

def make_grayscale_table():
    color_array()
    table = []
    for color in len(color_array()):
      print("adios")

# Método encargado de realizar la transformación de la imagen
# a una imagen en escala de grises
def colour_to_grayscale(working_copy_filename):
    #make_grayscale_table()
    img = PIL.Image.open(working_copy_filename)
    pixs = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            grey_value = round(0.222 * pixs[i,j][0] + 0.707 * pixs[i,j][1] + 0.071 * pixs[i,j][2])
            pixs[i,j] = (grey_value, grey_value, grey_value)
    img.save(working_copy_filename)
    del img