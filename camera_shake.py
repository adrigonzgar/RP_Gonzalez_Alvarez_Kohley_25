"""
Camera Shake Module - Donkey Kong Game
======================================
Este módulo maneja el efecto de sacudida de cámara para añadir impacto visual.
"""

import random
import math

class CameraShake:
    """Clase para manejar el efecto de sacudida de cámara"""
    
    def __init__(self):
        self.shake_amount = 0
        self.shake_duration = 0
        self.offset_x = 0
        self.offset_y = 0
    
    def start_shake(self, intensity=10, duration=15):
        """
        Inicia un efecto de sacudida
        
        Args:
            intensity: Intensidad de la sacudida (píxeles)
            duration: Duración en frames
        """
        self.shake_amount = intensity
        self.shake_duration = duration
    
    def update(self):
        """Actualiza el efecto de sacudida"""
        if self.shake_duration > 0:
            self.shake_duration -= 1
            
            # Calcular offset aleatorio
            if self.shake_duration > 0:
                # Reducir intensidad gradualmente
                current_intensity = self.shake_amount * (self.shake_duration / 15)
                self.offset_x = random.uniform(-current_intensity, current_intensity)
                self.offset_y = random.uniform(-current_intensity, current_intensity)
            else:
                self.offset_x = 0
                self.offset_y = 0
        else:
            self.offset_x = 0
            self.offset_y = 0
    
    def get_offset(self):
        """Retorna el offset actual de la cámara"""
        return int(self.offset_x), int(self.offset_y)
    
    def is_shaking(self):
        """Retorna si la cámara está sacudiéndose"""
        return self.shake_duration > 0

