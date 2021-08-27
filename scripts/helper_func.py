import os
import math

import pygame


def search_png(path):
    return [image for image in os.listdir(path) if image.endswith(".png")]

def load_image(path, size):
    load = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(load, size)

    return image

def get_distance(obj, other):
    return math.hypot(other.x - obj.x, other.y - obj.y)