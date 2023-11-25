import pygame, random

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
PLAYER_SPEED = 5
ENEMY_SPEED = 1
VELOCICADE_PERSEGUIDOR = 3.5
OBJECTIVE_SIZE = 20
ENEMY_SIZE = 20
PLAYER_SIZE = 5
PROJECTILE_SIZE = 10
OBJECTIVE_TIME = 3

# Inventário
INVENTORY_WIDTH = 1200
INVENTORY_HEIGHT = 800
SLOT_SIZE = 56  # Tamanho do slot do inventário
SLOT_BORDER = 5  # Espessura da borda do slot
SLOT_SPACING = 16  # Espaçamento entre os slots
MARGIN = 44  # Margem do canto superior esquerdo
rows, cols = 3, 5

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LARANJA = (255, 165, 0)
LIGHT_GRAY = (220, 220, 220)
MENU_BUTTON_COLOR = (0, 150, 0)

# Menu
BUTTON_WIDTH = 200
Botao_jogarx = 190
Botao_jogary = 98
BUTTON_HEIGHT = 50
MENU_BUTTON_SPACING = 150

screen = pygame.display.set_mode((1280, 720))
fixed_distance = 100  # A distância fixa que você deseja, por exemplo, 100 pixels