"""
Name Entry Screen Module - Donkey Kong Game
===========================================
Pantalla para ingresar el nombre cuando se logra un high score.
"""

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, YELLOW

def show_name_entry_screen(screen, clock, score, rank):
    """
    Muestra la pantalla para ingresar nombre
    
    Args:
        screen: Superficie de pygame
        clock: Reloj de pygame
        score: Puntuación obtenida
        rank: Posición en el ranking
        
    Returns:
        str: Nombre ingresado (máximo 5 caracteres)
    """
    name = ""
    max_length = 5
    
    font_large = pygame.font.Font(None, 64)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    cursor_blink = 0
    
    while True:
        cursor_blink += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return "PLAYER"  # Nombre por defecto
                elif len(name) < max_length:
                    # Solo letras y números
                    if event.unicode.isalnum():
                        name += event.unicode.upper()
        
        # Dibujar
        screen.fill(BLACK)
        
        # Título
        title_text = font_large.render("NEW HIGH SCORE!", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Ranking
        rank_text = font_medium.render(f"Rank #{rank}", True, WHITE)
        rank_rect = rank_text.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(rank_text, rank_rect)
        
        # Puntuación
        score_text = font_medium.render(f"Score: {score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        screen.blit(score_text, score_rect)
        
        # Prompt
        prompt_text = font_small.render("Enter your name:", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(prompt_text, prompt_rect)
        
        # Cuadro de entrada
        box_width = 300
        box_height = 60
        box_x = (SCREEN_WIDTH - box_width) // 2
        box_y = 350
        pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, YELLOW, (box_x, box_y, box_width, box_height), 3)
        
        # Nombre ingresado
        name_display = name + ("_" if (cursor_blink // 30) % 2 == 0 else " ")
        name_text = font_large.render(name_display, True, WHITE)
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + box_height // 2))
        screen.blit(name_text, name_rect)
        
        # Instrucciones
        instructions = font_small.render("Type name (max 5 chars), ENTER to confirm", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 450))
        screen.blit(instructions, instructions_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

