import pygame

from . import helper_func as hf


# map/tilemap is Game Object?
# if map/tilemap is Game Object it should be have a parent class GameObject
# however, the behavior of the map/tilemap with the GameObject class is very different. how to handle it?

class Map:
    def __init__(self, map, map_images, collide, position):
        self.size = (50, 50)
        self.map = self.json_to_charlist(map)
        self.images = self.load_map_images(map_images)
        self.imgs_collide = self.json_to_charlist(collide)
        self.position = position
        self.rects = []
    
    @staticmethod
    def json_to_charlist(file):
        return [char.split(",") for row in file for char in row]

    @staticmethod
    def generate_key(image):
        return "".join(char for char in image if char.isdecimal())
        
    def load_map_images(self, path):
        data = {}
        images = hf.search_png(path)
        for image in images:
            key = self.generate_key(image)

            data[key] = hf.load_image(f"{path}/{image}", self.size)
        
        return data
    
    def set_scroll(self, scroll):
        self.scroll = scroll

    def draw(self, screen):
        y = self.position[0]
        for row in self.map:
            x = self.position[1]
            for tile in row:
               screen.blit(self.images[tile], (x - self.scroll[0], y - self.scroll[1]))

               if tile in self.imgs_collide:
                   self.rects.append(pygame.Rect((x, y), self.size))
               
               x += self.size[0]

            y += self.size[1]