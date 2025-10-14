"""
Sound Manager Module - Donkey Kong Game
=======================================
Este módulo maneja todo el sistema de audio del juego:
- Efectos de sonido
- Música de fondo
- Control de volumen
- Generación procedural de sonidos
"""

import pygame
import math
import numpy as np

class SoundManager:
    """Gestor de sonidos y música del juego"""
    
    def __init__(self):
        """Inicializa el sistema de sonido"""
        self.enabled = True
        self.sfx_volume = 0.7
        self.music_volume = 0.5
        self.sounds = {}
        self.current_music = None
        
        try:
            # Buffer más pequeño para reducir latencia (128 en lugar de 512)
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=128)
            self.enabled = True
            print("Sistema de audio inicializado correctamente")
        except Exception as e:
            print(f"Error al inicializar audio: {e}")
            self.enabled = False
            return
        
        # Generar efectos de sonido
        self.generate_sounds()
    
    def generate_sounds(self):
        """Genera efectos de sonido proceduralmente"""
        if not self.enabled:
            return
        
        sample_rate = 22050
        
        # 1. Sonido de salto
        self.sounds['jump'] = self.generate_jump_sound(sample_rate)
        
        # 2. Sonido de recoger power-up
        self.sounds['powerup'] = self.generate_powerup_sound(sample_rate)
        
        # 3. Sonido de colisión/daño
        self.sounds['hit'] = self.generate_hit_sound(sample_rate)
        
        # 4. Sonido de completar nivel
        self.sounds['level_complete'] = self.generate_level_complete_sound(sample_rate)
        
        # 5. Sonido de caminar/pasos
        self.sounds['step'] = self.generate_step_sound(sample_rate)
        
        # 6. Sonido de subir escalera
        self.sounds['climb'] = self.generate_climb_sound(sample_rate)
        
        # 7. Sonido de barril rodando
        self.sounds['barrel_roll'] = self.generate_barrel_sound(sample_rate)
        
        # 8. Sonido de victoria
        self.sounds['victory'] = self.generate_victory_sound(sample_rate)
        
        print(f"Generados {len(self.sounds)} efectos de sonido")
    
    def generate_jump_sound(self, sample_rate):
        """Genera sonido de salto (sweep ascendente)"""
        duration = 0.1  # Más corto para menos delay
        samples = int(sample_rate * duration)
        
        # Frecuencia que sube de 300Hz a 800Hz (más agudo)
        frequency_start = 300
        frequency_end = 800
        
        sound_array = np.zeros(samples, dtype=np.int16)
        for i in range(samples):
            t = i / sample_rate
            freq = frequency_start + (frequency_end - frequency_start) * (i / samples)
            # Envolvente que decae
            envelope = (1 - i / samples) * 0.5
            sound_array[i] = int(envelope * 32767 * math.sin(2 * math.pi * freq * t))
        
        # Convertir a estéreo
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def generate_powerup_sound(self, sample_rate):
        """Genera sonido de recoger power-up (arpeggio ascendente)"""
        duration = 0.2  # Más corto
        samples = int(sample_rate * duration)
        
        # Arpeggio: C-E-G-C (do-mi-sol-do)
        frequencies = [523, 659, 784, 1047]
        samples_per_note = samples // len(frequencies)
        
        sound_array = np.zeros(samples, dtype=np.int16)
        for note_idx, freq in enumerate(frequencies):
            start = note_idx * samples_per_note
            end = start + samples_per_note
            for i in range(start, min(end, samples)):
                t = (i - start) / sample_rate
                envelope = 0.6 * math.exp(-t * 5)
                sound_array[i] = int(envelope * 32767 * math.sin(2 * math.pi * freq * t))
        
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def generate_hit_sound(self, sample_rate):
        """Genera sonido de colisión (ruido con pitch bajo)"""
        duration = 0.15  # Más corto
        samples = int(sample_rate * duration)
        
        sound_array = np.zeros(samples, dtype=np.int16)
        for i in range(samples):
            t = i / sample_rate
            # Ruido blanco con envolvente
            envelope = (1 - i / samples) * 0.7
            noise = np.random.random() * 2 - 1
            # Mezclar con tono bajo
            tone = math.sin(2 * math.pi * 100 * t)
            sound_array[i] = int(envelope * 32767 * (noise * 0.5 + tone * 0.5))
        
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def generate_level_complete_sound(self, sample_rate):
        """Genera sonido de nivel completado (fanfarria)"""
        duration = 0.8
        samples = int(sample_rate * duration)
        
        # Secuencia de notas: C-E-G-C-G-C (fanfarria)
        note_sequence = [523, 659, 784, 1047, 784, 1047]
        samples_per_note = samples // len(note_sequence)
        
        sound_array = np.zeros(samples, dtype=np.int16)
        for note_idx, freq in enumerate(note_sequence):
            start = note_idx * samples_per_note
            end = start + samples_per_note
            for i in range(start, min(end, samples)):
                t = (i - start) / sample_rate
                envelope = 0.5 * math.exp(-t * 3)
                sound_array[i] = int(envelope * 32767 * math.sin(2 * math.pi * freq * t))
        
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def generate_step_sound(self, sample_rate):
        """Genera sonido de paso (percusión corta)"""
        duration = 0.05
        samples = int(sample_rate * duration)
        
        sound_array = np.zeros(samples, dtype=np.int16)
        for i in range(samples):
            envelope = (1 - i / samples)
            noise = np.random.random() * 2 - 1
            sound_array[i] = int(envelope * 0.3 * 32767 * noise)
        
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def generate_climb_sound(self, sample_rate):
        """Genera sonido de subir escalera (tono corto)"""
        duration = 0.1
        samples = int(sample_rate * duration)
        
        sound_array = np.zeros(samples, dtype=np.int16)
        for i in range(samples):
            t = i / sample_rate
            envelope = (1 - i / samples) * 0.4
            sound_array[i] = int(envelope * 32767 * math.sin(2 * math.pi * 300 * t))
        
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def generate_barrel_sound(self, sample_rate):
        """Genera sonido de barril rodando (ruido grave)"""
        duration = 0.3
        samples = int(sample_rate * duration)
        
        sound_array = np.zeros(samples, dtype=np.int16)
        for i in range(samples):
            t = i / sample_rate
            envelope = 0.3
            # Ruido con frecuencia baja
            noise = np.random.random() * 2 - 1
            tone = math.sin(2 * math.pi * 80 * t)
            sound_array[i] = int(envelope * 32767 * (noise * 0.7 + tone * 0.3))
        
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def generate_victory_sound(self, sample_rate):
        """Genera sonido de victoria (melodía triunfal)"""
        duration = 1.5
        samples = int(sample_rate * duration)
        
        # Melodía de victoria: C-C-C-G-E-G-C
        note_sequence = [523, 523, 523, 784, 659, 784, 1047]
        note_durations = [0.15, 0.15, 0.15, 0.3, 0.2, 0.3, 0.5]
        
        sound_array = np.zeros(samples, dtype=np.int16)
        current_sample = 0
        
        for freq, duration_note in zip(note_sequence, note_durations):
            note_samples = int(sample_rate * duration_note)
            for i in range(note_samples):
                if current_sample >= samples:
                    break
                t = i / sample_rate
                envelope = 0.6 * math.exp(-t * 4)
                sound_array[current_sample] = int(envelope * 32767 * math.sin(2 * math.pi * freq * t))
                current_sample += 1
        
        stereo_array = np.column_stack((sound_array, sound_array))
        return pygame.sndarray.make_sound(stereo_array)
    
    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        try:
            sound = self.sounds[sound_name]
            sound.set_volume(self.sfx_volume)
            sound.play()
        except Exception as e:
            print(f"Error al reproducir sonido {sound_name}: {e}")
    
    def play_music(self, music_type="level"):
        """Reproduce música de fondo"""
        if not self.enabled:
            return
        
        # Por ahora, crear un tono de fondo simple
        # En el futuro, puedes cargar archivos MP3/OGG
        try:
            if self.current_music != music_type:
                self.current_music = music_type
                # Aquí podrías cargar música desde archivos
                # pygame.mixer.music.load('music.mp3')
                # pygame.mixer.music.set_volume(self.music_volume)
                # pygame.mixer.music.play(-1)  # Loop infinito
        except Exception as e:
            print(f"Error al reproducir música: {e}")
    
    def stop_music(self):
        """Detiene la música de fondo"""
        if not self.enabled:
            return
        
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def set_sfx_volume(self, volume):
        """Ajusta el volumen de efectos de sonido (0.0 a 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Ajusta el volumen de música (0.0 a 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.enabled:
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass
    
    def toggle_sound(self):
        """Activa/desactiva el sonido"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop_music()
        return self.enabled

