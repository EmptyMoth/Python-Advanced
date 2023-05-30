let mainPhoto = document.querySelector(".active-photo")
let miniPhoto = document.querySelectorAll(".preview-list li a")

for (let photo of miniPhoto) {
    photo.onclick = function (evt) {
        evt.preventDefault()
        mainPhoto.src = photo.href

        let currentPhoto = document.querySelector(".preview-list .active-item")
        currentPhoto.classList.remove("active-item")
        photo.classList.add("active-item")
    }
}