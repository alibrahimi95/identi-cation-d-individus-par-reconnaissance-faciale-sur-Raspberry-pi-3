# USAGE
# python3 encode_faces.py --dataset dataset --encodings encodings.pickle --detection-method cnn


# importer les paquets nécessaires
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# construire l'analyseur d'arguments et analyser les arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# saisir les chemins vers les images d'entrée dans notre jeu de données (dataset)
print("[Maching Learning] identification...")
imagePaths = list(paths.list_images(args["dataset"]))

# initialiser la liste des encodages et noms connus
knownEncodings = []
knownNames = []

# boucle sur les chemins d'image
for (i, imagePath) in enumerate(imagePaths):
	# extraire le nom de la personne du chemin de l'image
	print("[Maching Learning] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# load the input image and convert it from RGB (OpenCV ordering)
	# charger l'image d'entrée et la convertir à partir de RVB (commande OpenCV)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# détecter les coordonnées (x, y) des boîtes englobantes
	# correspondant à chaque face dans l'image d'entrée
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# calculer l'inclusion faciale pour le visage
	encodings = face_recognition.face_encodings(rgb, boxes)

	# boucle sur les encodages
	for encoding in encodings:
		# ajouter chaque codage + nom à notre ensemble de noms connus et
		# encodages
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump les encodages faciaux + les noms sur le disque
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
