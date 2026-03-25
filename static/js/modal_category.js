// --- Función para limpiar el modal ---
function resetCategoryModal(title = "Nueva Categoría") {
    document.getElementById("categoryModalTitle").innerText = title;
    const categoryId = document.getElementById("categoryId");
    const categoryName = document.getElementById("categoryName");
    const messageDiv = document.getElementById("categoryMessage");
    const deleteBtn = document.getElementById("deleteCategoryBtn");

    // Limpiar campos
    categoryId.value = "";
    categoryName.value = "";
    
    // Limpiar clases de error y mensajes
    categoryName.classList.remove("is-invalid");
    if (categoryName.nextElementSibling && categoryName.nextElementSibling.classList.contains("invalid-feedback")) {
        categoryName.nextElementSibling.textContent = "";
    }
    messageDiv.innerHTML = "";
    deleteBtn.classList.add("d-none");
}

// --- Nueva categoría ---
function newCategory() {
    resetCategoryModal("Nueva Categoría");

    const modal = new bootstrap.Modal(
        document.getElementById("categoryViewModal")
    );
    modal.show();
}

// --- Ver categoría para editar ---
async function viewCategory(id) {
    const response = await fetch(`/admin/categories/${id}`);
    const category = await response.json();

    resetCategoryModal("Editar Categoría");

    document.getElementById("categoryId").value = category.id;
    document.getElementById("categoryName").value = category.name;

    const deleteBtn = document.getElementById("deleteCategoryBtn");
    console.log("deleteBtn:", deleteBtn); // <-- aquí
    console.log("category.id:", category.id); // <-- opcional, verificar id

    deleteBtn.classList.remove("d-none");
    deleteBtn.onclick = () => deleteCategory(category.id);

    const modal = new bootstrap.Modal(
        document.getElementById("categoryViewModal")
    );
    modal.show();
}

// --- Guardar categoría (POST/PUT) ---
document.getElementById("categoryForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const id = document.getElementById("categoryId").value;
    const nameInput = document.getElementById("categoryName");
    const name = nameInput.value.trim();
    const messageDiv = document.getElementById("categoryMessage");

    // Limpiar errores previos
    resetCategoryModal(document.getElementById("categoryModalTitle").innerText);

    const url = id ? `/admin/categories/${id}` : `/admin/categories`;
    const method = id ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });

        if (response.ok) {
            messageDiv.innerHTML = '<div class="alert alert-success">Categoría guardada correctamente</div>';
            setTimeout(() => {
                bootstrap.Modal.getInstance(document.getElementById('categoryViewModal')).hide();
                location.reload();
            }, 1500);

        } else {
            const data = await response.json();
            if (data.detail && data.detail.includes("ya existe")) {
                nameInput.classList.add("is-invalid");
                nameInput.nextElementSibling.textContent = data.detail;
            } else {
                messageDiv.innerHTML = '<div class="alert alert-danger">Error al guardar categoría</div>';
            }
        }
    } catch (err) {
        console.error("Error de red o servidor:", err);
        messageDiv.innerHTML = '<div class="alert alert-danger">Error de conexión con el servidor</div>';
    }
});

// --- Limpiar modal al cerrarlo ---
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("categoryViewModal")
        .addEventListener("hidden.bs.modal", () => {
            resetCategoryModal();
        });
});


async function deleteCategory(id) {
    if (!confirm("¿Deseas eliminar esta categoría?")) return;

    const messageDiv = document.getElementById("categoryMessage");

    try {
        const response = await fetch(`/admin/categories/${id}`, {
            method: "DELETE"
        });

        if (response.ok) {
            messageDiv.innerHTML =
                '<div class="alert alert-success">Categoría eliminada correctamente</div>';

            setTimeout(() => {
                bootstrap.Modal
                    .getInstance(document.getElementById("categoryViewModal"))
                    .hide();
                location.reload();
            }, 1500);

        } else {
            messageDiv.innerHTML =
                '<div class="alert alert-danger">No se pudo eliminar la categoría</div>';
        }
    } catch (error) {
        messageDiv.innerHTML =
            '<div class="alert alert-danger">Error de conexión</div>';
    }
}
