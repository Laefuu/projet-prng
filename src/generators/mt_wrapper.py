import random
from .base_generator import BaseGenerator

class MT19937(BaseGenerator):
    """
    Wrapper autour du générateur Mersenne Twister de Python (random).
    """
    def __init__(self, seed: int = None):
        self.rng = random.Random()
        self.set_seed(seed)

    def set_seed(self, seed: int):
        self.rng.seed(seed)

    def next_int(self) -> int:
        """Retourne un entier de 32 bits."""
        return self.rng.getrandbits(32)