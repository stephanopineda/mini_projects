'''
Create a module name geometry
Add a function named area_of_rectangle that takes length and breadth as input and returns the area of a rectangle.
Add a function named area_of_circle that takes radius as input and returns the area of a circle.
Modify the __init__.py to include this module.
Import and test the function area_of_circle from python terminal.
'''
from math import pi

def area_of_rectangle(length, breadth):
    return length * breadth

def area_of_circle(radius):
    return pi * radius ** 2
