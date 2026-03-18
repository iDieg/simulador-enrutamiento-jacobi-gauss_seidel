# APLICACIÓN DE TERMINAL.
import numpy as np
import sys

def verificar_dominancia(A):
    # La matriz A es diagonalmente dominante si para cada fila i, el valor absoluto del elemento diagonal A[i][i] es mayor que la suma de los valores absolutos de los otros elementos de la fila.
    n = len(A)
    para_todo_i = True
    
    # Verificamos la condición de dominancia diagonal para cada fila
    for i in range(n):
        # Se suman los valores absolutos de los elementos no diagonales de la fila i
        suma_fila = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) <= suma_fila:
            para_todo_i = False
            break
    return para_todo_i

def jacobi(A, b, tol, max_iter=100):
    # El método de Jacobi es un método iterativo para resolver sistemas de ecuaciones lineales. En cada iteración, se calculan nuevos valores para cada variable utilizando los valores de la iteración anterior.
    n = len(b)
    x = np.zeros(n)       # Valores de la iteración vieja
    x_nuevo = np.zeros(n) # Valores de la iteración nueva
    
    print("\n" + "-"*60)
    print(" DESARROLLO PASO A PASO (MÉTODO DE JACOBI)")
    print("-"*60)
    
    jacobi_resultados_web = []
    
    for k in range(max_iter):
        print(f"\n[ Iteración {k+1} ]")
        
        # Calculamos los nuevos valores
        for i in range(n):
            terminos_str = []
            suma = 0
            for j in range(n):
                if j != i:
                    terminos_str.append(f"{A[i][j]}*({x[j]:.4f})")
                    suma += A[i][j] * x[j]
            
            cadena_suma = " + ".join(terminos_str).replace("+ -", "- ")
            x_nuevo[i] = (b[i] - suma) / A[i][i]
            print(f"  x{i+1} = ({b[i]} - [{cadena_suma}]) / {A[i][i]}  =>  x{i+1} = {x_nuevo[i]:.4f}")
            # Guardamos los resultados para la página web
            jacobi_resultados_web.append({
                "iteracion": k + 1,
                "variable": f"x{i+1}",
                "valor_nuevo": x_nuevo[i],
                "valor_viejo": x[i]
            })
            
        # Mostramos de dónde sale el cálculo del ERROR
        print("\n  [ Cálculo de Errores (|Nuevo - Viejo|) ]")
        errores_individuales = np.zeros(n)
        for i in range(n):
            # Error absoluto de cada variable
            errores_individuales[i] = abs(x_nuevo[i] - x[i])
            print(f"  Error x{i+1}: |{x_nuevo[i]:.4f} - {x[i]:.4f}| = {errores_individuales[i]:.6f}")
            
        # Extraemos el error máximo para evaluar la convergencia
        error_maximo = np.max(errores_individuales)
        print(f"  --> El error máximo de esta iteración es: {error_maximo:.6f}")
        
        # Actualizamos la memoria para la siguiente vuelta
        x = np.copy(x_nuevo)
        
        # Criterio de parada
        if error_maximo < tol:
            print(f"\n✅ Convergencia alcanzada exitosamente (Error Máximo {error_maximo:.6f} < {tol})")
            return x, k + 1, jacobi_resultados_web
            
    return x, max_iter, jacobi_resultados_web

