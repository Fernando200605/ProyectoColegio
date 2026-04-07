document.addEventListener('input', function (e) {
	if (e.target.id === "id_descripcion"){
		const error = document.getElementById("error_Descripcion")
		error.innerText = ""
		if (e.target.value.length < 3) {
			error.innerText = "Es muy corta"
		}
	}
})

//validacion de stocks 
document.addEventListener("input", function (e) {
	if (e.target.id === "id_stockActual"){
		const stockactual = document.getElementById("id_stockActual").value;
		const error = document.getElementById("error_StockActual")
		const nodecimal = /^[0-9]*$/.test(stockactual)
		error.innerText = "";
	if (!nodecimal){
		error.innerText = "El stock no puede ser decimal"
	}
	if (stockactual < 0){
		error.innerText = "El stock no puede ser negativo ";
	}
	if (isNaN(stockactual) && this.value == ""){
		error.innerText = "El stock debe tener valor numerico"
	}
	}
})
document.addEventListener("input",function (e) {
	if (e.target.id === "id_stockMinimo"){
		const stockminimo = document.getElementById("id_stockMinimo").value;
		const error =document.getElementById("error_StockMinimo");
		const nodecimal = /^[0-9]*$/.test(stockminimo)
		error.innerText = "";
	if (!nodecimal){
		error.innerText = "El stock no puede ser decimal"
	}
	if (stockminimo < 0){
		error.innerText = "El stock no puede ser negativo "
	}
	if (isNaN(stockminimo) && this.value !== ""){
		error.innerText = "El stock no puede ser decimal"
	}
	}
})
document.addEventListener("input",function (e){
	if (e.target.id == "id_ubicacion"){
		const ubicacion = document.getElementById("id_ubicacion").value;
		const error = document.getElementById("error_Ubicacion");
		const patron = /^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑüÜ\s\-.#]*$/.test(ubicacion);
		error.innerHTML = "";
	if (e.target.value.length < 4){
		error.innerHTML = "La Direccion Es Demasiado corta"
	}
	if (!patron){
		error.innerHTML ="No se aceptan caracteres especiales"
	}
	}
})