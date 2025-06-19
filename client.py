import requests
import time
from gpiozero import DistanceSensor

sensor = DistanceSensor(echo=27, trigger=17)

EC2_URL = 'http://52.53.128.170:5000/post_data'

while True:
    distancia_cm = round(sensor.distance * 100, 2)
    try:
        requests.post(EC2_URL, json={"distancia": distancia_cm})
        print(f"Enviado: {distancia_cm} cm")
    except Exception as e:
        print(f"Error al enviar: {e}")
    time.sleep(0.5)
