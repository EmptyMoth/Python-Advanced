let cardViewButtonGrid = document.querySelector(".card-view-button-grid")
let cardViewButtonList = document.querySelector(".card-view-button-list")

let cards = document.querySelector(".cards")

cardViewButtonGrid.onclick = function () {
    cards.classList.remove("list")
    cardViewButtonList.classList.remove("active")
    cardViewButtonGrid.classList.add("active")
}

cardViewButtonList.onclick = function () {
    cards.classList.add("list")
    cardViewButtonGrid.classList.remove("active")
    cardViewButtonList.classList.add("active")
}
