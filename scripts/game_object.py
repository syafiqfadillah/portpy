import random

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
