import pygame, math
from WeaponClass import *
from GameData import *
from particulas import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        scale_factor = 0.7  # Reduzir o tamanho para 70% do original

        # Para a sprite parada
        self.original_surf = pygame.image.load("texturas/sprites_walking/sprite_parado.png").convert_alpha()
        self.original_surf = pygame.transform.scale(self.original_surf, (int(70 * scale_factor), int(70 * scale_factor)))
        self.surf = self.original_surf.copy()

        # Para as sprites de caminhada
        self.walk1_surf = pygame.transform.scale(pygame.image.load("texturas/sprites_walking/sprite_walk1.png").convert_alpha(), (int(70 * scale_factor), int(70 * scale_factor)))
        self.walk2_surf = pygame.transform.scale(pygame.image.load("texturas/sprites_walking/sprite_walk2.png").convert_alpha(), (int(70 * scale_factor), int(70 * scale_factor)))
        self.surf = self.original_surf
        self.walking = False
        self.walk_count = 0  # Para controlar a alternância entre walk1 e walk2
        self.rect = self.surf.get_rect(center = (1280/2, 720/2))

        #Vida do jogador
        self.health = 1
        self.max_health = 1
        self.font = pygame.font.SysFont(None, 36)  # Fonte para renderizar a saúde

        #Dano, armas e velocidade
        self.damage = 1
        self.armas = [Pistol(), Shotgun(), Fist()]
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
            if random.random() < 0.3:  # Ajuste este valor para controlar a frequência das partículas
                particle = Particle(self.rect.center)
                PARTICLES.add(particle)
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
    
    def draw_health(self, screen): # Desenha a saúde no canto superior esquerdo
        health_str = f"{self.health} / {self.max_health}"
        health_text = self.font.render(health_str, True, (255, 0, 0))
        screen.blit(health_text, (10, 20))  

    def activate_ability(self, ability):
        ability.function(self)