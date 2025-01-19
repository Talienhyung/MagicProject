import cv2
import time
import requests
import numpy as np
from magic_card_identifier import *

# URL de la caméra (remplacez par votre URL)
camera_url = 'http://192.168.1.189:8080/video'

# Paramètres
capture_interval = 2  # Intervalle en secondes
output_folder = "./captured_images/"  # Dossier de sauvegarde
last_capture_time = time.time()
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Créer le dossier de sauvegarde s'il n'existe pas
import os
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

while True:
    try:
        # Obtenir une seule image depuis le flux vidéo
        response = requests.get(camera_url, stream=True, timeout=5)
        bytes_data = b''

        for chunk in response.iter_content(chunk_size=4096):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')  # Début d'une image JPEG
            b = bytes_data.find(b'\xff\xd9')  # Fin d'une image JPEG

            if a != -1 and b != -1:
                jpg = bytes_data[a:b + 2]
                bytes_data = bytes_data[b + 2:]

                # Convertir en tableau numpy
                img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                # Vérifier le temps écoulé pour capturer une image
                if time.time() - last_capture_time >= capture_interval:
                    # Sauvegarder l'image
                    timestamp = int(time.time())
                    filename = f"{output_folder}image_{timestamp}.jpeg"
                    for f in os.listdir(output_folder):
                        os.remove(os.path.join(output_folder, f))
                    cv2.imwrite(filename, img)
                    print(f"Image sauvegardée : {filename}")
                    search(filename)

                    last_capture_time = time.time()

                # Afficher l'image capturée
                cv2.imshow('Camera', img)

                # Quitter si 'q' est pressé
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion au flux : {e}")
        time.sleep(2)  # Réessayer après un délai
    except Exception as e:
        print(f"Erreur inattendue : {e}")

cv2.destroyAllWindows()
