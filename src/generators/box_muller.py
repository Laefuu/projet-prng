import math
import random
from .base_generator import BaseGenerator

class BoxMuller(BaseGenerator):
    """
    Transforme une source uniforme en distribution normale (Gaussienne).
    Formule : Z0 = sqrt(-2 ln U1) * cos(2 pi U2)
    """
    def __init__(self, seed: int = 1):
        self.rng = random.Random() # Source uniforme sous-jacente
        self.set_seed(seed)
        self.stored_value = None # Box-Muller génère 2 valeurs à la fois

    def set_seed(self, seed: int):
        self.rng.seed(seed)
        self.stored_value = None

    def next_sample(self) -> float:
        """
        Retourne un float suivant une loi normale standard.
        """
        # Si on a une valeur en réserve (car générées par paire), on la retourne
        if self.stored_value is not None:
            val = self.stored_value
            self.stored_value = None
            return val

        # Sinon on génère une nouvelle paire (U1, U2)
        u1 = self.rng.random()
        u2 = self.rng.random()
        
        # Éviter log(0)
        if u1 <= 0:
            u1 = 1e-10

        r = math.sqrt(-2.0 * math.log(u1))
        theta = 2.0 * math.pi * u2

        z0 = r * math.cos(theta)
        z1 = r * math.sin(theta)

        self.stored_value = z1
        return z0

    def next_int(self) -> int:
        """
        Pour respecter l'interface BaseGenerator.
        On mappe la distribution normale [-3, 3] vers un entier [0, 255] ou [0, MAX_INT].
        Ici, on fait une conversion simple pour visualisation : centré sur 128 (octet).
        """
        val = self.next_sample()
        # On scale : moyenne 128, écart-type 32. 
        # ~99.7% des valeurs seront entre 32 et 224.
        res = int(val * 32 + 128)
        return max(0, min(255, res))