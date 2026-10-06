document.querySelectorAll(".card-flip").forEach( card => {
    card.addEventListener("click", () => {
        card.classList.toggle("flipped");

    });
});