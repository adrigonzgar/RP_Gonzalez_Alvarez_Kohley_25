"""
Victory Screen Module - Donkey Kong Game
========================================
Este módulo maneja la pantalla de victoria cuando el jugador completa el nivel 5.
Muestra estadísticas finales, animaciones de celebración y opciones para continuar.
"""

import pygame
import sys
import time
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, GREEN, BLUE

class VictoryScreen:
    """Clase para manejar la pantalla de victoria"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.animation_frame = 0
        self.firework_particles = []
        
    def create_firework(self):
        """Crea partículas de fuegos artificiales"""
        x = pygame.math.Vector2(
            pygame.math.Vector2(self.screen_width // 2, self.screen_height // 2).x + 
            (200 * math.cos(self.animation_frame * 0.1)),
            pygame.math.Vector2(self.screen_width // 2, self.screen_height // 2).y + 
            (200 * math.sin(self.animation_frame * 0.1))
        )
        
        for _ in range(20):
            angle = (360 / 20) * _ + self.animation_frame
            speed = 3
            velocity = pygame.math.Vector2(
                speed * math.cos(math.radians(angle)),
                speed * math.sin(math.radians(angle))
            )
            color = [RED, YELLOW, GREEN, BLUE, (255, 0, 255)][_ % 5]
            self.firework_particles.append({
                'pos': x.copy(),
                'vel': velocity,
                'color': color,
                'life': 60
            })
    
    def update_fireworks(self):
        """Actualiza las partículas de fuegos artificiales"""
        for particle in self.firework_particles[:]:
            particle['pos'] += particle['vel']
            particle['vel'].y += 0.1  # Gravedad
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.firework_particles.remove(particle)
    
    def draw_fireworks(self, screen):
        """Dibuja los fuegos artificiales"""
        for particle in self.firework_particles:
            alpha = int(255 * (particle['life'] / 60))
            size = max(1, int(4 * (particle['life'] / 60)))
            pygame.draw.circle(screen, particle['color'], 
                             (int(particle['pos'].x), int(particle['pos'].y)), size)
    
    def draw(self, screen, player_stats, game_stats, total_time):
        """Dibuja la pantalla de victoria"""
        self.animation_frame += 1
        
        # Crear fuegos artificiales periódicamente
        if self.animation_frame % 30 == 0:
            self.create_firework()
        
        # Actualizar y dibujar fuegos artificiales
        self.update_fireworks()
        
        # Fondo con gradiente
        for y in range(self.screen_height):
            color_value = int(20 + (y / self.screen_height) * 40)
            pygame.draw.line(screen, (0, 0, color_value), (0, y), (self.screen_width, y))
        
        # Dibujar fuegos artificiales
        self.draw_fireworks(screen)
        
        # Título principal con animación
        font_huge = pygame.font.Font(None, 96)
        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 36)
        
        # Efecto de rebote en el título
        bounce = int(10 * math.sin(self.animation_frame * 0.1))
        
        # Sombra del título
        victory_shadow = font_huge.render("VICTORY!", True, (50, 50, 0))
        shadow_rect = victory_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, 100 + bounce + 4))
        screen.blit(victory_shadow, shadow_rect)
        
        # Título principal
        victory_text = font_huge.render("VICTORY!", True, YELLOW)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, 100 + bounce))
        screen.blit(victory_text, victory_rect)
        
        # Subtítulo
        subtitle_text = font_large.render("You completed all 5 levels!", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Estadísticas
        stats_y = 260
        total_score = player_stats['score'] + game_stats['score']
        
        stats_data = [
            ("FINAL SCORE", f"{total_score}", YELLOW),
            ("TIME PLAYED", f"{total_time:.1f}s", WHITE),
            ("BARRELS DODGED", f"{game_stats.get('barrels_dodged', 0)}", GREEN),
            ("POWERUPS COLLECTED", f"{game_stats.get('powerups_collected', 0)}", BLUE),
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            y_pos = stats_y + i * 50
            
            # Label
            label_text = font_small.render(label + ":", True, WHITE)
            label_rect = label_text.get_rect(right=SCREEN_WIDTH // 2 - 20, centery=y_pos)
            screen.blit(label_text, label_rect)
            
            # Value
            value_text = font_medium.render(value, True, color)
            value_rect = value_text.get_rect(left=SCREEN_WIDTH // 2 + 20, centery=y_pos)
            screen.blit(value_text, value_rect)
        
        # Mensaje de felicitación
        congrats_text = font_medium.render("Congratulations, Champion!", True, YELLOW)
        congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, 480))
        screen.blit(congrats_text, congrats_rect)
        
        # Instrucciones
        instructions = font_small.render("Press ENTER to return to menu", True, WHITE)
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
        screen.blit(instructions, instructions_rect)

def show_victory_screen(screen, clock, player_stats, game_stats, total_time):
    """
    Función principal para mostrar la pantalla de victoria
    
    Args:
        screen: Superficie de pygame
        clock: Reloj de pygame
        player_stats: Estadísticas del jugador
        game_stats: Estadísticas del game manager
        total_time: Tiempo total jugado
    """
    victory = VictoryScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    while True:
        # Dibujar la pantalla de victoria
        victory.draw(screen, player_stats, game_stats, total_time)
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return  # Volver al menú principal
                elif event.key == pygame.K_ESCAPE:
                    return  # Volver al menú principal

