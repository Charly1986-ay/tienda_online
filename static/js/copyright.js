// Llamada al endpoint para obtener el año
fetch('/get_current_year')
    .then(response => response.json())
    .then(data => {
        const copyrightElement = document.getElementById("copyright");
        copyrightElement.innerHTML = `© ${data.current_year} MiTienda`;  // Actualiza el copyright
    })
    .catch(error => console.error('Error al obtener el año:', error));
