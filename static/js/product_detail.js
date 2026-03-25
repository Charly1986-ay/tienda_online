document.addEventListener("DOMContentLoaded", function() {
    const decreaseBtn = document.getElementById("decreaseBtn");
    const increaseBtn = document.getElementById("increaseBtn");
    const quantityInput = document.getElementById("quantity");
    const maxStock = parseInt(quantityInput.getAttribute("max")); // Obtener el stock máximo del atributo "max"
    const minQuantity = parseInt(quantityInput.getAttribute("min")); // Obtener el mínimo

    // Asegurarse de que el valor de la cantidad no sea menor que 1
    decreaseBtn.addEventListener("click", function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue > minQuantity) {
            quantityInput.value = currentValue - 1;
        }
    });

    // Asegurarse de que el valor de la cantidad no sea mayor que el stock máximo
    increaseBtn.addEventListener("click", function() {
        let currentValue = parseInt(quantityInput.value);
        if (currentValue < maxStock) {
            quantityInput.value = currentValue + 1;
        }
    });
});