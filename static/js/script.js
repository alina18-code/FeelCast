document.querySelectorAll(".card_flip").forEach( card => {
    card.addEventListener("click", () => {
        console.log ("card clicked");
        card.classList.toggle("flipped");

    });
});