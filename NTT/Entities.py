import pygame, math, random, time
from Armas.PistolClass import Pistol
from Armas.ShotgunClass import Shotgun
from GameData import *
from XP.xpClass import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        scale_factor = 0.7  # Reduzir o tamanho para 70% do original

         # Para a sprite parada
        self.original_surf = pygame.image.load("sprites_walking/sprite_parado.png").convert_alpha()
        self.original_surf = pygame.transform.scale(self.original_surf, (int(70 * scale_factor), int(70 * scale_factor)))
        self.surf = self.original_surf.copy()

        # Para as sprites de caminhada
        self.walk1_surf = pygame.transform.scale(pygame.image.load("sprites_walking/sprite_walk1.png").convert_alpha(), (int(70 * scale_factor), int(70 * scale_factor)))
        self.walk2_surf = pygame.transform.scale(pygame.image.load("sprites_walking/sprite_walk2.png").convert_alpha(), (int(70 * scale_factor), int(70 * scale_factor)))
        
        self.surf = self.original_surf
        
        
        
        self.walking = False
        self.walk_count = 0  # Para controlar a alternância entre walk1 e walk2

        self.rect = self.surf.get_rect(center = (1280/2, 720/2))
        self.health = 1
        self.damage = 1
        self.armas = [Pistol(), Shotgun()]
        self.arma_atual = 0
        self.speed = PLAYER_SPEED

        # Ajustar a área de colisão do jogador para ser menor
        collision_reduction = 0.10  # Reduzir a área de colisão para 70% do tamanho original
        new_width = self.rect.width * collision_reduction
        new_height = self.rect.height * collision_reduction
        self.rect.inflate_ip(-new_width, -new_height)

    def update(self, pressed_keys):
    # Primeiro, vamos determinar se o jogador está se movendo ou não
        prev_position = self.rect.topleft
        if pressed_keys[pygame.K_w]:
            self.rect.move_ip(0, -PLAYER_SPEED)
        if pressed_keys[pygame.K_s]:
            self.rect.move_ip(0, PLAYER_SPEED)
        if pressed_keys[pygame.K_a]:
            self.rect.move_ip(-PLAYER_SPEED, 0)
        if pressed_keys[pygame.K_d]:
            self.rect.move_ip(PLAYER_SPEED, 0)

        if self.rect.topleft != prev_position:  # Se o jogador se moveu
            self.walking = True
        else:
            self.walking = False
    
        # Atualizar a sprite com base no movimento
        if self.walking:
            if self.walk_count < 5:  # Vamos mudar a sprite a cada 5 chamadas do update. Você pode ajustar este valor.
                self.surf = self.walk1_surf
            else:
                self.surf = self.walk2_surf

        # Resetar walk_count após atingir um certo valor
            self.walk_count = (self.walk_count + 1) % 10
        else:
            self.surf = self.original_surf

        # Mantém o jogador na tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Rotaciona a sprite para olhar na direção do mouse
        mx, my = pygame.mouse.get_pos()
        rel_x, rel_y = mx - self.rect.centerx, my - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.surf = pygame.transform.rotate(self.surf, int(angle-90))
        self.rect = self.surf.get_rect(center=self.rect.center)

        # Centralizar o rect
        self.rect.center = (self.rect.centerx, self.rect.centery)       

    def change_weapon(self, weapon_index):
        self.arma_atual = weapon_index
        self.damage = self.armas[self.arma_atual].DAMAGE
        
    def get_new_weapon(self, weapon):
        self.armas.append(weapon)

    def attack(self, target_position):
        return self.armas[self.arma_atual].attack(self.rect.center, target_position)

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
        if self.health <= 0:
            self.kill()
            return ExperiencePoint(self.rect.center, 2)  # Cria um ExperiencePoint com um valor de 2

    def draw_health_bar(self, surface):
        pygame.draw.rect(
            surface, GREEN,
            (self.rect.x, self.rect.y - 10, self.health * ENEMY_SIZE // 10, 5)
        )

    def update(self):
        direction = pygame.math.Vector2(self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)
        direction.normalize_ip()
        self.rect.move_ip(direction.x * VELOCICADE_PERSEGUIDOR, direction.y * VELOCICADE_PERSEGUIDOR)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.down_sprites = [
        pygame.image.load("sprites_walking/red_frente1.png").convert_alpha(),
        pygame.image.load("sprites_walking/red_frente2.png").convert_alpha(),
        pygame.image.load("sprites_walking/red_frente3.png").convert_alpha(),
        pygame.image.load("sprites_walking/red_frente2.png").convert_alpha()
        ]
        ANIMATION_SPEED = 300  # Define a velocidade de animação. Menor é mais rápido.
        self.current_sprite = 0
        self.animation_time = pygame.time.get_ticks()
        self.surf = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.surf.fill(RED)
        self.direction = random.choice(['up', 'down', 'left', 'right'])
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
        if self.health <= 0:
            self.kill()
            return ExperiencePoint(self.rect.center, 1)

    def draw_health_bar(self, surface):
        pygame.draw.rect(
            surface, GREEN, 
            (self.rect.x, self.rect.y - 10, self.health * ENEMY_SIZE // 10, 5)
        )
        if self.damage_text:
            font = pygame.font.Font(None, 20)
            text = font.render(self.damage_text, 1, WHITE)
            surface.blit(text, (self.rect.x, self.rect.y - 20))
   
    def update(self):
        ANIMATION_SPEED = 300
        current_time = pygame.time.get_ticks()
    
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
        
        
        
        
        