#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
from gpiozero import DistanceSensor
from threading import Thread
from time import sleep
from datetime import datetime

app = Flask(__name__)

# Inicializa el sensor de distancia
sensor = DistanceSensor(echo=27, trigger=17)
distance_cm = 0.0
data_log = []  # Almacena [hora, distancia] como lista de listas


# Hilo que actualiza la distancia periódicamente
def update_distance():
    global distance_cm
    while True:
        distance_cm = sensor.distance * 100  # Convertir a cm
        timestamp = datetime.now().strftime("%H:%M:%S")
        data_log.append([timestamp, distance_cm])
        if len(data_log) > 20:  # Limitar a los últimos 20 datos
            data_log.pop(0)
        sleep(0.5)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/distance')
def get_distance():
    return jsonify({'distance': round(distance_cm, 2)})


@app.route('/distance-data')
def distance_data():
    return jsonify(data_log[-20:])


if __name__ == '__main__':
    thread = Thread(target=update_distance)
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0', port=5000)
