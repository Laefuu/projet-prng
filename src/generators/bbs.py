from .base_generator import BaseGenerator

class BlumBlumShub(BaseGenerator):
    """
    Générateur Blum-Blum-Shub (CSPRNG).
    Formule: x_{n+1} = x_n^2 mod M
    """
    
    # Paramètres par défaut (petits pour la démo, comme demandé)
    # p et q doivent être congrus à 3 mod 4.
    DEFAULT_P = 30000000091 # Premier exemple
    DEFAULT_Q = 40000000003 # Premier exemple
    
    def __init__(self, seed: int = 123456, p=DEFAULT_P, q=DEFAULT_Q):
        self.p = p
        self.q = q
        self.M = p * q
        self.state = seed
        # Vérification basique de la seed (doit être première avec M et > 1)
        if self.state % self.p == 0 or self.state % self.q == 0:
            self.state += 1 
        self.set_seed(self.state)

    def set_seed(self, seed: int):
        # Pour BBS, la seed doit être au carré mod M pour démarrer
        self.state = (seed * seed) % self.M

    def next_bit(self) -> int:
        """Génère un seul bit."""
        self.state = (self.state * self.state) % self.M
        return self.state % 2  # Bit de parité (Least Significant Bit)

    def next_int(self) -> int:
        """
        Reconstitue un entier 32 bits en appelant 32 fois le générateur.
        C'est pour cela que BBS est lent.
        """
        val = 0
        for _ in range(32):
            val = (val << 1) | self.next_bit()
        return val