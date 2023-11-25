import pygame, random, time
from GameData import *
from Drops import *
from WeaponClass import Weapon  #Propriedades das armas e dos projéteis
from Entities import *
from xpClass import *
from InventoryClass import *
from Jogador import *
from menu import *
from multi import *
#------------------------------------------------------------------------------#------------------------------------------------------------------------------#

#def create_server(client, server_name):
#server_info = {"nome_do_servidor": server_name, "info": "alguma informação"}
    #client.publish("jogo/servidores", json.dumps(server_info))
    # Muda para a tela de espera

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1280, 720))
background = pygame.image.load('texturas/grama2.png')
background = pygame.transform.scale(background, (1280, 720))

#Importa e cria o player com sua sprite
player = Player()
sprite_parado = pygame.image.load("texturas/sprites_walking/sprite_parado.png").convert_alpha()

enemies = pygame.sprite.Group()             # Inicializando os inimigos
chasing_enemies = pygame.sprite.Group()     # Inicializando os inimigos que perseguem
objectives = pygame.sprite.Group()          # Inicializando os objetivos
projectiles = pygame.sprite.Group()
exp_points = pygame.sprite.Group()          # Inicializando os pontos de experiência
items_group = pygame.sprite.Group()         # iniciando itens
collectibles = pygame.sprite.Group()        # Iniciando grupo para itens e pontos de experiência

all_sprites = pygame.sprite.Group()

# Adicionando inimigos e objetivos
for i in range(5):
    new_enemy = Enemy()
    new_objective = Objective()
    enemies.add(new_enemy)
    objectives.add(new_objective)
    all_sprites.add(new_enemy)
    all_sprites.add(new_objective)

all_sprites.add(player)  # Mova essa linha aqui

enemy_groups = [enemies, chasing_enemies]  # Adicione outros grupos de inimigos aqui

# setando o clock e rastreando tempo inicial
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# Inicializando a barra de experiência
exp_bar = ExperienceBar(player)

experience_point = pygame.sprite.Group()
# Add an ExperiencePoint to the sprite group

# Variável para rastrear o estado de pausa
paused = False

overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))     # Cria uma nova superfície
overlay.fill((0, 0, 0))                                     # Preenche a superfície com preto
overlay.set_alpha(128)                                      # Define a transparência da superfície (0 = transparente, 255 = opaco)

# Variável para armazenar a tela atual
current_screen = None

# Variável para rastrear o estado do jogo
game_state = "MENU"
menu = Menu(screen)
running = True

# Inicializando a variável de tempo decorrido
cooldown_dano = 1000  # 1 segundo de cooldown
elapsed_time = 0        
ultimo_dano = 0
#------------------------------------------------------------------------------#------------------------------------------------------------------------------#

def draw_text(text, position, color=WHITE):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, rect)
    
running = True   
game_over = False

