import pygame, math
from Armas.WeaponClass import Weapon
from Armas.ProjectileClass import Projectile
from GameData import SCREEN_HEIGHT, SCREEN_WIDTH

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