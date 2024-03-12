// Отримуємо необхідні елементи з DOM
const openModalBtn = document.getElementById("openModalBtn");
const modal = document.getElementById("photoModal");
const closeModalBtn = document.getElementsByClassName("close")[0];

// Відкриваємо модальне вікно при кліку на кнопку
openModalBtn.addEventListener("click", function() {
    modal.style.display = "block";
});

// Закриваємо модальне вікно при кліку на "X"
closeModalBtn.addEventListener("click", function() {
    modal.style.display = "none";
});

// Закриваємо модальне вікно, якщо користувач клікнув поза ним
window.addEventListener("click", function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
});
