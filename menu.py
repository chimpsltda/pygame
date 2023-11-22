import pygame
from GameData import *

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('arial', 18)
        self.buttons = ["PLAY", "MULTIPLAYER", "SETTINGS"]
        self.button_rects = []
        self.clicked_button = None  # added this line

        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)) #Pause
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)
        self.current_screen = None
        self.previous_game_state = None
        self.pause_buttons = ["Retornar ao Menu"]
        # Carregar a imagem de fundo
        self.background_image = pygame.image.load('texturas/menu/menu_fundo.png')
        # Carregar sprites dos botões
        self.button_sprites = {
            "PLAY": pygame.image.load('texturas/menu/jogar_naoselecionado.png'),
            "MULTIPLAYER": pygame.image.load('texturas/menu/multijogador_naoselecionado.png'),
            "SETTINGS": pygame.image.load('texturas/menu/config_button.png')
        }
        # Carregar sprites dos botões quando o mouse estiver sobre eles
        self.button_sprites_hover = {
            "PLAY": pygame.image.load('texturas/menu/jogar_selecionado.png'),
            "MULTIPLAYER": pygame.image.load('texturas/menu/multijogador_selecionado.png'),
            "SETTINGS": pygame.image.load('texturas/menu/config_button.png')
        }
    
    def render(self):
        screen.fill((255, 255, 255)) 
        # Desenhar a imagem de fundo primeiro
        self.screen.blit(self.background_image, (0, 0))
        
        self.button_rects.clear()
        mouse_pos = pygame.mouse.get_pos()
        for index, button_text in enumerate(self.buttons):
            text_surface = self.font.render(button_text, True, BLACK)
            button_x = self.screen.get_width() // 2 - BUTTON_WIDTH // 2
            button_y = (self.screen.get_height() // 2 - BUTTON_HEIGHT // 2) + index * MENU_BUTTON_SPACING
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
            # Determina o estado do botão para escolher a sprite correta
            if button_rect.collidepoint(mouse_pos):
                button_sprite = self.button_sprites_hover[button_text]
            else:
                button_sprite = self.button_sprites[button_text]

            # Desenha a sprite do botão na tela
            self.screen.blit(button_sprite, (button_x, button_y))

            self.button_rects.append(button_rect)
            # Check if this button is the clicked button
            if index == self.clicked_button:
                button_color = (255, 0, 0)  # red
            else:
                button_color = MENU_BUTTON_COLOR
            
            pygame.draw.rect(self.screen, button_color, button_rect)
            self.screen.blit(text_surface, (button_x + (BUTTON_WIDTH - text_surface.get_width()) // 2, button_y + (BUTTON_HEIGHT - text_surface.get_height()) // 2))
            self.button_rects.append(button_rect)
        
    def check_button_clicks(self, pos):
        for index, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                self.clicked_button = index  # added this line
                if index == 0:
                    return "PLAY"
                elif index == 1:
                    return "MULTIPLAYER"
                elif index == 2:
                    return "SETTINGS"
        return None

    def render_pause(self, previous_game_state):
        
        self.previous_game_state = previous_game_state
        if self.previous_game_state != "PAUSED":
            self.current_screen = self.screen.copy()
            self.current_screen.blit(self.overlay, (0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render("PAUSADO", 1, WHITE)
            self.current_screen.blit(text, (SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2 - 20))
            
            self.screen.blit(self.current_screen, (0, 0))
            # Renderizar botões da tela de pausa
            self.button_rects.clear()
            for index, button_text in enumerate(self.pause_buttons):
                text_surface = self.font.render(button_text, True, BLACK)
                button_x = self.screen.get_width() // 2 - BUTTON_WIDTH // 2
                button_y = (self.screen.get_height() // 2 - BUTTON_HEIGHT // 2) + index * MENU_BUTTON_SPACING + 50  # +50 para posicionar abaixo do texto PAUSADO
                button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
                pygame.draw.rect(self.screen, MENU_BUTTON_COLOR, button_rect)
                self.screen.blit(text_surface, (button_x + (BUTTON_WIDTH - text_surface.get_width()) // 2, button_y + (BUTTON_HEIGHT - text_surface.get_height()) // 2))
                self.button_rects.append(button_rect)
           
        

        

        for index, button_text in enumerate(self.buttons):
            text_surface = self.font.render(button_text, True, BLACK)
            button_x = self.screen.get_width() // 2 - BUTTON_WIDTH // 2
            button_y = (self.screen.get_height() // 2 - BUTTON_HEIGHT // 2) + index * MENU_BUTTON_SPACING
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        
        
        pygame.display.flip()

    def check_pause_button_clicks(self, pos):
        for index, rect in enumerate(self.button_rects):
            if rect.collidepoint(pos):
                if self.pause_buttons[index] == "Retornar ao Menu":
                    return "MENU"
        return None