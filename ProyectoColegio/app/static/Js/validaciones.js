document.addEventListener('input', function (e) {
	if (e.target.id === "id_descripcion"){
		const error = document.getElementById("error_Descripcion")
		error.innerText = ""
		if (e.target.value.length < 10) {
            error.classList.add("text-danger");
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
})