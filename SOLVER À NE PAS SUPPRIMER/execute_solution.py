import socket
import time
import os

# ⚙️ Configuration
ROBOT_IP = "adreseIP"  # ← Adresse IP de ton robot UR3e
ROBOT_PORT = 30002         # Port standard de contrôle
COOLDOWN_SECONDS = 2.5     # Délai entre chaque mouvement
chemin_dossier = "Endroit/ou/les/scripts/sont  # ← Ton dossier contenant les .script

# 🔁 Ajouter "sleep(2.5)" à chaque fichier script si ce n’est pas déjà présent
for nom_fichier in os.listdir(chemin_dossier):
    if nom_fichier.endswith(".script"):
        chemin_complet = os.path.join(chemin_dossier, nom_fichier)
        with open(chemin_complet, "r+") as f:
            contenu = f.read().strip()
            if not contenu.endswith("sleep(2.5)"):
                f.write("\n\nsleep(2.5)\n")
                print(f"✅ Ajout de sleep(2.5) à : {nom_fichier}")
            else:
                print(f"⏩ Déjà présent dans : {nom_fichier}")

# 🚀 Envoie la séquence de mouvements au robot
def execute_moves(move_list):
    for move in move_list:
        script_name = move + ".script" 
        script_path = os.path.join(chemin_dossier, script_name)

        if not os.path.exists(script_path):
            print(f"❌ Fichier introuvable : {script_name}")
            continue

        try:
            with open(script_path, 'r') as file:
                script_content = file.read()

            print(f"📤 Envoi au robot : {script_name}")
            with socket.create_connection((ROBOT_IP, ROBOT_PORT), timeout=5) as sock:
                sock.sendall(script_content.encode('utf-8'))

            print(f"✅ Envoyé : {move} → {script_name}")
            time.sleep(COOLDOWN_SECONDS)

        except Exception as e:
            print(f"⚠️ Erreur lors de l'envoi de {script_name} : {e}")
