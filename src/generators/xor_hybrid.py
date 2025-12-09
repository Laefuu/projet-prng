from .base_generator import BaseGenerator
from .lcg import LCG
from .mt_wrapper import MT19937

class XORGenerator(BaseGenerator):
    """
    Générateur hybride combinant deux PRNGs via une opération XOR.
    """
    def __init__(self, seed: int = 42):
        # On initialise deux générateurs différents avec des graines dérivées
        # Pour l'exemple, on combine un LCG et un Mersenne Twister
        # (Ou deux LCG avec des paramètres différents pour voir l'effet)
        self.gen1 = LCG(seed=seed)
        self.gen2 = MT19937(seed=seed ^ 0xFFFFFFFF)
        self.set_seed(seed)

    def set_seed(self, seed: int):
        self.gen1.set_seed(seed)
        self.gen2.set_seed(seed ^ 0xAAAA5555) # Décorrélation simple des graines

    def next_int(self) -> int:
        """
        Retourne : Sortie(Gen1) XOR Sortie(Gen2)
        """
        val1 = self.gen1.next_int()
        val2 = self.gen2.next_int()
        return val1 ^ val2