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


from Welcome_Screen import initialize_screen

if __name__ == "__main__":
    initialize_screen()
