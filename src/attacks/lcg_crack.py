def egcd(a, b):
    """Algorithme d'Euclide étendu. Retourne (g, x, y) tel que ax + by = g."""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """Calcule l'inverse modulaire de a modulo m."""
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('L\'inverse modulaire n\'existe pas (a et m ne sont pas premiers entre eux)')
    else:
        return x % m

def crack_lcg_params(states, m):
    """
    Retrouve a et c à partir d'une séquence d'états et du module m.
    Nécessite au moins 3 états consécutifs : x0, x1, x2.
    Maths:
      x1 = a*x0 + c (mod m)
      x2 = a*x1 + c (mod m)
      => x2 - x1 = a(x1 - x0) (mod m)
      => a = (x2 - x1) * inv(x1 - x0) (mod m)
      => c = x1 - a*x0 (mod m)
    """
    if len(states) < 3:
        raise ValueError("Il faut au moins 3 états pour retrouver a et c.")

    x0 = states[0]
    x1 = states[1]
    x2 = states[2]

    # Calcul de a
    diff_outputs = (x2 - x1) % m
    diff_inputs = (x1 - x0) % m
    
    try:
        inverse = modinv(diff_inputs, m)
        a_found = (diff_outputs * inverse) % m
    except Exception:
        # Si l'inverse n'existe pas, c'est plus compliqué (plusieurs solutions possibles),
        # mais pour la démo pédagogique on suppose que ça marche.
        return None, None

    # Calcul de c
    c_found = (x1 - a_found * x0) % m

    return a_found, c_found