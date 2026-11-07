// Inputs marked data-numeric accept digits only
var numericInputs = document.querySelectorAll("input[data-numeric]");
numericInputs.forEach(function (input) {
    input.addEventListener("input", function () {
        input.value = input.value.replace(/[^0-9]/g, "");
    });
});

// Do not allow ordering more than the stock shown on the card
var quantityInputs = document.querySelectorAll("input[name='orderquantity']");
quantityInputs.forEach(function (input) {
    input.addEventListener("input", function () {
        var max = parseInt(input.max);
        if (parseInt(input.value) > max) {
            input.value = max;
        }
    });
});

// Product search filter on the buy page
var searchBox = document.getElementById("product-search");
if (searchBox) {
    searchBox.addEventListener("input", function () {
        var text = searchBox.value.toLowerCase().trim();
        var cards = document.querySelectorAll(".product-card");
        var shown = 0;
        cards.forEach(function (card) {
            if (card.dataset.search.indexOf(text) !== -1) {
                card.style.display = "";
                shown++;
            } else {
                card.style.display = "none";
            }
        });
        document.getElementById("no-match").hidden = shown !== 0;
    });
}
