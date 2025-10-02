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

def welcome_screen(screen, clock):
    """Pantalla de bienvenida simple con imagen de fondo"""
    # Cargar la imagen de fondo
    background_image = load_background_image()
    
    font_sub = pygame.font.Font(None, 50)
    sub_text = font_sub.render("Pulsa cualquier tecla para empezar", True, WHITE)

    waiting = True
    while waiting:
        if background_image:
            # Mostrar la imagen de fondo
            screen.blit(background_image, (0, 0))
        else:
            # Pantalla negra simple si no hay imagen
            screen.fill(BLACK)
            # Título de fallback
            font_title = pygame.font.Font(None, 90)
            title_text = font_title.render("DONKEY KONG", True, RED)
            screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//3))

        # Texto de instrucción (siempre visible)
        screen.blit(sub_text, (SCREEN_WIDTH//2 - sub_text.get_width()//2, SCREEN_HEIGHT - 100))

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
    """Función de compatibilidad para mantener la interfaz anterior"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Donkey Kong - Mini Game")
    clock = pygame.time.Clock()

    # Pantalla de bienvenida
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

# Solo ejecutar si se llama directamente (para testing)
if __name__ == "__main__":
    initialize_screen()

# Welcome_Screen.py: Pantalla de bienvenida simple que usa la imagen Pantalla_Carga_DK.jpg como fondo con funcionalidad básica de navegación.