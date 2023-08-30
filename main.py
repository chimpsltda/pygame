import pygame, random, time #Integrações do jogo
from GameData import *

#Armas
from Armas.WeaponClass import Weapon

#Shotgun
from Armas.ShotgunClass import Shotgun

#Pistola
from Armas.PistolClass import Pistol

#Melee(ainda não funciona)
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
#------------------------------------------------------------------------------#------------------------------------------------------------------------------#
#Jogador, Objetivos e Inimigos
from NTT.Entities import *
#------------------------------------------------------------------------------#------------------------------------------------------------------------------#
# Inicializando Pygame
pygame.init()

# Configurando a janela do jogo
screen = pygame.display.set_mode((1280, 720))
background = pygame.image.load('texturas/grama2.png')
background = pygame.transform.scale(background, (1280, 720))

#Cria o player com sua sprite
player = Player()
sprite_parado = pygame.image.load("sprites_walking/sprite_parado.png").convert_alpha()

# Inicializando os inimigos e os objetivos
enemies = pygame.sprite.Group()
chasing_enemies = pygame.sprite.Group()  # Inicializando os inimigos que perseguem
objectives = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Adicionando inimigos e objetivos
for i in range(5):
    new_enemy = Enemy()
    new_objective = Objective()
    enemies.add(new_enemy)
    objectives.add(new_objective)
    all_sprites.add(new_enemy)
    all_sprites.add(new_objective)

enemy_groups = [enemies, chasing_enemies]  # Adicione outros grupos de inimigos aqui

# setando o clock e rastreando tempo inicial
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# Inicializando a barra de experiência
exp_bar = ExperienceBar()
exp_points = pygame.sprite.Group()

# Variável para rastrear o estado de pausa
paused = False

overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Cria uma nova superfície
overlay.fill((0, 0, 0))  # Preenche a superfície com preto
overlay.set_alpha(128)  # Define a transparência da superfície (0 = transparente, 255 = opaco)

# Variável para armazenar a tela atual
current_screen = None

# Variável para rastrear o estado do jogo
game_state = "RUNNING"
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

            font = pygame.font.Font(None, 36) #
            text = font.render("Inventário", 1, WHITE)
            current_screen.blit(text, (40, 10)) 

        screen.blit(current_screen, (0, 0))  # Desenha a tela atual
        pygame.display.flip()

    elif game_state == "PAUSED":
        if previous_game_state != "PAUSED":  # Se o jogo é pausado, armazena a tela atual e escreve "PAUSED" por cima
            current_screen = screen.copy()
            current_screen.blit(overlay, (0, 0))  # Desenha a superfície sobre a tela
            font = pygame.font.Font(None, 36) #Fonte
            text = font.render("PAUSADO", 1, WHITE) #Texto e sua cor
            current_screen.blit(text, (SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2 - 20))#Local da msg de Pause

        screen.blit(current_screen, (0, 0))  # Desenha a tela atual
        pygame.display.flip()

    # Atualiza o estado anterior do jogo
    previous_game_state = game_state

    # Mantendo o loop na velocidade certa
    clock.tick(30)