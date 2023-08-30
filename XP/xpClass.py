import pygame
from GameData import *

class ExperiencePoint(pygame.sprite.Sprite):
    def __init__(self, pos, value=1):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((BLUE))  # Azul
        self.rect = self.surf.get_rect(center=pos)
        self.value = value
        
class ExperienceBar:
    def __init__(self):
        self.level = 0
        self.exp = 0

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= 10:
            self.exp -= 10
            self.level_up()

    def level_up(self):
        self.level += 1
        # Aqui você pode adicionar o código para mostrar as opções de nível

    def draw(self, surface):
        pygame.draw.rect(
            surface, BLUE, 
            (10, 0, self.exp * SCREEN_WIDTH // 10, 20)
        )