while running:
    if not game_over:
        tempo_atual = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "MULTIPLAYER" and event.type == pygame.MOUSEBUTTONDOWN:
                action = menu.check_multiplayer_button_clicks(event.pos)
                if action:
                    mqtt = MQTTConnection()
                    if action == "MENU":
                        game_state = "MENU"
                    if action == "CREATE":
                        mqtt.create_room()
                        screen.fill((0, 0, 0))
                    elif action == "JOIN":
                        game_state = "JOIN"
                    print(game_state)

            if game_state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
                print("aqui")
                action = menu.check_button_clicks(event.pos)
                if action:
                    if action == "PLAY":
                        game_state = "RUNNING"
                    elif action == "MULTIPLAYER":
                        game_state = "MULTIPLAYER"
                        
            if game_state == "PAUSED" and event.type == pygame.MOUSEBUTTONDOWN:
                new_state = menu.check_pause_button_clicks(event.pos)
                if new_state:
                    game_state = new_state

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
                if player.armas[player.arma_atual] is Fist():
                    player_position = player.rect.center
                    for enemy in enemies:
                        enemy_position = enemy.rect.center
                        if player.weapon.attack(player_position, enemy_position):
                            enemy.take_damage(Fist.DAMAGE)  # Supondo que o método `take_damage` exista
                            # Aqui você também pode implementar a lógica de knockback, se desejar.
                else:
                    new_projectile = player.attack(target_pos)
                    if isinstance(new_projectile, (list, tuple)):  # verifique se é uma lista ou tuple
                        for projetil in new_projectile:
                            projectiles.add(projetil)
                            all_sprites.add(projetil)

        if game_state == "RUNNING":
            pressed_keys = pygame.key.get_pressed()         # Atualizar a posição do jogador
            player.update(pressed_keys)
            projectiles.update()                            # Atualizar a posição dos projéteis
            enemies.update()                                # Atualizar a posição dos inimigos
            chasing_enemies.update()                        # Atualizando a posição dos inimigos que perseguem
            # Decrementar o temporizador da barra de saúde
            if player.health_bar_visible_timer > 0:
                player.health_bar_visible_timer -= clock.get_time() 
            # Quando um projétil atinge um inimigo
            for enemy_group in enemy_groups:
                collisions = pygame.sprite.groupcollide(projectiles, enemy_group, True, False)
                for projectile, hit_enemies in collisions.items():
                    for enemy in hit_enemies:
                        dropped_items = enemy.take_damage(player.damage)
                        for item in dropped_items:
                            all_sprites.add(item)
                            collectibles.add(item)  # Adicione o item ao grupo collectibles
                            if isinstance(item, ExperiencePoint):
                                exp_points.add(item)
                            else:
                                items_group.add(item)
                            adjust_dropped_items_positions(dropped_items)
                            # Se você tiver outros grupos específicos para diferentes tipos de itens no futuro, 
                            # você pode adicionar lógica adicional aqui.

            # Quando o jogador coleta um ponto de experiência
            collisions = pygame.sprite.spritecollide(player, collectibles, True)
            for item in collisions:
                if item != player:
                    if isinstance(item, ExperiencePoint):
                        exp_bar.gain_exp(item.value)
                        exp_points.remove(item)   # Se for um ponto de experiência, remova-o do grupo exp_points
                    else:
                        #player.add_to_inventory(item)
                        items_group.remove(item)  # Remova o item do grupo items_group
                        # Adicionando um item ao primeiro slot vazio
                        added = add_item_to_inventory(item, inventory_matrix)
                        if not added:
                            print("Inventário cheio!")  # O item não foi adicionado porque o inventário está cheio
            
            # Desenhando tudo na tela
            screen.blit(background, (0, 0))         # Desenha a imagem de fundo

            for objective in objectives:            # Atualizando os objetivos
                objective.update(player.rect)

            for particle in PARTICLES:
                screen.blit(particle.image, particle.rect)
                particle.update()

            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

            for enemy in enemies:
                enemy.draw_health_bar(screen)
                    
            

            # Desenhando a barra de experiência
            exp_bar.draw(screen)
            player.draw_health_bar(screen) 
            
            # Desenhando a barra de saúde dos inimigos laranjas
            for enemy in chasing_enemies:
                enemy.draw_health_bar(screen)
            if player.health_bar_visible_timer > 0:
                    player.health_bar_visible_timer -= clock.get_time() 
            for enemy_group in enemy_groups:
                for enemy in enemy_group:
                    if pygame.sprite.collide_rect(player, enemy):
                        if tempo_atual - ultimo_dano > cooldown_dano:
                            ultimo_dano = tempo_atual
                            player.health -= 1 - (player.resistance / 100)
                            player.health_bar_visible_timer = 2000  # 2 segundos de visibilidade
                            if player.health <= 0:
                                game_over = True
                            break
                                
                    

            def handle_projectile_enemy_collisions(projectiles_group, enemies_group):
                collisions = pygame.sprite.groupcollide(projectiles_group, enemies_group, True, False)
                for projectile, hit_enemies in collisions.items():
                    for enemy in hit_enemies:
                        exp_point = enemy.take_damage(player.damage)
                        if exp_point:
                            ExperiencePoint.add(exp_point)
                            all_sprites.add(exp_point)

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

        if game_state == "INVENTORY":  # Se o inventário estiver aberto
            if previous_game_state != "INVENTORY":  # Se acabou de abrir o inventário
                # Armazena a tela atual
                current_screen = screen.copy()

                # Desenha a superfície de sobreposição e o texto "PAUSED" na tela atual
                current_screen.blit(overlay, (0, 0))  # Desenha a superfície sobre a tela

                mostrar_inventario(current_screen, overlay)
                print_inventory(inventory_matrix)

            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = time.time() * 1000  # tempo em milissegundos
                if current_time - last_click_time > 200:  # 200 ms debounce time
                    handle_click(*event.pos)
                    mostrar_inventario(current_screen, overlay)
                    last_click_time = current_time

            screen.blit(current_screen, (0, 0))  # Desenha a tela atual
            pygame.display.flip()

        if game_state == "MENU":
            menu.render()
            pygame.display.flip()
        elif game_state == "MULTIPLAYER":
            menu.render_multiplayer_menu()
            pygame.display.flip()	
        elif game_state == "CREATE":
            mqtt.create_room_screen()
            pygame.display.flip()
        elif game_state == "PAUSED":
            menu.render_pause(previous_game_state)

        # Atualiza o estado anterior do jogo
        previous_game_state = game_state

        # Mantendo o loop na velocidade certa
        clock.tick(30)
    if game_over:
                # Cobre a tela com um retângulo escuro
                dark_overlay = pygame.Surface(screen.get_size())  # Cria uma superfície do tamanho da tela
                dark_overlay.set_alpha(180)  # Define a transparência (0-255, onde 255 é opaco)
                dark_overlay.fill((0, 0, 0))  # Preenche a superfície com preto
                screen.blit(dark_overlay, (0, 0))  # Desenha a superfície sobre a tela

                # Renderiza e centraliza a mensagem "Você Perdeu"
                font = pygame.font.Font(None, 74)  # Define a fonte e o tamanho
                text = font.render("Você Perdeu", True, (255, 255, 255))  # Cria o texto
                text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))  # Centraliza o texto
                screen.blit(text, text_rect)  # Desenha o texto sobre a tela
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                pygame.display.flip()  # Atualiza a tela para mostrar as mudanças