# Configurações do jogo
SCREEN_WIDTH, SCREEN_HEIGHT = 1980, 1080
PLAYER_SPEED = 5
ENEMY_SPEED = 2
VELOCICADE_PERSEGUIDOR = 3.5
OBJECTIVE_SIZE = 20
ENEMY_SIZE = 20
PLAYER_SIZE = 20
PROJECTILE_SIZE = 10
OBJECTIVE_TIME = 3  # Tempo em segundos para completar um objetivo

# Cores
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


import pygame, random, time
import math
                  #importa o jogador
                #importa as configurações
                  #importa o __init__ com a importação de todos os inimigos
                   #importa a barra de xp
                  #importa o objetivo


# Inicializando Pygame
pygame.init()

# Configurando a janela do jogo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.image.load('texturas/grama.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensionando a imagem para caber na tela

#classe da arma
class Weapon:
    def __init__(self):
        self.last_attack_time = 0

    def attack(self, position, target_position):
        raise NotImplementedError()

    def can_attack(self, current_time):
        raise NotImplementedError()
#classe da shotgun
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
#classe do projetil
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
#classe da pistola   
class Pistol(Weapon):
    DAMAGE = 2
    COOLDOWN = 1000  # 1000 milissegundos = 1 segundo

    def attack(self, position, target_position):
        # Cria um projétil se estiver fora do cooldown
        if self.can_attack(pygame.time.get_ticks()):
            self.last_attack_time = pygame.time.get_ticks()
            return [Projectile(position, target_position, damage=self.DAMAGE)]
        return []

    def can_attack(self, current_time):
        return current_time - self.last_attack_time > self.COOLDOWN
#classe do punho
class Fist(Weapon):
    DAMAGE = 1
    RANGE = 50   # Exemplo de alcance
    KNOCKBACK = 10

    def attack(self, position, target_position):
        # Aqui você deve implementar a lógica para verificar se o alvo está no alcance do punho
        # e se estiver, aplicar o dano e o knockback.
        pass

    def can_attack(self, current_time):
        # O punho não tem cooldown
        return True
#chamando a sprite do player parado
sprite_parado = pygame.image.load("sprites_walking/sprite_parado.png").convert_alpha()


#classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        scale_factor = 0.7  # Reduzir o tamanho para 70% do original

         # Para a sprite parada
        self.original_surf = pygame.image.load("sprites_walking/sprite_parado.png").convert_alpha()
        self.original_surf = pygame.transform.scale(self.original_surf, (int(150 * scale_factor), int(180 * scale_factor)))
        self.surf = self.original_surf.copy()

        # Para as sprites de caminhada
        self.walk1_surf = pygame.transform.scale(pygame.image.load("sprites_walking/sprite_walk1.png").convert_alpha(), (int(150 * scale_factor), int(180 * scale_factor)))
        self.walk2_surf = pygame.transform.scale(pygame.image.load("sprites_walking/sprite_walk2.png").convert_alpha(), (int(150 * scale_factor), int(180 * scale_factor)))
        
        self.surf = self.original_surf
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        
        self.walking = False
        self.walk_count = 0  # Para controlar a alternância entre walk1 e walk2

        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
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


# Inicializando o jogador
player = Player()

# Inicializando os inimigos e os objetivos
enemies = pygame.sprite.Group()
chasing_enemies = pygame.sprite.Group()  # Inicializando os inimigos que perseguem
objectives = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
#----------------------------------------------------------------------CLASSES-----------------------------------------------------------------------
#classe dos objetivos
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

#classe inimigos vermelhos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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

#classe do inimigo perseguidor
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

#classe do ponto de xp
class ExperiencePoint(pygame.sprite.Sprite):
    def __init__(self, pos, value=1):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((BLUE))  # Azul
        self.rect = self.surf.get_rect(center=pos)
        self.value = value






# Adicionando inimigos e objetivos
for i in range(5):
    new_enemy = Enemy()
    new_objective = Objective()
    enemies.add(new_enemy)
    objectives.add(new_objective)
    all_sprites.add(new_enemy)
    all_sprites.add(new_objective)

enemy_groups = [enemies, chasing_enemies]  # Adicione outros grupos de inimigos aqui

# Configurando o clock
clock = pygame.time.Clock()


#barra de xp
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

# Inicializando a barra de experiência
exp_bar = ExperienceBar()

# Inicializando os pontos de experiência
exp_points = pygame.sprite.Group()

# Variável para rastrear o estado de pausa
paused = False

# Rastreando o tempo de início
start_time = pygame.time.get_ticks()

overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria uma nova superfície
overlay.fill((0, 0, 0))  # Preenche a superfície com preto
overlay.set_alpha(128)  # Define a transparência da superfície (0 = transparente, 255 = opaco)

# Variável para armazenar a tela atual
current_screen = None

# Variável para rastrear o estado do jogo
game_state = "RUNNING"

# Loop principal do jogo
running = True

