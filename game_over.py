"""
Game Over Module - Donkey Kong Game
==================================
Este módulo maneja la pantalla de Game Over con las siguientes opciones:
- Regresar al inicio (volver a la pantalla de bienvenida)
- Ver estadísticas del juego
- Salir del juego
- Interfaz de navegación con teclado
- Animaciones y efectos visuales
"""

import pygame
import sys
import time
import math

class GameOverScreen:
    """Clase para manejar la pantalla de Game Over"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Colores
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 100, 255)
        self.GRAY = (128, 128, 128)
        
        # Opciones del menú
        self.menu_options = [
            "REGRESAR AL INICIO",
            "VER ESTADISTICAS", 
            "SALIR DEL JUEGO"
        ]
        
        self.selected_option = 0
        self.animation_frame = 0
        self.blink_timer = 0
        
        # Estadísticas del juego
        self.game_stats = {
            'final_score': 0,
            'level_reached': 1,
            'time_played': 0,
            'barrels_dodged': 0,
            'powerups_collected': 0,
            'lives_lost': 0
        }

    def update_stats(self, player_stats, game_manager_stats, time_played):
        """Actualiza las estadísticas del juego"""
        self.game_stats = {
            'final_score': player_stats.get('score', 0) + game_manager_stats.get('score', 0),
            'level_reached': game_manager_stats.get('level', 1),
            'time_played': time_played,
            'barrels_dodged': game_manager_stats.get('barrels_dodged', 0),
            'powerups_collected': game_manager_stats.get('powerups_collected', 0),
            'lives_lost': 3 - player_stats.get('lives', 0)
        }

    def handle_input(self, keys_pressed, events):
        """Maneja la entrada del usuario"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.selected_option  # Retorna la opción seleccionada
                elif event.key == pygame.K_ESCAPE:
                    return 2  # Salir del juego
        
        return -1  # No se seleccionó nada

    def draw_game_over_title(self, screen):
        """Dibuja el título de Game Over con efectos"""
        font_large = pygame.font.Font(None, 96)
        font_medium = pygame.font.Font(None, 48)
        
        # Efecto de parpadeo en el título
        alpha = int(128 + 127 * math.sin(self.animation_frame * 0.1))
        
        # Título principal
        title_text = font_large.render("GAME OVER", True, self.RED)
        title_x = self.screen_width // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_x, 80))
        
        # Subtítulo
        subtitle_text = font_medium.render("¡Mario ha perdido todas sus vidas!", True, self.WHITE)
        subtitle_x = self.screen_width // 2 - subtitle_text.get_width() // 2
        screen.blit(subtitle_text, (subtitle_x, 160))

    def draw_menu_options(self, screen):
        """Dibuja las opciones del menú"""
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        start_y = 280
        option_spacing = 60
        
        for i, option in enumerate(self.menu_options):
            y_pos = start_y + (i * option_spacing)
            
            # Color y efectos para la opción seleccionada
            if i == self.selected_option:
                # Efecto de parpadeo para la opción seleccionada
                if (self.blink_timer // 15) % 2 == 0:
                    color = self.YELLOW
                    # Dibujar flecha indicadora
                    arrow_text = font_medium.render("►", True, self.YELLOW)
                    screen.blit(arrow_text, (self.screen_width // 2 - 200, y_pos))
                else:
                    color = self.WHITE
            else:
                color = self.GRAY
            
            # Dibujar texto de la opción
            option_text = font_medium.render(option, True, color)
            option_x = self.screen_width // 2 - option_text.get_width() // 2
            screen.blit(option_text, (option_x, y_pos))
        
        # Instrucciones de control
        controls_text = font_small.render("Usa ^/v o WS para navegar, ENTER/SPACE para seleccionar", True, self.WHITE)
        controls_x = self.screen_width // 2 - controls_text.get_width() // 2
        screen.blit(controls_text, (controls_x, start_y + len(self.menu_options) * option_spacing + 40))

    def draw_statistics(self, screen):
        """Dibuja las estadísticas del juego"""
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # Título de estadísticas
        stats_title = font_large.render("ESTADISTICAS", True, self.BLUE)
        title_x = self.screen_width // 2 - stats_title.get_width() // 2
        screen.blit(stats_title, (title_x, 80))
        
        # Estadísticas individuales
        stats_data = [
            f"Puntuación Final: {self.game_stats['final_score']:,}",
            f"Nivel Alcanzado: {self.game_stats['level_reached']}",
            f"Tiempo Jugado: {self.game_stats['time_played']:.1f}s",
            f"Barriles Esquivados: {self.game_stats['barrels_dodged']}",
            f"Power-ups Recolectados: {self.game_stats['powerups_collected']}",
            f"Vidas Perdidas: {self.game_stats['lives_lost']}/3"
        ]
        
        start_y = 180
        line_spacing = 50
        
        for i, stat in enumerate(stats_data):
            y_pos = start_y + (i * line_spacing)
            
            # Alternar colores para mejor legibilidad
            color = self.WHITE if i % 2 == 0 else self.YELLOW
            
            stat_text = font_medium.render(stat, True, color)
            stat_x = self.screen_width // 2 - stat_text.get_width() // 2
            screen.blit(stat_text, (stat_x, y_pos))
        
        # Evaluación del rendimiento
        self.draw_performance_evaluation(screen, start_y + len(stats_data) * line_spacing + 40)
        
        # Instrucción para regresar
        back_text = font_small.render("Presiona cualquier tecla para regresar", True, self.GREEN)
        back_x = self.screen_width // 2 - back_text.get_width() // 2
        screen.blit(back_text, (back_x, self.screen_height - 60))

    def draw_performance_evaluation(self, screen, y_pos):
        """Dibuja una evaluación del rendimiento del jugador"""
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # Calcular evaluación basada en estadísticas
        score = self.game_stats['final_score']
        level = self.game_stats['level_reached']
        
        if score >= 10000 and level >= 3:
            evaluation = "¡EXCELENTE!"
            eval_color = self.GREEN
        elif score >= 5000 and level >= 2:
            evaluation = "¡MUY BIEN!"
            eval_color = self.YELLOW
        elif score >= 1000:
            evaluation = "BIEN"
            eval_color = self.BLUE
        else:
            evaluation = "SIGUE INTENTANDO"
            eval_color = self.RED
        
        # Dibujar evaluación
        eval_text = font_medium.render(f"Evaluación: {evaluation}", True, eval_color)
        eval_x = self.screen_width // 2 - eval_text.get_width() // 2
        screen.blit(eval_text, (eval_x, y_pos))
        
        # Mensaje motivacional
        if evaluation == "¡EXCELENTE!":
            message = "¡Eres un maestro del Donkey Kong!"
        elif evaluation == "¡MUY BIEN!":
            message = "¡Buen trabajo! Casi llegas a la cima."
        elif evaluation == "BIEN":
            message = "No está mal, pero puedes hacerlo mejor."
        else:
            message = "¡No te rindas! La práctica hace al maestro."
        
        message_text = font_small.render(message, True, self.WHITE)
        message_x = self.screen_width // 2 - message_text.get_width() // 2
        screen.blit(message_text, (message_x, y_pos + 50))

    def update(self):
        """Actualiza las animaciones"""
        self.animation_frame += 1
        self.blink_timer += 1

    def draw(self, screen):
        """Dibuja la pantalla de Game Over"""
        screen.fill(self.BLACK)
        self.draw_game_over_title(screen)
        self.draw_menu_options(screen)

    def show_statistics_screen(self, screen, clock):
        """Muestra la pantalla de estadísticas"""
        showing_stats = True
        
        while showing_stats:
            screen.fill(self.BLACK)
            self.draw_statistics(screen)
            
            pygame.display.flip()
            clock.tick(60)
            
            # Esperar a que el usuario presione una tecla
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    showing_stats = False

def show_game_over_screen(screen, clock, player_stats, game_manager_stats, time_played):
    """
    Función principal para mostrar la pantalla de Game Over
    
    Returns:
        0: Regresar al inicio
        1: Ver estadísticas
        2: Salir del juego
    """
    game_over = GameOverScreen(screen.get_width(), screen.get_height())
    game_over.update_stats(player_stats, game_manager_stats, time_played)
    
    running = True
    
    while running:
        # Actualizar animaciones
        game_over.update()
        
        # Obtener eventos
        events = pygame.event.get()
        keys_pressed = pygame.key.get_pressed()
        
        # Manejar cierre de ventana
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Manejar entrada del usuario
        selected = game_over.handle_input(keys_pressed, events)
        
        if selected != -1:
            if selected == 1:  # Ver estadísticas
                game_over.show_statistics_screen(screen, clock)
                # Después de ver estadísticas, volver al menú
            else:
                return selected  # Regresar al inicio (0) o Salir (2)
        
        # Dibujar
        game_over.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    return 2  # Por defecto, salir

# GameOver: Pantalla de fin de juego con opciones de navegación, estadísticas detalladas y evaluación del rendimiento del jugador.
