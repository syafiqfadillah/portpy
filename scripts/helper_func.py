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

def get_distance(obj, other):
    return math.hypot(other.x - obj.x, other.y - obj.y)

def json_to_charlist(file):
    return [char.split(",") for row in file for char in row] if file else []

def generate_key(image):
    return "".join(char for char in image if char.isdecimal())

def load_json(path):
    with open(path, "r") as f:
        file = json.load(f)
        return file

def check_value_type(data):
    return dict() if not data else data