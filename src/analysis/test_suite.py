from src.generators.base_generator import BaseGenerator
from .entropy import shannon_entropy, entropy_score
from .chi_squared import chi_squared_test, chi2_score

def run_statistical_tests(generator: BaseGenerator, sample_size=100000):
    """
    Exécute la batterie de tests sur un générateur donné.
    Génère 'sample_size' octets et analyse.
    """
    # 1. Génération de l'échantillon
    # On reset la seed pour reproductibilité si besoin, ou on laisse tel quel
    data = generator.next_bytes(sample_size)
    
    # 2. Entropie
    h_val = shannon_entropy(data)
    h_score = entropy_score(h_val)
    
    # 3. Chi-2
    chi2_stat, p_val = chi_squared_test(data)
    c_score = chi2_score(p_val)
    
    # 4. Rapport
    results = {
        "sample_size": sample_size,
        "entropy": {
            "value": h_val,
            "score": h_score,
            "verdict": "Excellent" if h_val > 7.9 else "Suspect"
        },
        "chi_squared": {
            "statistic": chi2_stat,
            "p_value": p_val,
            "score": c_score,
            "verdict": "Fail" if p_val < 0.01 else "Pass"
        }
    }
    return results