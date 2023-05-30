let themeButtonDark = document.querySelector(".theme-button-dark")
let themeButtonLight = document.querySelector(".theme-button-light")

themeButtonLight.onclick = function () {
    document.body.classList.remove("dark")
    themeButtonDark.classList.remove("active")
    themeButtonLight.classList.add("active")
}

themeButtonDark.onclick = function () {
    document.body.classList.add("dark")
    themeButtonLight.classList.remove("active")
    themeButtonDark.classList.add("active")
}


let fontButtonSansSerif = document.querySelector(".font-button-sans-serif")
let fontButtonSerif = document.querySelector(".font-button-serif")

fontButtonSansSerif.onclick = function () {
    document.body.classList.remove("serif")
    fontButtonSerif.classList.remove("active")
    fontButtonSansSerif.classList.add("active")
}

fontButtonSerif.onclick = function () {
    document.body.classList.add("serif")
    fontButtonSansSerif.classList.remove("active")
    fontButtonSerif.classList.add("active")
}
