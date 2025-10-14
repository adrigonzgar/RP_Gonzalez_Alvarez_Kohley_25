"""
High Score Manager Module - Donkey Kong Game
============================================
Este módulo maneja el sistema de puntuaciones altas:
- Guardar y cargar high scores
- Verificar si una puntuación es récord
- Mostrar tabla de mejores puntuaciones
"""

import json
import os
from datetime import datetime

class HighScoreManager:
    """Gestor de puntuaciones altas"""
    
    def __init__(self, filename='highscores.json'):
        self.filename = filename
        self.highscores = []
        self.max_scores = 10
        self.load_highscores()
    
    def load_highscores(self):
        """Carga las puntuaciones desde el archivo JSON"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    self.highscores = json.load(f)
            else:
                # Crear puntuaciones por defecto
                self.highscores = [
                    {"name": "MARIO", "score": 50000, "level": 5, "date": "2025-01-01"},
                    {"name": "LUIGI", "score": 45000, "level": 5, "date": "2025-01-01"},
                    {"name": "PEACH", "score": 40000, "level": 4, "date": "2025-01-01"},
                    {"name": "TOAD", "score": 35000, "level": 4, "date": "2025-01-01"},
                    {"name": "YOSHI", "score": 30000, "level": 3, "date": "2025-01-01"},
                    {"name": "BOWSR", "score": 25000, "level": 3, "date": "2025-01-01"},
                    {"name": "WARIO", "score": 20000, "level": 2, "date": "2025-01-01"},
                    {"name": "WALIG", "score": 15000, "level": 2, "date": "2025-01-01"},
                    {"name": "DAISY", "score": 10000, "level": 1, "date": "2025-01-01"},
                    {"name": "DK", "score": 5000, "level": 1, "date": "2025-01-01"},
                ]
                self.save_highscores()
        except Exception as e:
            print(f"Error al cargar high scores: {e}")
            self.highscores = []
    
    def save_highscores(self):
        """Guarda las puntuaciones en el archivo JSON"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.highscores, f, indent=2)
        except Exception as e:
            print(f"Error al guardar high scores: {e}")
    
    def is_highscore(self, score):
        """Verifica si una puntuación es récord"""
        if len(self.highscores) < self.max_scores:
            return True
        return score > self.highscores[-1]['score']
    
    def add_highscore(self, name, score, level):
        """Añade una nueva puntuación alta"""
        date = datetime.now().strftime("%Y-%m-%d")
        
        new_score = {
            "name": name.upper()[:5],  # Máximo 5 caracteres
            "score": score,
            "level": level,
            "date": date
        }
        
        self.highscores.append(new_score)
        
        # Ordenar por puntuación (mayor a menor)
        self.highscores.sort(key=lambda x: x['score'], reverse=True)
        
        # Mantener solo las top 10
        self.highscores = self.highscores[:self.max_scores]
        
        # Guardar
        self.save_highscores()
        
        # Retornar la posición en el ranking
        for i, score_entry in enumerate(self.highscores):
            if score_entry == new_score:
                return i + 1
        return -1
    
    def get_highscores(self):
        """Retorna la lista de high scores"""
        return self.highscores
    
    def get_rank(self, score):
        """Retorna en qué posición quedaría una puntuación"""
        for i, score_entry in enumerate(self.highscores):
            if score > score_entry['score']:
                return i + 1
        if len(self.highscores) < self.max_scores:
            return len(self.highscores) + 1
        return -1  # No entra en el top 10

