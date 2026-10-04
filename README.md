# Cache-cache objet — Détection d'objets en temps réel

## Description

Ce projet consiste à développer un **jeu de cache-cache d'objets utilisant la détection d'objets en temps réel** à partir d'une webcam.

Le principe est simple : deux équipes doivent trouver un objet indiqué à l'écran le plus rapidement possible. Une caméra filme la scène et un modèle **YOLOv8** analyse le flux vidéo afin de détecter l'objet recherché.

Le programme :

* utilise une webcam pour capturer la vidéo en temps réel ;
* utilise **YOLOv8** pour détecter les objets ;
* sélectionne aléatoirement un objet à rechercher ;
* affiche l'objet à trouver à l'écran ;
* mesure le temps nécessaire pour trouver l'objet ;
* permet à deux équipes de jouer successivement ;
* compare les temps des deux équipes ;
* affiche l'équipe gagnante.

## Technologies utilisées

* **Python 3**
* **OpenCV** pour la capture et l'affichage de la vidéo ;
* **Ultralytics YOLOv8** pour la détection d'objets ;
* **YOLOv8n** comme modèle de détection ;
* **Random** pour sélectionner aléatoirement les objets ;
* **Time** pour mesurer le temps de chaque manche.

## Structure du projet

```text
Object-Detection/
│
├── GAME/
│   ├── game.py
│   ├── objects/
│   │   ├── bouteille.jpg
│   │   ├── ciseaux.jpg
│   │   ├── horloge.jpg
│   │   ├── livre.jpg
│   │   ├── sac à dos.jpg
│   │   └── telephone.png
│   │
│   ├── objets_possible.txt
│   ├── start.txt
│   └── yolov8n.pt
│
├── README.md
└── requirements.txt
```

### Description des fichiers

| Fichier / dossier          | Description                             |
| -------------------------- | --------------------------------------- |
| `GAME/game.py`             | Programme principal du jeu              |
| `GAME/objects/`            | Images des objets disponibles           |
| `GAME/objets_possible.txt` | Liste des objets utilisables            |
| `GAME/start.txt`           | Informations de lancement               |
| `GAME/yolov8n.pt`          | Modèle YOLOv8 utilisé pour la détection |
| `requirements.txt`         | Dépendances Python du projet            |
| `README.md`                | Documentation du projet                 |

## Objets disponibles

Le jeu utilise actuellement les classes suivantes :

| Objet     | Classe YOLO  |
| --------- | ------------ |
| Bouteille | `bottle`     |
| Livre     | `book`       |
| Téléphone | `cell phone` |
| Sac à dos | `backpack`   |
| Ciseaux   | `scissors`   |
| Horloge   | `clock`      |

Les noms français sont utilisés pour l'affichage dans le jeu.

## Installation

### 1. Cloner le projet

```bash
git clone git@github.com:Alex-ov1/Object-Detection.git
cd Object-Detection
```

### 2. Créer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel Python :

```bash
python3 -m venv venv
```

Activer l'environnement :

