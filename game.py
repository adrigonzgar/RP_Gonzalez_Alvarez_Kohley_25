import pygame
import sys
import time
from Welcome_Screen import welcome_screen, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, YELLOW
from player import Player
from game_manager import GameManager, DemoPlayer
from game_over import show_game_over_screen

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
        
        # Verificar Game Over
        if player.lives <= 0:
            # Calcular tiempo total jugado
            total_time = time.time() - game_start_time
            
            # Obtener estadísticas
            player_stats = player.get_stats()
            game_manager_stats = {
                'score': game_manager.get_score(),
                'level': game_manager.level,
                'barrels_dodged': getattr(game_manager, 'barrels_dodged', 0),
                'powerups_collected': getattr(game_manager, 'powerups_collected', 0)
            }
            
            # Mostrar pantalla de Game Over
            choice = show_game_over_screen(screen, clock, player_stats, game_manager_stats, total_time)
            
            if choice == 0:  # Regresar al inicio
                return  # Salir del loop para volver al menú principal
            elif choice == 2:  # Salir del juego
                pygame.quit()
                sys.exit()
            # Si choice == 1 (estadísticas), ya se manejó en la función
        
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
        level_text = font_small.render(f"Level: {game_manager.level}", True, WHITE)
        
        screen.blit(score_text, (20, 20))
        # Dibujar corazones en lugar del texto de vidas
        game_manager.draw_hearts(screen, stats['lives'], 20, 50)
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

def demo_game_loop(screen, clock):
    """Loop del juego en modo demo (automático)"""
    # Crear el jugador (Mario)
    player = Player(100, SCREEN_HEIGHT - 200, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Crear el gestor del juego
    game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Crear el jugador automático para la demo
    demo_player = DemoPlayer(player, game_manager.get_platforms(), game_manager.get_ladders(), game_manager)
    
    # Variables del juego
    dt = clock.get_time() / 1000.0
    demo_duration = 60.0  # 60 segundos de demo
    demo_start_time = time.time()
    
    while True:
        dt = clock.get_time() / 1000.0
        elapsed_demo_time = time.time() - demo_start_time
        
        # Terminar demo después del tiempo límite
        if elapsed_demo_time >= demo_duration:
            return
        
        # Obtener input automático de la demo
        demo_keys = demo_player.update()
        
        # Actualizar jugador con input automático
        player.update(demo_keys, game_manager.get_platforms(), game_manager.get_ladders(), dt)
        
        # Actualizar lógica del juego
        game_manager.update(player)
        
        # Si el jugador muere en demo, reiniciar
        if player.lives <= 0:
            player = Player(100, SCREEN_HEIGHT - 200, SCREEN_WIDTH, SCREEN_HEIGHT)
            game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
            demo_player = DemoPlayer(player, game_manager.get_platforms(), game_manager.get_ladders(), game_manager)
        
        # Dibujar todo
        screen.fill(BLACK)
        
        # Dibujar el mapa y todos sus elementos
        game_manager.draw(screen)
        
        # Dibujar jugador
        player.draw(screen)
        
        # UI de la demo
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Indicador de DEMO
        demo_text = font_large.render("DEMO", True, RED)
        screen.blit(demo_text, (20, 20))
        
        # Estadísticas básicas
        stats = player.get_stats()
        total_score = stats['score'] + game_manager.get_score()
        
        score_text = font_small.render(f"Score: {total_score}", True, WHITE)
        level_text = font_small.render(f"Level: {game_manager.level}", True, WHITE)
        
        screen.blit(score_text, (20, 60))
        # Dibujar corazones en lugar del texto de vidas
        game_manager.draw_hearts(screen, stats['lives'], 20, 90)
        screen.blit(level_text, (20, 120))
        
        # Tiempo restante de demo
        time_left = demo_duration - elapsed_demo_time
        time_text = font_tiny.render(f"Demo termina en: {time_left:.1f}s", True, YELLOW)
        screen.blit(time_text, (SCREEN_WIDTH - 250, 20))
        
        # Instrucción para salir
        exit_text = font_tiny.render("Presiona cualquier tecla para jugar", True, GREEN)
        screen.blit(exit_text, (SCREEN_WIDTH//2 - exit_text.get_width()//2, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

        # Eventos - cualquier tecla termina la demo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return  # Terminar demo y volver al menú

def main():
    """Función principal del programa"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Donkey Kong")
    clock = pygame.time.Clock()
    
    # Loop principal del programa
    while True:
        # Mostrar pantalla de bienvenida
        mode = welcome_screen(screen, clock)
        
        if mode == "demo":
            # Iniciar modo demo
            demo_game_loop(screen, clock)
        else:
            # Iniciar el juego principal
            main_game_loop(screen, clock)
        
        # Si llegamos aquí, volver a la pantalla de bienvenida

if __name__ == "__main__":
    main()
