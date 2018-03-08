function debug(isActive) {
    if (isActive) {
        alert("начинаем дебажить");
        document.getElementById("left-menu").classList.remove("left-menu--hide");
        document.getElementById("filters").classList.add("disabled-block");
        document.getElementById("debug-menu").classList.remove("disabled-block");
        

    } else {
        alert("заканчиваем дебажить");

        document.getElementById("filters").classList.remove("disabled-block");
    }
}