```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancer le jeu

Se placer dans le dossier `GAME` :

```bash
cd GAME
```

Puis lancer :

```bash
python game.py
```

> Le fichier `yolov8n.pt` doit être présent dans le dossier `GAME`.

## Fonctionnement du jeu

### 1. Sélection de l'objet

Au démarrage, le programme parcourt automatiquement le dossier :

```text
GAME/objects/
```

Il récupère les images correspondant aux objets compatibles avec les classes reconnues par YOLO.

Un objet est ensuite choisi aléatoirement.

Par exemple :

```text
==============================
ÉQUIPE 1
OBJET À TROUVER : BOUTEILLE
==============================
```

### 2. Démarrage de la manche

Avant le début de la manche, l'écran indique :

```text
ESPACE = START
```

L'équipe appuie sur **Espace** pour commencer.

Le chronomètre démarre immédiatement.

### 3. Détection avec YOLO

Pendant la manche, chaque image provenant de la webcam est analysée par YOLOv8.

Pour chaque objet détecté avec une confiance supérieure ou égale à `0.50`, le programme affiche :

* un rectangle autour de l'objet ;
* le nom de la classe détectée ;
* le niveau de confiance.

Par exemple :

```text
bottle 0.87
```

signifie que YOLO estime à 87 % que l'objet détecté est une bouteille.

### 4. Détection de l'objet recherché

Le programme compare les objets détectés avec l'objet demandé.

Lorsque l'objet recherché est détecté :

```text
OBJET TROUVÉ !
```

La manche s'arrête automatiquement et le temps est enregistré.

Exemple :

```text
==============================
OBJET TROUVÉ - ÉQUIPE 1
Objet : BOUTEILLE
Temps : 4.82 secondes
==============================
```

## Déroulement des deux équipes

Le jeu fonctionne avec deux équipes.

### Équipe 1

L'équipe 1 reçoit un objet aléatoire.

Elle appuie sur **Espace** pour commencer et cherche l'objet devant la webcam.

Lorsque l'objet est trouvé, son temps est enregistré.

### Équipe 2

Après la fin de la première manche, appuyer sur **Espace** pour passer à l'équipe 2.

Un nouvel objet est sélectionné.

L'objet de l'équipe 2 est différent de celui de l'équipe 1 lorsque plusieurs objets sont disponibles.

L'équipe 2 effectue ensuite sa manche.

### Résultat final

Après la deuxième manche, appuyer sur **Espace** pour afficher le résultat final.

Le programme compare les deux temps :

```text
==============================
RESULTAT FINAL
==============================

Équipe 1 : 4.82 secondes
Équipe 2 : 6.31 secondes

ÉQUIPE 1 GAGNE !
```

L'équipe ayant réalisé le meilleur temps gagne.

## Commandes

| Touche   | Action                     |
| -------- | -------------------------- |
| `ESPACE` | Démarrer une manche        |
| `ESPACE` | Passer à l'équipe suivante |
| `ESPACE` | Afficher le résultat final |
| `Q`      | Quitter le jeu             |

## Webcam

Le programme utilise actuellement la webcam :

```text
/dev/video2
```

La caméra est configurée pour essayer d'utiliser :

* résolution : `1280 × 720` ;
* fréquence : `30 FPS` ;
* format : `MJPG` ;
* buffer réduit afin de limiter la latence.

Si votre webcam est accessible avec un autre périphérique, modifier cette ligne dans `game.py` :

```python
cap = cv2.VideoCapture("/dev/video2", cv2.CAP_V4L2)
```

Par exemple :

```python
cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
```

## Seuil de confiance

Le programme ignore les détections dont la confiance est inférieure à `0.50`.

Cette valeur est définie ici :

```python
if confidence < 0.50:
    continue
```

Un seuil plus élevé permet de réduire les fausses détections, tandis qu'un seuil plus faible peut permettre de détecter davantage d'objets mais avec un risque accru d'erreurs.

## Modèle YOLO

Le projet utilise :

```text
yolov8n.pt
```

Il s'agit de la version **Nano de YOLOv8**, choisie notamment pour permettre une détection suffisamment rapide en temps réel.

Le modèle est chargé avec :

```python
model = YOLO(MODEL_PATH)
```

## Architecture du jeu

Le fonctionnement général peut être résumé ainsi :

```text
             WEBCAM
                │
                ▼
       Capture vidéo OpenCV
                │
                ▼
          Modèle YOLOv8
                │
                ▼
       Détection des objets
                │
                ▼
     Comparaison avec la cible
                │
        ┌───────┴───────┐
        │               │
     Pas trouvé       Trouvé
        │               │
        ▼               ▼
 Continuer le jeu   Arrêter le chrono
                        │
                        ▼
                  Enregistrer temps
                        │
                        ▼
                 Équipe suivante
                        │
                        ▼
                  Résultat final
```

## Objectif du projet

L'objectif est de mettre en pratique la **détection d'objets en temps réel** dans une application interactive.

Le projet combine :

* vision par ordinateur ;
* détection d'objets ;
* traitement vidéo en temps réel ;
* interaction avec une webcam ;
* mesure du temps ;
* logique de jeu.

Le système permet ainsi de transformer un modèle de détection d'objets en une application ludique et interactive.
