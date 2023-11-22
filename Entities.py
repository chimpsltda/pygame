import pygame, random, time
from GameData import *
from xpClass import ExperiencePoint
from Drops import Capacitor
from math import atan2, degrees

class Objective(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((OBJECTIVE_SIZE, OBJECTIVE_SIZE))
        self.surf.fill(YELLOW)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.start_time = None

    def update(self, player_rect):
        if self.rect.colliderect(player_rect):
            if self.start_time is None:
                self.start_time = time.time()
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= OBJECTIVE_TIME:
                self.kill()
            else:
                progress = elapsed_time / OBJECTIVE_TIME
                pygame.draw.rect(
                    self.surf, GREEN, 
                    (0, 0, progress * OBJECTIVE_SIZE, 5)
                )
        else:
            self.start_time = None
            self.surf.fill(YELLOW)

class ChasingEnemy(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        # Carrega as duas sprites
        self.sprites = {
            "sprite1": pygame.transform.scale(
                pygame.image.load("texturas/sprites_walking/amarelo1.png").convert_alpha(),
                (30,21)  # Novas dimensões da sprite
            ),
            "sprite2": pygame.transform.scale(
                pygame.image.load("texturas/sprites_walking/amarelo2.png").convert_alpha(),
                (30, 20)  # Novas dimensões da sprite
            )
        }
        # Inicializa a sprite atual
        self.current_sprite = self.sprites["sprite1"]
        self.rect = self.current_sprite.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.health = 5
        self.target = target
        self.animation_time = 0
        self.animation_interval = 500
        self.surf = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.surf.fill((255, 165, 0))  # Laranja
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.health = 5
        self.target = target

    def take_damage(self, damage):
        self.health -= damage
        self.damage_text = str(damage)
        self.damage_time = pygame.time.get_ticks()
        dropped_items = []
        if self.health <= 0:
            self.kill()
            exp_points = ExperiencePoint(self.rect.center, 2)
            dropped_items.append(exp_points)
        return dropped_items  # Cria um ExperiencePoint com um valor de 2

    def draw_health_bar(self, surface):
        pygame.draw.rect(
            surface, GREEN,
            (self.rect.x, self.rect.y - 10, self.health * ENEMY_SIZE // 10, 5)
        )

    def update(self):
        # Direção do inimigo ao jogador
        direction_vector = pygame.math.Vector2(self.target.rect.centerx - self.rect.centerx,
                                               self.target.rect.centery - self.rect.centery)
        if direction_vector.length() > 0:
            direction_vector.normalize_ip()

        # Calcular o ângulo entre a direção e a horizontal
        angle = degrees(atan2(direction_vector.y, direction_vector.x))

        # Rotacionar a sprite atual em torno do centro
        self.surf = pygame.transform.rotate(self.current_sprite, -angle + 90)  # +90 para corrigir a orientação da sprite
        self.rect = self.surf.get_rect(center=self.rect.center)  # Atualiza o rect para o novo surf

        # Mover o inimigo na direção do jogador
        self.rect.move_ip(direction_vector.x * VELOCICADE_PERSEGUIDOR, direction_vector.y * VELOCICADE_PERSEGUIDOR)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.down_sprites = [
        pygame.image.load("texturas/sprites_walking/red_frente1.png").convert_alpha(),
        pygame.image.load("texturas/sprites_walking/red_frente2.png").convert_alpha(),
        pygame.image.load("texturas/sprites_walking/red_frente3.png").convert_alpha(),
        pygame.image.load("texturas/sprites_walking/red_frente2.png").convert_alpha()
        ]
        
        # Definindo as sprites para movimento lateral
        self.left_sprites = [
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_lado1.png").convert_alpha(), (34, 38)),
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_lado2.png").convert_alpha(), (34, 36)),
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_lado3.png").convert_alpha(), (34, 34)),
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_lado2.png").convert_alpha(), (34, 36))
        ]

        # Definindo as sprites para movimento de baixo para cima
        self.up_sprites = [
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_baixocima1.png").convert_alpha(), (34,38)),
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_baixocima2.png").convert_alpha(), (34,36)),
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_baixocima3.png").convert_alpha(), (34,34)),
        pygame.transform.scale(pygame.image.load("texturas/sprites_walking/red_baixocima2.png").convert_alpha(), (34,36))
        ]

        self.right_sprites = [pygame.transform.flip(sprite, True, False) for sprite in self.left_sprites]
        ANIMATION_SPEED = 300  # Define a velocidade de animação. Menor é mais rápido.
        self.current_sprite = 0
        self.animation_time = pygame.time.get_ticks()
        self.surf = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.surf.fill(RED)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.vida_maxima = 10
        self.health = 10
        self.damage_text = None
        self.damage_time = None
        if self.direction == 'up':
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(0, SCREEN_WIDTH),
                    SCREEN_HEIGHT + 20
                )
            )
        elif self.direction == 'down':
            self.rect = self.surf.get_rect(
                center = (
                    random.randint(0, SCREEN_WIDTH),
                    -20
                )
            )
        elif self.direction == 'left':
            self.rect = self.surf.get_rect(
                center = (
                    SCREEN_WIDTH + 20,
                    random.randint(0, SCREEN_HEIGHT)
                )
            )
        else:  # right
            self.rect = self.surf.get_rect(
                center = (
                    -20,
                    random.randint(0, SCREEN_HEIGHT)
                )
            )

    def take_damage(self, damage):
        self.health -= damage
        self.damage_text = str(damage)
        self.damage_time = pygame.time.get_ticks()
        dropped_items = []  # Lista para armazenar os itens dropados
        if self.health <= 0:
            self.kill()
            # Sempre dropa um ponto de experiência
            exp_point = ExperiencePoint(self.rect.center)
            dropped_items.append(exp_point)
        
            # 25% de chance de dropar um Capacitor
            if random.random() < 0.25:
                capacitor = Capacitor(self.rect.center)
                dropped_items.append(capacitor)
        return dropped_items
  
    def update(self):
        ANIMATION_SPEED = 300
        current_time = pygame.time.get_ticks()
        # Animação para movimento lateral
        if self.direction == 'left':
            if pygame.time.get_ticks() - self.animation_time > ANIMATION_SPEED:
                self.surf = self.left_sprites[self.current_sprite]
                self.current_sprite = (self.current_sprite + 1) % len(self.left_sprites)
                self.animation_time = pygame.time.get_ticks()
        elif self.direction == 'right':
            if pygame.time.get_ticks() - self.animation_time > ANIMATION_SPEED:
                self.surf = self.right_sprites[self.current_sprite]
                self.current_sprite = (self.current_sprite + 1) % len(self.right_sprites)
                self.animation_time = pygame.time.get_ticks()        
        # Animação para movimento de baixo para cima
        if self.direction == 'up':
            if pygame.time.get_ticks() - self.animation_time > ANIMATION_SPEED:
                self.surf = self.up_sprites[self.current_sprite]
                self.current_sprite = (self.current_sprite + 1) % len(self.up_sprites)
                self.animation_time = pygame.time.get_ticks()
        if self.direction == 'up':
            self.rect.move_ip(0, -ENEMY_SPEED)
        elif self.direction == 'down':
            if current_time - self.animation_time > ANIMATION_SPEED:
                self.surf = self.down_sprites[self.current_sprite]
                self.current_sprite = (self.current_sprite + 1) % len(self.down_sprites)
                self.animation_time = current_time
        self.rect.move_ip(0, ENEMY_SPEED)       
        if self.direction == 'up':
            self.rect.move_ip(0, -ENEMY_SPEED)
        elif self.direction == 'down':
            self.rect.move_ip(0, ENEMY_SPEED)
        elif self.direction == 'left':
            self.rect.move_ip(-ENEMY_SPEED, 0)
        else:  # right
            self.rect.move_ip(ENEMY_SPEED, 0)

        if self.rect.top > SCREEN_HEIGHT + 20 or self.rect.bottom < -20 or self.rect.left > SCREEN_WIDTH + 20 or self.rect.right < -20:
            self.kill()
        
        if self.damage_time and pygame.time.get_ticks() - self.damage_time > 1000:
            self.damage_text = None
    
    def draw_health_bar(self, surface): #Barras de vida dos inimigos
        health_bar_image = pygame.image.load('texturas/Barra_de_vida.png').convert_alpha()
        health_bar_image = pygame.transform.scale(health_bar_image, (ENEMY_SIZE*1.5, ENEMY_SIZE*1.5))
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y - 10

        health_bar_width = self.health * ENEMY_SIZE // 10
        health_bar_rect = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, 5)
        porcentagem_de_vida = (self.health / self.vida_maxima) * 100
        if porcentagem_de_vida >= 70:
            pygame.draw.rect(surface, GREEN, health_bar_rect)
        elif 70 >= porcentagem_de_vida >= 30:
            pygame.draw.rect(surface, YELLOW, health_bar_rect)
        else:
            pygame.draw.rect(surface, RED, health_bar_rect)

        offset_x = 5
        offset_y = 12

        surface.blit(health_bar_image, (health_bar_x - offset_x, health_bar_y - offset_y))

        if self.damage_text:
            font = pygame.font.Font(None, 20)
            text = font.render(self.damage_text, 1, WHITE)
            surface.blit(text, (self.rect.x, self.rect.y - 20))