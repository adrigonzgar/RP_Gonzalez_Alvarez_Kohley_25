import pygame
import sys

# Configuración de pantalla
SCREEN_WIDTH = 896
SCREEN_HEIGHT = 640
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (160, 32, 240)

def welcome_screen(screen, clock):
    font_title = pygame.font.Font(None, 90)
    font_sub = pygame.font.Font(None, 50)

    title_text = font_title.render("DONKEY KONG", True, PURPLE)
    sub_text = font_sub.render("Pulsa cualquier tecla para empezar", True, WHITE)

    waiting = True
    while waiting:
        screen.fill(BLACK)

        # Dibujar textos centrados
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//3))
        screen.blit(sub_text, (SCREEN_WIDTH//2 - sub_text.get_width()//2, SCREEN_HEIGHT//2))

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
