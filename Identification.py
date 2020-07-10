# USAGE
# python3 Identification.py --cascade haarcascade_frontalface_default.xml --encodings encodings.pickle

# importer les packages nécessaires 
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import os
from ml import*
try:
    import dill as pickle
except ImportError:
    import pickle
#from pickle import *
import time
import cv2

# construire l'analyseur d'arguments et analyser les arguments 
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
args = vars(ap.parse_args())

# Charger les visages connus avec Haarcascade d'OpenCV pour la détection de visages

print("Debut Biometrie pour la videosurveillance ")
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])
#face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


# initialiser le flux vidéo et laisser le capteur de la caméra se réchauffer
print("[INFO] starting video ...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
#cap = cv2.VideoCapture(0)

# démarrer le compteur FPS
# FPS sont couramment utilisés pour désigner le nombre d'images par seconde (sigle français : IPS). 
fps = FPS().start()

# boucle sur les images du flux de fichiers vidéo
while True:
	# récupérez l'image du flux vidéo fileté et redimensionnez-la
	# 500px (pour accélérer le traitement) notre cas on a utilisé 1024
	frame = vs.read()
	frame = imutils.resize(frame, width=1024)

	# convertir le cadre d'entrée de (1) BGR en niveaux de gris (pour la détection des visages) et (2) de BGR en RGB (pour la reconnaissance des visages)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# détecter les visages dans le cadre en niveaux de gris
	rects = detector.detectMultiScale(gray, scaleFactor=1.1,
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)

	# OpenCV renvoie les coordonnées du cadre de sélection dans l'ordre (x, y, w, h)
	# mais nous avons besoin dans l’ordre (en haut, à droite, en bas, à gauche), de sorte que nous
	# besoin de faire un peu de réorganisation
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	# calculez les imbrications faciales pour chaque boîte englobante
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

	# faire une boucle sur les plis du visage
	for encoding in encodings:
		# essayer de faire correspondre chaque visage dans l'image d'entrée à nos encodages connus
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
                
                
		name = "** Acces Autorise **"		

                
		# vérifier si nous avons trouvé une correspondance
		if True in matches:
			# trouver les index de tous les visages correspondants puis initialiser un
			# dictionnaire pour compter le nombre total de fois chaque visage
			# a été jumelé
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}

			# boucle sur les index correspondants et maintenir un compte pour
			# chaque visage reconnu
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1

			# déterminer la face reconnue avec le plus grand nombre
			# des votes (note: en cas de cravate improbable Python
			# sélectionnera la première entrée dans le dictionnaire)
			name = max(counts, key=counts.get)
			table(name)

		# mettre à jour la liste des noms
		names.append(name)

	# boucle sur les visages reconnus
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 0, 255), 5)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			1.00, (0, 0, 255), 3)
		roi_gray = gray[right:right+left, top:top+bottom]
		roi_color = frame[right:right+left, top:top+bottom]
		eyes = detector.detectMultiScale(roi_gray)
		for (ex,ey,ew,eh) in eyes:
			cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)
		

	# afficher l'image sur notre écran
	cv2.imshow("Biometrie pour la videosurveillance", frame)
	key = cv2.waitKey(1) & 0xFF
	
	# si la touche `q` a été enfoncée, sortir de la boucle
	if key == ord("q") or key == ord("+") or key == ord("Q"):
		break

	# mettre à jour le compteur FPS
	fps.update()

# arrêter le chronomètre et afficher les informations FPS
fps.stop()
print("FIN DE PROGRAMME")
print("LA VIDEO EST CLOSED")
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# faire de nettoyage
cv2.destroyAllWindows()
vs.stop()
