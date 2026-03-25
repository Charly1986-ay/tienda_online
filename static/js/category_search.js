function filterCategories() {

    const category = document.getElementById("categoryFilter")?.value || "";

    const query = category ? `?category=${encodeURIComponent(category)}` : '';

    window.location.href = `/admin/categories${query}`;
    
}

// Resetear filtro
function resetFilter() {
    document.getElementById("categoryFilter").value = ""; // Limpiar input
    window.location.href = "/admin/categories"; // Recargar sin filtros
}

// Filtrado instantáneo en la tabla mientras se escribe
document.getElementById("categoryFilter").addEventListener("keyup", () => {
    const filter = document.getElementById("categoryFilter").value.toLowerCase();
    document.querySelectorAll("#categories-body tr").forEach(row => {
        const category = row.cells[1].textContent.toLowerCase();
        row.style.display = category.includes(filter) ? "" : "none";
    });
});