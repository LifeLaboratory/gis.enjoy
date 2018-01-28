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



var setPoints = 0;

function initMap() {
    console.log("init");
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();

    //start = new google.maps.LatLng(56.845229, 60.645281);
    //end = new google.maps.LatLng(56.841996, 60.658903);



    //var ekb = new google.maps.LatLng(56.845417, 60.645740);
    var nsk = new google.maps.LatLng(55.027978, 82.951315);
    var mapOptions = {
        zoom:14,
        center: nsk
    };

    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    directionsDisplay.setMap(map);


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

                document.getElementById("hint").innerHTML = "Выберите конечную точку точку";
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
                document.getElementById("hint").innerHTML = "Выберите интересующие вас категории и нажмите \"Построить маршрут\" <br> Для сброса точек кликните на карту";
                document.getElementById("filters").style.left = "0";
                document.getElementById("parameters").style.display = "none";
                document.getElementById("build-route").classList.toggle("menu__element--main-point");
                break;

            case 2:
                setPoints = 0 ;
                markerA.setMap(null);
                markerB.setMap(null);
                document.getElementById("hint").innerHTML = "Выберите исходную точку точку";
                document.getElementById("search-address").placeholder = "Адрес отправления";
                document.getElementById("filters").style.left = "-300px";
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
    console.log("Весь массив выбранного пути ");
    console.log(routeCordArray[id]);
    var markers = new Array();
    for (var i = 0; i < routeCordArray[id].length; i++) {
        waypts.push({
            location: routeCordArray[id][i],
            stopover: true
        });

        markers[i] = new google.maps.Marker({
            position: routeCordArray[id][i],
            map: map,
            title: i,
            label: i
        });
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

function removeRoute() {
    directionsDisplay.setDirections({routes: []});
}

// Create a <script> tag and set the USGS URL as the source.
var script = document.createElement('script');
// This example uses a local copy of the GeoJSON stored at
// http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
//script.src = 'https://developers.google.com/maps/documentation/javascript/examples/json/earthquake_GeoJSONP.js';

document.getElementsByTagName('head')[0].appendChild(script);
