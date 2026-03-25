// static/js/navbar-padding.js
document.addEventListener("DOMContentLoaded", function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        document.body.style.paddingTop = navbar.offsetHeight + "px";
    }
});


var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })