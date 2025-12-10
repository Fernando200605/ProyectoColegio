document.addEventListener("DOMContentLoaded", function () {
    const username = document.getElementById("username");
    const newPassword = document.getElementById("newpassword");
    const confirmPassword = document.getElementById("confirmpassword");

    const userError = document.getElementById("userError");
    const passwordError = document.getElementById("passwordError");
    const confirmError = document.getElementById("confirmError");

    // Validación usuario: solo letras
    if(username) {
        username.addEventListener("input", function () {
            const regex = /^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$/;
            userError.textContent = regex.test(username.value) ? "" : "Solo se permiten letras.";
        });
    }

    // Validación contraseña fuerte
    if(newPassword){
        newPassword.addEventListener("input", function () {
            const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
            passwordError.textContent = regex.test(newPassword.value) ? "" : "Debe tener 8+ caracteres, mayúscula, minúscula, número y símbolo.";

            confirmError.textContent = (confirmPassword.value && confirmPassword.value !== newPassword.value) 
                ? "Las contraseñas no coinciden." : "";
        });
    }

    // Validación confirmación
    if(confirmPassword){
        confirmPassword.addEventListener("input", function () {
            confirmError.textContent = confirmPassword.value !== newPassword.value ? "Las contraseñas no coinciden." : "";
        });
    }

    // Evitar envío si hay errores
    const resetForm = document.getElementById("resetForm");
    if(resetForm){
        resetForm.addEventListener("submit", function (e) {
            if (userError.textContent || passwordError.textContent || confirmError.textContent) {
                e.preventDefault();
                alert("Por favor corrige los errores antes de continuar.");
            }
        });
    }
});

// --- Mostrar / ocultar contraseña ---
const eyeIcon = document.getElementById('eye');
const passwordInput = document.getElementById('password');
const newpassword = document.getElementById('newpassword');
const confirmPasswordInput = document.getElementById('confirmpassword');

if(eyeIcon){
    eyeIcon.addEventListener('click', () => {
        // login
        if(passwordInput){
            passwordInput.type = passwordInput.type === 'password' ? 'text' : 'password';
        }
        // recuperación
        if(newpassword){
            newpassword.type = newpassword.type === 'password' ? 'text' : 'password';
        }
        if(confirmPasswordInput){
            confirmPasswordInput.type = confirmPasswordInput.type === 'password' ? 'text' : 'password';
        }
        // cambiar icono
        eyeIcon.classList.toggle('fa-eye');
        eyeIcon.classList.toggle('fa-eye-slash');
    });
}

// === Login ===
const form = document.querySelector("form");
const usuarioInput = document.getElementById("usuario");
const usuarioError = document.getElementById("usuario-error");
const passwordError = document.getElementById("password-error");

if(usuarioInput){
    usuarioInput.addEventListener("input", () => {
        let usuario = usuarioInput.value.trim();
        let usuarioRegex = /^[A-Za-z]{3,20}$/;
        if (!usuarioRegex.test(usuario)) {
            usuarioError.textContent = "El usuario debe tener solo letras (3 a 20 caracteres).";
            usuarioInput.classList.add("input-error");
        } else {
            usuarioError.textContent = "";
            usuarioInput.classList.remove("input-error");
        }
    });
}

if(passwordInput){
    passwordInput.addEventListener("input", () => {
        let password = passwordInput.value.trim();
        if (password.length < 6) {
            passwordError.textContent = "La contraseña debe tener mínimo 6 caracteres.";
            passwordInput.classList.add("input-error");
        } else {
            passwordError.textContent = "";
            passwordInput.classList.remove("input-error");
        }
    });
}

if(form){
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        let usuario = usuarioInput.value.trim();
        let password = passwordInput.value.trim();
        let usuarioRegex = /^[A-Za-z]{3,20}$/;

        let valid = true;

        if (!usuarioRegex.test(usuario)) {
            usuarioError.textContent = "El usuario debe tener solo letras (3 a 20 caracteres).";
            valid = false;
        }

        if (password.length < 6) {
            passwordError.textContent = "La contraseña debe tener mínimo 6 caracteres.";
            passwordInput.value = "";
            valid = false;
        }

        if (valid) {
            form.submit();
        }
    });
}
