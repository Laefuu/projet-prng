import math
from collections import Counter

def shannon_entropy(data: bytes) -> float:
    """
    Calcule l'entropie de Shannon sur une séquence d'octets.
    Retourne une valeur en bits (max 8.0 pour des octets).
    """
    if not data:
        return 0.0

    # Compter les occurrences de chaque octet
    counts = Counter(data)
    total_len = len(data)
    
    entropy = 0.0
    for count in counts.values():
        p_i = count / total_len
        if p_i > 0:
            entropy -= p_i * math.log2(p_i)
            
    return entropy

def entropy_score(entropy_val: float) -> float:
    """
    Normalise l'entropie sur [0, 1].
    8.0 -> 1.0 (Parfait)
    0.0 -> 0.0 (Nul)
    """
    return min(entropy_val / 8.0, 1.0)