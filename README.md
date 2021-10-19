# Proyecto-VPC-JN

Repositorio en el que se ubica el código y pruebas de mla primera práctica de la asignatura de Visión por Computador.
Trabajaremos con: <https://pysimplegui.readthedocs.io/en/latest/> seguir tutorial de instalación para Python 3.

> 19/10/2021

Lo primero que he hecho ha sido cambiar el tema:

```python
sg.theme('Dark Grey 3')
```

Ademas he editado el código base para conseguir que en lugar de toda la ruta solo se mostrara el nombre de la imagen abierta:

```python
shortname = values['-FILE LIST-'][0] 
```

Para evitar que el tamaño y posición de la ventana cambien en función del tamaño original de cada imagen, definí el tamaño estándar de 1080x720 pixeles, aún así, se le sigue dando la opción al usuario de cambiar el tamaño de la imagen al que desee:

![Resize option](https://gyazo.com/7925e99d122ba0e224513a1edd0663e7)

