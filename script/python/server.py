import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
from analizador_enrutamiento_jacobi import resultados_web

# Funcion para configurar la ruta base del proyecto, asegurando que Flask pueda servir los archivos estáticos correctamente
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(
    __name__,
    static_folder=BASE_DIR,
    static_url_path='/static'
)

CORS(app)  # Permitir solicitudes desde otros dominios

@app.route('/')
def index():
    # Se busca el archivo index.html en la raíz del proyecto
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/api/calcular', methods=['POST'])
def calcular():
    try:
        datos = request.json
        n = int(datos['n'])
        tol = float(datos['tol'])
        cap_max = float(datos['capacidad_max'])
        
        # 1. Reconstruimos la Matriz A (Topología)
        A = np.zeros((n, n))
        for i in range(n):
            A[i][i] = 1.0 # La diagonal siempre es 1.0
            for j in range(n):
                if i != j:
                    # Obtenemos el porcentaje enviado desde el HTML
                    pct = float(datos['enlaces'].get(f"{i}-{j}", 0))
                    A[i][j] = -(abs(pct) / 100.0)
                    
        # 2. Reconstruimos el Vector b (Tráfico de Internet)
        b = np.array([float(x) for x in datos['trafico_externo']])
        
        # 3. Ejecutamos tu función matemática
        resultados = resultados_web(A, b, tol, cap_max)
        
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    print("Iniciando servidor del Simulador de Enrutamiento...")
    app.run(debug=True, port=5000)
