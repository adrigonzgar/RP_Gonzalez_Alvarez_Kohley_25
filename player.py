"""
Player Module - Donkey Kong Game
================================
Este módulo contiene la clase Player que maneja toda la funcionalidad del jugador (Mario):
- Movimiento (izquierda, derecha, subir escaleras)
- Salto y física básica
- Animaciones y sprites
- Colisiones
- Estados (parado, corriendo, saltando, subiendo)
- Puntuación y vidas
"""

import pygame
import math

class Player:
    def __init__(self, x, y, screen_width, screen_height):
        """
        Inicializa el jugador (Mario)
        
        Args:
            x (int): Posición inicial X
            y (int): Posición inicial Y
            screen_width (int): Ancho de la pantalla
            screen_height (int): Alto de la pantalla
        """
        # Posición y dimensiones
        self.x = x
        self.y = y
        self.width = 24
        self.height = 32
        
        # Límites de pantalla
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Referencia al sound manager (se asignará externamente)
        self.sound_manager = None
        
        # Velocidades
        self.speed = 4
        self.jump_speed = 9
        self.gravity = 0.8
        self.max_fall_speed = 10
        
        # Estado de movimiento
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.on_ladder = False
        
        # Estados del jugador
        self.facing_right = True
        self.is_jumping = False
        self.is_climbing = False
        self.is_moving = False
        
        # Animación
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8  # frames entre cambios de sprite
        
        # Game stats
        self.lives = 3
        self.score = 0
        self.level = 1
        
        # Colores para el sprite simple
        self.colors = {
            'hat': (255, 0, 0),      # Rojo
            'skin': (255, 220, 177), # Color piel
            'shirt': (0, 0, 255),    # Azul
            'overalls': (0, 0, 255), # Azul
            'shoes': (139, 69, 19),  # Marrón
            'outline': (0, 0, 0)     # Negro
        }

    def update(self, keys_pressed, platforms, ladders, dt, moving_platforms=None):
        """
        Actualiza el estado del jugador cada frame
        
        Args:
            keys_pressed: Teclas presionadas actualmente
            platforms: Lista de plataformas para colisiones
            ladders: Lista de escaleras
            dt: Delta time (tiempo entre frames)
            moving_platforms: Lista de plataformas móviles (opcional)
        """
        # Resetear estados
        self.is_moving = False
        self.is_climbing = False
        
        # Manejar input del teclado
        self._handle_input(keys_pressed)
        
        # Aplicar física
        self._apply_physics(dt)
        
        # Manejar wrap-around horizontal ANTES de verificar colisiones
        self._handle_wrap_around()
        
        # Verificar colisiones
        self._check_collisions(platforms, ladders, moving_platforms)
        
        # Actualizar animación
        self._update_animation()
        
        # Mantener límites verticales
        self._clamp_vertical()

    def _handle_input(self, keys_pressed):
        """Maneja la entrada del teclado"""
        # Movimiento horizontal
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.vel_x = -self.speed
            self.facing_right = False
            self.is_moving = True
            
        elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.vel_x = self.speed
            self.facing_right = True
            self.is_moving = True
        else:
            self.vel_x = 0
        
        # Salto
        if (keys_pressed[pygame.K_SPACE] or keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and self.on_ground:
            self.vel_y = -self.jump_speed
            self.is_jumping = True
            self.on_ground = False
            # Reproducir sonido de salto
            if self.sound_manager:
                self.sound_manager.play_sound('jump')
        
        # Subir/bajar escaleras
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            if self.on_ladder:
                self.vel_y = -self.speed
                self.is_climbing = True
                
        elif keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            if self.on_ladder:
                self.vel_y = self.speed
                self.is_climbing = True

    def _apply_physics(self, dt):
        """Aplica física básica (gravedad, movimiento)"""
        # Aplicar gravedad si no está en escalera
        if not self.on_ladder:
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed
        
        # Actualizar posición
        self.x += self.vel_x
        self.y += self.vel_y

    def _check_collisions(self, platforms, ladders, moving_platforms=None):
        """Verifica colisiones con plataformas y escaleras"""
        # Crear rectángulo del jugador
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # Verificar escaleras
        self.on_ladder = False
        for ladder in ladders:
            if player_rect.colliderect(ladder):
                self.on_ladder = True
                break
        
        # Verificar plataformas
        self.on_ground = False
        
        # Primero verificar plataformas móviles
        if moving_platforms:
            for moving_platform in moving_platforms:
                platform_rect = moving_platform.get_rect()
                
                # Verificar colisión horizontal (si el jugador está encima horizontalmente)
                horizontal_overlap = (self.x + self.width > platform_rect.left + 2 and 
                                     self.x < platform_rect.right - 2)
                
                if horizontal_overlap:
                    player_bottom = self.y + self.height
                    platform_top = platform_rect.top
                    
                    # Verificar si está sobre la plataforma (con margen generoso)
                    if self.vel_y >= 0 and player_bottom >= platform_top - 5 and player_bottom <= platform_top + 15:
                        # Posicionar firmemente sobre la plataforma
                        self.y = platform_rect.top - self.height
                        self.vel_y = 0
                        self.on_ground = True
                        self.is_jumping = False
                        
                        # Mover al jugador con la plataforma
                        if moving_platform.move_type == "horizontal":
                            self.x += moving_platform.move_speed * moving_platform.direction
                        elif moving_platform.move_type == "vertical":
                            # Para plataformas verticales, mantener pegado
                            self.y = platform_rect.top - self.height
                        break
        
        # Luego verificar plataformas estáticas solo si no está en una móvil
        if not self.on_ground:
            for platform in platforms:
                if player_rect.colliderect(platform):
                    # Colisión desde arriba (aterrizar en plataforma)
                    if self.vel_y > 0 and self.y < platform.top:
                        self.y = platform.top - self.height
                        self.vel_y = 0
                        self.on_ground = True
                        self.is_jumping = False
                        break

    def _update_animation(self):
        """Actualiza la animación del sprite"""
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.is_moving:
                self.animation_frame = (self.animation_frame + 1) % 3  # 3 frames de animación
            else:
                self.animation_frame = 0  # Frame estático

    def _handle_wrap_around(self):
        """Maneja el wrap-around horizontal del jugador"""
        # Wrap-around horizontal: si sale por la izquierda, aparece por la derecha
        if self.x < -self.width:
            self.x = self.screen_width
        elif self.x > self.screen_width:
            self.x = -self.width

    def _clamp_vertical(self):
        """Mantiene los límites verticales del jugador"""
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height
            self.on_ground = True
            self.vel_y = 0

    def draw(self, screen):
        """
        Dibuja el jugador en pantalla con pixel art simple
        
        Args:
            screen: Superficie de pygame donde dibujar
        """
        # Dibujar sombra simple
        shadow_rect = pygame.Rect(self.x + 2, self.y + self.height - 2, self.width - 4, 4)
        pygame.draw.ellipse(screen, (50, 50, 50), shadow_rect)
        
        # Determinar offset de animación
        offset_x = 0
        if self.is_moving and not self.is_jumping:
            offset_x = int(2 * math.sin(self.animation_frame * 2))
        
        # Dibujar sprite de Mario
        self._draw_mario_sprite(screen, self.x + offset_x, self.y)
        
        # Dibujar indicadores de estado (debug)
        if self.is_jumping:
            pygame.draw.circle(screen, (255, 255, 0), (self.x + self.width//2, self.y - 10), 3)
        if self.on_ladder:
            pygame.draw.circle(screen, (0, 255, 0), (self.x + self.width//2, self.y - 10), 3)

    def _draw_mario_sprite(self, screen, x, y):
        """Dibuja el sprite de Mario en pixel art"""
        # Gorra
        hat_rect = pygame.Rect(x + 4, y, 16, 8)
        pygame.draw.rect(screen, self.colors['hat'], hat_rect)
        
        # Cara
        face_rect = pygame.Rect(x + 4, y + 8, 16, 8)
        pygame.draw.rect(screen, self.colors['skin'], face_rect)
        
        # Bigote
        mustache_rect = pygame.Rect(x + 8, y + 12, 8, 4)
        pygame.draw.rect(screen, self.colors['outline'], mustache_rect)
        
        # Cuerpo (overol)
        body_rect = pygame.Rect(x + 2, y + 16, 20, 12)
        pygame.draw.rect(screen, self.colors['overalls'], body_rect)
        
        # Brazos
        if self.facing_right:
            arm_left = pygame.Rect(x - 2, y + 18, 6, 8)
            arm_right = pygame.Rect(x + 20, y + 18, 6, 8)
        else:
            arm_left = pygame.Rect(x, y + 18, 6, 8)
            arm_right = pygame.Rect(x + 18, y + 18, 6, 8)
        
        pygame.draw.rect(screen, self.colors['skin'], arm_left)
        pygame.draw.rect(screen, self.colors['skin'], arm_right)
        
        # Piernas (con animación de caminar)
        leg_offset = 0
        if self.is_moving and self.animation_frame % 2:
            leg_offset = 2
        
        leg_left = pygame.Rect(x + 6 - leg_offset, y + 28, 4, 4)
        leg_right = pygame.Rect(x + 14 + leg_offset, y + 28, 4, 4)
        pygame.draw.rect(screen, self.colors['overalls'], leg_left)
        pygame.draw.rect(screen, self.colors['overalls'], leg_right)
        
        # Zapatos
        shoe_left = pygame.Rect(x + 4 - leg_offset, y + 32, 6, 4)
        shoe_right = pygame.Rect(x + 14 + leg_offset, y + 32, 6, 4)
        pygame.draw.rect(screen, self.colors['shoes'], shoe_left)
        pygame.draw.rect(screen, self.colors['shoes'], shoe_right)

    def jump(self):
        """Método público para hacer saltar al jugador"""
        if self.on_ground:
            self.vel_y = -self.jump_speed
            self.is_jumping = True
            self.on_ground = False
            # Reproducir sonido de salto
            if self.sound_manager:
                self.sound_manager.play_sound('jump')

    def add_score(self, points):
        """Añadir puntos al score"""
        self.score += points

    def lose_life(self):
        """Perder una vida"""
        self.lives -= 1
        return self.lives <= 0  # Retorna True si game over

    def reset_position(self, x, y):
        """Resetear posición del jugador"""
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.is_jumping = False

    def get_rect(self):
        """Retorna el rectángulo de colisión del jugador"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_stats(self):
        """Retorna las estadísticas del jugador"""
        return {
            'score': self.score,
            'lives': self.lives,
            'level': self.level,
            'position': (self.x, self.y)
        }

# Clase Player: Maneja toda la funcionalidad del jugador Mario incluyendo movimiento, física, animaciones, colisiones y estadísticas del juego.
