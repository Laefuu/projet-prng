# Fichier: src/generators/lcg.py
from .base_generator import BaseGenerator

class LCG(BaseGenerator):
    """
    Implémentation d'un Linear Congruential Generator (LCG).
    Formule : X_{n+1} = (a * X_n + c) mod m
    """

    # Paramètres par défaut (ceux de glibc/GCC)
    DEFAULT_A = 1103515245
    DEFAULT_C = 12345
    DEFAULT_M = 2**31

    def __init__(self, seed: int = 1, a: int = DEFAULT_A, c: int = DEFAULT_C, m: int = DEFAULT_M):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed
    
    def set_seed(self, seed: int):
        self.state = seed & (self.m - 1) # Assure que la seed est dans les bornes

    def next_int(self) -> int:
        """Calcule et retourne le prochain état."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def get_params(self):
        """Retourne les paramètres a, c, m (utile pour l'attaque)."""
        return self.a, self.c, self.m