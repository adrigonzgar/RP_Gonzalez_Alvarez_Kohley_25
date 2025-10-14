"""
Loading Screen Module - Donkey Kong Game
========================================
Este módulo maneja la pantalla de carga con barra de progreso
mientras se inicializan los recursos del juego.
"""

import pygame
import time
import math
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, YELLOW, GREEN, BLUE

class LoadingScreen:
    """Clase para manejar la pantalla de carga"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.progress = 0
        self.animation_frame = 0
        
    def draw(self, screen, progress, loading_text="Loading..."):
        """
        Dibuja la pantalla de carga con barra de progreso
        
        Args:
            screen: Superficie de pygame
            progress: Progreso actual (0.0 a 1.0)
            loading_text: Texto a mostrar
        """
        self.animation_frame += 1
        
        # Fondo oscuro
        screen.fill(BLACK)
        
        # Fuentes
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        # Título del juego
        title_text = font_large.render("DONKEY KONG", True, RED)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        
        # Sombra del título
        shadow_text = font_large.render("DONKEY KONG", True, (80, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 3, 153))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Texto de carga con puntos animados
        dots = "." * ((self.animation_frame // 15) % 4)
        loading_display = loading_text + dots
        loading_text_render = font_medium.render(loading_display, True, WHITE)
        loading_rect = loading_text_render.get_rect(center=(SCREEN_WIDTH // 2, 250))
        screen.blit(loading_text_render, loading_rect)
        
        # Barra de progreso
        bar_width = 500
        bar_height = 40
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 350
        
        # Fondo de la barra (oscuro)
        background_rect = pygame.Rect(bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10)
        pygame.draw.rect(screen, (50, 50, 50), background_rect)
        pygame.draw.rect(screen, WHITE, background_rect, 2)
        
        # Barra de progreso (relleno)
        progress_width = int(bar_width * progress)
        if progress_width > 0:
            # Gradiente de color según el progreso
            if progress < 0.33:
                bar_color = RED
            elif progress < 0.66:
                bar_color = YELLOW
            else:
                bar_color = GREEN
            
            progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
            pygame.draw.rect(screen, bar_color, progress_rect)
            
            # Efecto de brillo en la barra
            shine_offset = (self.animation_frame * 3) % (progress_width + 50)
            if shine_offset < progress_width:
                shine_rect = pygame.Rect(bar_x + shine_offset - 25, bar_y, 50, bar_height)
                shine_surface = pygame.Surface((50, bar_height))
                shine_surface.fill(WHITE)
                shine_surface.set_alpha(100)
                screen.blit(shine_surface, shine_rect)
        
        # Borde de la barra
        border_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, WHITE, border_rect, 3)
        
        # Porcentaje
        percentage = int(progress * 100)
        percentage_text = font_small.render(f"{percentage}%", True, WHITE)
        percentage_rect = percentage_text.get_rect(center=(SCREEN_WIDTH // 2, bar_y + bar_height + 40))
        screen.blit(percentage_text, percentage_rect)
        
        # Elementos decorativos - barril giratorio
        barrel_x = SCREEN_WIDTH // 2 - 250
        barrel_y = 450
        self.draw_spinning_barrel(screen, barrel_x, barrel_y)
        
        # Mario corriendo
        mario_x = SCREEN_WIDTH // 2 + 200
        mario_y = 450
        self.draw_running_mario(screen, mario_x, mario_y)
        
        pygame.display.flip()
    
    def draw_spinning_barrel(self, screen, x, y):
        """Dibuja un barril giratorio decorativo"""
        brown = (139, 69, 19)
        dark_brown = (101, 67, 33)
        
        # Rotación
        rotation = (self.animation_frame * 5) % 360
        
        # Cuerpo del barril
        size = 30
        pygame.draw.circle(screen, brown, (x, y), size)
        pygame.draw.circle(screen, dark_brown, (x, y), size - 5)
        
        # Líneas del barril (rotadas)
        for i in range(4):
            angle = rotation + (i * 90)
            end_x = x + int(size * 0.8 * math.cos(math.radians(angle)))
            end_y = y + int(size * 0.8 * math.sin(math.radians(angle)))
            pygame.draw.line(screen, BLACK, (x, y), (end_x, end_y), 3)
    
    def draw_running_mario(self, screen, x, y):
        """Dibuja a Mario corriendo en el lugar"""
        # Animación de piernas
        leg_offset = int(5 * math.sin(self.animation_frame * 0.3))
        
        # Colores
        red = (255, 0, 0)
        blue = (0, 0, 255)
        skin = (255, 220, 177)
        
        # Gorra
        pygame.draw.rect(screen, red, (x - 8, y - 15, 16, 8))
        
        # Cara
        pygame.draw.rect(screen, skin, (x - 8, y - 7, 16, 8))
        
        # Cuerpo
        pygame.draw.rect(screen, blue, (x - 10, y + 1, 20, 12))
        
        # Piernas (animadas)
        pygame.draw.rect(screen, blue, (x - 8 - leg_offset, y + 13, 6, 8))
        pygame.draw.rect(screen, blue, (x + 2 + leg_offset, y + 13, 6, 8))

def show_loading_screen(screen, clock, initialization_steps):
    """
    Muestra la pantalla de carga mientras se inicializan los recursos
    
    Args:
        screen: Superficie de pygame
        clock: Reloj de pygame
        initialization_steps: Lista de tuplas (función, descripción) a ejecutar
        
    Returns:
        dict: Resultados de las inicializaciones
    """
    loading = LoadingScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    results = {}
    
    total_steps = len(initialization_steps)
    
    for i, (init_func, description) in enumerate(initialization_steps):
        # Calcular progreso
        progress = i / total_steps
        
        # Dibujar pantalla de carga
        loading.draw(screen, progress, description)
        
        # Ejecutar paso de inicialización
        try:
            result = init_func()
            results[description] = result
        except Exception as e:
            print(f"Error en inicialización: {description} - {e}")
            results[description] = None
        
        # Pequeña pausa para que se vea la animación
        time.sleep(0.1)
        clock.tick(FPS)
    
    # Mostrar 100% completado
    loading.draw(screen, 1.0, "Complete!")
    time.sleep(0.5)
    
    return results

