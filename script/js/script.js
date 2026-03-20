    let n_actual = 0;
    let pasosGlobales = { jacobi: [], gauss: [] };

    // Genera las casillas de input dependiendo de la cantidad de routers
    function generarCampos() {
        n_actual = parseInt(document.getElementById('n_routers').value);
        const contenedorEnlaces = document.getElementById('enlaces_dinamicos');
        const contenedorTrafico = document.getElementById('trafico_dinamico');
        
        contenedorEnlaces.innerHTML = '';
        contenedorTrafico.innerHTML = '';

        for (let i = 0; i < n_actual; i++) {
            let rowHTML = `<div class="row mb-2 align-items-center"><div class="col-2 fw-bold">Al Router ${i+1}:</div>`;
            for (let j = 0; j < n_actual; j++) {
                if (i !== j) {
                    rowHTML += `
                    <div class="col">
                        <input type="number" class="form-control enlace-input" data-i="${i}" data-j="${j}" placeholder="Desde R${j+1} (%)" min="0" max="100">
                    </div>`;
                } else {
                    rowHTML += `<div class="col text-center text-muted">--</div>`;
                }
            }
            rowHTML += `</div>`;
            contenedorEnlaces.innerHTML += rowHTML;

            // Vector b
            contenedorTrafico.innerHTML += `
            <div class="col-md-3">
                <input type="number" class="form-control trafico-input" data-i="${i}" placeholder="Router ${i+1} (MB/s)">
            </div>`;
        }
        document.getElementById('matriz_container').classList.remove('d-none');
    }

    // Recopila los datos y los envía a Python
    async function ejecutarSimulacion() {
        const payload = {
            n: n_actual,
            tol: document.getElementById('tolerancia').value,
            capacidad_max: document.getElementById('capacidad').value,
            enlaces: {},
            trafico_externo: []
        };

        // Recolectar matriz A
        document.querySelectorAll('.enlace-input').forEach(input => {
            payload.enlaces[`${input.dataset.i}-${input.dataset.j}`] = input.value || 0;
        });

        // Recolectar vector b
        document.querySelectorAll('.trafico-input').forEach(input => {
            payload.trafico_externo[input.dataset.i] = input.value || 0;
        });

        // Enviar a Flask
        try {
            const response = await fetch('https://simulador-enrutamiento-jacobi-gauss.onrender.com/api/calcular', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            
            if (data.error) {
                alert("Error en el servidor: " + data.error);
                return;
            }

            // En caso de no ser dominante, mostrar mensaje y no intentar renderizar pasos
            console.log(data.mensaje_dominancia);
            console.log(data.reporte_diagnostico);
            if (data.mensaje_dominancia && data.mensaje_dominancia.includes("NO es diagonalmente dominante.")) {
                mostrarResultados(data); // Aún mostramos el diagnóstico
                document.getElementById('contenidoMatematico').innerHTML = "<p class='text-danger'>El sistema no es diagonalmente dominante. No se pueden garantizar resultados correctos con Jacobi o Gauss-Seidel.</p>";
                return;
            }
        
            mostrarResultados(data);
            pasosGlobales.jacobi = data.pasos_jacobi || []; // Guardamos los pasos
            pasosGlobales.gauss = data.pasos_gauss || [];
            renderizarPasos();
        } catch (error) {
            console.error("Error de conexión:", error);
        }
    }

    // Dibuja la tabla con los resultados recibidos
    function mostrarResultados(data) {
        document.getElementById('resultados_container').classList.remove('d-none');
        document.getElementById('mensaje_dominancia').innerText = data.mensaje_dominancia;
        
        const tabla = document.getElementById('tabla_resultados');
        tabla.innerHTML = '';

        data.reporte_diagnostico.resultados_routers.forEach(router => {
            let colorClase = "";
            if(router.estado_enlace.includes("Saturado")) colorClase = "table-danger";
            else if(router.estado_enlace.includes("Alerta")) colorClase = "table-warning";
            else colorClase = "table-success";

            tabla.innerHTML += `
                <tr class="${colorClase}">
                    <td>${router.router}</td>
                    <td><strong>${router.carga_total}</strong></td>
                    <td>${router.estado_enlace}</td>
                </tr>
            `;
        });

        document.getElementById('eficiencia_texto').innerText = 
            `Iteraciones requeridas: Jacobi (${data.reporte_diagnostico.iteraciones_jacobi}) | Gauss-Seidel (${data.reporte_diagnostico.iteraciones_gauss_seidel})`;
    }





// función para escribir las fórmulas
function renderizarPasos() {
    const metodo = document.getElementById('selectorMetodo').value;
    const contenedor = document.getElementById('contenidoMatematico');
    
    // Si aún no se ha ejecutado la simulación, no hacemos nada
    const pasos = metodo === 'jacobi' ? pasosGlobales.jacobi : pasosGlobales.gauss;
    if (!pasos || pasos.length === 0) {
        console.log(pasos)
        console.log(pasosGlobales.jacobi)
        contenedor.innerHTML = "<p class='text-muted'>Por favor, ejecuta el diagnóstico primero.</p>";
        return;
    }
    
    let html = "";
    pasos.forEach(p => {
        // Si es la primera variable del sistema (x1), ponemos un encabezado de iteración
        if (p.variable === "x1") {
            html += `<div class='mt-4 mb-2 p-2 bg-light border-start border-primary border-4'>
                        <strong>Iteración ${p.iteracion}</strong>
                     </div>`;
        }
        
        // Construimos la expresión en LaTeX
        // Usamos la estructura: x_i = (b_i - suma) / A_ii
        html += `<div class='mb-3 border-bottom pb-2'>
            <span class="text-primary fw-bold">${p.variable}<sup>(k+1)</sup>:</span> 
            <span style="font-size: 1.1rem;">
                \\( x_{${p.variable.slice(1)}}^{(k+1)} = \\frac{b_{${p.variable.slice(1)}} - \\sum a_{ij}x_j^{(k)}}{a_{ii}} = \\mathbf{ ${p.valor_nuevo.toFixed(4)} } \\)
            </span>
            <div class='text-muted' style='font-size:0.8rem; margin-left: 25px;'>
                Error absoluto: <code class="text-danger">|${p.valor_nuevo.toFixed(4)} - ${p.valor_viejo.toFixed(4)}| = ${Math.abs(p.valor_nuevo - p.valor_viejo).toFixed(6)}</code>
            </div>
         </div>`;
    });
    
    contenedor.innerHTML = html;

    // IMPORTANTE: Esto "despierta" a MathJax para que dibuje las fórmulas
    if (window.MathJax && window.MathJax.typeset) {
        window.MathJax.typeset();
    }
}