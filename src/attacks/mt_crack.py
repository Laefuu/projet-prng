def undo_right_shift_xor(value, shift):
    """
    Inverse l'opération: y = x ^ (x >> shift)
    """
    result = value
    for _ in range(32 // shift):
        result = value ^ (result >> shift)
    return result

def undo_left_shift_xor_and_mask(value, shift, mask):
    """
    Inverse l'opération: y = x ^ ((x << shift) & mask)
    """
    result = value
    for _ in range(32 // shift):
        result = value ^ ((result << shift) & mask)
    return result

def untemper(y):
    """
    Inverse la fonction de 'tempering' du MT19937 pour retrouver l'état interne.
    Les constantes sont celles du standard MT19937.
    
    Opérations standard (Forward):
    y ^= (y >> 11)
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 15) & 0xefc60000
    y ^= (y >> 18)
    """
    
    # On inverse les opérations dans l'ordre INVERSE (de la dernière à la première)
    
    # 4. y ^= (y >> 18)
    y = undo_right_shift_xor(y, 18)
    
    # 3. y ^= (y << 15) & 0xefc60000
    y = undo_left_shift_xor_and_mask(y, 15, 0xefc60000)
    
    # 2. y ^= (y << 7) & 0x9d2c5680
    y = undo_left_shift_xor_and_mask(y, 7, 0x9d2c5680)
    
    # 1. y ^= (y >> 11)
    y = undo_right_shift_xor(y, 11)
    
    return y

# Suite de src/attacks/mt_crack.py ...

class MT19937Engine:
    """
    Implémentation pure Python du MT19937 pour pouvoir injecter l'état reconstruit.
    """
    def __init__(self, state_vector):
        self.MT = list(state_vector) # Le tableau d'état de 624 entiers
        self.index = 624 # Forcer la régénération au prochain appel
        
    def next_int(self):
        if self.index >= 624:
            self.twist()
        
        y = self.MT[self.index]
        
        # Tempering standard
        y ^= (y >> 11)
        y ^= ((y << 7) & 0x9d2c5680)
        y ^= ((y << 15) & 0xefc60000)
        y ^= (y >> 18)
        
        self.index += 1
        return y & 0xffffffff

    def twist(self):
        for i in range(624):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff)
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.MT[i] ^= 0x9908b0df
        self.index = 0