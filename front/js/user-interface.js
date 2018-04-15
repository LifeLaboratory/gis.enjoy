var priority = new Array();
var resultCords = new Array();
var routes;
var selectedRoute;
var routesList = new Array();

var hint;
var leftMenu;

function createCORSRequest(method, url) {
    var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr) {
        xhr.open(method, url, true);
    } else if (typeof XDomainRequest != "undefined") {
        xhr = new XDomainRequest();
        xhr.open(method, url);
    } else {
        xhr = null;
    }
    return xhr;
}

function getFilters() {
    var httpRequest = 'http://90.189.132.25:13451/filter';

    var xhr = createCORSRequest('GET', httpRequest);
    xhr.send(); //отправка даты

    xhr.onload = function () {
        document.getElementById("placeholder").classList.add("disabled-block");
        console.log("фильтры");

        var filters = JSON.parse(this.responseText);
        console.log(routes);

        var filtersContainer = document.getElementById('filters');

        for (var i = 0; i < filters.data.length; i++) {
            var name = filters.data[i];

            filtersContainer.innerHTML += '<div todatabase="' + name + '" id="filters__category' + i + '" ' +
                'class="left-menu__category">' + name + '</div>'
        }


        setTimeout(setFiltersAction(), 4000);

    };

    xhr.onerror = function () {
        document.getElementById("placeholder").classList.add("disabled-block");
    };

}

function setFiltersAction() {
    var isok = true;

    for (var i = 0; isok != false; i++) {
        var element = document.getElementById("filters__category" + i);

        if (element) {
            addActionForParameters(i);
        } else {
            isok = false;
        }
    }
}

function addActionForParameters(id) {
    document.getElementById("filters__category" + id).onclick = function () {
        console.log(document.getElementById("filters__category" + id).getAttribute('toDataBase'));

        if (!document.getElementById("filters__category" + id).classList.contains("left-menu__category--active")) { // Не еще не выбран
            //priority[priority.length] = $("#filters__category" + id).html(); // ТАК БЫЛО И РАБОТАЛО

            priority[priority.length] = document.getElementById("filters__category" + id).getAttribute('toDataBase');
            document.getElementById("filters__category" + id).classList.toggle("left-menu__category--active");
        } else {
            document.getElementById("filters__category" + id).classList.toggle("left-menu__category--active");
            for (var i = 0; i< priority.length; i++) {
                if (priority[i] === document.getElementById("filters__category" + id).getAttribute('toDataBase')) {
                    for (var j = i; j < priority.length-1; j++) {
                        priority[j] = priority[j+1]
                    }

                    priority.splice(priority.length-1, 1);
                    break;
                }
            }
        }

        console.log("После");
        console.log(priority);
    };
}

function showRoutes(from) {
    document.getElementById("routes-block").classList.remove("disabled-block");
    document.getElementById("left-menu").classList.add("left-menu--hide");

    var str = "";

    for (var i = 0; i < routesList.length; i++) {
        str+= '<div class="routes__one-route" id="routes__one-route' + i + '">';

        for (var j = 0; j < routesList[i].length; j++) {
            if (j+1 < routesList[i].length) {
                str+= routesList[i][j] + " -> ";
            } else {
                str+= routesList[i][j];
            }
        }
        str+= '</div>'
    }
    document.getElementById("routes-block").innerHTML = str;

    for (var i = 0; i < routesList.length; i++) {
        setActionForRoute(i);
    }

    switch (from) {
        case 'build-route':
            document.getElementById("back-to-set-parameters-link").onclick = function () {
                document.getElementById("routes-block").classList.toggle("disabled-block");
                document.getElementById("left-menu").classList.remove("left-menu--hide");
                document.getElementById("hint").classList.toggle("disabled-block");
                selectMenu("main-menu");
            };
            break;

        case 'change-route':
            document.getElementById("back-to-route-on-map-link").onclick = function () {
                document.getElementById("routes-block").classList.add("disabled-block");
                document.getElementById("route-menu").classList.remove("disabled-block");
                document.getElementById("change-route-menu").classList.add("disabled-block");
            };
            break;

        default:
            document.getElementById("back-to-set-parameters-link").onclick = function () {
                document.getElementById("routes-block").classList.toggle("disabled-block");
                document.getElementById("left-menu--hide").style.left = "0";
                document.getElementById("hint").classList.toggle("disabled-block");
            };
            break;
    }
}

function setActionForRoute(id) {
    document.getElementById("routes__one-route" + id).onclick = function () {
        selectedRoute = id;
        document.getElementById("routes-block").classList.toggle("disabled-block");
        selectMenu("route-menu");
        calculateAndDisplayRoute(id, directionsService, directionsDisplay);
    };
}

function makeList() {
    for (var i = 0; i < routes.route.length; i++) {
        routesList[i] = new Array();
        for (var j = 0; j < routes.route[i].name.length; j++ )
        routesList[i][j] = routes.route[i].name[j];
    }

    console.log("routes list: ");
    console.log(routesList);
    makeCordArray();
    showRoutes("build-route");
}

