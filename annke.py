import cv2
import numpy as np
import requests
import time

url = "http://admin:@192.168.2.88/NetSDK/Video/encode/channel/101/snapshot"

while True:
    try:
        resp = requests.get(url, timeout=2)
        img_array = np.frombuffer(resp.content, np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow('Annke Snapshot Stream', frame)
        else:
            print("No se pudo decodificar la imagen.")
    except Exception as e:
        print("Error:", e)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    time.sleep(0.1)  # Ajusta para la "tasa de cuadros" deseada

cv2.destroyAllWindows()