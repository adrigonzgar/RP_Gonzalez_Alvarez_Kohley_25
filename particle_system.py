"""
Particle System Module - Donkey Kong Game
=========================================
Este módulo maneja el sistema de partículas para efectos visuales:
- Polvo al aterrizar
- Chispas al recoger power-ups
- Explosiones al colisionar
- Estelas de movimiento
"""

import pygame
import random
import math

class Particle:
    """Clase para una partícula individual"""
    def __init__(self, x, y, vel_x, vel_y, color, size, lifetime):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 0.2
    
    def update(self):
        """Actualiza la posición y estado de la partícula"""
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += self.gravity
        self.lifetime -= 1
        
        # Reducir tamaño con el tiempo
        self.size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
        
        return self.lifetime > 0
    
    def draw(self, screen):
        """Dibuja la partícula"""
        if self.lifetime > 0:
            # Calcular alpha basado en lifetime
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            
            # Crear superficie con alpha
            particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(particle_surface, color_with_alpha, (self.size, self.size), self.size)
            
            screen.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    """Sistema de gestión de partículas"""
    
    def __init__(self):
        self.particles = []
    
    def update(self):
        """Actualiza todas las partículas"""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen):
        """Dibuja todas las partículas"""
        for particle in self.particles:
            particle.draw(screen)
    
    def create_dust_effect(self, x, y, direction=0):
        """Crea efecto de polvo al aterrizar"""
        colors = [(200, 200, 200), (180, 180, 180), (160, 160, 160)]
        
        for _ in range(8):
            angle = random.uniform(-45, 45) + direction
            speed = random.uniform(1, 3)
            vel_x = speed * math.cos(math.radians(angle))
            vel_y = speed * math.sin(math.radians(angle)) - random.uniform(1, 2)
            
            color = random.choice(colors)
            size = random.randint(2, 4)
            lifetime = random.randint(15, 30)
            
            self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def create_sparkle_effect(self, x, y, color_type='gold'):
        """Crea efecto de chispas al recoger power-ups"""
        if color_type == 'gold':
            colors = [(255, 215, 0), (255, 255, 0), (255, 200, 0)]
        elif color_type == 'red':
            colors = [(255, 0, 0), (255, 100, 100), (255, 50, 50)]
        elif color_type == 'blue':
            colors = [(0, 100, 255), (0, 150, 255), (100, 200, 255)]
        else:
            colors = [(255, 255, 255), (200, 200, 200), (255, 255, 100)]
        
        for _ in range(15):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 5)
            vel_x = speed * math.cos(math.radians(angle))
            vel_y = speed * math.sin(math.radians(angle))
            
            color = random.choice(colors)
            size = random.randint(2, 5)
            lifetime = random.randint(20, 40)
            
            self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def create_explosion_effect(self, x, y):
        """Crea efecto de explosión al colisionar"""
        colors = [(255, 100, 0), (255, 150, 0), (255, 200, 0), (255, 0, 0)]
        
        for _ in range(20):
            angle = random.uniform(0, 360)
            speed = random.uniform(3, 7)
            vel_x = speed * math.cos(math.radians(angle))
            vel_y = speed * math.sin(math.radians(angle))
            
            color = random.choice(colors)
            size = random.randint(3, 6)
            lifetime = random.randint(15, 35)
            
            self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def create_trail_effect(self, x, y, color=(100, 100, 255)):
        """Crea efecto de estela al moverse rápido"""
        vel_x = random.uniform(-0.5, 0.5)
        vel_y = random.uniform(-0.5, 0.5)
        size = random.randint(2, 4)
        lifetime = random.randint(10, 20)
        
        self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def create_star_effect(self, x, y):
        """Crea efecto de estrellas (para power-ups especiales)"""
        colors = [(255, 255, 0), (255, 255, 255), (255, 200, 0)]
        
        for _ in range(5):
            angle = random.uniform(0, 360)
            speed = random.uniform(1, 3)
            vel_x = speed * math.cos(math.radians(angle))
            vel_y = speed * math.sin(math.radians(angle)) - 2
            
            color = random.choice(colors)
            size = random.randint(3, 5)
            lifetime = random.randint(25, 45)
            
            self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def create_crown_sparkle(self, x, y):
        """Crea efecto especial para la corona"""
        colors = [(255, 215, 0), (255, 255, 0), (255, 255, 255)]
        
        for _ in range(30):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 6)
            vel_x = speed * math.cos(math.radians(angle))
            vel_y = speed * math.sin(math.radians(angle)) - 3
            
            color = random.choice(colors)
            size = random.randint(3, 7)
            lifetime = random.randint(30, 60)
            
            self.particles.append(Particle(x, y, vel_x, vel_y, color, size, lifetime))
    
    def get_particle_count(self):
        """Retorna el número de partículas activas"""
        return len(self.particles)

