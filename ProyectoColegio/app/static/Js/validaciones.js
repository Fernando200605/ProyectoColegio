
document.addEventListener('input', function (e) {
	if (e.target.id === "id_descripcion"){
		const error = document.getElementById("error_Descripcion")
		error.innerText = ""
		if (e.target.value.length < 3) {
			error.innerText = "Es muy corta"
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