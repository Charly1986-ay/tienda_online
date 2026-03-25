function applyFilters() {
    const field = document.getElementById('filterField').value;
    const value = document.getElementById('filterValue').value;
    const estado = document.getElementById('filterEstadoUs').value;
    const role = document.querySelector('input[name="filterRole"]:checked')?.value || '';

    const params = new URLSearchParams();

    if (field && value) {
        params.append(field, value);  // envia directamente username/fullname/email
    }

    if (estado) params.append('disabled', estado);
    if (role) params.append('role', role);

    // Redirige a la ruta limpia si no hay filtros
    window.location.href = `${window.location.pathname}?${params.toString()}`;
}

function resetFilters() {
    // Limpiar inputs y selects
    document.getElementById('filterField').value = '';
    document.getElementById('filterValue').value = '';
    document.getElementById('filterEstadoUs').value = '';
    document.querySelectorAll('input[name="filterRole"]').forEach(radio => radio.checked = false);
    document.getElementById('roleTodos').checked = true;

    // Redirigir a la ruta base de FastAPI sin query params
    window.location.href = '/admin/users';
}