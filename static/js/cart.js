document.addEventListener("DOMContentLoaded", () => {
    // Elementos
    const cartItems = document.getElementById("cartItems");
    const totalContainer = document.querySelector(".cart-total strong");
    const cartBtn = document.getElementById("cartBtn");
    const emptyCartBtn = document.getElementById("emptyCartBtn");
    const checkoutBtn = document.getElementById("checkoutBtn");
    const modal = document.getElementById("modalProducts");
    const closeBtn = modal.querySelector(".close");

    let total = 0;

    // -----------------------------
    // Funciones auxiliares
    // -----------------------------
    function updateTotal() {
        let newTotal = 0;
        cartItems.querySelectorAll(".cart-item").forEach(item => {
            newTotal += parseFloat(item.dataset.subtotal);
        });
        total = newTotal;
        totalContainer.textContent = `Total: $${total.toFixed(2)}`;
    }

    function createParagraph(text, isStrong = false) {
        const p = document.createElement("p");
        if (isStrong) {
            const strong = document.createElement("strong");
            strong.textContent = text;
            p.appendChild(strong);
        } else {
            p.textContent = text;
        }
        return p;
    }

    function createRemoveButton(itemDiv) {
        const btn = document.createElement("button");
        btn.textContent = "Quitar";
        btn.classList.add("remove-btn");
        btn.addEventListener("click", () => {
            cartItems.removeChild(itemDiv);
            updateTotal();
            saveCartToLocalStorage();
        });
        return btn;
    }

    function createCartItem({id, name, price, quantity}) {
        const subtotal = price * quantity;

        const itemDiv = document.createElement("div");
        itemDiv.classList.add("cart-item");

        itemDiv.dataset.id = id;
        itemDiv.dataset.price = price;
        itemDiv.dataset.quantity = quantity;
        itemDiv.dataset.subtotal = subtotal.toFixed(2);

        itemDiv.appendChild(createParagraph(name, true));
        itemDiv.appendChild(createParagraph(`Precio: $${price.toFixed(2)}`));

        const cantidadP = createParagraph(`Cantidad: ${quantity}`);
        cantidadP.classList.add("cantidad");
        itemDiv.appendChild(cantidadP);

        const subtotalP = createParagraph(`Subtotal: $${subtotal.toFixed(2)}`);
        subtotalP.classList.add("subtotal");
        itemDiv.appendChild(subtotalP);

        itemDiv.appendChild(createRemoveButton(itemDiv));
        itemDiv.appendChild(document.createElement("hr"));

        return itemDiv;
    }

    // -----------------------------
    // LocalStorage
    // -----------------------------
    function saveCartToLocalStorage() {
        const items = [];
        cartItems.querySelectorAll(".cart-item").forEach(item => {
            items.push({
                id: item.dataset.id,
                name: item.querySelector("strong").textContent,
                price: parseFloat(item.dataset.price),
                quantity: parseInt(item.dataset.quantity),
                subtotal: parseFloat(item.dataset.subtotal)
            });
        });
        localStorage.setItem("cart", JSON.stringify(items));
    }

    function loadCartFromLocalStorage() {
        const itemsData = JSON.parse(localStorage.getItem("cart")) || [];
        cartItems.innerHTML = "";

        itemsData.forEach(item => {
            const cartItem = createCartItem(item);
            cartItems.appendChild(cartItem);
        });

        updateTotal();
    }

    // -----------------------------
    // Toast
    // -----------------------------
    function showToast(msg, type = "success") {
        const toast = document.getElementById("cartToast");
        toast.textContent = msg;
        toast.className = `cart-toast show ${type}`;
        setTimeout(() => toast.className = "cart-toast", 2000);
    }

    // -----------------------------
    // Agregar productos
    // -----------------------------
    window.addProductToCart = ({id, name, price, quantity}) => {
        let existingItem = cartItems.querySelector(`.cart-item[data-id="${id}"]`);

        if (existingItem) {
            let currentQty = parseInt(existingItem.dataset.quantity) + quantity;
            existingItem.dataset.quantity = currentQty;

            const newSubtotal = price * currentQty;
            existingItem.dataset.subtotal = newSubtotal.toFixed(2);

            existingItem.querySelector(".cantidad").textContent = `Cantidad: ${currentQty}`;
            existingItem.querySelector(".subtotal").textContent = `Subtotal: $${newSubtotal.toFixed(2)}`;
        } else {
            cartItems.appendChild(createCartItem({id, name, price, quantity}));
        }

        updateTotal();
        saveCartToLocalStorage();
        showToast(`${name} agregado al carrito`, "success");
    };

    document.querySelectorAll(".add-to-cart-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const quantityInput = document.getElementById("quantity");
            const selectedQuantity = quantityInput ? parseInt(quantityInput.value) : 1;

            const product = {
                id: String(btn.dataset.id).trim(),
                name: btn.dataset.name,
                price: parseFloat(btn.dataset.price),
                quantity: selectedQuantity
            };

            window.addProductToCart(product);
        });
    });

    // -----------------------------
    // Modal show/close
    // -----------------------------
    function showCartModal() {
        loadCartFromLocalStorage();
        modal.style.display = "flex";
    }

    cartBtn && cartBtn.addEventListener("click", showCartModal);
    closeBtn.addEventListener("click", () => modal.style.display = "none");
    window.addEventListener("click", e => {
        if (e.target === modal) modal.style.display = "none";
    });

    // -----------------------------
    // Vaciar y checkout
    // -----------------------------
    emptyCartBtn.addEventListener("click", () => {
        cartItems.innerHTML = "";
        total = 0;
        totalContainer.textContent = `Total: $0.00`;
        localStorage.removeItem("cart");
    });

    checkoutBtn.addEventListener("click", async () => {
        const cartData = JSON.parse(localStorage.getItem("cart")) || [];

        if (cartData.length === 0) {
            showToast("Tu carrito está vacío.", "error");
            return;
        }

        const totalAmount = cartData.reduce((sum, item) => sum + item.subtotal, 0);

        try {
            const res = await fetch("/buy", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ items: cartData, total: totalAmount })
            });

            // 🔹 Si el middleware redirige al login
            if (res.redirected) {
                modal.style.display = "none";

                showToast("Debes iniciar sesión para completar la compra.", "error");

                setTimeout(() => {
                    window.location.href = res.url; // /auth/login
                }, 1200);

                return;
            }

            if (!res.ok) {
                showToast("Hubo un error al procesar la compra.", "error");
                return;
            }

            await res.json();

            showToast(`Pago procesado correctamente por $${totalAmount.toFixed(2)}`, "success");

            // Limpiar carrito
            cartItems.innerHTML = "";
            totalContainer.textContent = `Total: $0.00`;
            localStorage.removeItem("cart");

            setTimeout(() => {
                modal.style.display = "none";
            }, 1000);

        } catch (err) {
            console.error(err);
            showToast("Hubo un error al procesar la compra.", "error");
        }
    });

    // -----------------------------
    // Inicializar
    // -----------------------------
    loadCartFromLocalStorage();
});