def gauss_seidel(A, b, tol, max_iter=100):
    # El método de Gauss-Seidel es similar a Jacobi, pero en lugar de esperar a que se calculen todos los nuevos valores antes de actualizar, actualiza cada variable inmediatamente después de calcularla, lo que puede acelerar la convergencia.
    n = len(b)
    x = np.zeros(n)
    
    gauss_seidel_resultados_web = []
    
    print("\n" + "="*60)
    print(" DESARROLLO PASO A PASO (MÉTODO DE GAUSS-SEIDEL)")
    print("="*60)
    
    for k in range(max_iter):
        print(f"\n[ Iteración {k+1} ]")
        
        # Guardamos los valores viejos para el cálculo de errores
        x_viejo = np.copy(x) 
        
        # Calculamos los nuevos valores
        for i in range(n):
            terminos_str = []
            suma = 0
            
            for j in range(n):
                if j != i:
                    # En Gauss-Seidel, usamos el valor más actualizado de x[j] si j < i, y el valor viejo si j > i
                    terminos_str.append(f"{A[i][j]}*({x[j]:.4f})")
                    suma += A[i][j] * x[j]
            
            cadena_suma = " + ".join(terminos_str).replace("+ -", "- ")
            
            # Actualización inmediata de la variable x[i]
            x[i] = (b[i] - suma) / A[i][i]
            
            print(f"  x{i+1} = ({b[i]} - [{cadena_suma}]) / {A[i][i]}  =>  x{i+1} = {x[i]:.4f}")
            # Guardamos los resultados para la página web
            gauss_seidel_resultados_web.append({
                "iteracion": k + 1,
                "variable": f"x{i+1}",
                "valor_nuevo": x[i],
                "valor_viejo": x_viejo[i]
            })
            
        # Mostramos el cálculo del ERROR
        print("\n  [ Cálculo de Errores (|Nuevo - Viejo|) ]")
        errores_individuales = np.zeros(n)
        for i in range(n):
            errores_individuales[i] = abs(x[i] - x_viejo[i])
            print(f"  Error x{i+1}: |{x[i]:.4f} - {x_viejo[i]:.4f}| = {errores_individuales[i]:.6f}")
            
        # Extraemos el error máximo
        error_maximo = np.max(errores_individuales)
        print(f"  --> El error máximo de esta iteración es: {error_maximo:.6f}")
        
        # Criterio de parada
        if error_maximo < tol:
            print(f"\n✅ Convergencia alcanzada con Gauss-Seidel (Error Máximo {error_maximo:.6f} < {tol})")
            return x, k + 1, gauss_seidel_resultados_web
            
    return x, max_iter, gauss_seidel_resultados_web

# API DE RETORNO DE RESULTADOS PARA PÁGINA WEB
# Esta función puede ser utilizada para enviar los resultados a una interfaz web, proporcionando un reporte detallado del diagnóstico de la red basado en los cálculos realizados con los métodos de Jacobi y Gauss-Seidel.
def resultados_web(matriz_A, vector_b, tol, capacidad_max):
    es_dominante = verificar_dominancia(matriz_A)
    if es_dominante:
        mensaje_dominancia = "La matriz es diagonalmente dominante."
    else:
        mensaje_dominancia = "La matriz NO es diagonalmente dominante. (por favor verifique los porcentajes ingresados, si el porcentaje de tráfico es muy alto entre routers, podría no cumplirse la condición de dominancia diagonal, lo que afectaría la convergencia del método de Jacobi)."
        
        
    # Calculo de resultados
    resultado_jacobi, iteraciones_jacobi, pasos_jacobi = jacobi(matriz_A, vector_b, tol)
    resultado_gauss_seidel, iteraciones_gauss_seidel, pasos_gauss_seidel = gauss_seidel(matriz_A, vector_b, tol)
    
    # Reporte de diagnostico completo de cada router basado en el resultado de Jacobi y gauss-seidel, para mostrar en la página web
    reporte_diagnostico = {
        "iteraciones_jacobi": iteraciones_jacobi,
        "iteraciones_gauss_seidel": iteraciones_gauss_seidel,
        "resultados_routers": [],
        "paso_a_paso_jacobi": pasos_jacobi,
        "paso_a_paso_gauss": pasos_gauss_seidel
    }
    
    # Resultados routers o servidores
    for i in range(len(vector_b)):
        trafico = round(resultado_jacobi[i], 2)
        if trafico > capacidad_max:
            estado = "❌ Saturado (Cuello de botella)"
        elif trafico >= (capacidad_max * 0.8):
            estado = "⚠️ Alerta (Carga > 80%) Posible saturación"
        else:
            estado = "✅ Óptimo, sin riesgo de saturación"
        
        reporte_diagnostico["resultados_routers"].append({
            "router": f"Router {i+1}",
            "carga_total": trafico, # (MB/s)
            "estado_enlace": estado
        })
    
    return {
        "matriz_A": matriz_A.tolist(),
        "vector_b": vector_b.tolist(),
        "resultado_jacobi": resultado_jacobi.tolist(),
        "resultado_gauss_seidel": resultado_gauss_seidel.tolist(),
        "mensaje_dominancia": mensaje_dominancia,
        "reporte_diagnostico": reporte_diagnostico,
    }

