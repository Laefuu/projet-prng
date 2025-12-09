from src.generators.lcg import LCG
from src.generators.mt_wrapper import MT19937
from src.generators.system_rng import SystemRNG
from src.generators.bbs import BlumBlumShub
import time
from src.generators.xor_hybrid import XORGenerator
from src.generators.box_muller import BoxMuller

def test_gen(name, generator_class):
    print(f"--- Test de {name} ---")
    gen = generator_class()
    start = time.time()
    
    # Générer 5 entiers
    vals = [gen.next_int() for _ in range(5)]
    
    end = time.time()
    print(f"Sortie: {vals}")
    print(f"Temps pour 5 entiers: {(end-start)*1000:.4f} ms")
    print("-" * 20)

if __name__ == "__main__":
    test_gen("LCG", LCG)
    test_gen("Mersenne Twister", MT19937)
    test_gen("System RNG", SystemRNG)
    test_gen("Blum-Blum-Shub", BlumBlumShub)
    test_gen("XOR Hybride", XORGenerator)
    
    print("--- Test de Box-Muller ---")
    bm = BoxMuller()
    samples = [bm.next_sample() for _ in range(5)]
    print(f"Sortie (Floats gaussiens) : {[round(x, 4) for x in samples]}")
    # Vérifions que next_int nous donne bien des octets centrés sur 128
    ints = [bm.next_int() for _ in range(10)]
    print(f"Sortie (Mappée int 0-255) : {ints}")
    print("-" * 20)