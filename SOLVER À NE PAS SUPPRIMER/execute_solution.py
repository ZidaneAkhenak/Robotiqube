import socket
import time
import os

# Configuration du robot UR
ROBOT_IP = "Ton adresse IP"
ROBOT_PORT = 

# Dossier contenant les scripts
chemin_dossier = "/endroit/où/tes/script"

# Cooldowns pour chaque mouvement
COOLDOWNS = {
    'U1': 25,
    'U3': 25,
    'U2': 30,
    'R1': 85,
    'R3': 85,
    'R2': 90,
    'F1': 90,
    'F3': 95,
    'F2': 100,
}

def execute_moves(move_list):
    for idx, move in enumerate(move_list):
        script_name = move + ".script"
        script_path = os.path.join(chemin_dossier, script_name)

        print(f"\n➡️ [{idx + 1}/{len(move_list)}] Préparation du mouvement : {move}")

        if not os.path.exists(script_path):
            print(f"❌ Fichier introuvable : {script_name}")
            continue

        try:
            with open(script_path, 'r') as file:
                script_content = file.read()

            if not script_content.strip():
                print(f"⚠️ Le fichier {script_name} est vide. Mouvement ignoré.")
                continue
            
            print(f"📤 Envoi de {script_name} au robot...")
            with socket.create_connection((ROBOT_IP, ROBOT_PORT), timeout=5) as sock:
                time.sleep(0.3)  # Pause de sécurité
                sock.sendall(script_content.encode('utf-8'))
                time.sleep(0.2)  # ✅ Nouvelle ligne pour laisser le robot lire avant fermeture
                sock.shutdown(socket.SHUT_WR)

            



            cooldown = COOLDOWNS.get(move, 1.0)
            print(f"⏳ Attente de {cooldown:.1f} secondes après le mouvement {move}...")
            time.sleep(cooldown)

        except Exception as e:
            print(f"⚠️ Erreur lors de l'envoi de {script_name} : {e}")

    print("\n✅ Tous les mouvements ont été traités.")

if __name__ == '__main__':
    # Exemple de solution pour test
    example_solution = ["R1", "U3", "F2"]
    execute_moves(example_solution)
