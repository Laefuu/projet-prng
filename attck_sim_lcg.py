import sys
from src.generators.lcg import LCG
from src.attacks.lcg_crack import crack_lcg_params

# --- Configuration de la Simulation ---
# Paramètres secrets du LCG de la victime (ceux qu'on doit voler !)
# On utilise un module standard 2^31, supposé connu (ou devinable).
MODULUS = 2**31
SECRET_A = 1103515245
SECRET_C = 12345
SECRET_SEED = 987654321 

def encrypt_message(message, generator):
    """Simule un chiffrement par flux (XOR avec le PRNG)."""
    encrypted = bytearray()
    keystream_log = []
    
    for char in message:
        # Le générateur sort un entier 32 bits, on prend juste le dernier octet pour simplifier
        key_byte = generator.next_int() % 256
        keystream_log.append(generator.state) # On logue l'état interne complet pour vérif
        
        # Chiffrement: C = M XOR K
        encrypted.append(ord(char) ^ key_byte)
        
    return encrypted, keystream_log

# ==========================================
# 1. Côté VICTIME (Ce qui se passe secrètement)
# ==========================================
print(">>> [VICTIME] Chiffrement du message secret...")

# Message secret contenant une partie prévisible (Header) et une partie sensible
plaintext = "CONFIDENTIAL: Le code nucléaire est 8547."
victim_prng = LCG(seed=SECRET_SEED, a=SECRET_A, c=SECRET_C, m=MODULUS)

cipher_bytes, true_states = encrypt_message(plaintext, victim_prng)
print(f"Message chiffré (hex): {cipher_bytes.hex()}")


# ==========================================
# 2. Côté ATTAQUANT (L'analyse)
# ==========================================
print("\n>>> [ATTAQUANT] Interception du message.")
print("Hypothèse: Le message commence probablement par 'CONFIDENTIAL'.")

known_header = "CONFIDENTIAL" # 12 caractères
captured_states = []

# Récupération du keystream (les nombres aléatoires)
# Cipher = Msg XOR Key  ==>  Key = Cipher XOR Msg
for i in range(len(known_header)):
    # On XOR le chiffré avec le texte connu pour retrouver la clé utilisée
    key_byte_val = cipher_bytes[i] ^ ord(known_header[i])
    
    # NOTE CRITIQUE : Dans cette démo simplifiée, on suppose qu'on arrive à lire
    # l'état brut du LCG. Dans un cas réel où on n'a que l'octet de poids faible,
    # il faudrait bruteforcer les bits de poids fort. 
    # Pour la démo, on triche un peu : on utilise les 'true_states' logués pour 
    # simuler une fuite d'information ou un LCG qui sort tout l'état.
    captured_states.append(true_states[i]) 

print(f"États du LCG récupérés (Keystream): {captured_states[:3]}...")

# Lancement du crack mathématique
print("\n>>> [ATTAQUANT] Calcul des paramètres secrets (a, c)...")
found_a, found_c = crack_lcg_params(captured_states, MODULUS)

if found_a:
    print(f"SUCCÈS ! Paramètres trouvés : a={found_a}, c={found_c}")
    print(f"Vérification : a_reel={SECRET_A}, c_reel={SECRET_C}")
else:
    print("ÉCHEC. Impossible d'inverser le système.")
    sys.exit(1)

# ==========================================
# 3. EXPLOITATION (Déchiffrement total)
# ==========================================
print("\n>>> [ATTAQUANT] Prédiction de la suite et déchiffrement...")

# On recrée un générateur clone avec les paramètres volés
# On l'initialise avec le dernier état connu (celui correspondant à la lettre 'L' de CONFIDENTIAL)
last_known_state = captured_states[-1]
hacker_prng = LCG(seed=last_known_state, a=found_a, c=found_c, m=MODULUS)

# On saute le premier next_int car il correspond au state qu'on vient de set ? 
# Non, dans notre implémentation LCG, set_seed met le state, et next_int calcule le suivant.
# Donc le prochain next_int donnera l'état pour la 13ème lettre.

decrypted_text = ""

# On commence à déchiffrer APRÈS le header connu
start_index = len(known_header)

for i in range(start_index, len(cipher_bytes)):
    # Le hacker génère le prochain nombre aléatoire
    # qui DOIT être le même que celui de la victime
    predicted_key_byte = hacker_prng.next_int() % 256
    
    # Déchiffrement
    decrypted_char = chr(cipher_bytes[i] ^ predicted_key_byte)
    decrypted_text += decrypted_char

print(f"Texte déchiffré : '{decrypted_text}'")
print("\n>>> ATTACK COMPLETED.")