function makeCordArray() {
    for (var i = 0; i < routes.route.length; i++) {
        routeCordArray[i] = new Array();

        for (var j = 0; j < routes.route[i].X.length; j++) {
            routeCordArray[i][j] = {
                lat: routes.route[i].X[j],
                lng: routes.route[i].Y[j]
            };
        }
    }
    console.log("Полученный массив координат");
    console.log(routeCordArray);
}

function selectMenu(activeMenu) {
    //if (!activeMenu) return 0;

    console.log(activeMenu);

    document.getElementById("main-menu").classList.add("disabled-block");
    document.getElementById("route-menu").classList.add("disabled-block");
    document.getElementById("change-route-menu").classList.add("disabled-block");
    document.getElementById("select-route-menu").classList.add("disabled-block");

    var elem = document.getElementById(activeMenu);
    //if (elem.classList.contains("disabled-block"))

        elem.classList.remove("disabled-block");
}

$(document).ready(function(){
    hint = new Hint();
    //leftMenu = new LeftMenu();
    getFilters();

    function start() {
        selectMenu("main-menu");
        removeRoute();
        removeWindowActionForMarker();

        setPoints = 0;
        markerA.setMap(null);
        markerB.setMap(null);

        hint.setHint('start-point');

        document.getElementById("parameters").style.display = "flex";
        document.getElementById("search-address").placeholder = "Адрес отправления";
        document.getElementById("build-route").classList.toggle("menu__element--main-point");
        document.getElementById("routes-block").classList.add("disabled-block");
    }



    //тест
/*

    var answ = {
        "route": [
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "ducken", "fuck"],
                "time": [20, 30, 35, 40],
                "descr": ["descr_lenina", "discr_duck", "duckduck", "discr_fuck"],
                "X": [56.845229, 56.839619, 56.841996, 56.840200],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.658903, 60.654428]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            },
            {
                "name": ["Lenina", "duck", "fuck", "ducken"],
                "time": [20, 30, 40, 35],
                "descr": ["descr_lenina", "discr_duck", "discr_fuck", "duckduck"],
                "X": [56.845229, 56.839619, 56.840200, 56.841996],
                "type": ["park", "galery", "park", "park"],
                "Y": [60.645281, 60.647116, 60.654428, 60.658903]
            }
        ]
    };
    results = JSON.stringify(answ);
    routes = JSON.parse(results);
    
*/

    document.getElementById("build-route").onclick = function () {

        var time = Number($("#hours").val())*60 + Number($("#minutes").val());
        document.getElementById("placeholder").classList.toggle("disabled-block");
        results = {
            origin: {
                X: resultCords[0][0],
                Y: resultCords[0][1]
            },
            destination: {
                X: resultCords[1][0],
                Y: resultCords[1][1]
            },
            time: time,
            priority: priority
        };
        results = JSON.stringify(results);
        results = JSON.parse(results);


        console.log(JSON.stringify(results));

        console.log("sending start");
        console.log();

        //var httpRequest = "http://localhost:13451/list?data=" + JSON.stringify(results);
        //var httpRequest = "http://90.189.132.25:13451/geo?data=" + JSON.stringify(results);
        //const httpRequest = 'http://90.189.132.25:13451/geo?data={"origin":{"X":53.341805,"Y":83.751245},"destination":{"X":53.344153,"Y":83.783141},"time":480,"priority":["парк","музей","памятник","кинотеатр"]}';
        var httpRequest = 'http://90.189.132.25:13451/geo?data=' + JSON.stringify(results);

        var xhr = createCORSRequest('GET', httpRequest);
        xhr.send(); //отправка даты

        xhr.onload = function () {
            document.getElementById("placeholder").classList.toggle("disabled-block");
            console.log("полученные данные");
            console.log(this.responseText);

            //routes = $.parseJSON(this.responseText);
            routes = JSON.parse(this.responseText);
            console.log(routes);

            makeList();
            //showRoutes();
        };

        xhr.onerror = function () {
            //console.log('error ' + this.status);
            document.getElementById("placeholder").classList.toggle("disabled-block");
        };
        document.getElementById("hint").classList.toggle("disabled-block");

        selectMenu("select-route-menu");
        //makeList(); //ДЛЯ ТЕСТА, ПОТОМ УБРАТЬ
    };

    document.getElementById("change-route").onclick = function () {
        selectMenu("change-route-menu");
        showRoutes("change-route");
    };

    document.getElementById("change-parameters").onclick = function () {
        start();
    };

    document.getElementById("reselect-points").onclick = function () {
        start();
    };

    document.getElementById("random-route").onclick = function () {
        var randomIndex = Math.round(Math.random() * (routesList.length - 1));
        console.log(randomIndex);
        selectMenu("change-route-menu");

        document.getElementById("routes-block").classList.add("disabled-block");
        calculateAndDisplayRoute(randomIndex, directionsService, directionsDisplay);
    };
});
