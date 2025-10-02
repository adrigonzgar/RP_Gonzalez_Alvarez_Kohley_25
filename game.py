import pygame
import sys
import time
from Welcome_Screen import welcome_screen, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, YELLOW
from player import Player
from game_manager import GameManager

# Colores adicionales que necesitamos
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

def main_game_loop(screen, clock):
    """Loop principal del juego Donkey Kong"""
    running = True
    game_start_time = time.time()
    
    # Crear el jugador (Mario)
    player = Player(100, SCREEN_HEIGHT - 200, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Crear el gestor del juego
    game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Variables del juego
    dt = clock.get_time() / 1000.0  # Delta time en segundos
    
    while running:
        dt = clock.get_time() / 1000.0
        
        # Obtener teclas presionadas
        keys_pressed = pygame.key.get_pressed()
        
        # Actualizar jugador
        player.update(keys_pressed, game_manager.get_platforms(), game_manager.get_ladders(), dt)
        
        # Actualizar lógica del juego
        game_manager.update(player)
        
        # Dibujar todo
        screen.fill(BLACK)
        
        # Dibujar el mapa y todos sus elementos
        game_manager.draw(screen)
        
        # Dibujar jugador
        player.draw(screen)
        
        # UI del juego
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Estadísticas del jugador
        stats = player.get_stats()
        total_score = stats['score'] + game_manager.get_score()
        
        score_text = font_small.render(f"Score: {total_score}", True, WHITE)
        lives_text = font_small.render(f"Lives: {stats['lives']}", True, WHITE)
        level_text = font_small.render(f"Level: {game_manager.level}", True, WHITE)
        
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 50))
        screen.blit(level_text, (20, 80))
        
        # Mostrar número de barriles activos
        barrel_count = len(game_manager.barrels)
        barrel_text = font_tiny.render(f"Barrels: {barrel_count}", True, RED)
        screen.blit(barrel_text, (20, 110))
        
        # Controles
        controls_text = font_tiny.render("Controls: WASD/Arrows to move, Space to jump, ESC to exit, R for welcome", True, WHITE)
        screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
        
        # Tiempo transcurrido
        elapsed = time.time() - game_start_time
        time_text = font_tiny.render(f"Game Time: {elapsed:.1f}s", True, GREEN)
        screen.blit(time_text, (SCREEN_WIDTH - 150, 20))
        
        pygame.display.flip()
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # Volver a la pantalla de bienvenida
                    welcome_screen(screen, clock)
                    game_start_time = time.time()  # Reiniciar contador
                elif event.key == pygame.K_SPACE:
                    # Salto adicional con barra espaciadora
                    player.jump()

def main():
    """Función principal del programa"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Donkey Kong")
    clock = pygame.time.Clock()
    
    # Mostrar pantalla de bienvenida primero
    welcome_screen(screen, clock)
    
    # Luego iniciar el juego principal
    main_game_loop(screen, clock)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


