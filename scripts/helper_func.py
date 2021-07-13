import os
import math
import json

import pygame


def search_png(path):
    return [image for image in os.listdir(path) if image.endswith(".png")]

def load_image(path, size):
    load = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(load, size)

    return image

def load_json(path):
    with open(path, "r") as f:
        file = json.load(f)
        return file

def get_value_json(key):
    return [value for value in key.keys()]

def get_distance(obj, other):
    return math.hypot(other.x - obj.x, other.y - obj.y)