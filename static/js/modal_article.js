// Nuevo Articulo
function newArticle() {
    //loadCategories();
    document.getElementById("articleModalTitle").innerText = "Nuevo Artículo";
    document.getElementById("productId").value = "";
    document.getElementById("productName").value = "";
    document.getElementById("productPrice").value = "";
    document.getElementById("productQty").value = "";
    document.getElementById("productCategory").selectedIndex = 0;
    document.getElementById("productState").selectedIndex = 0;
    document.getElementById("productDesc").value = "";
    const img = document.getElementById("imgPreview");
    img.src = "";
    img.classList.add("d-none");
}


document.getElementById('productImg').addEventListener('change', function() {
    const preview = document.getElementById('imgPreview');
    preview.innerHTML = ''; // limpiar previo

    const file = this.files[0];
    if (!file) return;

    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    img.style.maxWidth = '100%';
    img.style.height = 'auto';
    img.classList.add('img-thumbnail');

    preview.appendChild(img);
});



document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!validateProductForm()) return;

    hideFormAlert();

    const id = document.getElementById('productId').value;

    const formData = new FormData(e.target);

    const url = id ? `/admin/articles/${id}` : '/admin/articles';
    const method = id ? 'PUT' : 'POST';

    const response = await fetch(url, {
        method,
        body: formData
    });

    if (response.ok) {
        showGlobalAlert("✅ Artículo guardado correctamente");

        const modal = bootstrap.Modal.getInstance(
            document.getElementById("productModal")
        );
        modal.hide();

        setTimeout(() => {
            location.reload();
        }, 1500);

    } else {
        const error = await response.json();

        if (response.status === 409) {
            showFormAlert("⚠️ " + error.detail);
        } else {
            showGlobalAlert("❌ Error al guardar el artículo", "danger");
        }
    }
});


function viewArticle(id) {
    fetch(`/admin/articles/${id}`)
        .then(response => response.json())
        .then(data => {
            // Debug opcional (puedes quitarlo luego)
            console.log(data);

            document.getElementById('productId').value = data.id;
            document.getElementById('productName').value = data.name;
            document.getElementById('productCategory').value = data.category_id;
            document.getElementById('productPrice').value = data.price;
            document.getElementById('productQty').value = data.stock;
            document.getElementById('productDesc').value = data.description;

            const imgPreview = document.getElementById('imgPreview');
            imgPreview.innerHTML = '';

            const img = document.createElement('img');

            // 🔒 Manejo seguro de imagen
            const imageName = data.image_name?.trim() || 'default.png';
            img.src = `/static/img/${imageName}`;

            img.style.maxWidth = '100%';
            img.style.height = 'auto';
            img.classList.add('img-thumbnail');

            // Debug si no carga
            img.onerror = () => {
                console.error('No se pudo cargar la imagen:', img.src);
            };

            imgPreview.appendChild(img);

            const modal = new bootstrap.Modal(
                document.getElementById('productModal')
            );
            modal.show();
        })
    .catch(error => {
        console.error('Error al obtener los datos del artículo:', error);
    });
}

function showFormAlert(message) {
    const alert = document.getElementById("formAlert");
    alert.innerHTML = message;
    alert.classList.remove("d-none");
}

function hideFormAlert() {
    const alert = document.getElementById("formAlert");
    alert.classList.add("d-none");
    alert.innerHTML = "";
}

function showGlobalAlert(message, type = "success") {
    const alert = document.getElementById("globalAlert");
    alert.className = `alert alert-${type}`;
    alert.innerHTML = message;
    alert.classList.remove("d-none");

    // auto-ocultar
    setTimeout(() => {
        alert.classList.add("d-none");
    }, 4000);
}

const MAX_IMAGE_SIZE = 10 * 1024 * 1024; // 10 MB

function validateProductForm() {
    hideFormAlert();

    const name = productName.value.trim();
    const price = productPrice.value;
    const qty = productQty.value;
    const category = productCategory.value;
    const desc = productDesc.value.trim();
    const img = productImg;

    if (name.length < 3)
        return showFormAlert("⚠️ El nombre debe tener al menos 3 caracteres.");

    if (price === "" || Number(price) < 0)
        return showFormAlert("⚠️ El precio debe ser mayor o igual a 0.");

    if (!Number.isInteger(Number(qty)) || qty <= 0)
        return showFormAlert("⚠️ La cantidad debe ser mayor a 0.");

    if (!category)
        return showFormAlert("⚠️ Debe seleccionar una categoría.");

    if (desc.length < 10)
        return showFormAlert("⚠️ La descripción debe tener al menos 10 caracteres.");

    if (img.files.length > 0) {
        const file = img.files[0];

        if (!file.type.startsWith("image/")) {
            return showFormAlert("⚠️ El archivo debe ser una imagen.");
        }

        if (file.size > MAX_IMAGE_SIZE) {
            return showFormAlert("⚠️ La imagen no debe superar los 10 MB.");
        }
    }
    return true;
}