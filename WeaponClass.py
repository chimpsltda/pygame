import pygame, math
from GameData import *

#Manutenção das armas
class Weapon:
    def __init__(self):
        self.last_attack_time = 0

    def attack(self, position, target_position):
        raise NotImplementedError()

    def can_attack(self, current_time):
        raise NotImplementedError()
    
#Manutenção dos projéteis
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

#Pistola
class Pistol(Weapon):
    DAMAGE = 3
    COOLDOWN = 300  # 1000 milissegundos = 1 segundo

    def attack(self, position, target_position):
        # Cria um projétil se estiver fora do cooldown
        if self.can_attack(pygame.time.get_ticks()):
            self.last_attack_time = pygame.time.get_ticks()
            return [Projectile(position, target_position, damage=self.DAMAGE)]
        return []

    def can_attack(self, current_time):
        return current_time - self.last_attack_time > self.COOLDOWN

#Escopeta
class Shotgun(Weapon):
    PROJECTILE_COUNT = 5
    DAMAGE = 5
    COOLDOWN = 3000  # 3000 milissegundos = 3 segundos

    def attack(self, position, target_position):
        projectiles = []
        if self.can_attack(pygame.time.get_ticks()):
            self.last_attack_time = pygame.time.get_ticks()
        
            # Calcula a direção principal
            dir_x = target_position[0] - position[0]
            dir_y = target_position[1] - position[1]
            magnitude = math.sqrt(dir_x**2 + dir_y**2)
            dir_x /= magnitude
            dir_y /= magnitude
            
            # Calcula o ângulo principal do tiro
            main_angle = math.atan2(dir_y, dir_x)
            
            # Calcula o desvio entre os projéteis
            spread = math.radians(45)  # Define a dispersão total (neste caso, 45 graus)
            angle_step = spread / (self.PROJECTILE_COUNT - 1)
            
            # Calcula o ângulo inicial (meio para a esquerda)
            start_angle = main_angle - (spread / 2.0)
            
            for i in range(self.PROJECTILE_COUNT):
                # Calcula a direção x e y para este projétil
                new_dir_x = math.cos(start_angle + i * angle_step)
                new_dir_y = math.sin(start_angle + i * angle_step)
                
                # Multiplica pela velocidade ou magnitude desejada, se necessário
                speed = 10  # Defina a velocidade que desejar aqui
                new_dir_x *= speed
                new_dir_y *= speed
                
                # Cria o projétil com a nova direção
                projectiles.append(Projectile(position, (position[0] + new_dir_x, position[1] + new_dir_y), damage=self.DAMAGE))
                
        return projectiles

    def can_attack(self, current_time):
        return current_time - self.last_attack_time > self.COOLDOWN
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

