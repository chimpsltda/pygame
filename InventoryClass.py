import pygame
from GameData import *
from Drops import *

rows, cols = 3, 5

# Matriz para armazenar os itens do inventário
inventory_matrix = [[None for _ in range(cols)] for _ in range(rows)]

item_dragged = None   # Salvando o item no mouse
selected_item = None  # Inicialize selected_item antes de entrar no loop principal
clicked_slot = None
last_click_time = 0
capacitor_test = Capacitor((100, 100))
inventory_matrix[0][0] = capacitor_test

def mostrar_inventario(screen, overlay):
    font = pygame.font.Font(None, 36)
    text = font.render("Inventário", 1, WHITE)
    screen.blit(text, (40, 10))
    
    inventory_screen = pygame.image.load('Texturas\Teste.png').convert_alpha() #inventario
    inventory_screen = pygame.transform.scale(inventory_screen, (INVENTORY_WIDTH, INVENTORY_HEIGHT))
    
    start_x = MARGIN
    start_y = MARGIN
    
    for row in range(rows):
        for col in range(cols):
            slot_x = start_x + col * (SLOT_SIZE + SLOT_SPACING)
            slot_y = start_y + row * (SLOT_SIZE + SLOT_SPACING)
        
            # Desenha a imagem da borda
            pygame.draw.rect(inventory_screen, (100, 100, 100), (slot_x - SLOT_BORDER, slot_y - SLOT_BORDER, SLOT_SIZE + 2 * SLOT_BORDER, SLOT_SIZE + 2 * SLOT_BORDER))
            
            # Desenha o slot
            pygame.draw.rect(inventory_screen, (255, 255, 255), (slot_x, slot_y, SLOT_SIZE, SLOT_SIZE))

            # Se o slot tiver um item, desenhe o item
            item = inventory_matrix[row][col]
            if item:
                item_image = pygame.transform.scale(item.surf, (SLOT_SIZE, SLOT_SIZE))  # Redimensiona a imagem do item para caber no slot
                inventory_screen.blit(item_image, (slot_x, slot_y))

    x = (SCREEN_WIDTH - INVENTORY_WIDTH) // 2
    y = (SCREEN_HEIGHT - INVENTORY_HEIGHT) // 2
    screen.blit(inventory_screen, (x, y))

    # Verifica a posição do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Ajusta as coordenadas do mouse para se alinhar com a posição do inventário na tela
    adjusted_mouse_x = mouse_x - (SCREEN_WIDTH - INVENTORY_WIDTH) // 2
    adjusted_mouse_y = mouse_y - (SCREEN_HEIGHT - INVENTORY_HEIGHT) // 2

    # Obtém o slot sob o mouse
    row, col = get_slot_from_pos(adjusted_mouse_x, adjusted_mouse_y)

    # Se o mouse estiver sobre um slot com um item, mostra a tooltip
    if row is not None and inventory_matrix[row][col]:
        draw_item_tooltip(screen, inventory_matrix[row][col], mouse_x, mouse_y)



def add_item_to_inventory(item, inventory_matrix):
    for row in range(len(inventory_matrix)):
        for col in range(len(inventory_matrix[row])):
            if not inventory_matrix[row][col]:  # Se o slot estiver vazio
                inventory_matrix[row][col] = item
                print("item adicionado ao inventário: ",item)
                return True
    return False  # Se todos os slots estiverem ocupados
    
def print_inventory(inventory_matrix):
    print("Inventário:")
    for row in inventory_matrix:
        for item in row:
            if item:
                print(item.name)
            else:
                print("Vazio")
        print("-----")

def get_slot_from_pos(x, y):
    # Dada uma posição do mouse, determine em qual slot do inventário ela está (se houver)
    for row in range(rows):
        for col in range(cols):
            slot_x = MARGIN + col * (SLOT_SIZE + SLOT_SPACING)
            slot_y = MARGIN + row * (SLOT_SIZE + SLOT_SPACING)
            if slot_x <= x < slot_x + SLOT_SIZE and slot_y <= y < slot_y + SLOT_SIZE:
                return row, col
    return None, None

def handle_click(x, y):
    global selected_item

    row, col = get_slot_from_pos(x - (SCREEN_WIDTH - INVENTORY_WIDTH) // 2, y - (SCREEN_HEIGHT - INVENTORY_HEIGHT) // 2)

    if row is not None:  # Se um slot válido foi clicado
        clicked_slot = inventory_matrix[row][col]
        if not selected_item and clicked_slot:
            # Seleciona o item se um slot foi clicado e nenhum item estava selecionado antes
            selected_item = clicked_slot
            inventory_matrix[row][col] = None
        elif selected_item:
            # Coloca o item selecionado no slot clicado e o item anteriormente no slot passa a ser o selecionado
            inventory_matrix[row][col], selected_item = selected_item, clicked_slot

def draw_item_tooltip(screen, item, x, y):
    font = pygame.font.Font(None, 24)
    text = font.render(item.name, 1, WHITE)
    text_width, text_height = font.size(item.name)

    # Definindo tamanho e posição da tooltip
    padding = 5
    box_width = text_width + 2 * padding
    box_height = text_height + 2 * padding

    box_x = x + 10  # para a tooltip aparecer ligeiramente à direita do cursor
    box_y = y

    # Desenha o retângulo da tooltip
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 1)  # Borda branca

    # Desenha o texto da tooltip dentro do retângulo
    screen.blit(text, (box_x + padding, box_y + padding))
