import cv2
import numpy as np
import solver as sv
from execute_solution import execute_moves  # ✅ Corrigé ici

# Couleurs disponibles
COLOR_KEYS = {
    'w': 'U',  # White (Up)
    'r': 'R',  # Red (Right)
    'g': 'F',  # Green (Front)
    'y': 'D',  # Yellow (Down)
    'o': 'L',  # Orange (Left)
    'b': 'B',  # Blue (Back)
}
COLOR_BGR = {
    'U': (255, 255, 255),
    'R': (0, 0, 255),
    'F': (0, 255, 0),
    'D': (0, 255, 255),
    'L': (0, 165, 255),
    'B': (255, 0, 0),
}

detected_faces = []
current_face = 0
square_positions = [(270, 190), (370, 190), (270, 290), (370, 290)]

def detect_face():
    cap = cv2.VideoCapture(0)
    print("Appuie sur 'c' pour capturer une face, 'q' pour quitter")
    face_colors = []
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        for x, y in square_positions:
            cv2.rectangle(frame, (x, y), (x + 40, y + 40), (0, 255, 0), 2)
        cv2.imshow("Capture Face", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            for x, y in square_positions:
                roi = hsv[y:y + 40, x:x + 40]
                avg_color = np.mean(roi.reshape(-1, 3), axis=0)
                face_colors.append(guess_color_from_hsv(avg_color))
            break
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return face_colors

def guess_color_from_hsv(hsv_pixel):
    h, s, v = hsv_pixel
    if v < 50:
        return 'B'
    if s < 50:
        return 'U'
    if h < 10 or h > 160:
        return 'R'
    elif 10 < h < 25:
        return 'L'
    elif 25 < h < 40:
        return 'D'
    elif 40 < h < 85:
        return 'F'
    else:
        return 'B'

def modify_colors(facelets):
    selected = 0
    positions = [(50, 50), (150, 50), (50, 150), (150, 150)]

    def get_clicked_index(x, y):
        for i, (px, py) in enumerate(positions):
            if px <= x <= px + 80 and py <= y <= py + 80:
                return i
        return -1

    def mouse_callback(event, x, y, flags, param):
        nonlocal selected
        if event == cv2.EVENT_LBUTTONDOWN:
            idx = get_clicked_index(x, y)
            if idx != -1:
                selected = idx

    cv2.namedWindow("Modifier Couleurs")
    cv2.setMouseCallback("Modifier Couleurs", mouse_callback)

    while True:
        img = np.zeros((300, 300, 3), dtype=np.uint8)
        for i, facelet in enumerate(facelets):
            x, y = positions[i]
            color = COLOR_BGR[facelet]
            cv2.rectangle(img, (x, y), (x + 80, y + 80), color, -1)
            if i == selected:
                cv2.rectangle(img, (x, y), (x + 80, y + 80), (0, 255, 255), 2)
            cv2.putText(img, facelet, (x + 28, y + 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        cv2.imshow("Modifier Couleurs", img)
        key = cv2.waitKey(0) & 0xFF

        if key == 13:
            break
        elif chr(key) in COLOR_KEYS:
            facelets[selected] = COLOR_KEYS[chr(key)]

    cv2.destroyWindow("Modifier Couleurs")
    return facelets

def faces_to_string(faces):
    cube_string = ''.join(faces)
    if len(cube_string) != 24:
        raise ValueError(f"Erreur : la chaîne de couleurs doit contenir exactement 24 caractères, mais elle en contient {len(cube_string)}")
    return cube_string

def main():
    print("== Rubik's Cube 2x2: Capture des faces ==")
    faces = []
    for i in range(6):
        print(f"Capture face {i + 1}/6")
        colors = detect_face()
        if len(colors) != 4:
            print("Erreur lors de la capture. Relancez.")
            return
        colors = modify_colors(colors)
        faces.extend(colors)

    print("Correction manuelle des couleurs terminée")
    print("Faces finales :", ''.join(faces))
    
    cube_string = faces_to_string(faces)
    print("Cube string pour résolution :", cube_string)

    solution = sv.solve(cube_string)
    print("Solution :", solution)

    # ✅ Conversion et exécution
    move_list = solution.strip().split()
    execute_moves(move_list)  # ✅ Appel direct à la fonction de mouvement

if __name__ == "__main__":
    main()import cv2
import numpy as np
import solver as sv
from execute_solution import execute_moves  # ✅ Corrigé ici

# Couleurs disponibles
COLOR_KEYS = {
    'w': 'U',  # White (Up)
    'r': 'R',  # Red (Right)
    'g': 'F',  # Green (Front)
    'y': 'D',  # Yellow (Down)
    'o': 'L',  # Orange (Left)
    'b': 'B',  # Blue (Back)
}
COLOR_BGR = {
    'U': (255, 255, 255),
    'R': (0, 0, 255),
    'F': (0, 255, 0),
    'D': (0, 255, 255),
    'L': (0, 165, 255),
    'B': (255, 0, 0),
}

detected_faces = []
current_face = 0
square_positions = [(270, 190), (370, 190), (270, 290), (370, 290)]

def detect_face():
    cap = cv2.VideoCapture(0)
    print("Appuie sur 'c' pour capturer une face, 'q' pour quitter")
    face_colors = []
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        for x, y in square_positions:
            cv2.rectangle(frame, (x, y), (x + 40, y + 40), (0, 255, 0), 2)
        cv2.imshow("Capture Face", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            for x, y in square_positions:
                roi = hsv[y:y + 40, x:x + 40]
                avg_color = np.mean(roi.reshape(-1, 3), axis=0)
                face_colors.append(guess_color_from_hsv(avg_color))
            break
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return face_colors

def guess_color_from_hsv(hsv_pixel):
    h, s, v = hsv_pixel
    if v < 50:
        return 'B'
    if s < 50:
        return 'U'
    if h < 10 or h > 160:
        return 'R'
    elif 10 < h < 25:
        return 'L'
    elif 25 < h < 40:
        return 'D'
    elif 40 < h < 85:
        return 'F'
    else:
        return 'B'

def modify_colors(facelets):
    selected = 0
    positions = [(50, 50), (150, 50), (50, 150), (150, 150)]

    def get_clicked_index(x, y):
        for i, (px, py) in enumerate(positions):
            if px <= x <= px + 80 and py <= y <= py + 80:
                return i
        return -1

    def mouse_callback(event, x, y, flags, param):
        nonlocal selected
        if event == cv2.EVENT_LBUTTONDOWN:
            idx = get_clicked_index(x, y)
            if idx != -1:
                selected = idx

    cv2.namedWindow("Modifier Couleurs")
    cv2.setMouseCallback("Modifier Couleurs", mouse_callback)

    while True:
        img = np.zeros((300, 300, 3), dtype=np.uint8)
        for i, facelet in enumerate(facelets):
            x, y = positions[i]
            color = COLOR_BGR[facelet]
            cv2.rectangle(img, (x, y), (x + 80, y + 80), color, -1)
            if i == selected:
                cv2.rectangle(img, (x, y), (x + 80, y + 80), (0, 255, 255), 2)
            cv2.putText(img, facelet, (x + 28, y + 55), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        cv2.imshow("Modifier Couleurs", img)
        key = cv2.waitKey(0) & 0xFF

        if key == 13:
            break
        elif chr(key) in COLOR_KEYS:
            facelets[selected] = COLOR_KEYS[chr(key)]

    cv2.destroyWindow("Modifier Couleurs")
    return facelets

def faces_to_string(faces):
    cube_string = ''.join(faces)
    if len(cube_string) != 24:
        raise ValueError(f"Erreur : la chaîne de couleurs doit contenir exactement 24 caractères, mais elle en contient {len(cube_string)}")
    return cube_string

def main():
    print("== Rubik's Cube 2x2: Capture des faces ==")
    faces = []
    for i in range(6):
        print(f"Capture face {i + 1}/6")
        colors = detect_face()
        if len(colors) != 4:
            print("Erreur lors de la capture. Relancez.")
            return
        colors = modify_colors(colors)
        faces.extend(colors)

    print("Correction manuelle des couleurs terminée")
    print("Faces finales :", ''.join(faces))
    
    cube_string = faces_to_string(faces)
    print("Cube string pour résolution :", cube_string)

    solution = sv.solve(cube_string)
    print("Solution :", solution)

    # ✅ Conversion et exécution
    move_list = solution.strip().split()
    execute_moves(move_list)  # ✅ Appel direct à la fonction de mouvement

if __name__ == "__main__":
    main()
