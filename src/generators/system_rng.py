import os
from .base_generator import BaseGenerator

class SystemRNG(BaseGenerator):
    """
    Utilise /dev/urandom ou CryptGenRandom (via os.urandom).
    Considéré comme cryptographiquement sûr (CSPRNG).
    """
    def set_seed(self, seed: int):
        # Le SystemRNG ne prend généralement pas de seed utilisateur 
        # car il se base sur l'entropie système.
        # On ignore l'appel ou on l'utilise pour mélanger (optionnel).
        pass

    def next_int(self) -> int:
        """Récupère 4 octets aléatoires et les convertit en entier."""
        random_bytes = os.urandom(4)
        return int.from_bytes(random_bytes, byteorder='big')