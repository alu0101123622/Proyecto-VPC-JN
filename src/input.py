"""
    University of La Laguna - Degree in Computer Engineering
    Fourth grade - Computer vision
    2021-2022

    Authors:    Jorge Acevedo de León       -   alu0101123622@ull.edu.es
                Nerea Rodríguez Hernández   -   alu0101215693@ull.edu.es
    
    File input.py: Input functions are implemented.
"""
import pyautogui

## Method in charge of verifying that the cursor is over the image
def is_cursor_over_image(img_x_pos , img_y_pos, img_height, img_width):
    cursor_pos = pyautogui.position()
    if (img_x_pos <= cursor_pos[0] <= (img_x_pos + img_width)):
        if(img_y_pos <= cursor_pos[1] <= (img_y_pos + img_height)):
            return 1
    return 0

## Method responsible for returning the cursor position
def cursor_image_pos(img_x_pos , img_y_pos):
    cursor_pos = pyautogui.position()
    x = cursor_pos[0] - img_x_pos
    y = cursor_pos[1] - img_y_pos
    return ([x, y])

## Method in charge of calculating the position of the cursor image for rectangle
def cursor_image_pos_for_rectangle(img_x_pos , img_y_pos):
    cursor_pos = pyautogui.position()
    x = cursor_pos[0] - img_x_pos
    y = cursor_pos[1] - img_y_pos
    return (x, y)
