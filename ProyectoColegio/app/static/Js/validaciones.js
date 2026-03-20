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