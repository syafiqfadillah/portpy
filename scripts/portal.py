import pygame

import animations as a

from game_object import GameObject


class Portal(GameObject):
    def __init__(self, position):
        self.anim = a.Animations((100, 100))
        open_path = "../assets/portal/open"
        self.anim.load_animations("open", open_path, 8, loop=False)
        idle_path = "../assets/portal/idle"
        self.anim.load_animations("idle", idle_path, 8, loop=True)
        
        self.anim.set_state("open")

        super().__init__(self.anim.animations_db[self.anim.state][0], position)
    
    def idle(self):
        if self.anim.end_frame():
            self.anim.set_state("idle")

    def draw(self, screen):
        self.anim.play(screen, self.position)

        self.idle()