import pygame

from .colors import Colors


class HealthBar:
    def __init__(self, width, position):
        width = width//3
        height = 5
        self.health = pygame.Rect(position, (width, height))
        self.red_bar = pygame.Rect(position, (width, height))

    def get_health(self):
        return self.health.width
    
    def get_bar_width(self):
        return self.red_bar.width
    
    def increase(self, value):
        self.health.width += value

    def decrease(self, value):
        self.health.width -= value

    def update(self, position):
        self.health.x = position[0] + 23
        self.health.y = position[1] + 19
        self.red_bar.x = self.health.x
        self.red_bar.y = self.health.y

    def draw(self, screen):
        pygame.draw.rect(screen, Colors.RED, self.red_bar)
        pygame.draw.rect(screen, Colors.GREEN, self.health)
