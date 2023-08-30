import pygame, math
from GameData import WHITE, PROJECTILE_SIZE, screen


class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, damage):
        super().__init__()
        self.surf = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=start_pos)
        
        # Calcula a direção normalizada
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        self.direction = (dx/distance, dy/distance)

        self.damage = damage  # O dano é passado ao criar o projétil

    def update(self):
        self.rect.move_ip(self.direction[0]*10, self.direction[1]*10)
        if not screen.get_rect().colliderect(self.rect):
            self.kill()