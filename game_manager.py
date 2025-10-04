"""
Game Manager Module - Donkey Kong Game
=====================================
Este módulo maneja toda la lógica central del juego de Donkey Kong:
- Inicialización y configuración del mapa
- Carga de gráficos y recursos visuales
- Sistema de sonidos y música
- Manejo de enemigos (barriles, fuego)
- Sistema de recompensas y power-ups
- Lógica de niveles y progresión
- Gestión de colisiones y física del mundo
"""

import pygame
import random
import math
import os

class Barrel:
    """Clase para los barriles enemigos"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed_x = random.choice([-2, 2])  # Dirección inicial aleatoria
        self.speed_y = 0
        self.gravity = 0.5
        self.on_platform = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.last_platform_y = y  # Para detectar cuando cae un nivel
        self.fall_threshold = 50   # Mínima altura de caída para cambiar dirección

    def update(self, platforms):
        """Actualiza el movimiento del barril"""
        # Aplicar gravedad
        self.speed_y += self.gravity
        if self.speed_y > 8:
            self.speed_y = 8
        
        # Mover
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Verificar colisiones con plataformas
        barrel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        previous_on_platform = self.on_platform
        self.on_platform = False
        
        for platform in platforms:
            if barrel_rect.colliderect(platform):
                if self.speed_y > 0:  # Cayendo
                    # Calcular cuánto ha caído desde la última plataforma
                    fall_distance = self.y - self.last_platform_y
                    
                    self.y = platform.top - self.height
                    self.speed_y = 0
                    self.on_platform = True
                    
                    # Si ha caído al menos el threshold, cambiar dirección aleatoriamente
                    if fall_distance >= self.fall_threshold:
                        self.speed_x = random.choice([-2, 2])
                        self.last_platform_y = self.y  # Actualizar última posición de plataforma
                    
                    break
        
        # Si estaba en una plataforma y ahora no, actualizar la posición de referencia
        if previous_on_platform and not self.on_platform:
            self.last_platform_y = self.y
        
        # Animación
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

    def draw(self, screen):
        """Dibuja el barril"""
        # Colores del barril
        brown = (139, 69, 19)
        dark_brown = (101, 67, 33)
        
        # Cuerpo del barril
        pygame.draw.rect(screen, brown, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, dark_brown, (self.x+2, self.y+2, self.width-4, self.height-4))
        
        # Líneas del barril
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y+5), (self.x+self.width, self.y+5), 1)
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y+10), (self.x+self.width, self.y+10), 1)
        pygame.draw.line(screen, (0, 0, 0), (self.x, self.y+15), (self.x+self.width, self.y+15), 1)

    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PowerUp:
    """Clase para power-ups y recompensas"""
    def __init__(self, x, y, type_name="hammer"):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.type = type_name  # "hammer", "bonus", "life"
        self.collected = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.float_offset = 0

    def update(self):
        """Actualiza la animación del power-up"""
        self.animation_timer += 1
        if self.animation_timer >= 8:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 6
        
        # Efecto de flotación
        self.float_offset = int(3 * math.sin(self.animation_frame * 0.5))

    def draw(self, screen):
        """Dibuja el power-up"""
        draw_y = self.y + self.float_offset
        
        if self.type == "hammer":
            # Martillo
            handle_color = (139, 69, 19)
            head_color = (169, 169, 169)
            pygame.draw.rect(screen, handle_color, (self.x+6, draw_y, 4, 12))
            pygame.draw.rect(screen, head_color, (self.x+2, draw_y, 12, 6))
            
        elif self.type == "bonus":
            # Bonus (diamante)
            colors = [(255, 215, 0), (255, 255, 0)]
            color = colors[self.animation_frame % 2]
            points = [
                (self.x + 8, draw_y),
                (self.x + 12, draw_y + 4),
                (self.x + 8, draw_y + 8),
                (self.x + 4, draw_y + 4)
            ]
            pygame.draw.polygon(screen, color, points)
            
        elif self.type == "life":
            # Vida extra (corazón)
            pygame.draw.circle(screen, (255, 0, 0), (self.x + 4, draw_y + 4), 3)
            pygame.draw.circle(screen, (255, 0, 0), (self.x + 10, draw_y + 4), 3)
            pygame.draw.polygon(screen, (255, 0, 0), [
                (self.x + 1, draw_y + 6),
                (self.x + 8, draw_y + 12),
                (self.x + 15, draw_y + 6)
            ])

    def get_rect(self):
        """Retorna el rectángulo de colisión"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

