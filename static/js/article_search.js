// Función para aplicar filtros
    function applyFilters() {
        const name = document.getElementById("filterNombre")?.value || "";
        const category = document.getElementById("filterCategorie")?.value || "";
        const available = document.getElementById("filterEstado")?.value || "";

        let query = "?";
        if (name) query += `name=${encodeURIComponent(name)}&`;
        if (category) query += `category=${category}&`;
        if (available) query += `available=${available}&`;

        window.location.href = `/admin/articles${query}`;
    }

    document.addEventListener("DOMContentLoaded", () => {
        // Modal
        loadCategorySelect("productCategory", "Seleccione una categoría");

        // Filtro
        const filterSelect = document.getElementById("filterCategorie");
        if (filterSelect) {
            const selectedFilter = filterSelect.dataset.selected || "";
            loadCategorySelect("filterCategorie", "Todas las categorías", selectedFilter);
        }
});
