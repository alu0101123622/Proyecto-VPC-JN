"""
    Universidad de La Laguna - Grado en Ingenería Informática
    Cuarto Curso - Visión por Computador
    2021-2022

    Autores:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    Fichero main.py: Programa principal del proyecto
"""
from typing import Tuple
import PIL.Image

# Método encargado de obtener los valores de las imágenes
# de width y heigth
def get_pixel_values(filename):
    img = PIL.Image.open(filename, 'r')
    width, height = img.size
    pixel_values = list(img.getdata())
    print('Los datos de la imagen son widht: %s, height: %s' % (str(width), str(height)))
    #print(pixel_values)
    del img
    return pixel_values
##¡ Método que calcula la precuencia de los colores de la imagen
def frequency(pixel_values):
    grey_pix_freq =  {}
    red_pix_freq =   {}
    green_pix_freq = {}
    blue_pix_freq =  {}
    print(type(pixel_values[0]))
    if type(pixel_values[0]) == tuple:   # Imagen a color
      # Para el rojo
      for pixel in pixel_values:
          if pixel[0] in red_pix_freq:
              red_pix_freq[pixel[0]] += 1
          else:
              red_pix_freq[pixel[0]] = 1
      for pixel in sorted(red_pix_freq):
          print(f'{pixel}: {red_pix_freq[pixel]}')
      # Para el verde
      for pixel in pixel_values:
          if pixel[1] in green_pix_freq:
              green_pix_freq[pixel[1]] += 1
          else:
              green_pix_freq[pixel[1]] = 1
      for pixel in sorted(green_pix_freq):
          print(f'{pixel}: {green_pix_freq[pixel]}')
      # Para el blue
      for pixel in pixel_values:
          if pixel[2] in blue_pix_freq:
              blue_pix_freq[pixel[2]] += 1
          else:
              blue_pix_freq[pixel[2]] = 1
      for pixel in sorted(blue_pix_freq):
          print(f'{pixel}: {blue_pix_freq[pixel]}')
      return red_pix_freq, green_pix_freq, blue_pix_freq
    else:                                           # Imagen a B&W
      for pixel in pixel_values:
          if pixel in grey_pix_freq:
              grey_pix_freq[pixel] += 1
          else:
              grey_pix_freq[pixel] = 1
      for pixel in sorted(grey_pix_freq):
          print(f'{pixel}: {grey_pix_freq[pixel]}')
      return grey_pix_freq 
