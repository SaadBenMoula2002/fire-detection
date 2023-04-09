import cv2
import vonage

# Identifiants Vonage
client = vonage.Client(key="944bd750", secret="0DituTcNXPVvRtLd")
sms = vonage.Sms(client)

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)

# Initialisation des paramètres de détection d'incendie
min_area = 100  # aire minimale de la zone de feu
threshold = 30  # seuil de détection de la flamme
fire_detected = False

while True:
    # Capture d'une image
    ret, frame = cap.read()
    
    # Conversion de l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Filtrage de l'image pour supprimer le bruit
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    # Détection des contours dans l'image
    edges = cv2.Canny(gray, threshold, threshold * 2)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Vérification de la présence d'un feu dans l'image
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            fire_detected = True
            break
        else:
            fire_detected = False
    
    # Affichage de l'image et de la détection de feu
    cv2.imshow('frame', frame)
    if fire_detected:
        print("Fire detected!")
        responseData = sms.send_message(
    {
        "from": "Vonage APIs",
        "to": 212660016663,
        "text": " Flame detected !",
    }
)
        fire_detected = False
    
    # Sortie de la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libération de la capture vidéo et fermeture de la fenêtre
cap.release()
cv2.destroyAllWindows()