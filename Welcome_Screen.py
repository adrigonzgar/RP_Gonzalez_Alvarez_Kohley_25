import pygame
import sys
import math
import random

# Configuración de pantalla
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 640
FPS = 60

# Colores temáticos de Donkey Kong
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
DARK_RED = (139, 0, 0)
STEEL_BLUE = (70, 130, 180)
PINK = (255, 192, 203)

def draw_barrel(screen, x, y, size=30):
    """Dibuja un barril estilizado"""
    # Cuerpo del barril
    pygame.draw.ellipse(screen, BROWN, (x, y, size, size))
    pygame.draw.ellipse(screen, DARK_RED, (x+2, y+2, size-4, size-4))
    # Líneas del barril
    pygame.draw.line(screen, BROWN, (x, y+size//3), (x+size, y+size//3), 2)
    pygame.draw.line(screen, BROWN, (x, y+2*size//3), (x+size, y+2*size//3), 2)

def draw_ladder(screen, x, y, height=100, width=20):
    """Dibuja una escalera"""
    # Lados de la escalera
    pygame.draw.rect(screen, YELLOW, (x, y, 4, height))
    pygame.draw.rect(screen, YELLOW, (x+width-4, y, 4, height))
    # Peldaños
    for i in range(0, height, 15):
        pygame.draw.rect(screen, YELLOW, (x, y+i, width, 3))

def draw_girder(screen, x, y, width=200, height=15):
    """Dibuja una viga de construcción"""
    pygame.draw.rect(screen, STEEL_BLUE, (x, y, width, height))
    pygame.draw.rect(screen, BLUE, (x+2, y+2, width-4, height-4))
    # Remaches
    for i in range(x+10, x+width-10, 20):
        pygame.draw.circle(screen, WHITE, (i, y+height//2), 3)

def draw_animated_background(screen, frame_count):
    """Dibuja elementos de fondo animados"""
    # Barriles cayendo
    for i in range(3):
        barrel_x = 100 + i * 300 + (frame_count * 2) % 200
        barrel_y = 50 + math.sin(frame_count * 0.05 + i) * 20
        draw_barrel(screen, int(barrel_x), int(barrel_y), 25)
    
    # Vigas estructurales
    draw_girder(screen, 50, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 100)
    draw_girder(screen, 100, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 200)
    draw_girder(screen, 150, SCREEN_HEIGHT - 300, SCREEN_WIDTH - 300)
    
    # Escaleras
    draw_ladder(screen, 200, SCREEN_HEIGHT - 200, 100)
    draw_ladder(screen, SCREEN_WIDTH - 250, SCREEN_HEIGHT - 300, 100)
    
    # Donkey Kong silueta (simple)
    kong_x = SCREEN_WIDTH - 150
    kong_y = SCREEN_HEIGHT - 320
    # Cuerpo
    pygame.draw.ellipse(screen, BROWN, (kong_x, kong_y, 60, 80))
    # Brazos
    pygame.draw.ellipse(screen, BROWN, (kong_x-20, kong_y+20, 30, 40))
    pygame.draw.ellipse(screen, BROWN, (kong_x+50, kong_y+20, 30, 40))
    # Cara
    pygame.draw.ellipse(screen, ORANGE, (kong_x+10, kong_y+5, 40, 35))

def create_sound_manager():
    """Prepara el sistema de sonido para futuras implementaciones"""
    try:
        pygame.mixer.init()
        return True
    except:
        print("Sistema de sonido no disponible")
        return False

def welcome_screen(screen, clock):
    font_title = pygame.font.Font(None, 90)
    font_sub = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 30)

    waiting = True
    frame_count = 0
    
    while waiting:
        frame_count += 1
        
        # Fondo degradado
        for y in range(SCREEN_HEIGHT):
            color_intensity = int(20 + (y / SCREEN_HEIGHT) * 30)
            color = (color_intensity, color_intensity//2, color_intensity//3)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Elementos de fondo animados
        draw_animated_background(screen, frame_count)

        # Título con efecto de color dinámico
        title_color_r = int(255 * (0.5 + 0.5 * math.sin(frame_count * 0.1)))
        title_color_g = int(100 + 155 * (0.5 + 0.5 * math.sin(frame_count * 0.15)))
        title_color_b = int(50 + 205 * (0.5 + 0.5 * math.sin(frame_count * 0.08)))
        title_color = (title_color_r, title_color_g, title_color_b)
        
        title_text = font_title.render("DONKEY KONG", True, title_color)
        
        # Efecto de sombra para el título
        shadow_text = font_title.render("DONKEY KONG", True, BLACK)
        screen.blit(shadow_text, (SCREEN_WIDTH//2 - title_text.get_width()//2 + 3, SCREEN_HEIGHT//3 + 3))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//3))

        # Subtítulo con efecto parpadeante
        blink_intensity = int(255 * (0.3 + 0.7 * abs(math.sin(frame_count * 0.2))))
        sub_color = (blink_intensity, blink_intensity, blink_intensity)
        sub_text = font_sub.render("Presiona cualquier tecla para comenzar", True, sub_color)
        screen.blit(sub_text, (SCREEN_WIDTH//2 - sub_text.get_width()//2, SCREEN_HEIGHT//2 + 50))

        # Información adicional
        info_text1 = font_small.render("¡Ayuda a Mario a rescatar a Pauline!", True, YELLOW)
        info_text2 = font_small.render("Evita los barriles y sube las escaleras", True, YELLOW)
        
        screen.blit(info_text1, (SCREEN_WIDTH//2 - info_text1.get_width()//2, SCREEN_HEIGHT//2 + 120))
        screen.blit(info_text2, (SCREEN_WIDTH//2 - info_text2.get_width()//2, SCREEN_HEIGHT//2 + 150))

        # Puntuación alta simulada
        high_score_text = font_small.render("HIGH SCORE: 47500", True, RED)
        screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, SCREEN_HEIGHT - 80))

        # Efectos de partículas (estrellas parpadeantes)
        for i in range(15):
            star_x = random.randint(0, SCREEN_WIDTH)
            star_y = random.randint(0, SCREEN_HEIGHT//4)
            if (frame_count + i * 10) % 60 < 30:  # Parpadeo
                pygame.draw.circle(screen, WHITE, (star_x, star_y), 1)

        pygame.display.flip()
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # cualquier tecla
                waiting = False

def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Donkey Kong - Mini Game")
    clock = pygame.time.Clock()
    
    # Inicializar sistema de sonido
    sound_available = create_sound_manager()
    if sound_available:
        print("Sistema de sonido inicializado correctamente")

    # Pantalla de bienvenida
    welcome_screen(screen, clock)

    # Aquí empieza el juego principal
    running = True
    while running:
        screen.fill((30, 30, 30))  # fondo de prueba
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    initialize_screen()
