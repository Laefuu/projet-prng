import numpy as np
from scipy import stats

def ks_test_uniform(data: bytes):
    """
    Test de Kolmogorov-Smirnov pour vérifier l'uniformité continue.
    On normalise les octets [0, 255] vers [0.0, 1.0].
    
    H0: Les données suivent une loi uniforme U(0,1).
    """
    if not data:
        return 0.0, 0.0

    # Normalisation des données
    # Note: Ajouter un petit bruit aléatoire (dithering) est parfois conseillé 
    # pour les données discrètes testées contre des lois continues, 
    # mais pour ce projet, une normalisation simple suffit.
    values = np.frombuffer(data, dtype=np.uint8) / 255.0
    
    # Test contre la CDF (Cumulative Distribution Function) uniforme
    statistic, p_value = stats.kstest(values, 'uniform')
    
    return statistic, p_value

def ks_test_normal(values: list):
    """
    Test KS spécifique pour les générateurs gaussiens (Box-Muller).
    Attend une liste de floats, pas des bytes.
    H0: Les données suivent une loi Normale N(0,1).
    """
    # 'norm' par défaut est moyenne=0, écart-type=1
    statistic, p_value = stats.kstest(values, 'norm')
    return statistic, p_value