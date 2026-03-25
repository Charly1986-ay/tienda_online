document.addEventListener("DOMContentLoaded", () => {

    // ===================== TOGGLE MENU =====================
    const nav = document.getElementById("menu");
    const hamburger = document.querySelector(".hamburger");

    hamburger.addEventListener("click", () => {
        nav.classList.toggle("active");
    });

    // ===================== AUTOCOMPLETADO =====================
    const input = document.getElementById("searchInput");

    // Creamos el contenedor de sugerencias directamente en body
    const suggestionsBox = document.createElement("div");
    suggestionsBox.id = "suggestions";
    suggestionsBox.className = "suggestions-box";
    document.body.appendChild(suggestionsBox);

    let timeout = null;
    let controller = null;

    input.addEventListener("input", () => {
        clearTimeout(timeout);
        const query = input.value.trim();

        if (!query) {
            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";
            return;
        }

        timeout = setTimeout(async () => {
            if (controller) controller.abort();
            controller = new AbortController();

            try {
                const response = await fetch(`/search-suggestions?q=${encodeURIComponent(query)}`, {
                    signal: controller.signal
                });
                const data = await response.json();

                suggestionsBox.innerHTML = "";
                if (!Array.isArray(data) || data.length === 0) {
                    suggestionsBox.style.display = "none";
                    return;
                }

                data.forEach(item => {
                    const div = document.createElement("div");
                    div.className = "suggestion-item";
                    div.textContent = item;

                    div.addEventListener("click", () => {
                        input.value = item;
                        suggestionsBox.innerHTML = "";
                        suggestionsBox.style.display = "none";
                    });

                    suggestionsBox.appendChild(div);
                });

                // Posicionamos el dropdown respecto al input
                const rect = input.getBoundingClientRect();
                suggestionsBox.style.position = "absolute";
                suggestionsBox.style.top = (rect.bottom + window.scrollY) + "px";
                suggestionsBox.style.left = (rect.left + window.scrollX) + "px";
                suggestionsBox.style.width = rect.width + "px";
                suggestionsBox.style.display = "block";

            } catch (error) {
                if (error.name !== "AbortError") console.error("Error fetch:", error);
            }
        }, 300);
    });

    // Ocultar sugerencias al hacer click fuera
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".autocomplete-wrapper")) {
            suggestionsBox.style.display = "none";
        }
    });

    // Evitar que el form recargue la página
    /*const form = document.querySelector(".search-form");
    form.addEventListener("submit", (e) => e.preventDefault());*/

});