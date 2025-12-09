from src.generators.base_generator import BaseGenerator
from .entropy import shannon_entropy, entropy_score
from .chi_squared import chi_squared_test, chi2_score
from .autocorrelation import autocorrelation_test, max_autocorr_score
from .ks_test import ks_test_uniform

def run_statistical_tests(generator: BaseGenerator, sample_size=50000):
    """
    Exécute la batterie complète de tests sur un générateur.
    """
    # 1. Génération des données brutes (octets)
    data = generator.next_bytes(sample_size)
    
    # --- Test 1: Entropie ---
    h_val = shannon_entropy(data)
    h_score = entropy_score(h_val)
    
    # --- Test 2: Chi-Carré (Uniformité des octets) ---
    chi2_stat, chi2_p = chi_squared_test(data)
    
    # --- Test 3: Autocorrélation (Indépendance temporelle) ---
    # Lags choisis arbitrairement pour détecter des cycles courts et moyens
    ac_results = autocorrelation_test(data, lags=[1, 2, 8, 32])
    ac_score = max_autocorr_score(ac_results)
    
    # --- Test 4: Kolmogorov-Smirnov (Uniformité continue) ---
    ks_stat, ks_p = ks_test_uniform(data)
    
    # --- Agrégation des résultats ---
    results = {
        "sample_size": sample_size,
        "entropy": {
            "value": h_val,
            "score": h_score
        },
        "chi_squared": {
            "p_value": chi2_p,
            "verdict": "Pass" if chi2_p > 0.01 else "Fail"
        },
        "autocorrelation": {
            "coeffs": ac_results,
            "score": ac_score, # 1.0 = Bien, 0.0 = Corrélation forte
        },
        "ks_test": {
            "statistic": ks_stat,
            "p_value": ks_p,
            "verdict": "Pass" if ks_p > 0.01 else "Fail"
        }
    }
    
    # Calcul d'un "Global Score" simple (moyenne pondérée)
    # On pondère fortement l'entropie et l'autocorrélation
    # Les p-values sont binaires (pass/fail) donc plus dures à moyenner linéairement
    global_score = (h_score * 0.4) + (ac_score * 0.4) + (1.0 if chi2_p > 0.01 else 0.0) * 0.2
    results["global_score"] = global_score
    
    return results