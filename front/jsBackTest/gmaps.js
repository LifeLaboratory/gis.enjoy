var directionsDisplay;
var directionsService;
var start;
var end;
var map;
var routeCordArray = new Array();
var markerA;
var markerB;
var cordA;
var cordB;
var image;
var markers = new Array();
var markersCords = new Array();
var infoWindows = new Array();


var setPoints = 0;

function initMap() {
    console.log("init");
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();

    var ekb = new google.maps.LatLng(56.845417, 60.645740);
    var nsk = new google.maps.LatLng(55.027978, 82.951315);
    var msk = new google.maps.LatLng(55.752951, 37.617365);
    var mapOptions = {
        zoom:14,
        center: msk
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    directionsDisplay.setMap(map);

    image = {
        url: 'https://foiz.ru/style/icons/info.png',
        size: new google.maps.Size(20, 20),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 32)
    };


    var contentString = "lorem  asdasdddddddddd asd hujhiu g sifhgidsfhgisdh sdfhgdhsfg isdjfhg ijshsdfu ghsiddfhsug idsuhfisdfhg isisdfhg isfduiudfshg "

    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    google.maps.event.addListener(map,'click',function(event) {
        switch(setPoints) {
            case 0:
                setPoints++;
                cordA = {
                    lat: event.latLng.lat(),
                    lng: event.latLng.lng()
                };

                start = new google.maps.LatLng(event.latLng.lat(), event.latLng.lng());

                resultCords[0] = [event.latLng.lat(), event.latLng.lng()];

                markerA = new google.maps.Marker({
                    position: cordA,
                    map: map,
                    title: 'Начало пути',
                    label: 'A'
                });

                markerA.addListener('click', function() {
                    infowindow.open(map, markerA);
                });

                hint.setHint('finish-point');

                document.getElementById("search-address").placeholder = "Адрес прибытия";

                break;
            case 1:
                setPoints++;
                cordB = {
                    lat: event.latLng.lat(),
                    lng: event.latLng.lng()
                };


                end = new google.maps.LatLng(event.latLng.lat(), event.latLng.lng());

                resultCords[1] = [event.latLng.lat(), event.latLng.lng()];

                markerB = new google.maps.Marker({
                    position: cordB,
                    map: map,
                    title: 'Конец пути',
                    label: 'B'
                });

                hint.setHint('select-category');

                document.getElementById("left-menu").classList.remove("left-menu--hide");
                document.getElementById("parameters").style.display = "none";
                document.getElementById("build-route").classList.toggle("menu__element--main-point");
                break;

            case 2:
                setPoints = 0 ;
                markerA.setMap(null);
                markerB.setMap(null);
                hint.setHint('start-point');

                document.getElementById("search-address").placeholder = "Адрес отправления";
                document.getElementById("left-menu").classList.add("left-menu--hide");
                document.getElementById("build-route").classList.toggle("menu__element--main-point");
                document.getElementById("parameters").style.display = "flex";
                break;
        }

        console.log(event.latLng.lat());
        console.log(event.latLng.lng());
    });
}


function calculateAndDisplayRoute(id, directionsService, directionsDisplay) {
    var waypts = [];
    console.log("Весь массив выбранного пути");
    console.log(routeCordArray[id]);
    for (var i = 0; i < routeCordArray[id].length; i++) {
        waypts.push({
            location: routeCordArray[id][i],
            stopover: true
        });

        markersCords[i] = {
            lat: routeCordArray[id][i].lat - 0.000268,
            lng: routeCordArray[id][i].lng -0.000398
        };

        markers[i] = new google.maps.Marker({
            position: markersCords[i],
            map: map,
            title: routes.route.name,
            label: "",
            icon: image
        });
        console.log("desct log");
        console.log(routes.route[id].descr);
        infoWindows[i] = new google.maps.InfoWindow({
            content: routes.route[id].descr[i]
        });
        addWindowActionForMarker(i);
    }

    directionsService.route({
        origin: start,
        destination: end,
        waypoints: waypts,
        optimizeWaypoints: true,
        travelMode: 'WALKING'
    }, function(response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

function addWindowActionForMarker(i) {
    markers[i].addListener('click', function() {
        infoWindows[i].open(map, markers[i]);
    });
}

function removeWindowActionForMarker() {
    for (var i = 0; i < markersCords.length; i ++) {
        markers[i].setMap(null);
        delete markers[i];
    }

    markers.length = 0;
}

function removeRoute() {
    directionsDisplay.setDirections({routes: []});
}


var script = document.createElement('script');

document.getElementsByTagName('head')[0].appendChild(script);
