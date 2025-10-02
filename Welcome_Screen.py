import pygame
import sys
import os
import math
import random
import time

# Configuración de pantalla
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 640
FPS = 60

# Colores básicos
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# Variables globales para efectos
start_time = time.time()

def load_background_image():
    """Carga la imagen de fondo del Donkey Kong"""
    try:
        if os.path.exists("Pantalla_Carga_DK.jpg"):
            image = pygame.image.load("Pantalla_Carga_DK.jpg")
            # Escalar la imagen al tamaño de la pantalla
            return pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            print("Imagen Pantalla_Carga_DK.jpg no encontrada")
            return None
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return None

def draw_simple_fallback(screen):
    """Pantalla simple si no se puede cargar la imagen"""
    screen.fill(BLACK)
    font_large = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    
    # Título
    title_text = font_large.render("DONKEY KONG", True, RED)
    title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
    screen.blit(title_text, (title_x, SCREEN_HEIGHT // 3))
    
    # Instrucción
    start_text = font_small.render("PRESS ANY KEY TO START", True, YELLOW)
    start_x = SCREEN_WIDTH // 2 - start_text.get_width() // 2
    screen.blit(start_text, (start_x, SCREEN_HEIGHT // 2))

def apply_fade_in_effect(surface, elapsed_time, fade_duration=2.0):
    """Aplica efecto de fade in a una superficie"""
    if elapsed_time < fade_duration:
        alpha = int(255 * (elapsed_time / fade_duration))
        fade_surface = surface.copy()
        fade_surface.set_alpha(alpha)
        return fade_surface
    return surface

def apply_zoom_effect(surface, elapsed_time, zoom_duration=1.5):
    """Aplica efecto de zoom suave de entrada"""
    if elapsed_time < zoom_duration:
        progress = elapsed_time / zoom_duration
        # Curva suave (ease-out)
        zoom_factor = 1.0 + (0.1 * (1 - progress))
        
        original_size = surface.get_size()
        new_width = int(original_size[0] * zoom_factor)
        new_height = int(original_size[1] * zoom_factor)
        
        zoomed = pygame.transform.scale(surface, (new_width, new_height))
        
        # Centrar la imagen zoomeada
        x_offset = (SCREEN_WIDTH - new_width) // 2
        y_offset = (SCREEN_HEIGHT - new_height) // 2
        
        return zoomed, (x_offset, y_offset)
    
    return surface, (0, 0)

def draw_blinking_text(screen, text, font, color, x, y, frame_count, blink_speed=30):
    """Dibuja texto parpadeante"""
    if (frame_count // blink_speed) % 2 == 0:
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
        return True
    return False

def draw_blinking_cursor(screen, x, y, frame_count, blink_speed=25):
    """Dibuja cursor parpadeante clásico"""
    if (frame_count // blink_speed) % 2 == 0:
        pygame.draw.rect(screen, WHITE, (x, y, 12, 20))

def draw_stars_effect(screen, frame_count):
    """Dibuja estrellas parpadeantes en las esquinas"""
    star_positions = [
        (50, 50), (SCREEN_WIDTH-50, 50), (50, SCREEN_HEIGHT-50), (SCREEN_WIDTH-50, SCREEN_HEIGHT-50),
        (100, 80), (SCREEN_WIDTH-100, 80), (80, SCREEN_HEIGHT-100), (SCREEN_WIDTH-80, SCREEN_HEIGHT-100),
        (150, 30), (SCREEN_WIDTH-150, 30), (30, SCREEN_HEIGHT-150), (SCREEN_WIDTH-30, SCREEN_HEIGHT-150)
    ]
    
    for i, (x, y) in enumerate(star_positions):
        # Cada estrella parpadea con diferente timing
        if (frame_count + i * 10) % 60 < 30:
            # Dibujar estrella de 5 puntas simple
            star_size = 3 + int(2 * math.sin(frame_count * 0.1 + i))
            pygame.draw.circle(screen, YELLOW, (x, y), star_size)
            # Efecto de cruz
            pygame.draw.line(screen, WHITE, (x-star_size, y), (x+star_size, y), 1)
            pygame.draw.line(screen, WHITE, (x, y-star_size), (x, y+star_size), 1)

def draw_noise_effect(screen, frame_count, intensity=10):
    """Dibuja efecto de ruido sutil para simular arcade antiguo"""
    if frame_count % 3 == 0:  # Solo cada 3 frames para no ser muy intenso
        for _ in range(intensity):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(200, 255)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (x, y), 1)

def draw_overlay_texts(screen, frame_count):
    """Dibuja textos superpuestos con efectos"""
    font_medium = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 32)
    font_tiny = pygame.font.Font(None, 24)
    
    # Texto principal parpadeante
    press_key_x = SCREEN_WIDTH // 2 - 120
    press_key_y = SCREEN_HEIGHT - 100
    draw_blinking_text(screen, "PRESS ANY KEY", font_medium, YELLOW, 
                      press_key_x, press_key_y, frame_count, 40)
    
    # Cursor parpadeante después del texto
    cursor_x = press_key_x + 240
    cursor_y = press_key_y + 5
    draw_blinking_cursor(screen, cursor_x, cursor_y, frame_count)
    
    # Puntuación alta en esquina superior derecha
    high_score_text = font_small.render("HI-SCORE", True, RED)
    screen.blit(high_score_text, (SCREEN_WIDTH - 150, 20))
    score_text = font_small.render("047500", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 130, 50))
    
    # Mensaje de bienvenida con fade
    welcome_alpha = int(128 + 127 * math.sin(frame_count * 0.05))
    welcome_color = (*CYAN[:3], welcome_alpha) if len(CYAN) == 3 else CYAN
    welcome_surface = font_small.render("WELCOME TO DONKEY KONG", True, CYAN)
    welcome_surface.set_alpha(welcome_alpha)
    welcome_x = SCREEN_WIDTH // 2 - welcome_surface.get_width() // 2
    screen.blit(welcome_surface, (welcome_x, 30))
    
    # Créditos discretos
    credits_text = font_tiny.render("(C) 1981 NINTENDO - RECREATED", True, WHITE)
    credits_x = SCREEN_WIDTH // 2 - credits_text.get_width() // 2
    screen.blit(credits_text, (credits_x, SCREEN_HEIGHT - 30))

def prepare_sound_system():
    """Prepara el sistema de sonido para futuras implementaciones"""
    try:
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        return True
    except:
        print("Sistema de sonido no disponible")
        return False


def welcome_screen(screen, clock):
    # Cargar la imagen de fondo
    background_image = load_background_image()
    
    # Preparar sistema de sonido
    sound_available = prepare_sound_system()
    
    waiting = True
    frame_count = 0
    screen_start_time = time.time()
    
    while waiting:
        frame_count += 1
        elapsed_time = time.time() - screen_start_time
        
        # Limpiar pantalla
        screen.fill(BLACK)
        
        if background_image:
            # Aplicar efectos de transición a la imagen
            current_image = background_image.copy()
            
            # Efecto de fade in
            current_image = apply_fade_in_effect(current_image, elapsed_time, 1.5)
            
            # Efecto de zoom suave
            zoomed_image, offset = apply_zoom_effect(current_image, elapsed_time, 1.0)
            
            # Mostrar la imagen con efectos
            screen.blit(zoomed_image, offset)
        else:
            # Usar pantalla de fallback si no se puede cargar la imagen
            draw_simple_fallback(screen)
        
        # Agregar efectos visuales superpuestos
        draw_stars_effect(screen, frame_count)
        draw_noise_effect(screen, frame_count, 5)  # Ruido sutil
        draw_overlay_texts(screen, frame_count)
        
        # Efecto de parpadeo sutil de toda la pantalla (muy ocasional)
        if frame_count % 300 == 0:  # Cada 5 segundos aproximadamente
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.fill(WHITE)
            flash_surface.set_alpha(30)
            screen.blit(flash_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

        # Eventos mejorados
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Efecto visual al presionar tecla
                flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                flash_surface.fill(YELLOW)
                flash_surface.set_alpha(50)
                screen.blit(flash_surface, (0, 0))
                pygame.display.flip()
                pygame.time.wait(100)  # Breve pausa para el efecto
                waiting = False

def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Donkey Kong - Enhanced Edition")
    clock = pygame.time.Clock()

    # Pantalla de bienvenida mejorada con tu imagen
    welcome_screen(screen, clock)

    # Aquí empieza el juego principal
    running = True
    game_start_time = time.time()
    
    while running:
        screen.fill(BLACK)
        
        # Texto temporal para el juego con efectos
        font_large = pygame.font.Font(None, 48)
        font_small = pygame.font.Font(None, 32)
        
        game_text = font_large.render("GAME STARTS HERE", True, WHITE)
        screen.blit(game_text, (SCREEN_WIDTH//2 - game_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        # Instrucciones temporales
        instruction_text = font_small.render("Press ESC to exit", True, YELLOW)
        screen.blit(instruction_text, (SCREEN_WIDTH//2 - instruction_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        
        # Tiempo transcurrido
        elapsed = time.time() - game_start_time
        time_text = font_small.render(f"Time: {elapsed:.1f}s", True, GREEN)
        screen.blit(time_text, (20, 20))
        
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()

if __name__ == "__main__":
    initialize_screen()
