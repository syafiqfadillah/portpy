import os

import pygame

from . import helper_func as hf


class Animations:
    def __init__(self, size):
        self.size = size
        self.frame = 0
        self.animations_loop = []
        self.animations_db = {}

    def load_images(self, path):
        images = []
        
        images_dir = hf.search_png(path)
        for image in images_dir:
            load = hf.load_image(f"{path}/{image}", self.size)

            images.append(load)

        return images

    def load_animations(self, name, images, frame_durations, loop=True):
        images = self.load_images(images)

        if loop:
            self.animations_loop.append(name)

        data = []
        for image in range(len(images)):
            for _ in range(frame_durations):
                data.append(images[image])

        self.animations_db[name] = data

    def set_state(self, new_state):
        self.state = new_state
    
    def end_frame(self):
        return self.frame >= len(self.animations_db[self.state])

    def frame_control(self):
        if self.end_frame():
            self.frame = 0 if self.state in self.animations_loop else len(self.animations_db[self.state])

    def frame_increase(self):
        self.frame += 1

    def play(self, screen, position):
        self.frame_increase()
        self.frame_control()
        screen.blit(self.animations_db[self.state][self.frame-1], position)

    
class EntityAnimations(Animations):
    def __init__(self):
        super().__init__((80, 80))

    def die_change_state(self):
        self.set_state("die")

    def attack_change_state(self):
        if self.state in ("idle left", "walk left"):
            self.set_state("attack left")
        elif self.state in ("idle right", "walk right"):
            self.set_state("attack right")

    def walk_change_state(self):
        if self.state in ("idle left", "attack left"):
            self.set_state("walk left")
        elif self.state in ("idle right", "attack right"):
            self.set_state("walk right")

    def idle_change_state(self):
        if self.state in ("walk right", "attack right"):
            self.set_state("idle right")
        elif self.state in ("walk left", "attack left"):
            self.set_state("idle left")
