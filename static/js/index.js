const grid = document.getElementById("productGrid");
const loadMoreBtn = document.getElementById("loadMoreBtn");

let page = Number(grid.dataset.page || 1);
let totalPages = Number(grid.dataset.totalPages || 1);
let isLoading = false;

async function loadMore() { 
    if (isLoading || page >= totalPages) return;

    isLoading = true;
    loadMoreBtn.disabled = true;
    loadMoreBtn.textContent = "Cargando...";

    try {
        const response = await fetch(`/articles?page=${page + 1}`);
        const data = await response.json();

        data.articles.forEach(a => {
            const div = document.createElement("div");
            div.className = "product";
            div.innerHTML = `
                <a href="/articles/${a.id}" class="product-link">
                    <div class="product">
                        <img src="/static/img/${a.image_name}" class="img-item">
                        <h3>${a.name}</h3>
                        <p class="price">$${a.price}</p>
                    </div>
                </a>
            `;
            grid.appendChild(div);
        });

        page = data.page;
        totalPages = data.total_pages;

        // Si ya no hay más páginas, ocultar el botón
        if (page >= totalPages) {
            loadMoreBtn.style.display = "none"; // <- aquí se oculta
        } else {
            loadMoreBtn.textContent = "Ver más artículos";
            loadMoreBtn.disabled = false;
        }

    } catch (err) {
        console.error(err);
        loadMoreBtn.textContent = "Error al cargar";
        loadMoreBtn.disabled = false;
    } finally {
        isLoading = false;
    }
}

loadMoreBtn.addEventListener("click", loadMore);