import random

import pygame

import helper_func as hf

from game_object import GameObject


class Hearth(GameObject):
    def __init__(self, position):
        path = "../assets/hearth/hearth_0.png"
        self.image = hf.load_image(path, (16, 16))
        self.health = 10
        self.vel = -5
        self.increase = random.choice([0.4, 0.6, 0.8])

        self.original_pos = position

        super().__init__(self.image, position)

    def jump(self):
        self.vel += self.increase

        if self.rect.y > self.original_pos[1]:
            self.vel = -5
        
        self.rect.y += self.vel

    def draw(self, screen):
        self.jump()
        screen.blit(self.image, self.position)