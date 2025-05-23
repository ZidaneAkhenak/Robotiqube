import os
import time
import socket

# Dossier contenant les programmes .urp des mouvements sur la clé USB du robot
URP_FOLDER = "/programs/usb/Mouvements_cube_rubik"  # Chemin sur la clé USB montée dans le robot

# Adresse IP et port du robot UR (modifie selon ta configuration)
ROBOT_IP = "192.168.2.84"
ROBOT_PORT = 30002  # Port par défaut pour l'envoi de scripts

def get_program_name(move):
    """
    Traduit un mouvement du cube (U, U2, U', etc.) en nom de fichier de programme (.urp).
    Exemple :
        - "U"  → "U"
        - "U2" → "U2"
        - "U'" → "U3"
    """
    if move.endswith("'"):
        return move[0] + "3"  # Ex : "F'" → "F3"
    else:
        return move  # "U", "U2", etc.

def send_program_to_robot(program_path):
    """
    Envoie un script de chargement de programme URP au robot via socket.
    Cela utilise la commande 'load' puis 'play' du programme .urp.
    """
    try:
        # Génère une commande URScript pour charger et exécuter le programme
        ur_script = f'load("{program_path}")\nplay\n'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ROBOT_IP, ROBOT_PORT))
            sock.sendall(ur_script.encode("utf-8"))
            print(f"[INFO] Programme envoyé : {program_path}")
            time.sleep(1.0)  # Attente pour exécution du mouvement
    except Exception as e:
        print(f"[ERREUR] Échec de l'envoi du programme : {e}")

def execute_moves(move_list):
    """
    Exécute une liste de mouvements (ex: ['U', 'R', 'U2', 'R3']) sur le robot.
    """
    for move in move_list:
        program_name = get_program_name(move)
        program_path = f"{URP_FOLDER}/{program_name}.urp"
        send_program_to_robot(program_path)
