//ymaps.ready(init);

function init(routIndex) {
    var myMap = new ymaps.Map("map", {
        //center: [55.745508, 37.435225],
        center: [results.origin.X, results.origin.Y],
        //center: [54.9870301969, 82.8739339379],
        zoom: 13
    }, {
        searchControlProvider: 'yandex#search'
    });

    // Добавим на карту схему проезда
    // от улицы Крылатские холмы до станции метро "Кунцевская"
    // через станцию "Молодежная" и затем до станции "Пионерская".
    // Точки маршрута можно задавать 3 способами:
    // как строка, как объект или как массив геокоординат.
    ymaps.route(routeCords[routIndex]).then(function (route) {
        myMap.geoObjects.add(route);
        // Зададим содержание иконок начальной и конечной точкам маршрута.
        // С помощью метода getWayPoints() получаем массив точек маршрута.
        // Массив транзитных точек маршрута можно получить с помощью метода getViaPoints.
        var points = route.getWayPoints(),
            lastPoint = points.getLength() - 1;
        // Задаем стиль метки - иконки будут красного цвета, и
        // их изображения будут растягиваться под контент.
        points.options.set('preset', 'islands#redStretchyIcon');
        // Задаем контент меток в начальной и конечной точках.
        points.get(0).properties.set('iconContent', 'Точка отправления');
        points.get(lastPoint).properties.set('iconContent', 'Точка прибытия');
    }, function (error) {
        alert('Возникла ошибка: ' + error.message);
    });


    //далее идет добавление подсказок

/*

    var placemark = new YMaps.Placemark(new YMaps.GeoPoint(37.609218,55.753559), {hideIcon: false});

// Добавляет метку на карту
    myMap.addOverlay(placemark);

*/

/*

    var placemark = new YMaps.Placemark(new YMaps.GeoPoint(55.731272, 37.447198));

    placemark.name = "Москва";
    placemark.description = "Столица Российской Федерации";

    map.addOverlay(placemark);
*/


}




















/*



ymaps.ready(init);

function init(routIndex) {
    var myMap = new ymaps.Map("map", {
        //center: [55.745508, 37.435225],
        //center: [results.origin.X, results.origin.Y],
        center: [55.731272, 37.447198],
        zoom: 13
    }, {
        searchControlProvider: 'yandex#search'
    });

    // Добавим на карту схему проезда
    // от улицы Крылатские холмы до станции метро "Кунцевская"
    // через станцию "Молодежная" и затем до станции "Пионерская".
    // Точки маршрута можно задавать 3 способами:
    // как строка, как объект или как массив геокоординат.
    ymaps.route([
        'Москва, улица Крылатские холмы',
        {
            point: 'Москва, метро Молодежная',
            // метро "Молодежная" - транзитная точка
            // (проезжать через эту точку, но не останавливаться в ней).
            type: 'viaPoint'
        },
        [55.731272, 37.447198], // метро "Кунцевская".
        {
            point: 'Москва, метро Багратионовская',
            // метро "Молодежная" - транзитная точка
            // (проезжать через эту точку, но не останавливаться в ней).
            type: 'viaPoint'
        },
        'Москва, метро Пионерская'
    ]).then(function (route) {
        myMap.geoObjects.add(route);
        // Зададим содержание иконок начальной и конечной точкам маршрута.
        // С помощью метода getWayPoints() получаем массив точек маршрута.
        // Массив транзитных точек маршрута можно получить с помощью метода getViaPoints.
        var points = route.getWayPoints(),
            lastPoint = points.getLength() - 1;
        // Задаем стиль метки - иконки будут красного цвета, и
        // их изображения будут растягиваться под контент.
        points.options.set('preset', 'islands#redStretchyIcon');
        // Задаем контент меток в начальной и конечной точках.
        points.get(0).properties.set('iconContent', 'Точка отправления');
        points.get(lastPoint).properties.set('iconContent', 'Точка прибытия');
    }, function (error) {
        alert('Возникла ошибка: ' + error.message);
    });


    //далее идет добавление подсказок

    /!*

        var placemark = new YMaps.Placemark(new YMaps.GeoPoint(37.609218,55.753559), {hideIcon: false});

    // Добавляет метку на карту
        myMap.addOverlay(placemark);

    *!/

    /!*

        var placemark = new YMaps.Placemark(new YMaps.GeoPoint(55.731272, 37.447198));

        placemark.name = "Москва";
        placemark.description = "Столица Российской Федерации";

        map.addOverlay(placemark);
    *!/


}*/
