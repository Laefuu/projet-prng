import numpy as np
from scipy import stats

def chi_squared_test(data: bytes):
    """
    Effectue le test du Chi-2 d'uniformité sur des octets.
    H0 (Hypothèse nulle) : Les données sont uniformément distribuées.
    
    Retourne:
        chi2_stat: La statistique de test
        p_value: La probabilité que H0 soit vraie ( > 0.01 ou 0.05 est bon)
    """
    if not data:
        return 0.0, 0.0
    
    n = len(data)
    observed_counts = np.zeros(256, dtype=int)
    
    # Compter les occurrences (histogramme)
    for byte in data:
        observed_counts[byte] += 1
        
    # Fréquence attendue pour une distribution uniforme parfaite
    expected_count = n / 256.0
    
    # Calcul de la statistique Chi-2: sum((O - E)^2 / E)
    # On utilise scipy pour la p-value qui est complexe à calculer à la main
    chi2_stat, p_value = stats.chisquare(observed_counts, f_exp=expected_count)
    
    return chi2_stat, p_value

def chi2_score(p_value: float) -> float:
    """
    Score normalisé basé sur la p-value.
    Si p_value < 0.01 (1%), on rejette l'aléatoire (Score 0).
    Sinon, on considère que c'est plausible.
    Pour le projet, on peut retourner la p-value directement comme indicateur de qualité [0,1].
    """
    return p_value