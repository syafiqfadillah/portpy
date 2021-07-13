import pygame
from pygame.constants import SCRAP_CLIPBOARD

import animations as a

import helper_func  as hf


class GameObject:
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect(center=position)
    
    def set_scroll(self, scroll):
        self.scroll = scroll

    def update(self):
        self.position = (self.rect.x - self.scroll[0], self.rect.y - self.scroll[1])

    def draw(self, screen):
        screen.blit(self.image, self.position) 


class Puzzles(GameObject):
    def __init__(self, position):
        self.anim = a.Animations((32, 32))
        self.anim.load_animations("lock", "../assets/puzzles/lock", 8)
        self.anim.load_animations("unlock", "../assets/puzzles/unlock", 30, loop=False)

        self.anim.set_state("lock")

        super().__init__(self.anim.animations_db[self.anim.state][0], position)

    def collected(self):
        self.anim.set_state("unlock")

        if self.anim.end_frame():
            return True

        return False

    def draw(self, screen):
        self.anim.play(screen, self.position)
