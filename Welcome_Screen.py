import pygame
import sys
import os

# Configuración de pantalla
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 640
FPS = 60

# Colores básicos
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

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


def welcome_screen(screen, clock):
    # Cargar la imagen de fondo
    background_image = load_background_image()
    
    waiting = True
    
    while waiting:
        if background_image:
            # Mostrar la imagen de fondo
            screen.blit(background_image, (0, 0))
        else:
            # Usar pantalla de fallback si no se puede cargar la imagen
            draw_simple_fallback(screen)

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
    pygame.display.set_caption("Donkey Kong")
    clock = pygame.time.Clock()

    # Pantalla de bienvenida con tu imagen
    welcome_screen(screen, clock)

    # Aquí empieza el juego principal
    running = True
    while running:
        screen.fill(BLACK)
        
        # Texto temporal para el juego
        font = pygame.font.Font(None, 48)
        game_text = font.render("GAME STARTS HERE", True, WHITE)
        screen.blit(game_text, (SCREEN_WIDTH//2 - game_text.get_width()//2, SCREEN_HEIGHT//2))
        
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    initialize_screen()
