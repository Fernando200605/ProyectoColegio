let miModalInstancia = null;
let campoActivo = null; // 👈 Variable para saber qué select actualizar

function abrirModalCreacionDesdeCampo(fieldId) {
    const select = document.getElementById(fieldId);

    if (!select) {
        console.error('Select no encontrado:', fieldId);
        return;
    }

    const url = select.dataset.crearUrl; // data-crear-url
    const fieldName = select.name;

    if (!url) {
        console.error('El select no tiene data-crear-url');
        return;
    }

    abrirModalCreacion(url, fieldName);
}
function MostrarMensaje(Texto) {
    Swal.fire({
        icon: 'success',
        title: 'Registro creado',
        text: Texto,
        showConfirmButton: false,
        timer: 2000,
        timerProgressBar: true
    })
}

function abrirModalCreacion(url, fieldName) {
    const modalElement = document.getElementById('modalGeneral');
    const contenedor = document.getElementById('contenedorModal');

    campoActivo = fieldName; // 👈 Guardamos el nombre del campo (ej: 'marca')

    fetch(url)
        .then(response => response.text())
        .then(html => {
            contenedor.innerHTML = html;

            if (miModalInstancia) { miModalInstancia.dispose(); }

            miModalInstancia = new bootstrap.Modal(modalElement);
            miModalInstancia.show();

            // Configurar botones de cerrar
            const btnCerrar = contenedor.querySelectorAll('[data-bs-dismiss="modal"]');
            btnCerrar.forEach(boton => {
                boton.onclick = () => miModalInstancia.hide();
            });

            const form = contenedor.querySelector('#formGenericoModal');
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                const formData = new FormData(this);
                limpiarErrores(form);

                fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            miModalInstancia.hide();
                            if (data.message){
                                MostrarMensaje(data.message)
                            }
                            actualizarSelectDinamico(data.id, data.nombre);
                        } else {
                            mostrarErrores(form, data.errors);
                        }
                    })
                    .catch(error => console.error('Error:', error));
            });
        });
}

// Reemplaza tu 'actualizarSelectTipo' por esta función genérica
function actualizarSelectDinamico(id, nombre) {
    if (campoActivo) {
        // Busca el select por el nombre que guardamos al abrir el modal
        const select = document.querySelector(`select[name="${campoActivo}"]`);
        if (select) {
            const nuevaOpcion = new Option(nombre, id, true, true);
            select.add(nuevaOpcion);
            // Disparamos el evento change por si tienes otras dependencias
            select.dispatchEvent(new Event('change'));
        }
    }
}
function mostrarErrores(form, errores) {
    for (let campo in errores) {
        const input = form.querySelector(`[name="${campo}"]`);
        if (input) {
            input.classList.add('is-invalid');
            const errorDiv = document.getElementById(`error_${campo}`);
            if (errorDiv) {
                errorDiv.innerText = errores[campo].join(' ');
            }
        }
    }
}

function limpiarErrores(form) {
    form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    form.querySelectorAll('.invalid-feedback').forEach(el => el.innerText = '');
}