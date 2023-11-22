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

def increase_health(player):
    # Quando o jogador ativa esta habilidade, aumenta a saúde e saúde máxima em 1.
    player.health += 1
    player.max_health += 1
    print(f"A saúde máxima do jogador aumentou para {player.max_health} e a saúde atual é {player.health}.")

# As habilidades "Poder de Fogo" e "Defesa Forte" ainda precisam de funções associadas para alterar as características do jogador.
ALL_ABILITIES = [
    Ability("Poder de Fogo", None, "Aumenta o dano em 10%"), 
    Ability("Defesa Forte", None, "Reduz o dano recebido em 10%"),
    Ability("Aumentar Saúde", increase_health, "Aumenta a saúde e saúde máxima em 1.")
]

class ExperienceBar:
    def __init__(self, player):
        self.level = 0
        self.exp = 0
        self.exp_to_next_level = 10
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
        print("Escolha uma das seguintes habilidades:")
        
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice.name}: {choice.description}")

        player_choice = int(input("Digite o número da sua escolha: ")) - 1
        chosen_ability = choices[player_choice]
        chosen_ability.activate(self.player)  # ative a habilidade no jogador
        print(f"Você escolheu: {chosen_ability.name}")

    def draw(self, surface):
        pygame.draw.rect(
            surface, BLUE, 
            (10, 0, self.exp * SCREEN_WIDTH // self.exp_to_next_level, 20)
        )
