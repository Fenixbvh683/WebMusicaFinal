// currentYear.js
document.addEventListener("DOMContentLoaded", function() {
    var currentYear = new Date().getFullYear();
    document.getElementById("current-year").textContent = currentYear;
});
