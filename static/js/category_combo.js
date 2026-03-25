async function loadCategorySelect(selectId, defaultText = "Seleccione una categoría", selectedId = null) {
    const select = document.getElementById(selectId);
    if (!select) return;

    select.innerHTML = `<option value="">${defaultText}</option>`;

    try {
        const response = await fetch("/admin/categories/combo");
        const categories = await response.json();

        categories.forEach(cat => {
            const option = document.createElement("option");
            option.value = cat.id;
            option.textContent = cat.name;
            if (selectedId && String(cat.id) === String(selectedId)) option.selected = true;
            select.appendChild(option);
        });
    } catch (err) {
        console.error(`Error cargando categorías para select #${selectId}:`, err);
    }
}