# INTERFAZ DEL SISTEMA
if __name__ == "__main__":
    print("="*60)
    print(" SISTEMA DE ANÁLISIS DE TRÁFICO Y ENRUTAMIENTO (JACOBI)")
    print("="*60)

    tol = float(input("\nIngrese la tolerancia para la convergencia (ej. 0.001): "))

    while tol <= 0 or tol >= 1:
        print(" [ERROR] La tolerancia debe ser un número positivo o menor que 1. Por favor, ingrese un valor válido.")
        # Solicita nuevamente la tolerancia hasta que se ingrese un valor válido
        tol = float(input("Ingrese la tolerancia para la convergencia (ej. 0.001): "))

    n = int(input("\nIngrese la cantidad de routers en la red: "))
    while n <= 0:
        print(" [ERROR] La cantidad de routers debe ser un número entero positivo. Por favor, ingrese un valor válido.")
        n = int(input("Ingrese la cantidad de routers en la red: "))

    A = np.zeros((n, n))
    b = np.zeros(n)

    print("\n--- CONFIGURACIÓN DE ENRUTAMIENTO INTERNO ---")

    # Ingresando valores de la matriz A
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i][j] = 1.0
            else:
                porcentaje = float(input(f"Ingrese el porcentaje de tráfico que el Router {i+1} recibe del Router {j+1} (0-100%): "))
                
                # Validación del porcentaje ingresado
                while porcentaje < 0 or porcentaje > 100:
                    print(" [ERROR] El porcentaje debe estar entre 0 y 100. Por favor, ingrese un valor válido.")
                    porcentaje = float(input(f"Ingrese el porcentaje de tráfico que el Router {i+1} recibe del Router {j+1} (0-100%): "))
                
                # Asignamos el valor negativo del porcentaje a la matriz A para representar la relación de tráfico entre routers
                A[i][j] = -(abs(porcentaje) / 100.0)

    print("\nVerificando matriz para el método de Jacobi...")
    if verificar_dominancia(A):
        print(" [OK] La matriz es diagonalmente dominante.")
    else:
        print(" [ALERTA] La matriz NO es diagonalmente dominante. (por favor verifique los porcentajes ingresados, si el porcentaje de tráfico es muy alto entre routers, podría no cumplirse la condición de dominancia diagonal, lo que afectaría la convergencia del método de Jacobi).")
        sys.exit()

    print("\n--- TRÁFICO EXTERNO (INTERNET) ---")
    for i in range(n):
        b[i] = float(input(f"Tráfico entrante al Router {i+1} (MB/s): "))

    capacidad_max = float(input("\nIngrese la capacidad máxima soportada por los equipos (MB/s): "))
    
    # Validación de capacidad máxima
    while capacidad_max <= 0:
        print(" [ERROR] La capacidad máxima debe ser un número positivo. Por favor, ingrese un valor válido.")
        capacidad_max = float(input("Ingrese la capacidad máxima soportada por los equipos (MB/s): "))

    print("\n" + "-"*60)
    print(" SISTEMA DE ECUACIONES LINEALES GENERADO")
    print("-" * 60)
    for i in range(n):
        terminos = []
        for j in range(n):
            terminos.append(f"{A[i][j]}*x{j+1}")
        ecuacion = " + ".join(terminos).replace("+ -", "- ")
        print(f" {ecuacion} = {b[i]}")

    # Ejecutamos las funciones matemáticas (retornan: resultado, iteraciones y pasos)
    resultado_j, iter_j, pasos_j = jacobi(A, b, tol)
    resultado_gs, iter_gs, pasos_gs = gauss_seidel(A, b, tol)

    # Tabla de resultados y diagnóstico
    print("\n" + "="*60)
    print(" REPORTE FINAL DE DIAGNÓSTICO DE RED")
    print("="*60)
    print(f" Eficiencia Algorítmica -> Jacobi: {iter_j} iteraciones | Gauss-Seidel: {iter_gs} iteraciones\n")

    # Se verifica cual metodo fue más eficiente
    if iter_j < iter_gs:
        print("Método más eficiente -> Jacobi")
    else:
        print("Método más eficiente -> Gauss-seidel")
    
    print(f" {'EQUIPO (NODO)':<15} | {'CARGA TOTAL (MB/s)':<20} | {'ESTADO DEL ENLACE'}")
    print("-" * 60)

    # Verificador de estado de cada router basado en el tráfico calculado
    for i in range(n):
        trafico = round(resultado_j[i], 2)
        if trafico > capacidad_max:
            estado = "❌ SATURADO (Cuello de botella)"
        elif trafico >= (capacidad_max * 0.8):
            estado = "⚠️ ALERTA (Carga > 80%) Posible saturación"
        else:
            estado = "✅ Óptimo, sin riesgo de saturación"
        print(f" Router {i+1:<8} | {trafico:<20} | {estado}")
    print("="*60 + "\n")