import math
import pygame

screen = pygame.display.set_mode((800,600))

# In main while loop: a degree counter and speed variable
def circular(origin,angle:float,radius:float):
    x = origin[0] + math.cos(math.radians(angle))*radius
    y = origin[1] + math.sin(math.radians(angle))*radius
    return x,y

# In main while loop: a degree counter and speed variable
def sine_movement(angle:float,min:float,max:float):
    scale = (max-min)/2
    x = scale*math.sin(math.radians(angle))+min+scale
    return x