import pygame

from . import helper_func as hf
from .game_object import GameObject


class Map(GameObject):
    def __init__(self, map, map_images, collide, position):
        self.size = (50, 50)
        self.map = hf.json_to_charlist(map)
        self.images = self.load_map_images(map_images)
        self.imgs_collide = hf.json_to_charlist(collide)
        self.position = position
        self.rects = self.set_rects()
        
    def load_map_images(self, path):
        data = {}
        images = hf.search_png(path)
        for image in images:
            key = hf.generate_key(image)

            data[key] = hf.load_image(f"{path}/{image}", self.size)
        
        return data

    def get_rects(self):
        return self.rects

    def set_rects(self):
        rects = []
        for rect in self.map:
            for collide in self.imgs_collide:
                if collide in rect:
                    rects.append(collide)

        return rects

    def update(self):
        self.draw_tile = {}
        y = self.position[0]
        key = 0
        for row in self.map:
            x = self.position[1]
            for tile in row:
                self.draw_tile[key] = [self.images[tile], x - self.scroll[0], y - self.scroll[1]]
               
                x += self.size[0]
                key += 1

            y += self.size[1]


    def draw(self, screen):
        for tile in self.draw_tile.keys():
            screen.blit(self.draw_tile[tile][0], (self.draw_tile[tile][1], self.draw_tile[tile][2]))