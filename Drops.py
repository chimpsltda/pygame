import pygame

def adjust_dropped_items_positions(dropped_items):
    for i in range(len(dropped_items)):
        for j in range(i+1, len(dropped_items)):
            item1 = dropped_items[i]
            item2 = dropped_items[j]
            
            while pygame.sprite.collide_rect(item1, item2):
                # Move item1 para a esquerda e item2 para a direita
                item1.rect.x -= 1
                item2.rect.x += 1
                
                # Move item1 para cima e item2 para baixo
                item1.rect.y -= 1
                item2.rect.y += 1

class Capacitor(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.name = "Capacitor"
        self.surf = pygame.image.load('texturas/Capacitor.png')
        self.rect = self.surf.get_rect(center=position)
    def render(self, screen):
        screen.blit(self.surf, self.rect)