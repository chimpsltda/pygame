import pygame, random

from GameData import *

class ExperiencePoint(pygame.sprite.Sprite):
    def __init__(self, pos, value=1):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((BLUE))  # Azul
        self.rect = self.surf.get_rect(center=pos)
        self.value = value

class Ability:
    def __init__(self, name, function, description):
        self.name = name
        self.function = function  # Isto pode ser None para habilidades sem função específica
        self.description = description

    def activate(self, player):
        if self.function:
            self.function(player)

def increase_resistance(player):
    # Quando o jogador ativa esta habilidade, reduz o dano recebido em 10%.
    player.resistance += 3
    print(f"A resistência do jogador aumentou para {player.resistance} %.")

def increase_health(player):
    # Quando o jogador ativa esta habilidade, aumenta a saúde e saúde máxima em 1.
    player.max_health += 2
    player.health = player.max_health
    print(f"A saúde máxima do jogador aumentou para {player.max_health} e a saúde atual é {player.health}.")

def increase_damage(player):
    # Quando o jogador ativa esta habilidade, aumenta o dano em 1%.
    player.damage_extra += 1
    print(f"O dano do jogador aumentou para {player.damage_extra} %.")

# As habilidades "Poder de Fogo" e "Defesa Forte" ainda precisam de funções associadas para alterar as características do jogador.
ALL_ABILITIES = [
    Ability("Poder de Fogo", increase_damage, "Aumenta o dano em 10%"), 
    Ability("Defesa Forte", increase_resistance, "Reduz o dano recebido em 10%"),
    Ability("Aumentar Saúde", increase_health, "Aumenta a saúde e saúde máxima em 1.")
]

class ExperienceBar:
    def __init__(self, player):
        self.level = 0
        self.exp = 0
        self.exp_to_next_level = 2
        self.player = player  # mantenha uma referência ao jogador

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1
        self.show_level_options()
        self.exp_to_next_level += 5

    def show_level_options(self):
        choices = random.sample(ALL_ABILITIES, 3)
        print(f"Parabéns! Você subiu para o nível {self.level}!")

        running = True
        selected_option = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        chosen_ability = choices[selected_option]
                        chosen_ability.activate(self.player)
                        print(f"Você escolheu: {chosen_ability.name}")
                        running = False

            # Desenhar opções
            self.draw_options(choices, selected_option)

    def draw_options(self, choices, selected_option):
        screen.fill((0, 0, 0))  # Limpar tela (ou desenhar fundo)
        font = pygame.font.Font(None, 36)
        for i, choice in enumerate(choices):
            text = font.render(f"{choice.name}: {choice.description}", True, (255, 255, 255))
            if i == selected_option:
                pygame.draw.rect(screen, (0, 255, 0), text.get_rect(topleft=(100, 50 + i * 40)), 2)
            screen.blit(text, (100, 50 + i * 40))

        pygame.display.flip()

    def draw(self, surface):
        pygame.draw.rect(
            surface, BLUE, 
            (10, 0, self.exp * SCREEN_WIDTH // self.exp_to_next_level, 20)
        )
