import cv2
import os
import random
import time
from ultralytics import YOLO

# configuration
OBJECTS_FOLDER = "objects"
MODEL_PATH = "yolov8n.pt"

# noms affichés
NOMS = {
    "bottle": "BOUTEILLE",
    "book": "LIVRE",
    "cell phone": "TELEPHONE",
    "backpack": "SAC À DOS",
    "scissors": "CISEAUX",
    "clock": "HORLOGE"
}

# noms fichier → classe yolo
YOLO_CLASSES = {
    "bouteille": "bottle",
    "livre": "book",
    "telephone": "cell phone",
    "sac à dos": "backpack",
    "ciseaux": "scissors",
    "horloge": "clock"
}

# chargement des objets
objects = []

for filename in os.listdir(OBJECTS_FOLDER):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        name = os.path.splitext(filename)[0].lower()

        # On garde seulement les objets connus de YOLO
        if name in YOLO_CLASSES:
            objects.append(name)

if not objects:
    print("ERREUR : aucun objet compatible dans objects/")
    exit()

print("Objets disponibles :")

for obj in objects:
    print(" -", obj)

# chargement de yolo
print()
print("Chargement de YOLO...")

model = YOLO(MODEL_PATH)

print("YOLO chargé !")

# webcam UGREEN
cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)

if not cap.isOpened():
    print("ERREUR: impossible d'ouvrir la webcam UGREEN.")
    exit()

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

# Réduire le buffer pour limiter la latence
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("Ouverte :", cap.isOpened())
print("Largeur :", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Hauteur :", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("FPS :", cap.get(cv2.CAP_PROP_FPS))

# variables du jeu
team = 1

target = None
target_class = None
target_display = None

started = False
finished_round = False
game_finished = False

start_time = None
final_time = None

team1_time = None
team2_time = None


# choisir un objet de la base de donnée
def choose_object(exclude=None):
    global target
    global target_class
    global target_display

    available_objects = objects.copy()

    if exclude in available_objects and len(available_objects) > 1:
        available_objects.remove(exclude)

    target = random.choice(available_objects)

    target_class = YOLO_CLASSES[target]
    target_display = NOMS[target_class]

choose_object()

print()
print("==============================")
print("ÉQUIPE 1")
print("OBJET À TROUVER :", target_display)
print("==============================")

# tant que le jeu n'est pas terminé
while True:
    ret, frame = cap.read()

    if not ret:
        print("Impossible de lire la webcam.")
        break

    height, width = frame.shape[:2]

    cv2.putText(frame, "CACHE-CACHE OBJET", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

    # affichage de l'équipe
    if not game_finished:
        cv2.putText(frame, f"EQUIPE {team}", (30, 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

        # objet à trouver
        cv2.putText(frame,f"TROUVE : {target_display}", (30, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)


    # avant le début de la manche
    if not started and not finished_round and not game_finished:
        cv2.putText(frame, "ESPACE = START", (30, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # manche commencée
    if started and not finished_round and not game_finished:
        # chronomètre
        elapsed = time.time() - start_time

        cv2.putText(frame, f"TEMPS : {elapsed:.2f} s", (30, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # YOLO
        results = model(frame, verbose=False)
        found = False

        # analyse des détections
        for result in results:
            for box in result.boxes:
                confidence = float(box.conf[0])

                # ignorer les détections peu fiables
                if confidence < 0.50:
                    continue

                class_id = int(box.cls[0])
                detected_name = model.names[class_id]

                # coordonnées de la boîte
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # DESSIN DE LA DÉTECTION
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                cv2.putText(frame, f"{detected_name} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if detected_name.lower() == target_class.lower():
                    found = True


        # objet trouvé
        if found:
            final_time = time.time() - start_time

            finished_round = True
            started = False

            # enregistrer temps equipe
            if team == 1:
                team1_time = final_time
            else:
                team2_time = final_time

            print()
            print("==============================")
            print(f"OBJET TROUVÉ - ÉQUIPE {team}")
            print("Objet :", target_display)
            print(f"Temps : {final_time:.2f} secondes")
            print("==============================")


    # fin de la manche
    if finished_round and not game_finished:
        cv2.putText(frame, "OBJET TROUVE !", (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        cv2.putText(frame, f"TEMPS FINAL : {final_time:.2f} s", (30, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # equipe 1 fini
        if team == 1:
            cv2.putText(frame, "ESPACE = EQUIPE 2", (30, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # equipe 2 fini
        else:
            cv2.putText(frame, "ESPACE = RESULTAT", (30, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # résultat final
    if game_finished:
        cv2.putText(frame, "RESULTAT FINAL", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)

        cv2.putText(frame, f"EQUIPE 1 : {team1_time:.2f} s", (30, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, f"EQUIPE 2 : {team2_time:.2f} s", (30, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)

        # comparaison
        if team1_time < team2_time:
            winner_text = "EQUIPE 1 GAGNE !"
        elif team2_time < team1_time:
            winner_text = "EQUIPE 2 GAGNE !"
        else:
            winner_text = "EGALITE !"

        cv2.putText(frame, winner_text, (30, 320), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0),3)

        cv2.putText(frame, "Q = QUITTER", (30, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # affichage
    cv2.imshow("Cache-cache Objet", frame)

    # attente de la touche clavier pour quitter
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # démarrer la manche avec la touche espace
    if key == 32:
        if not started and not finished_round and not game_finished:
            started = True
            start_time = time.time()

            print()
            print("GO !")
            print("Équipe :", team)
            print("Cherche :", target_display)

        # passer de l'équipe 1 à 2
        elif finished_round and team == 1:
            team = 2
            finished_round = False
            final_time = None

            choose_object(exclude=target)

            print()
            print("==============================")
            print("ÉQUIPE 2")
            print("OBJET À TROUVER :", target_display)
            print("==============================")

        # résultat final
        elif finished_round and team == 2:
            game_finished = True

            print()
            print("==============================")
            print("RESULTAT FINAL")
            print("==============================")

            print(f"Équipe 1 : {team1_time:.2f} secondes")
            print(f"Équipe 2 : {team2_time:.2f} secondes")

            if team1_time < team2_time:
                print("ÉQUIPE 1 GAGNE !")
            elif team2_time < team1_time:
                print("ÉQUIPE 2 GAGNE !")
            else:
                print("ÉGALITÉ !")

# fermeture
cap.release()
cv2.destroyAllWindows()