elapsed_time = 0 # Inicializando a variável de tempo decorrido

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Verificar se a tecla ESC foi pressionada
                if game_state == "RUNNING":
                    game_state = "PAUSED"
                    elapsed_time = pygame.time.get_ticks() - start_time  # Atualiza o tempo decorrido
                else:
                    game_state = "RUNNING"
                    start_time = pygame.time.get_ticks() - elapsed_time  # Ajusta o start_time
                    
            if event.key == pygame.K_e:  # Verificar se a tecla 'e' foi pressionada
                if game_state == "RUNNING":
                    game_state = "INVENTORY"
                    elapsed_time = pygame.time.get_ticks() - start_time  # Atualiza o tempo decorrido
                elif game_state == "INVENTORY":
                    game_state = "RUNNING"
                    start_time = pygame.time.get_ticks() - elapsed_time  # Ajusta o start_time
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                if event.key == pygame.K_1:
                    player.change_weapon(0)
                elif event.key == pygame.K_2:
                    player.change_weapon(1)
                elif event.key == pygame.K_3:
                    player.change_weapon(2)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Quando o botão do mouse é pressionado, crie um novo projétil
            target_pos = pygame.mouse.get_pos()  # Posição do mouse
            new_projectile = player.attack(target_pos)
            for projetil in new_projectile:
                projectiles.add(projetil)
                all_sprites.add(projetil)

                   
    if game_state == "RUNNING":
        # Atualizar a posição do jogador
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        # Atualizar a posição dos projéteis
        projectiles.update()
        # Atualizar a posição dos inimigos
        enemies.update()
        # Atualizando a posição dos inimigos que perseguem
        chasing_enemies.update()

        # Atualizando os objetivos
        for objective in objectives:
            objective.update(player.rect)

        # Quando um projétil atinge um inimigo
        collisions = pygame.sprite.groupcollide(projectiles, enemies, True, False)
        for projectile, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                exp_point = enemy.take_damage(player.damage)
                if exp_point:
                    exp_points.add(exp_point)
                    all_sprites.add(exp_point)

        # Quando o jogador coleta um ponto de experiência
        collisions = pygame.sprite.spritecollide(player, exp_points, True)
        for exp_point in collisions:
            exp_bar.gain_exp(exp_point.value)  # Usa o valor do ponto de experiência

        # Desenhando tudo na tela
        screen.blit(background, (0, 0))  # Desenha a imagem de fundo
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        for enemy in enemies:
            enemy.draw_health_bar(screen)

        # Desenhando a barra de experiência
        exp_bar.draw(screen)
        # Desenhando a barra de saúde dos inimigos laranjas
        for enemy in chasing_enemies:
            enemy.draw_health_bar(screen)

        for enemy_group in enemy_groups:
            for enemy in enemy_group:
                if pygame.sprite.collide_rect(player, enemy):
                    player.kill()
                    running = False
                    break  # Sai do loop assim que uma colisão é detectada

        def handle_projectile_enemy_collisions(projectiles_group, enemies_group):
            collisions = pygame.sprite.groupcollide(projectiles_group, enemies_group, True, False)
            for projectile, hit_enemies in collisions.items():
                for enemy in hit_enemies:
                    exp_point = enemy.take_damage(player.damage)
                    if exp_point:
                        exp_points.add(exp_point)
                        all_sprites.add(exp_point)

        #enemy_groups = [enemies, chasing_enemies]

        for enemy_group in enemy_groups:
            handle_projectile_enemy_collisions(projectiles, enemy_group)

        # Verificando se todos os objetivos foram concluídos
        if not objectives:
            font = pygame.font.Font(None, 36)
            text = font.render("VOCÊ SOBREVIVEU!", 1, WHITE)
            screen.blit(text, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            pygame.display.flip()
            time.sleep(2)

            # Reiniciando o jogo
            player = Player()
            all_sprites = pygame.sprite.Group()
            all_sprites.add(player)
            enemies = pygame.sprite.Group()
            objectives = pygame.sprite.Group()
            projectiles = pygame.sprite.Group()
            for i in range(5):
                new_enemy = Enemy()
                new_objective = Objective()
                enemies.add(new_enemy)
                objectives.add(new_objective)
                all_sprites.add(new_enemy)
                all_sprites.add(new_objective)

        # Verificando se passaram 30 segundos
        if pygame.time.get_ticks() - start_time > 30000 and not paused:
            if random.random() < 0.01:  # 1% de chance de adicionar um novo inimigo laranja a cada frame
                new_chasing_enemy = ChasingEnemy(player)
                chasing_enemies.add(new_chasing_enemy)
                all_sprites.add(new_chasing_enemy)
        else:
            elapsed_time = pygame.time.get_ticks() - start_time

        # Adicionando novos inimigos
        if random.random() < 0.02:  # 2% chance de adicionar um novo inimigo a cada frame
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        pygame.display.flip()

    elif game_state == "INVENTORY":  # Se o inventário estiver aberto
        if previous_game_state != "INVENTORY":  # Se acabou de abrir o inventário
            # Armazena a tela atual
            current_screen = screen.copy()

            # Desenha a superfície de sobreposição e o texto "PAUSED" na tela atual
            current_screen.blit(overlay, (0, 0))  # Desenha a superfície sobre a tela

            font = pygame.font.Font(None, 36)
            text = font.render("Inventário", 1, WHITE)
            current_screen.blit(text, (40, 10)) 

        screen.blit(current_screen, (0, 0))  # Desenha a tela atual
        pygame.display.flip()

    elif game_state == "PAUSED":  # Se o jogo estiver pausado
        if previous_game_state != "PAUSED":  # Se o jogo acabou de ser pausado
            # Armazena a tela atual
            current_screen = screen.copy()

            # Desenha a superfície de sobreposição e o texto "PAUSED" na tela atual
            current_screen.blit(overlay, (0, 0))  # Desenha a superfície sobre a tela

            font = pygame.font.Font(None, 36)
            text = font.render("PAUSADO", 1, WHITE)
            current_screen.blit(text, (SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2 - 20))

        screen.blit(current_screen, (0, 0))  # Desenha a tela atual
        pygame.display.flip()

    # Atualiza o estado anterior do jogo
    previous_game_state = game_state


    # Mantendo o loop na velocidade certa
    clock.tick(30)











    
