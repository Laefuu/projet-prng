import random
from src.attacks.mt_crack import untemper, MT19937Engine

print(">>> Initialisation de la cible (Python Random Module)...")
# La victime utilise le random standard
random.seed(123456) 

print(">>> L'attaquant écoute 624 valeurs...")
collected_outputs = []
reconstructed_state = []

# Phase 1: Collecte
# On a besoin d'exactement 624 nombres de 32 bits
for i in range(624):
    # random.getrandbits(32) renvoie la sortie brute du MT19937
    val = random.getrandbits(32)
    collected_outputs.append(val)
    
    # Phase 2: Untempering (Calcul de l'état interne)
    internal_val = untemper(val)
    reconstructed_state.append(internal_val)

print(f"   [OK] 624 valeurs collectées.")
print(f"   Dernière valeur vue: {collected_outputs[-1]}")

print(">>> Clonage du générateur...")
# On injecte l'état reconstruit dans notre moteur maison
cloned_rng = MT19937Engine(reconstructed_state)

print("\n>>> TEST DE PRÉDICTION (Futur immédiat)")
print(f"{'#':<5} | {'VRAI (Python Random)':<25} | {'PRÉDIT (Attaquant)':<25} | {'Status'}")
print("-" * 70)

success_count = 0
for i in range(10):
    # La victime génère le nombre suivant
    real_next = random.getrandbits(32)
    
    # L'attaquant calcule le nombre suivant avec son clone
    predicted_next = cloned_rng.next_int()
    
    status = "SUCCÈS" if real_next == predicted_next else "ÉCHEC"
    if status == "SUCCÈS": success_count += 1
        
    print(f"{i+1:<5} | {real_next:<25} | {predicted_next:<25} | {status}")

print("-" * 70)
if success_count == 10:
    print("\n>>> RÉSULTAT: Générateur cloné à 100%. L'attaquant contrôle le futur.")
else:
    print("\n>>> RÉSULTAT: Échec de l'attaque.")