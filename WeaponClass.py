import pygame, math
from GameData import *
ANIMATION_SPEED = 100

#Manutenção das armas
class Weapon:
    def __init__(self):
        self.last_attack_time = 0

    def attack(self, position, target_position):
        raise NotImplementedError()
    
    def can_attack(self, current_time):
        return current_time - self.last_attack_time > self.COOLDOWN

#Manutenção dos projéteis
class Projectile(pygame.sprite.Sprite):
    NEW_WIDTH = 12  # Substitua pelo valor desejado
    NEW_HEIGHT = 12
    def __init__(self, start_pos, target_pos, damage, weapon_type):
        super().__init__()
        self.surf = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=start_pos)
        self.weapon_type = weapon_type
        self.animation_time = pygame.time.get_ticks()
        self.current_sprite = 0

        # Direção do projétil
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        self.angle = math.degrees(math.atan2(-dy, dx))

        if weapon_type == 'Pistol':
            self.sprites = [
                pygame.transform.scale(pygame.image.load("texturas/sprites_walking/tiropistola_1.png").convert_alpha(), (15, 15)),
                pygame.transform.scale(pygame.image.load("texturas/sprites_walking/tiropistola_2.png").convert_alpha(), (15, 15))           
            ]

        elif weapon_type == 'Shotgun':
            self.sprites = [
                pygame.transform.scale(pygame.image.load("texturas/sprites_walking/tiro_12.png").convert_alpha(), (14, 12)),
            ]
        self.surf = self.sprites[0]  # Começa com a primeira sprite
        self.rect = self.surf.get_rect(center=start_pos)
        # Calcula a direção normalizada
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        self.direction = (dx/distance, dy/distance)

        self.damage = damage  # O dano é passado ao criar o projétil

    def update(self):
        # Animação
        if pygame.time.get_ticks() - self.animation_time > ANIMATION_SPEED:
            if self.weapon_type == 'Pistol':
                self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.surf = self.sprites[self.current_sprite]
            self.animation_time = pygame.time.get_ticks()
        self.rect.move_ip(self.direction[0]*10, self.direction[1]*10)

        # Orientação da sprite da Shotgun
        if self.weapon_type == 'Shotgun':
            # Suponha que você tem uma variável para a direção do projétil
            # e que você pode determinar se está indo para a direita.
            self.surf = pygame.transform.rotate(self.sprites[0], self.angle)
            self.rect = self.surf.get_rect(center=self.rect.center)
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

#Pistola
class Pistol(Weapon):
    DAMAGE = 1              # 1
    COOLDOWN = 500         # 1000 milissegundos = 1 segundo

    def attack(self, position, target_position):
        if self.can_attack(pygame.time.get_ticks()):
            self.last_attack_time = pygame.time.get_ticks()
            return [Projectile(position, target_position, damage=self.DAMAGE, weapon_type='Pistol')]
        return []

#Escopeta
class Shotgun(Weapon):
    PROJECTILE_COUNT = 5    # 5
    DAMAGE = 5              # 5
    COOLDOWN = 2000         # 2000 milissegundos = 2 segundos

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
                projectiles.append(Projectile(position, (position[0] + new_dir_x, position[1] + new_dir_y), damage=self.DAMAGE, weapon_type='Shotgun'))
                
        return projectiles
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Fist(Weapon):
    DAMAGE = 1
    RANGE = 50
    KNOCKBACK = 10
    COOLDOWN = 700

    def attack(self, position, target_position):
        if self.can_attack(pygame.time.get_ticks()):
            self.last_attack_time = pygame.time.get_ticks()
            dx = target_position[0] - position[0]
            dy = target_position[1] - position[1]

            distance = (dx**2 + dy**2)**0.5

            if distance <= self.RANGE:
                # Aqui você pode aplicar o dano e o knockback
                # Por exemplo: enemy.take_damage(self.DAMAGE)
                # Se desejar implementar o knockback, você pode alterar a posição do inimigo com base na direção do ataque.
                direction = (dx/distance, dy/distance)
                knockback_x = position[0] + direction[0] * self.KNOCKBACK
                knockback_y = position[1] + direction[1] * self.KNOCKBACK
                return True
            return False
