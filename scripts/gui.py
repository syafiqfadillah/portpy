import random

import pygame

from .colors import Colors


class Text:
    def __init__(self, text, size, position):
        self.font = pygame.font.Font("assets/font/ARCADECLASSIC.TTF", size)
        self.text = text
        self.rect = pygame.Rect(position, (size, size))

    def draw(self, screen):
        screen.blit(self.font.render(self.text, True, Colors.WHITE), (self.rect.x, self.rect.y))


class Score(Text):
    def __init__(self, collected, limit, size, position):
        self.limit = limit
        super().__init__(f"{collected}/{limit}", size, position)
    
    def get_limit(self):
        return int(self.limit)
    
    def set_score(self, score):
        self.text = f"{score}/{self.limit}"


class BounceText(Text):
    def __init__(self, text, size, position):
        super().__init__(self, text, size, position)
        self.position = position
        self.velocity = -9
        self.x_movement = random.randint(-3, 3)

    def bounce(self):
        if self.velocity < self.rect.y:
            self.rect.x += self.x_movement
            self.velocity += 0.8

        self.rect.y += self.velocity

    def gone(self):
        return self.rect.y > self.position[1]+5


class Button:
    def __init__(self, texts, position):
        self.position = pygame.math.Vector2(position)
        self.rect = pygame.Rect(self.position, (60, 50))
        self.text_pos = (self.rect.centerx-20, self.rect.centery-15)
        self.text = Text(texts, 20, self.text_pos)
    
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.RED, self.rect)
        self.text.draw(screen)