import pygame, random

PARTICLES = pygame.sprite.Group()

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image_list = [
            pygame.image.load("texturas/particulas/folha1.png").convert_alpha(),
            pygame.image.load("texturas/particulas/folha2.png").convert_alpha(),
            pygame.image.load("texturas/particulas/folha3.png").convert_alpha(),
            pygame.image.load("texturas/particulas/folha4.png").convert_alpha(),
        ]
        self.image = random.choice(self.image_list)
        self.rect = self.image.get_rect(center=pos)
        self.alpha = 255  # Inicialmente completamente opaco
        self.angle = random.randint(0, 360)  # Rotação aleatória inicial
        self.image = pygame.transform.rotate(self.image, self.angle)
        
    def update(self):
        self.alpha -= 5  # Valor de 5 define a velocidade de desaparecimento. Ajuste conforme necessário.
        if self.alpha <= 0:  # Se a partícula estiver completamente transparente, remova-a
            self.kill()
            return
        temp_surf = self.image.copy()
        temp_surf.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
        self.image = temp_surf