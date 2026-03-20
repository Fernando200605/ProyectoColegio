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