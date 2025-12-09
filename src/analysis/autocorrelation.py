import numpy as np

def autocorrelation_test(data: bytes, lags=[1, 2, 8, 16]):
    """
    Calcule l'autocorrélation de la série de données pour différents décalages (lags).
    Une valeur proche de 1 ou -1 indique une forte corrélation (mauvais).
    Une valeur proche de 0 indique une indépendance (bon).
    """
    if not data:
        return {}
    
    # Conversion des octets en tableau numpy d'entiers
    series = np.frombuffer(data, dtype=np.uint8).astype(float)
    n = len(series)
    results = {}
    
    for lag in lags:
        if n <= lag:
            results[lag] = 0.0
            continue
            
        # On compare la série avec elle-même décalée de 'lag'
        # Slice: x[0 : n-lag] vs x[lag : n]
        x = series[:-lag]
        y = series[lag:]
        
        # Calcul du coefficient de corrélation de Pearson
        # La matrice de corr est [[1, corr], [corr, 1]], on prend [0,1]
        corr = np.corrcoef(x, y)[0, 1]
        
        if np.isnan(corr):
            corr = 0.0
            
        results[lag] = corr
        
    return results

def max_autocorr_score(results: dict) -> float:
    """
    Retourne un score agrégé basé sur la pire corrélation trouvée.
    Score = 1.0 - |max_correlation|
    1.0 = Parfait (0 correlation)
    0.0 = Échec total (correlation de 1 ou -1)
    """
    if not results:
        return 0.0
    
    # On cherche la valeur absolue maximale parmi tous les lags
    max_corr = max(abs(val) for val in results.values())
    
    # On s'assure que le score reste dans [0, 1]
    return max(0.0, 1.0 - max_corr)