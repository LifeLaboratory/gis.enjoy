function Hint() {
    this.hintElement = document.getElementById("hint");
}

Hint.prototype.setHint = function(isActive) {
    switch (isActive) {
        case 'disable':
            this.hintElement.classList.add("disabled-block");
            break;
        case 'start-point':
            this.hintElement.classList.remove("disabled-block");
            this.hintElement.innerHTML = "Выберите исходную точку точку";
            break;
        case 'finish-point':
            this.hintElement.classList.remove("disabled-block");
            this.hintElement.innerHTML = "Выберите конечную точку";
            break;
        case 'select-category':
            this.hintElement.classList.remove("disabled-block");
            this.hintElement.innerHTML = "Выберите интересующие вас категории и нажмите \"Построить маршрут\" <br> Для сброса точек кликните на карту";
            break;
        default:
            this.hintElement.classList.toggle("disabled-block");
            break;
    }
};