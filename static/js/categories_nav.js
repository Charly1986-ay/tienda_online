async function loadCategories() {
    const response = await fetch('/categories');
    const data = await response.json();

    const navContainer = document.getElementById('menu-categories');

    data.categories.forEach(cat => {
        const a = document.createElement('a');
        a.href = `/?category=${cat.id}`;  // <-- CORRECCIÓN
        a.textContent = cat.name;
        navContainer.appendChild(a);
    });
}

loadCategories();