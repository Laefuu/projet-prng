# Fichier: src/generators/base_generator.py
from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    """
    Classe abstraite définissant l'interface pour tous les PRNGs du projet.
    Cela permet d'utiliser les mêmes fonctions de test pour tous les générateurs.
    """

    @abstractmethod
    def set_seed(self, seed: int):
        """Initialise la graine du générateur."""
        pass

    @abstractmethod
    def next_int(self) -> int:
        """Retourne le prochain entier généré (brut)."""
        pass

    def next_bytes(self, length: int) -> bytes:
        """
        Génère une séquence d'octets de longueur donnée.
        Méthode générique qui peut être surchargée si nécessaire.
        """
        result = bytearray()
        while len(result) < length:
            val = self.next_int()
            # On découpe l'entier en octets (4 octets pour un int 32 bits classique)
            # Note: cela dépend de la taille de sortie du générateur (ici supposé 32 bits min)
            result.extend(val.to_bytes(4, 'big'))
        return bytes(result[:length])