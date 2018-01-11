var results;
var routes;
var routeCords = new Array();
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

function showMap(routIndex) {
    $("#select-options").addClass("disabled-block");
    $("#routes").addClass("disabled-block");
    $("#map-container").removeClass("disabled-block");
    console.log("showmap");
    init(routIndex);
}

function showRoutes() {
    $("#select-options").addClass("disabled-block");
    $("#routes").removeClass("disabled-block");
    $("#map-container").addClass("disabled-block");

    routes = JSON.parse(routes);
    console.log(routes.route[0].name);


    var str = "";
    for (var i = 0; i < routes.route.length; i++) {
        str+='<div id="route' + i + '" class="route">';
        for (var j = 0; j < routes.route[i].name.length; j++)  {
            str+= '<div class="route__point"> ' + routes.route[i].name[j] + ' </div>';
            if (j != routes.route[i].name.length - 1) {
                str+= '<div class="route__arrow">  -->  </div>';
            }
        }
        str+='</div>';
    }
    $("#routes").html(str);

    addActionForRoutes();

    for (var i = 0; i < routes.route.length; i++) {
        routeCords[i] = new Array();
        console.log("i: " + i);
        for (var j = 0; j < routes.route[i].name.length; j++) {
            routeCords[i][j] = [routes.route[i].X[j], routes.route[i].Y[j]];
            console.log(routeCords[i][j]);
        }

    }
    console.log(routeCords);
}

function otherWay() {
    $("#map").html("");

    $("#select-options").addClass("disabled-block");
    $("#routes").removeClass("disabled-block");
    $("#map-container").addClass("disabled-block");
}

function otherPriotity() {

    $("#select-options").removeClass("disabled-block");

    $("#step0").removeClass("disabled-block");

    var i = 1;
    console.log("other priotiy " + i);
    while (document.getElementById("step" + i)) {
        console.log("op");
        $("#step" + i).addClass("disabled-block");
        i++;
        zeroStep();
    }

    $("#routes").addClass("disabled-block");
    $("#map-container").addClass("disabled-block");
}

var cords = new Array();

function sendResult() {
    var time = Number($("#hours").val())*60 + Number($("#minutes").val());

    results = {
        origin: {
            X: cords[0][0],
            Y: cords[0][1]
        },
        destination: {
            X: cords[1][0],
            Y: cords[1][1]
        },
        time: time,
        type: [],
        star: []
    };

    results = JSON.stringify(results);
    results = JSON.parse(results);

    var i = 0;
    while (document.getElementById("option" + i)) {
        results.type[i] = $("#option" + i).html();
        results.star[i] = Number($("#rating" + i).val());
        i++;
    }

    console.log("sending start");
    console.log();
    //var httpRequest = "http://192.168.49.77:13451/geo?data=" + JSON.stringify(results);
    var httpRequest = "http://192.168.49.77:13451/test?data=" + JSON.stringify(results);

    var xhr = createCORSRequest('GET', httpRequest);
    xhr.send(); //отправка даты

    xhr.onload = function () {
        console.log("полученные данные");
        routes = $.parseJSON(this.responseText);
        console.log(routes);
        showRoutes();
    };

    xhr.onerror = function () {
        //wconsole.log('error ' + this.status);
    };
}


function takeAddress() {
    console.log($("#start-address").val());
    console.log($("#end-address").val());

    console.log("Начальные координаты ");
    var startAddress = $("#start-address").val() + " Новосибирск";
    var finishAddress = $("#end-address").val() + " Новосибирск";

    get_coords(startAddress, 0);
    get_coords(finishAddress, 1);
}
function second() {
    console.log(cords);
}
function get_coords(address, i) {
    // Поиск координат
    //var cords;
    ymaps.geocode(address, { results: 1 }).then(function (res) {
            // Выбираем первый результат геокодирования
            var firstGeoObject = res.geoObjects.get(0);
            cords[i] = firstGeoObject.geometry.getCoordinates();
            console.log("Задаются кордс");
            second();
        },
        function (err) {
            // Если геокодирование не удалось,
            // сообщаем об ошибке
            alert(err.message);
        });
}

$prevButton = $("#prev-step");
$nextButton = $("#next-step");

function countSteps() {
    var is = true;
    var i = 0;
    while (is) {
        if (!document.getElementById("step" + i)) {
            is = false;
            continue;
        }
        i++;
    }
    return i;
}

function switchStep(direction) {
    switch(direction) {
        case 'next':
            if ($step === 0) {
                takeAddress();
            }
            if ($step != $lastStep) {
                console.log("switch next");
                console.log($("step" + $step));
                $("#step" + $step).addClass("disabled-block");
                $step++;
                $("#step" + $step).removeClass("disabled-block");
            }
            break;
        case 'prev':
            if($step){
                $("#step" + $step).addClass("disabled-block");
                $step--;
                $("#step" + $step).removeClass("disabled-block");
            }
            break;
        default:
            break;
    }

    if ($step === $lastStep) {
        $("#next").html('<button id="show-routes" class="select-options__next-button">Показать маршруты</button>');

        $("#show-routes").click(function () {
            sendResult();
        });
    } else {
        $("#next").html('<button id="next-step" class="select-options__next-button">Далее</button>');
        $("#next-step").click(function () {
            console.log("next button click");
            switchStep("next");
        });
    }

    console.log("Step = " + $step);
}

function zeroStep() {
    $step = 0;
    console.log("step=" + $step);
    $("#next").html('<button id="next-step" class="select-options__next-button">Далее</button>');
    $("#next-step").click(function () {
        console.log("next button click");
        switchStep("next");
    });
}

$nextButton.click(function () {
    console.log("next button click");
    switchStep("next");
});

$prevButton.click(function () {
    console.log("prev button click");
    switchStep("prev");
});

$step = 0;
$lastStep = countSteps() - 1;