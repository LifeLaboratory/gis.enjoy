function addActionForRoutes() {
    var i = 0;
    while (document.getElementById("route" + i)) {
        setAction("#route" + i, i);
        i++;
    }
}

function setAction (id, routIndex) {
    $(id).click(function () {
        console.log("rout click");
        showMap(routIndex);
    });
}
