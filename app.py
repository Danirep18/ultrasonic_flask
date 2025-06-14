from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)

# Almacenar valores de distancia
datos_distancia = []

@app.route('/')
def index():
    return render_template('index.html', datos=datos_distancia)

@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()
    if data and 'distancia' in data:
        entrada = {
            'distancia': data['distancia'],
            'hora': datetime.now().strftime('%H:%M:%S')
        }
        datos_distancia.append(entrada)
        # Limitar a las últimas 20 entradas
        datos_distancia[:] = datos_distancia[-20:]
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "msg": "Falta campo 'distancia'"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
