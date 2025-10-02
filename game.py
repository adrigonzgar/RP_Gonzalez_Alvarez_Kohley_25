import pygame
import sys
import time
from Welcome_Screen import show_welcome_screen, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, GREEN

def main_game_loop(screen, clock):
    """Loop principal del juego Donkey Kong"""
    running = True
    game_start_time = time.time()
    
    while running:
        screen.fill(BLACK)
        
        # Texto temporal para el juego con efectos
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        game_text = font_large.render("DONKEY KONG GAME", True, WHITE)
        screen.blit(game_text, (SCREEN_WIDTH//2 - game_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        # Instrucciones
        instruction_text = font_small.render("Press ESC to exit", True, YELLOW)
        screen.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
        instruction_text2 = font_small.render("Press R to return to welcome screen", True, GREEN)
        screen.blit(instruction_text2, (SCREEN_WIDTH//2 - instruction_text2.get_width()//2, SCREEN_HEIGHT//2 + 50))
        
        # Tiempo transcurrido
        elapsed = time.time() - game_start_time
        time_text = font_small.render(f"Game Time: {elapsed:.1f}s", True, GREEN)
        screen.blit(time_text, (20, 20))
        
        # Placeholder para el juego
        placeholder_text = font_small.render("Here will be the Donkey Kong game logic", True, RED)
        screen.blit(placeholder_text, (SCREEN_WIDTH//2 - placeholder_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
        
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Volver a la pantalla de bienvenida
                    show_welcome_screen(screen, clock)
                    game_start_time = time.time()  # Reiniciar contador

def main():
    """Función principal del programa"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Donkey Kong")
    clock = pygame.time.Clock()
    
    # Mostrar pantalla de bienvenida primero
    show_welcome_screen(screen, clock)
    
    # Luego iniciar el juego principal
    main_game_loop(screen, clock)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
