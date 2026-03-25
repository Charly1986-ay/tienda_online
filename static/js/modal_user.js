const formUser = document.getElementById('formUser');
const modalEl = document.getElementById('modalUser');
// Instancia global del modal
const userModal = bootstrap.Modal.getOrCreateInstance(modalEl);

// Abrir modal para crear usuario
function newUser() {
    document.getElementById("modalUserLabel").innerText = "Nuevo Usuario";
    formUser.reset();
    formUser.dataset.id = '';  // create
    // Contraseña obligatoria en create
    document.getElementById('password').required = true;
    document.getElementById('repeat_password').required = true;
    userModal.show();
}

// Abrir modal para ver/editar usuario
function viewUser(id) {
    fetch(`/admin/users/${id}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("modalUserLabel").innerText = "Ver / Editar Usuario";
            formUser.dataset.id = data.id;  // update
            document.getElementById('userId').value = data.id;
            document.getElementById('username').value = data.username;
            document.getElementById('full_name').value = data.full_name;
            document.getElementById('email').value = data.email;

            // Contraseña opcional en update
            document.getElementById('password').value = '';
            document.getElementById('repeat_password').value = '';
            document.getElementById('password').required = false;
            document.getElementById('repeat_password').required = false;

            userModal.show();
        })
        .catch(error => console.error('Error al obtener los datos del usuario:', error));
}

// Manejo del submit del formulario
formUser.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Limpiar errores previos
    document.querySelectorAll('.text-danger').forEach(el => el.innerText = '');
    const generalError = document.getElementById('error_general');
    generalError.classList.add('d-none');
    generalError.innerText = '';

    const formData = new FormData(formUser);
    const id = formUser.dataset.id;  // create si vacío, update si tiene valor
    const user = Object.fromEntries(formData.entries());

    // Validación manual de contraseña en create
    if (!id) {
        if (!user.password || !user.repeat_password) {
            document.getElementById('error_password').innerText = "La contraseña es obligatoria";
            document.getElementById('error_repeat_password').innerText = "La contraseña es obligatoria";
            return; // detiene el envío
        }
    }

    const url = id ? `/admin/users/${id}` : "/admin/users";

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(user)
        });

        const data = await response.json();

        if (data.success) {
            console.log("Usuario guardado:", data.user);
            formUser.reset();
            userModal.hide();
            // Refresh de tabla después de cerrar modal
            location.reload();
        } else {
            // Mostrar errores en la UI
            showErrors(data.errors);
        }

    } catch (error) {
        console.error("Error al guardar usuario:", error);
        generalError.classList.remove('d-none');
        generalError.innerText = "Ocurrió un error inesperado";
    }
});

// Función para mostrar errores del service en el modal
function showErrors(errorCode) {
    const messages = {
        password_mismatch: "Las contraseñas no coinciden",
        username_taken: "El usuario ya está en uso",
        email_taken: "El correo ya está registrado"
    };

    const message = messages[errorCode] || "Ocurrió un error inesperado";
    console.warn("Error del service:", errorCode);  // log para debugging

    if (errorCode === "password_mismatch") {
        document.getElementById('error_repeat_password').innerText = message;
    } else if (errorCode === "username_taken") {
        document.getElementById('error_username').innerText = message;
    } else if (errorCode === "email_taken") {
        document.getElementById('error_email').innerText = message;
    } else {
        const generalError = document.getElementById('error_general');
        generalError.classList.remove('d-none');
        generalError.innerText = message;
    }
}