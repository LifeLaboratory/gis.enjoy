function LeftMenu() {
    this.hintElement = document.getElementById("hint");
}

LeftMenu.prototype.setHint = function(isActive) {
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

LeftMenu.prototype.show = function () {
    this.hintElement.classList.remove("left-menu--hide");
};

LeftMenu.prototype.hide = function () {
    this.hintElement.classList.add("left-menu--hide");
};

LeftMenu.prototype.setActionForMenuElements = function () {
    var isok = true;

    for (var i = 0; isok != false; i++) {
        var element = document.getElementById("filters__category" + i);

        if (element) {
            addActionForParameters(i);
        } else {
            isok = false;
        }
    }





};