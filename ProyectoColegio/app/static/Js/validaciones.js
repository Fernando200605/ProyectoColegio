
document.addEventListener('input', function (e) {
    const target = e.target;

    // --- 1. Validar Nombre (Evaluando errores primero) ---
    if (target.name === "nombre") {
        const error = document.getElementById("error_nombre");
        const valor = target.value.trim();
        error.className = "small d-block mt-1"; // Reset de color

        if (valor.length === 0) {
            error.textContent = "El nombre no puede estar vacío";
            error.classList.add("text-danger");
        } else if (valor.length < 3) {
            error.textContent = "Nombre demasiado corto (mínimo 3 letras)";
            error.classList.add("text-danger");
        } else if (/[0-9]/.test(valor)) {
            error.textContent = "El nombre no debe contener números";
            error.classList.add("text-danger");
        } else {
            error.textContent = "Nombre válido";
            error.classList.add("text-success");
        }
    }

    // --- 2. Validar Email ---
    if (target.id === "id_email") {
        const error = document.getElementById("error_email");
        const email = target.value.toLowerCase().trim();
        const dominiosValidos = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com"];
        error.className = "small d-block mt-1";

        if (email.length === 0) {
            error.textContent = "El correo es obligatorio";
            error.classList.add("text-danger");
        } else if (!email.includes("@") || !email.includes(".")) {
            error.textContent = "Formato inválido (ejemplo@correo.com)";
            error.classList.add("text-danger");
        } else {
            const dominioIngresado = email.split("@")[1];
            if (!dominiosValidos.includes(dominioIngresado)) {
                error.textContent = "Solo se permite Gmail, Hotmail u Outlook";
                error.classList.add("text-danger");
            } else {
                error.textContent = "Correo válido";
                error.classList.add("text-success");
            }
        }
    }

    // --- 3. Validar Contraseña ---
    if (target.id === "id_password") {
        const error = document.getElementById("error_password");
        const barra = document.getElementById("barra-fuerza");
        const pass = target.value;
        error.className = "small d-block mt-1";

        // Pruebas lógicas
        const tieneMayuscula = /[A-Z]/.test(pass);
        const tieneNumero = /[0-9]/.test(pass);
        const tieneEspecial = /[!@#$%^&*(),.?":{}|<>]/.test(pass);
        const tieneLongitud = pass.length >= 8;

        // Barra de fuerza (Se actualiza siempre)
        let puntos = (tieneLongitud + tieneMayuscula + tieneNumero + tieneEspecial) * 25;
        if (barra) {
            barra.style.width = puntos + "%";
            if (puntos <= 25) barra.className = "progress-bar bg-danger";
            else if (puntos <= 75) barra.className = "progress-bar bg-warning";
            else barra.className = "progress-bar bg-success";
        }

        // EVALUACIÓN POR PRIORIDAD DE ERROR
        if (pass.length === 0) {
            error.textContent = "La contraseña es obligatoria";
            error.classList.add("text-danger");
        } else if (!tieneLongitud) {
            error.textContent = "Mínimo 8 caracteres";
            error.classList.add("text-danger");
        } else if (!tieneMayuscula) {
            error.textContent = "Debe tener al menos una mayúscula";
            error.classList.add("text-danger");
        } else if (!tieneNumero) {
            error.textContent = "Debe incluir al menos un número";
            error.classList.add("text-danger");
        } else if (!tieneEspecial) {
            error.textContent = "Debe incluir un carácter especial (!@#$...)";
            error.classList.add("text-danger");
        } else {
            error.textContent = "Contraseña segura";
            error.classList.add("text-success");
        }
    }

    // --- 4. Confirmar Contraseña ---
    if (target.id === "id_confirmar_password") {
        const error = document.getElementById("error_confirmar_password");
        const passPrincipal = document.getElementById("id_password").value;
        error.className = "small d-block mt-1";

        if (target.value !== passPrincipal) {
            error.textContent = "Las contraseñas no coinciden";
            error.classList.add("text-danger");
        } else if (target.value === "") {
            error.textContent = "";
        } else {
            error.textContent = "Las contraseñas coinciden";
            error.classList.add("text-success");
        }
    }
});

document.addEventListener('input', function (e) {
	if (e.target.id === "id_descripcion"){
		const error = document.getElementById("error_Descripcion")
		error.innerText = ""
		if (e.target.value.length < 10) {
			error.innerText = "la descripción es demasiado muy corta"
		}
		if (e.target.value.length > 200) {
			error.innerText = "La descripción no puede superar los 200 caracteres"
		}
		if (e.target.value.length == 0) {
			error.innerText = "la descripción no puede estar vacia"
		}

	}

	// TÍTULO

	if (e.target.id === "id_titulo"){
		const error = document.getElementById("error_Titulo")
		error.innerText = ""

		if (/^\d+$/.test(e.target.value)){
			error.innerText = "El título no puede contener solo números"
		}

		if (!/^[a-zA-ZÁÉÍÓÚáéíóúÑñ0-9 ]+$/.test(e.target.value)){
			error.innerText = "El título no puede contener caracteres especiales"
		}
	}


	// FECHA INICIO

	if (e.target.id === "id_fecha_inicio"){
		const error = document.getElementById("error_Fecha inicio")
		error.innerText = ""

		if (e.target.value){
			const fechaInicio = new Date(e.target.value)
			const ahora = new Date()

			if (fechaInicio < ahora){
				error.innerText = "La fecha de inicio no puede ser una fecha pasada"
			}
		}
	}

	// FECHA FIN

	if (e.target.id === "id_fecha_fin"){
		const error = document.getElementById("error_Fecha fin")
		error.innerText = ""

		if (e.target.value){
			const fechaFin = new Date(e.target.value)
			const ahora = new Date()

			if (fechaFin < ahora){
				error.innerText = "La fecha de fin no puede ser una fecha pasada"
			}
		}
	}


	// VALIDACIÓN ENTRE FECHAS

	const fechaInicioInput = document.getElementById("id_fecha_inicio")
	const fechaFinInput = document.getElementById("id_fecha_fin")
	const errorFechaFin = document.getElementById("error_fecha_fin")

	if (fechaInicioInput && fechaFinInput){
		if (fechaInicioInput.value && fechaFinInput.value){
			const inicio = new Date(fechaInicioInput.value)
			const fin = new Date(fechaFinInput.value)

			if (inicio >= fin){
				errorFechaFin.innerText = "La fecha de fin debe ser mayor que la fecha de inicio"
			}
		}
	}
})

document.addEventListener('input', function (e) {

    // 🔹 OBSERVACIONES (mín 10, máx 200)
    if (e.target.id === "id_observaciones") {
        const error = document.getElementById("error_Observaciones");
        error.innerText = "";

        if (e.target.value.length > 200) {
            error.innerText = "Las observaciones no pueden tener mas de 200 caracteres.";
        } else if (e.target.value.length < 10 && e.target.value.length > 0) {
            error.innerText = "Las observaciones deben tener minimo 10 caracteres";
        }
    }
})

document.addEventListener('input', function (e) {
    // 🔹 HORA ENTRADA → estado automático
    if (e.target.id === "id_horaentrada") {
        const estado = document.getElementById("id_estado");

        if (e.target.value) {
            const limite = "07:00";
            estado.value = (e.target.value <= limite) ? "A tiempo" : "Tarde";
        }
    }
});

document.addEventListener('input', function (e) { 
    // 🔹 VALIDACIÓN HORAS (entrada < salida)
    if (e.target.id === "id_horaentrada" || e.target.id === "id_horasalida") {

        const entrada = document.getElementById("id_horaentrada").value;
        const salida = document.getElementById("id_horasalida").value;
        const error = document.getElementById("error_Horasalida");

        error.innerText = "";

        if (entrada && salida) {
            if (entrada >= salida) {
                error.innerText = "La hora de salida debe ser posterior a la de entrada.";
            }
        }

    }
});
