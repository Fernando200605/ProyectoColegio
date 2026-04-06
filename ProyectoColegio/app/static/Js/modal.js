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

	campoActivo = fieldName;

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
							if (data.message) {
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

function abrirPerfil() {
	const modalElement = document.getElementById('modalGeneral');
	const contenedor = document.getElementById('contenedorModal');
	const nombre = document.getElementById('name')
	const img = document.getElementById('img')

	fetch("/ejemplo/usuario/perfil/", {
		headers: { 'X-Requested-With': 'XMLHttpRequest' }
	})
		.then(res => res.json().catch(() => null)) // intenta parsear JSON
		.then(data => {
			if (data && data.redirect) {
				window.location.href = data.redirect; // usuario no logueado
				return;
			}

			// si no es JSON, asumimos HTML (usuario logueado)
			return fetch("/ejemplo/usuario/perfil/")
		})
		.then(response => response.text())
		.then(html => {
			contenedor.innerHTML = html;

			// ✅ Mismo patrón que abrirModalCreacion
			if (miModalInstancia) { miModalInstancia.dispose(); }
			miModalInstancia = new bootstrap.Modal(modalElement);
			miModalInstancia.show();
			const contraseña = document.getElementById("password")
			const error = document.getElementById("error")
			const tieneMin = /[a-z]/.test(contraseña)
			const errorBox = document.getElementById("errorBox");

			contraseña.addEventListener("input", () => {

				const valor = contraseña.value;
				errorBox.innerHTML = "";

				let errores = [];
				if (valor.length < 5) {
					errores.push("Mínimo 5 caracteres");
				}

				if (!/[A-Z]/.test(valor)) {
					errores.push("Debe tener una mayúscula");
				}

				if (!/[0-9]/.test(valor)) {
					errores.push("Debe tener un número");
				}

				if (!/[#$@+\-]/.test(valor)) {
					errores.push("Debe tener un símbolo especial");
				}

				if (valor.length === 0) {
					errorBox.classList.remove("active", "error-box", "pass-box");
					return;
				}

				// ❌ HAY ERRORES
				if (errores.length > 0) {

					errorBox.classList.add("error-box", "active");
					errorBox.classList.remove("pass-box");

					errores.forEach(err => {
						const div = document.createElement("div");
						div.textContent = err;
						div.classList.add("error-item");
						errorBox.appendChild(div);
					});

				}
				else {

					errorBox.classList.add("pass-box", "active");
					errorBox.classList.remove("error-box");

					const div = document.createElement("div");
					div.textContent = "Contraseña segura";
					div.classList.add("error-item");
					errorBox.appendChild(div);
				}

			});

			const btnCerrar = contenedor.querySelectorAll('[data-bs-dismiss="modal"]');
			btnCerrar.forEach(boton => {
				boton.onclick = () => miModalInstancia.hide();
			});

			const form = contenedor.querySelector('#formPerfil');
			if (form) {
				form.addEventListener('submit', function (e) {
					e.preventDefault();
					const formData = new FormData(this);
					const mensaje = document.getElementById('mensajePerfil');

					fetch(this.action, {
						method: 'POST',
						body: formData,
						headers: { 'X-Requested-With': 'XMLHttpRequest' }
					})
						.then(res => res.json())
						.then(data => {
							if (data.success) {
								miModalInstancia.hide();
								if (data.message) { MostrarMensaje(data.message); }
								if (nombre && data.nombre) {
									nombre.innerText = data.nombre
								}
							} else {
								mensaje.innerHTML = `<div class="alert alert-danger p-2">${data.message || 'Error al actualizar.'}</div>`;
							}
						})
						.catch(error => console.error('Error:', error));
				});
			}
		})
		.catch(err => console.error("Error al cargar perfil:", err));
}

function abrirNotificacion() {
	const modalElement = document.getElementById('modalGeneral');
	const contenedor = document.getElementById('contenedorModal');
	fetch("/ejemplo/mis_notificaciones/")
		.then(response => response.text())
		.then(html => {
			console.log(html)
			contenedor.innerHTML = html;
			if (miModalInstancia) { miModalInstancia.dispose(); }
			miModalInstancia = new bootstrap.Modal(modalElement);
			miModalInstancia.show();
		})
}
// ------------------------------
// ELEMENTOS DEL DOM
// ------------------------------
const chatBox = document.getElementById('chatBox');
const input = document.getElementById('inputMensaje');
const boton = document.getElementById('btnEnviar');

const btnChat = document.getElementById("btnChat");
const chatContainer = document.getElementById("chatContainer");
const cerrar = document.getElementById("cerrarChat");

// ------------------------------
// FUNCIONES DE CONTROL DEL CHAT
// ------------------------------

// 🔥 Abrir chat
function abrirChat() {
  chatContainer.classList.add("chat-activo");
  btnChat.classList.add("oculto");
}

// 🔥 Cerrar chat
function cerrarChat() {
  chatContainer.classList.remove("chat-activo");
  btnChat.classList.remove("oculto");
}

// Eventos abrir/cerrar
btnChat.addEventListener("click", abrirChat);
cerrar.addEventListener("click", cerrarChat);

// 🔥 Cerrar al hacer clic fuera
document.addEventListener("click", function (e) {
  const clickDentroChat = chatContainer.contains(e.target);
  const clickBoton = btnChat.contains(e.target);

  if (!clickDentroChat && !clickBoton) {
    cerrarChat();
  }
});

// ------------------------------
// FUNCIONES DEL CHAT
// ------------------------------

// 💬 Agregar mensaje
function agregarMensaje(texto, tipo) {
  const mensaje = document.createElement('div');
  mensaje.classList.add('mensaje', tipo);

  // Etiqueta bonita (Tú / Bot)
  const autor = tipo === 'usuario' ? 'Tú' : 'Bot';

  mensaje.innerHTML = `<strong>${autor}:</strong> ${texto}`;

  chatBox.appendChild(mensaje);

  // Scroll automático
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ⏳ Mostrar "escribiendo..."
function mostrarEscribiendo() {
  const mensaje = document.createElement('div');
  mensaje.classList.add('mensaje', 'bot');
  mensaje.id = "escribiendo";

  mensaje.innerHTML = "Bot está escribiendo...";

  chatBox.appendChild(mensaje);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// ❌ Quitar "escribiendo..."
function quitarEscribiendo() {
  const escribiendo = document.getElementById("escribiendo");
  if (escribiendo) escribiendo.remove();
}

// 📤 Enviar mensaje
function enviarMensaje() {
  const texto = input.value.trim();

  if (texto === '') return;

  // Mostrar mensaje usuario
  agregarMensaje(texto, 'usuario');

  // Limpiar input
  input.value = '';

  // Mostrar "escribiendo..."
  mostrarEscribiendo();

  // Petición al backend
  fetch('/ejemplo/preguntas/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ mensaje: texto }),
  })
    .then((res) => res.json())
    .then((data) => {
      quitarEscribiendo();
      agregarMensaje(data.respuesta, 'bot');
    })
    .catch(() => {
      quitarEscribiendo();
      agregarMensaje('Error al conectar con el servidor', 'bot');
    });
}

// ------------------------------
// EVENTOS
// ------------------------------

// Botón enviar
boton.addEventListener('click', enviarMensaje);

// Enter para enviar
input.addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    enviarMensaje();
  }
});