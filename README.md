# Simulador de Análisis de Tráfico y Enrutamiento

**Versión:** 2.0
**Autores:** Diego Romero, Tatiana Chavez, Alejandra González, Ricardo Herrera  

---
## Actualización

* Interfaz gráfica interactiva, interfaz desarrollada en HTML/CSS/JS que permite al usuario configurar topologías de red dinámicamente mediante formularios visuales.
* El desarrollo matemático paso a paso (tanto de Jacobi como de Gauss-Seidel) ahora se empaqueta y se renderiza directamente en el navegador del usuario como una consola virtual.

## Descripción del Proyecto
Este programa, WebApp es un simulador computacional diseñado para predecir y analizar el tráfico de datos entre routers en una topología de red. Para resolver la distribución de las cargas, el simulador modela la red como un sistema de ecuaciones lineales y lo resuelve mediante el **Método Numérico de Jacobi**. 

Adicionalmente, el software integra el método de **Gauss-Seidel** para fines de validación matemática y análisis comparativo de la eficiencia algorítmica. El simulador solicita al usuario la topología (matriz de distribución), el tráfico externo (Internet) y la capacidad máxima, devolviendo un diagnóstico preciso del estado de la red e imprimiendo el desarrollo paso a paso para fines académicos.

---

## Reglas de Diagnóstico
Tras calcular la carga total que procesará cada nodo, el simulador evalúa los resultados contra la capacidad máxima predefinida y emite los siguientes estados:

* **❌ Saturado (Cuello de botella):** El tráfico excede la capacidad máxima del router. Riesgo inminente de caída.
* **⚠️ Alerta:** El tráfico se encuentra entre el 80% y el 100% de la capacidad máxima.
* **✅ Óptimo:** El tráfico es menor al 80% de la capacidad. El equipo opera sin riesgo de saturación.

> **Nota de Seguridad:** El programa verifica matemáticamente la topología ingresada. Si la matriz generada no es estrictamente diagonalmente dominante, el algoritmo alertará al usuario y detendrá la ejecución de forma segura para evitar cálculos divergentes o resultados erróneos.

---

## Recomendaciones de Uso
1. **Conservación de la Dominancia:** Asegúrese de ingresar porcentajes de tráfico interno que sumen menos del 100% (representado por 1.0 en la diagonal) para cada router.
2. **Coherencia de Cargas:** Verifique que el tráfico entrante desde Internet sea proporcional y coherente con la capacidad máxima de los equipos para obtener diagnósticos apegados a la realidad física de una red.

---

## Uso de la API (Integración Web)
El simulador cuenta con un backend en Flask que permite su consumo a través de peticiones HTTP. A continuación, se muestra un ejemplo de cómo consumir la API desde un script externo utilizando Python y la librería `requests`.

### Requisitos previos:
Asegúrese de tener el servidor local en ejecución (`python app.py`) en el puerto 5000 y la librería instalada (`pip install requests`).

### Script de Ejemplo (Python):
```python
import requests
import json

# Se define la URL de nuestra API local
URL_API = "http://localhost:5000/api/simular"

# Preparamos el escenario de red con un ejemplo de 3 routers
payload = {
    "matriz_A": [
        [1.0, -0.2, 0.0],
        [-0.3, 1.0, -0.4],
        [0.0, -0.5, 1.0]
    ],
    "vector_b": [1000, 10, 10],   # Tráfico externo entrante (MB/s)
    "tol": 0.001,                 # Tolerancia de error exigida
    "capacidad_max": 400          # Límite de hardware por nodo
}

# Se realiza petición POST al servidor
respuesta = requests.post(URL_API, json=payload)

# Respuesta del servidor
if respuesta.status_code == 200:
    datos = respuesta.json()
    print("✅ Simulación exitosa.\n")
    print(f"Iteraciones Jacobi: {datos['iteraciones_jacobi']}")
    print(f"Iteraciones Gauss-Seidel: {datos['iteraciones_gauss_seidel']}\n")
    
    print("--- REPORTE DE NODOS ---")
    for router in datos['reporte_diagnostico']['resultados_routers']:
        print(f"{router['router']} | Carga: {router['carga_total']} MB/s | Estado: {router['estado_enlace']}")
else:
    print(f"❌ Error en la conexión. Código: {respuesta.status_code}")