let shortArticles = document.querySelectorAll(".blog-article")

for (let shortArticle of shortArticles) {
    let dropDownButton = shortArticle.querySelector(".more")
    dropDownButton.onclick = function () {
        shortArticle.classList.remove("short")
    }
}