class GameManager:
    """Gestor principal del juego Donkey Kong"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Listas de entidades del juego
        self.barrels = []
        self.power_ups = []
        self.platforms = []
        self.ladders = []
        
        # Configuración del juego
        self.barrel_spawn_timer = 0
        self.barrel_spawn_rate = 180  # Frames entre spawns
        self.level = 1
        self.score = 0
        
        # Sistema de spawn de power-ups aleatorios
        self.hammer_spawn_timer = 0
        self.hammer_spawn_rate = 600  # Frames entre spawns de martillos (10 segundos a 60 FPS)
        self.bonus_spawn_timer = 0
        self.bonus_spawn_rate = 900   # Frames entre spawns de bonus (15 segundos a 60 FPS)
        self.max_random_powerups = 3  # Máximo número de power-ups aleatorios en pantalla
        
        # Estadísticas adicionales
        self.barrels_dodged = 0
        self.powerups_collected = 0
        
        # Sistema de sonido
        self.sounds_enabled = False
        self.sounds = {}
        
        # Inicializar sistemas
        self.initialize_level()
        self.load_sounds()

class DemoPlayer:
    """Clase para simular un jugador automático en modo demo"""
    
    def __init__(self, player, platforms, ladders, game_manager=None):
        self.player = player
        self.platforms = platforms
        self.ladders = ladders
        self.game_manager = game_manager
        self.demo_timer = 0
        self.current_action = "wait"
        self.action_timer = 0
        self.target_x = player.x
        
    def update(self):
        """Actualiza la IA de la demo"""
        self.demo_timer += 1
        self.action_timer += 1
        
        # Cambiar de acción cada cierto tiempo
        if self.action_timer > 120:  # 2 segundos
            self.action_timer = 0
            actions = ["move_left", "move_right", "jump", "wait", "climb"]
            self.current_action = random.choice(actions)
            
            # Establecer objetivo aleatorio para movimiento
            if self.current_action in ["move_left", "move_right"]:
                self.target_x = random.randint(50, 800)
        
        return self.get_demo_input()
    
    def get_demo_input(self):
        """Genera input simulado para la demo"""
        keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_SPACE: False,
            pygame.K_a: False,
            pygame.K_d: False,
            pygame.K_w: False,
            pygame.K_s: False
        }
        
        if self.current_action == "move_left":
            keys[pygame.K_LEFT] = True
            keys[pygame.K_a] = True
        elif self.current_action == "move_right":
            keys[pygame.K_RIGHT] = True
            keys[pygame.K_d] = True
        elif self.current_action == "jump" and self.player.on_ground:
            keys[pygame.K_SPACE] = True
        elif self.current_action == "climb" and self.player.on_ladder:
            if random.choice([True, False]):
                keys[pygame.K_UP] = True
                keys[pygame.K_w] = True
            else:
                keys[pygame.K_DOWN] = True
                keys[pygame.K_s] = True
        
        # Evitar barriles básico - moverse en dirección opuesta
        if self.game_manager:
            player_rect = self.player.get_rect()
            for barrel in self.game_manager.barrels:
                barrel_rect = barrel.get_rect()
                if abs(barrel_rect.centerx - player_rect.centerx) < 100 and abs(barrel_rect.centery - player_rect.centery) < 50:
                    if barrel_rect.centerx > player_rect.centerx:
                        keys[pygame.K_LEFT] = True
                        keys[pygame.K_a] = True
                    else:
                        keys[pygame.K_RIGHT] = True
                        keys[pygame.K_d] = True
                    break
        
        return keys

# Agregar las funciones que faltan a GameManager
def initialize_level(self):
    """Inicializa el mapa del nivel actual"""
    self.platforms.clear()
    self.ladders.clear()
    self.power_ups.clear()
    self.barrels.clear()
    
    # Crear plataformas del nivel 1 (estilo Donkey Kong clásico)
    self.platforms = [
        # Suelo principal
        pygame.Rect(0, self.screen_height - 50, self.screen_width, 50),
        
        # Primer nivel
        pygame.Rect(50, self.screen_height - 150, 300, 20),
        pygame.Rect(450, self.screen_height - 150, 300, 20),
        
        # Segundo nivel
        pygame.Rect(100, self.screen_height - 250, 250, 20),
        pygame.Rect(500, self.screen_height - 250, 250, 20),
        
        # Tercer nivel
        pygame.Rect(150, self.screen_height - 350, 200, 20),
        pygame.Rect(550, self.screen_height - 350, 200, 20),
        
        # Nivel superior (donde está Donkey Kong)
        pygame.Rect(200, self.screen_height - 450, 400, 20),
    ]
    
    # Crear escaleras
    self.ladders = [
        # Escaleras del primer nivel
        pygame.Rect(370, self.screen_height - 170, 20, 120),
        pygame.Rect(430, self.screen_height - 170, 20, 120),
        
        # Escaleras del segundo nivel
        pygame.Rect(320, self.screen_height - 270, 20, 120),
        pygame.Rect(480, self.screen_height - 270, 20, 120),
        
        # Escaleras del tercer nivel
        pygame.Rect(370, self.screen_height - 370, 20, 120),
        pygame.Rect(530, self.screen_height - 370, 20, 120),
        
        # Escalera final
        pygame.Rect(400, self.screen_height - 470, 20, 120),
    ]
    
    # Colocar power-ups estratégicamente
    self.power_ups = [
        PowerUp(200, self.screen_height - 170, "hammer"),
        PowerUp(600, self.screen_height - 270, "bonus"),
        PowerUp(300, self.screen_height - 370, "life"),
        PowerUp(650, self.screen_height - 370, "bonus"),
    ]

# Agregar todas las funciones que faltan a GameManager
def load_sounds(self):
    """Carga los archivos de sonido"""
    try:
        pygame.mixer.init()
        self.sounds_enabled = True
        print("Sistema de sonido inicializado")
    except:
        print("No se pudo inicializar el sistema de sonido")
        self.sounds_enabled = False

def play_sound(self, sound_name):
    """Reproduce un sonido"""
    if self.sounds_enabled and sound_name in self.sounds:
        self.sounds[sound_name].play()

def spawn_barrel(self):
    """Genera un nuevo barril"""
    spawn_x = random.randint(200, 600)
    spawn_y = self.screen_height - 480
    barrel = Barrel(spawn_x, spawn_y)
    self.barrels.append(barrel)

def spawn_random_powerup(self, powerup_type):
    """Genera un power-up aleatorio en una plataforma"""
    # Contar power-ups aleatorios existentes (excluyendo los fijos)
    random_powerups = [p for p in self.power_ups if not p.collected]
    if len(random_powerups) >= self.max_random_powerups:
        return  # No spawnear más si ya hay demasiados
    
    # Elegir una plataforma aleatoria (excluyendo el suelo y la plataforma superior)
    if len(self.platforms) < 3:
        return
    
    # Usar plataformas del medio (niveles 1, 2, 3)
    available_platforms = self.platforms[1:-1]  # Excluir suelo y plataforma superior
    platform = random.choice(available_platforms)
    
    # Calcular posición aleatoria en la plataforma
    spawn_x = random.randint(platform.x + 20, platform.x + platform.width - 20)
    spawn_y = platform.y - 20  # Un poco arriba de la plataforma
    
    # Crear el power-up
    powerup = PowerUp(spawn_x, spawn_y, powerup_type)
    self.power_ups.append(powerup)

def update(self, player):
    """Actualiza toda la lógica del juego"""
    # Spawn de barriles
    self.barrel_spawn_timer += 1
    if self.barrel_spawn_timer >= self.barrel_spawn_rate:
        self.barrel_spawn_timer = 0
        self.spawn_barrel()
        self.barrel_spawn_rate = max(60, 180 - (self.level * 20))
    
    # Spawn de power-ups aleatorios
    self.hammer_spawn_timer += 1
    if self.hammer_spawn_timer >= self.hammer_spawn_rate:
        self.hammer_spawn_timer = 0
        self.spawn_random_powerup("hammer")
        # Reducir tiempo de spawn en niveles más altos
        self.hammer_spawn_rate = max(300, 600 - (self.level * 50))
    
    self.bonus_spawn_timer += 1
    if self.bonus_spawn_timer >= self.bonus_spawn_rate:
        self.bonus_spawn_timer = 0
        self.spawn_random_powerup("bonus")
        # Reducir tiempo de spawn en niveles más altos
        self.bonus_spawn_rate = max(450, 900 - (self.level * 75))

    # Actualizar barriles
    for barrel in self.barrels[:]:
        barrel.update(self.platforms)
        if barrel.y > self.screen_height or barrel.x < -50 or barrel.x > self.screen_width + 50:
            self.barrels.remove(barrel)
            self.barrels_dodged += 1

    # Actualizar power-ups
    for power_up in self.power_ups:
        if not power_up.collected:
            power_up.update()

    # Verificar colisiones del jugador
    self.check_collisions(player)

def check_collisions(self, player):
    """Verifica colisiones entre el jugador y otros objetos"""
    player_rect = player.get_rect()
    
    # Colisiones con barriles
    for barrel in self.barrels[:]:
        if player_rect.colliderect(barrel.get_rect()):
            player.lose_life()
            self.barrels.remove(barrel)
            self.play_sound('hit')
            break
    
    # Colisiones con power-ups
    for power_up in self.power_ups:
        if not power_up.collected and player_rect.colliderect(power_up.get_rect()):
            power_up.collected = True
            self.powerups_collected += 1
            self.play_sound('powerup')
            
            if power_up.type == "hammer":
                self.score += 500
            elif power_up.type == "bonus":
                self.score += 1000
            elif power_up.type == "life":
                if player.lives < 3:  # Si necesita la vida
                    player.lives += 1
                    # No dar puntos porque necesita la vida
                else:  # Si ya tiene todas las vidas (3/3)
                    # Dar puntos porque no necesita la vida
                    self.score += 2000

def draw(self, screen):
    """Dibuja todos los elementos del mapa"""
    # Dibujar plataformas
    for platform in self.platforms:
        pygame.draw.rect(screen, (0, 100, 255), platform)
        pygame.draw.rect(screen, (0, 80, 200), (platform.x, platform.y, platform.width, 5))
        for i in range(platform.x, platform.x + platform.width, 20):
            pygame.draw.line(screen, (0, 60, 150), (i, platform.y), (i, platform.y + platform.height), 1)

    # Dibujar escaleras
    for ladder in self.ladders:
        pygame.draw.rect(screen, (255, 255, 0), (ladder.x, ladder.y, 4, ladder.height))
        pygame.draw.rect(screen, (255, 255, 0), (ladder.x + ladder.width - 4, ladder.y, 4, ladder.height))
        for i in range(ladder.y, ladder.y + ladder.height, 15):
            pygame.draw.rect(screen, (255, 255, 0), (ladder.x, i, ladder.width, 3))

    # Dibujar Donkey Kong
    self.draw_donkey_kong(screen)

    # Dibujar barriles
    for barrel in self.barrels:
        barrel.draw(screen)

    # Dibujar power-ups
    for power_up in self.power_ups:
        if not power_up.collected:
            power_up.draw(screen)

def draw_donkey_kong(self, screen):
    """Dibuja a Donkey Kong en la parte superior"""
    dk_x = 350
    dk_y = self.screen_height - 520
    
    pygame.draw.rect(screen, (139, 69, 19), (dk_x, dk_y + 20, 60, 40))
    pygame.draw.rect(screen, (139, 69, 19), (dk_x + 10, dk_y, 40, 30))
    pygame.draw.rect(screen, (222, 184, 135), (dk_x + 15, dk_y + 5, 30, 20))
    pygame.draw.rect(screen, (0, 0, 0), (dk_x + 20, dk_y + 10, 4, 4))
    pygame.draw.rect(screen, (0, 0, 0), (dk_x + 30, dk_y + 10, 4, 4))
    pygame.draw.rect(screen, (139, 69, 19), (dk_x - 10, dk_y + 25, 15, 25))
    pygame.draw.rect(screen, (139, 69, 19), (dk_x + 55, dk_y + 25, 15, 25))

def get_platforms(self):
    """Retorna las plataformas para el sistema de colisiones"""
    return self.platforms

def get_ladders(self):
    """Retorna las escaleras para el sistema de colisiones"""
    return self.ladders

def get_score(self):
    """Retorna la puntuación actual"""
    return self.score

def draw_hearts(self, screen, lives, x, y, heart_size=30):
    """Dibuja corazones para mostrar las vidas del jugador con mejor diseño"""
    heart_color = (255, 0, 0)  # Rojo
    broken_heart_color = (80, 80, 80)  # Gris oscuro para corazones rotos
    
    for i in range(3):  # Siempre mostrar 3 corazones
        heart_x = x + i * (heart_size + 8)
        heart_y = y
        
        if i < lives:
            # Dibujar corazón completo con mejor forma
            self._draw_single_heart(screen, heart_x, heart_y, heart_size, heart_color, False)
        else:
            # Dibujar corazón roto con X
            self._draw_single_heart(screen, heart_x, heart_y, heart_size, broken_heart_color, True)

def _draw_single_heart(self, screen, x, y, size, color, broken=False):
    """Dibuja un solo corazón con forma más realista y detallada"""
    center_x = x + size // 2
    center_y = y + size // 2
    heart_radius = size // 3
    
    # Calcular puntos para el corazón más realista
    # Parte superior: dos círculos más grandes
    left_circle_center = (center_x - heart_radius//2, center_y - heart_radius//3)
    right_circle_center = (center_x + heart_radius//2, center_y - heart_radius//3)
    circle_radius = heart_radius * 0.8
    
    # Dibujar los círculos superiores
    pygame.draw.circle(screen, color, left_circle_center, int(circle_radius))
    pygame.draw.circle(screen, color, right_circle_center, int(circle_radius))
    
    # Parte inferior del corazón: triángulo más suave
    # Puntos del triángulo inferior
    bottom_point = (center_x, center_y + heart_radius)
    left_point = (center_x - heart_radius * 1.2, center_y + heart_radius * 0.3)
    right_point = (center_x + heart_radius * 1.2, center_y + heart_radius * 0.3)
    
    # Crear un polígono más suave para la parte inferior
    heart_points = [
        left_point,
        (center_x - heart_radius * 0.8, center_y + heart_radius * 0.6),
        bottom_point,
        (center_x + heart_radius * 0.8, center_y + heart_radius * 0.6),
        right_point
    ]
    pygame.draw.polygon(screen, color, heart_points)
    
    # Rellenar las áreas donde se conectan los círculos con el triángulo
    # Pequeños rectángulos para suavizar la transición
    pygame.draw.rect(screen, color, 
                    (center_x - heart_radius//2, center_y - heart_radius//6, 
                     heart_radius, heart_radius//3))
    
    # Si está roto, dibujar X más elegante
    if broken:
        line_width = max(2, size // 12)
        # X diagonal con mejor proporción
        margin = size // 8
        start_x, start_y = x + margin, y + margin
        end_x, end_y = x + size - margin, y + size - margin
        pygame.draw.line(screen, (120, 120, 120), (start_x, start_y), (end_x, end_y), line_width)
        pygame.draw.line(screen, (120, 120, 120), (end_x, start_y), (start_x, end_y), line_width)
        
        # Añadir un pequeño efecto de "grieta" en el centro
        crack_width = line_width // 2
        crack_length = size // 4
        crack_x = center_x - crack_length // 2
        crack_y = center_y - crack_length // 2
        pygame.draw.line(screen, (100, 100, 100), 
                        (crack_x, crack_y), 
                        (crack_x + crack_length, crack_y + crack_length), 
                        crack_width)

def next_level(self):
    """Avanza al siguiente nivel"""
    self.level += 1
    self.barrel_spawn_rate = max(60, 180 - (self.level * 20))
    # Resetear timers de power-ups para el nuevo nivel
    self.hammer_spawn_timer = 0
    self.bonus_spawn_timer = 0
    self.initialize_level()

def reset_game(self):
    """Reinicia el juego"""
    self.level = 1
    self.score = 0
    self.barrel_spawn_timer = 0
    self.barrel_spawn_rate = 180
    # Resetear timers de power-ups
    self.hammer_spawn_timer = 0
    self.bonus_spawn_timer = 0
    self.hammer_spawn_rate = 600
    self.bonus_spawn_rate = 900
    self.initialize_level()

# Agregar todas las funciones como métodos de GameManager
GameManager.initialize_level = initialize_level
GameManager.load_sounds = load_sounds
GameManager.play_sound = play_sound
GameManager.spawn_barrel = spawn_barrel
GameManager.spawn_random_powerup = spawn_random_powerup
GameManager.update = update
GameManager.check_collisions = check_collisions
GameManager.draw = draw
GameManager.draw_donkey_kong = draw_donkey_kong
GameManager.get_platforms = get_platforms
GameManager.get_ladders = get_ladders
GameManager.get_score = get_score
GameManager.draw_hearts = draw_hearts
GameManager._draw_single_heart = _draw_single_heart
GameManager.next_level = next_level
GameManager.reset_game = reset_game

# GameManager: Controla todos los aspectos del juego incluyendo mapa, enemigos, recompensas, sonidos y lógica de niveles para Donkey Kong.
