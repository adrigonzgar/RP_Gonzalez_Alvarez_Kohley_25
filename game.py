import pygame
import sys
import time
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, GREEN, BLUE
from Welcome_Screen import welcome_screen
from player import Player
from game_manager import GameManager, DemoPlayer
from game_over import show_game_over_screen
from victory_screen import show_victory_screen
from loading_screen import show_loading_screen

def show_level_selector(screen, clock):
    """
    Muestra un selector de niveles para testing
    
    Returns:
        int: Número del nivel seleccionado (1-5)
    """
    selected_level = 1
    max_level = 5
    
    # Fuentes
    font_large = pygame.font.Font(None, 64)
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    
    # Colores
    SELECTOR_BG = (30, 30, 30)
    SELECTOR_BORDER = (100, 100, 100)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    selected_level = max(1, selected_level - 1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    selected_level = min(max_level, selected_level + 1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return selected_level
                elif event.key == pygame.K_ESCAPE:
                    return 1  # Volver al nivel 1 por defecto
        
        # Dibujar fondo
        screen.fill(BLACK)
        
        # Título
        title_text = font_large.render("SELECT LEVEL", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        
        # Dibujar niveles
        level_spacing = 120
        start_x = (SCREEN_WIDTH - (max_level * level_spacing)) // 2 + 60
        
        for level in range(1, max_level + 1):
            x = start_x + (level - 1) * level_spacing
            y = SCREEN_HEIGHT // 2
            
            # Dibujar cuadro del nivel
            box_size = 80
            box_rect = pygame.Rect(x - box_size//2, y - box_size//2, box_size, box_size)
            
            if level == selected_level:
                # Nivel seleccionado - resaltado
                pygame.draw.rect(screen, YELLOW, box_rect)
                pygame.draw.rect(screen, WHITE, box_rect, 4)
                level_color = BLACK
            else:
                # Nivel no seleccionado
                pygame.draw.rect(screen, SELECTOR_BG, box_rect)
                pygame.draw.rect(screen, SELECTOR_BORDER, box_rect, 2)
                level_color = WHITE
            
            # Número del nivel
            level_text = font_large.render(str(level), True, level_color)
            level_text_rect = level_text.get_rect(center=(x, y))
            screen.blit(level_text, level_text_rect)
            
            # Nombre del nivel debajo
            level_names = ["Tutorial", "Speed Up", "Moving", "Vertical", "Gauntlet"]
            name_text = font_small.render(level_names[level - 1], True, WHITE if level != selected_level else YELLOW)
            name_rect = name_text.get_rect(center=(x, y + 60))
            screen.blit(name_text, name_rect)
        
        # Instrucciones
        instructions = font_small.render("Use ← → to select, ENTER to start, ESC to cancel", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        screen.blit(instructions, instructions_rect)
        
        # Indicador de flechas
        if selected_level > 1:
            left_arrow = font_large.render("◄", True, YELLOW)
            screen.blit(left_arrow, (start_x - 100, SCREEN_HEIGHT // 2 - 30))
        
        if selected_level < max_level:
            right_arrow = font_large.render("►", True, YELLOW)
            screen.blit(right_arrow, (start_x + (max_level - 1) * level_spacing + 80, SCREEN_HEIGHT // 2 - 30))
        
        pygame.display.flip()
        clock.tick(FPS)

def show_level_complete_message(screen, clock, next_level):
    """
    Muestra un mensaje parpadeante de nivel completado
    
    Args:
        screen: Superficie de pygame
        clock: Reloj de pygame
        next_level: Número del siguiente nivel
    """
    # Duración del mensaje (2 segundos)
    duration = 2.0
    start_time = time.time()
    
    # Guardar el contenido actual de la pantalla
    screen_copy = screen.copy()
    
    # Fuentes
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 48)
    
    while time.time() - start_time < duration:
        # Calcular el parpadeo
        elapsed = time.time() - start_time
        blink = int(elapsed * 8) % 2  # Parpadea 8 veces por segundo
        
        # Restaurar la pantalla original
        screen.blit(screen_copy, (0, 0))
        
        # Crear overlay semitransparente
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        # Dibujar mensaje si está en fase visible del parpadeo
        if blink == 1:
            # Texto principal
            level_text = font_large.render(f"LEVEL {next_level}", True, YELLOW)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            
            # Sombra del texto
            shadow_text = font_large.render(f"LEVEL {next_level}", True, (50, 50, 0))
            shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 27))
            screen.blit(shadow_text, shadow_rect)
            screen.blit(level_text, level_rect)
            
            # Texto secundario
            complete_text = font_medium.render("LEVEL COMPLETE!", True, WHITE)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(complete_text, complete_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Procesar eventos para evitar que el programa se congele
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def main_game_loop(screen, clock, is_fullscreen, starting_level=1):
    """Loop principal del juego Donkey Kong"""
    running = True
    game_start_time = time.time()
    current_screen = screen
    current_fullscreen = is_fullscreen
    
    # Crear superficie virtual para renderizar el juego
    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Crear el jugador (Mario) - Inicia en el centro, cayendo desde arriba
    player = Player(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Crear el gestor del juego
    game_manager = GameManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Establecer el nivel inicial
    game_manager.level = starting_level
    game_manager.initialize_level()
    
    # Variables del juego
    dt = clock.get_time() / 1000.0  # Delta time en segundos
    
    while running:
        dt = clock.get_time() / 1000.0
        
        # Obtener teclas presionadas
        keys_pressed = pygame.key.get_pressed()
        
        # Actualizar jugador
        player.update(keys_pressed, game_manager.get_platforms(), game_manager.get_ladders(), dt, game_manager.get_moving_platforms())
        
        # Actualizar lógica del juego
        level_completed = game_manager.update(player)
        
        # Verificar si se completó el nivel
        if level_completed:
            # Verificar si completó el nivel 5 (último nivel)
            if game_manager.level >= 5:
                # Calcular tiempo total jugado
                total_time = time.time() - game_start_time
                
                # Obtener estadísticas finales
                player_stats = player.get_stats()
                game_manager_stats = {
                    'score': game_manager.get_score(),
                    'level': game_manager.level,
                    'barrels_dodged': getattr(game_manager, 'barrels_dodged', 0),
                    'powerups_collected': getattr(game_manager, 'powerups_collected', 0)
                }
                
                # Mostrar pantalla de victoria
                show_victory_screen(screen, clock, player_stats, game_manager_stats, total_time)
                
                # Volver al menú principal
                return
            else:
                # Mostrar mensaje de nivel completado
                show_level_complete_message(screen, clock, game_manager.level + 1)
                
                # Avanzar al siguiente nivel
                game_manager.level += 1
                game_manager.initialize_level()
                
                # Resetear posición del jugador - cayendo desde el centro
                player.reset_position(SCREEN_WIDTH // 2 - 12, SCREEN_HEIGHT // 2)
        
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
        
        # Dibujar todo en la superficie virtual
        game_surface.fill(BLACK)
        
        # Dibujar el mapa y todos sus elementos
        game_manager.draw(game_surface)
        
        # Dibujar jugador
        player.draw(game_surface)
        
        # UI del juego
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 24)
        
        # Estadísticas del jugador
        stats = player.get_stats()
        total_score = stats['score'] + game_manager.get_score()
        
        score_text = font_small.render(f"Score: {total_score}", True, WHITE)
        level_text = font_small.render(f"Level: {game_manager.level}", True, WHITE)
        
        game_surface.blit(score_text, (20, 20))
        # Dibujar corazones en lugar del texto de vidas
        game_manager.draw_hearts(game_surface, stats['lives'], 20, 50)
        game_surface.blit(level_text, (20, 80))
        
        # Mostrar número de barriles activos
        barrel_count = len(game_manager.barrels)
        barrel_text = font_tiny.render(f"Barrels: {barrel_count}", True, RED)
        game_surface.blit(barrel_text, (20, 110))
        
        # Controles
        controls_text = font_tiny.render("Controls: WASD/Arrows, Space=jump, ESC=exit, R=menu, F11=fullscreen", True, WHITE)
        game_surface.blit(controls_text, (20, SCREEN_HEIGHT - 30))
        
        # Tiempo transcurrido
        elapsed = time.time() - game_start_time
        time_text = font_tiny.render(f"Game Time: {elapsed:.1f}s", True, GREEN)
        game_surface.blit(time_text, (SCREEN_WIDTH - 150, 20))
        
        # Escalar y dibujar en la pantalla real
        if current_fullscreen:
            # Calcular escala para mantener aspecto
            screen_w, screen_h = current_screen.get_size()
            scale_x = screen_w / SCREEN_WIDTH
            scale_y = screen_h / SCREEN_HEIGHT
            scale = min(scale_x, scale_y)
            
            new_w = int(SCREEN_WIDTH * scale)
            new_h = int(SCREEN_HEIGHT * scale)
            
            scaled_surface = pygame.transform.scale(game_surface, (new_w, new_h))
            
            # Centrar en pantalla
            x = (screen_w - new_w) // 2
            y = (screen_h - new_h) // 2
            
            current_screen.fill(BLACK)
            current_screen.blit(scaled_surface, (x, y))
        else:
            current_screen.blit(game_surface, (0, 0))
        
        pygame.display.flip()
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Detectar cuando se maximiza la ventana (botón maximizar)
                # Si la ventana se redimensiona a casi el tamaño de la pantalla, ir a fullscreen
                if not current_fullscreen:
                    info = pygame.display.Info()
                    if event.w >= info.current_w - 100 and event.h >= info.current_h - 100:
                        current_screen, current_fullscreen = toggle_fullscreen(current_screen, current_fullscreen)
                    else:
                        # Actualizar el tamaño de la ventana
                        current_screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    # Alternar pantalla completa
                    current_screen, current_fullscreen = toggle_fullscreen(current_screen, current_fullscreen)
                elif event.key == pygame.K_r:
                    # Volver a la pantalla de bienvenida
                    welcome_screen(screen, clock)
                    game_start_time = time.time()  # Reiniciar contador
                elif event.key == pygame.K_SPACE:
                    # Salto adicional con barra espaciadora
                    player.jump()

def demo_game_loop(screen, clock):
    """Loop del juego en modo demo (automático)"""
    # Crear el jugador (Mario) - Inicia en el centro, cayendo desde arriba
    player = Player(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
    
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
        player.update(demo_keys, game_manager.get_platforms(), game_manager.get_ladders(), dt, game_manager.get_moving_platforms())
        
        # Actualizar lógica del juego
        game_manager.update(player)
        
        # Si el jugador muere en demo, reiniciar
        if player.lives <= 0:
            player = Player(SCREEN_WIDTH // 2 - 12, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT)
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
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    return  # Terminar demo y volver al menú

def toggle_fullscreen(screen, is_fullscreen):
    """
    Alterna entre pantalla completa y modo ventana
    
    Args:
        screen: Superficie actual de pygame
        is_fullscreen: Estado actual de pantalla completa
        
    Returns:
        tuple: (nueva_pantalla, nuevo_estado_fullscreen)
    """
    if is_fullscreen:
        # Cambiar a modo ventana
        new_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        # Cambiar a pantalla completa (obtener resolución nativa)
        new_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    pygame.display.set_caption("Donkey Kong")
    return new_screen, not is_fullscreen

def main():
    """Función principal del programa"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Donkey Kong")
    clock = pygame.time.Clock()
    is_fullscreen = False  # Estado de pantalla completa
    
    # Mostrar pantalla de carga al inicio
    initialization_steps = [
        (lambda: pygame.mixer.init(), "Initializing audio system"),
        (lambda: pygame.font.init(), "Loading fonts"),
        (lambda: time.sleep(0.2), "Loading game resources"),
        (lambda: time.sleep(0.2), "Loading level configurations"),
        (lambda: time.sleep(0.2), "Preparing game engine"),
        (lambda: time.sleep(0.2), "Loading sprites and graphics"),
        (lambda: time.sleep(0.2), "Setting up game world"),
        (lambda: time.sleep(0.1), "Finalizing initialization"),
    ]
    
    show_loading_screen(screen, clock, initialization_steps)
    
    # Loop principal del programa
    while True:
        # Mostrar pantalla de bienvenida
        mode = welcome_screen(screen, clock)
        
        if mode == "demo":
            # Iniciar modo demo
            demo_game_loop(screen, clock)
        elif mode == "level_select":
            # Mostrar selector de niveles
            selected_level = show_level_selector(screen, clock)
            # Iniciar el juego en el nivel seleccionado
            main_game_loop(screen, clock, is_fullscreen, selected_level)
        else:
            # Iniciar el juego principal desde nivel 1
            main_game_loop(screen, clock, is_fullscreen, 1)
        
        # Si llegamos aquí, volver a la pantalla de bienvenida

if __name__ == "__main__":
    main()
