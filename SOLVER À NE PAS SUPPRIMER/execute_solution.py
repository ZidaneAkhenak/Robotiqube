import os
import time
import socket
# Dossier contenant les scripts de mouvement pour le robot UR
URSCRIPT_FOLDER = "mouvements_caméra"  # Adapte ce chemin selon ton organisation de fichiers

# Paramètres de la connexion TCP (IP et port du robot UR)
ROBOT_IP = "192.168.1.100"  # Remplace par l'IP de ton robot UR
ROBOT_PORT = 30002  # Port par défaut pour communiquer avec un robot UR via TCP

# Importation de ton solveur Kociemba ou similaire
from solver import sv  # Remplace par l'import correct de ton solveur Kociemba

def normalize_moves(solution_str):
    """
    Normalise les mouvements reçus en format standard UR, notamment les U2 et U3.
    Convertit les mouvements complexes (U2, U3) en séquences simples (U U, U' U' U').
    """
    moves = solution_str.strip().split()
    normalized = []

    for move in moves:
        base = move[0]  # Mouvement de base comme 'U', 'R', etc.
        suffix = move[1:] if len(move) > 1 else ''  # Gérer les suffixes comme '2', "'", etc.

        # Gérer les doubles et triples mouvements
        if suffix == "2":
            normalized += [base, base]  # Double mouvement
        elif suffix == "3":
            normalized += [base + "'"] * 3  # Triple mouvement (U' U' U')
        else:
            normalized.append(move)  # Mouvement simple (U, R, F', etc.)
    
    return normalized

def execute_move(move):
    """
    Exécute un mouvement en envoyant le fichier correspondant au robot via TCP.
    Le fichier doit exister dans le répertoire `mouvements_ur`.
    """
    filename = f"mouvement {move}.script"  # Nom du fichier URScript
    filepath = os.path.join(URSCRIPT_FOLDER, filename)

    if os.path.exists(filepath):
        print(f"[INFO] Envoi du mouvement : {move}")
        # Lire le script du fichier et l'envoyer au robot
        with open(filepath, "r") as f:
            script_content = f.read()
            send_to_robot(script_content)  # Envoi du script au robot
            time.sleep(0.5)  # Pause pour permettre au robot d'exécuter le mouvement
    else:
        print(f"[ERREUR] Fichier introuvable pour le mouvement : {filepath}")

def send_to_robot(script_content):
    """
    Envoie un script au robot UR via TCP.
    Utilise un socket pour se connecter à l'IP et au port du robot.
    """
    try:
        # Création de la connexion TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ROBOT_IP, ROBOT_PORT))  # Connexion au robot
            sock.sendall(script_content.encode("utf-8"))  # Envoi du script
            print(f"[INFO] Script envoyé au robot : {script_content[:50]}...")  # Affichage partiel pour sécurité
            time.sleep(0.5)  # Pause après envoi
    except Exception as e:
        print(f"[ERREUR] Impossible de connecter au robot : {e}")

def solve_cube(cube_string):
    """
    Résout le Rubik's Cube 2x2 en utilisant le solveur Kociemba ou un solveur similaire.
    Le cube_string doit être un string représentant l'état du cube.
    """
    solution = sv.solve(cube_string)  # Appel du solveur de Kociemba
    print("Solution :", solution)  # Affiche la solution trouvée par le solveur
    return solution  # Retourne la solution sous forme de string

def execute_solution(cube_string):
    """
    Exécute une solution complète en appelant chaque mouvement dans l'ordre,
    après avoir converti et envoyé les scripts correspondants au robot.
    """
    solution_str = solve_cube(cube_string)  # Calculer la solution à partir de la string du cube
    print("[INFO] Solution reçue :", solution_str)
    
    moves = normalize_moves(solution_str)  # Normalisation des mouvements
    for move in moves:
        execute_move(move)  # Envoi du mouvement au robot


