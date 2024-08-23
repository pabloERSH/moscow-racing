ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            center: [55.9941, 36.2714],
            zoom: 10
        }, {
            searchControlProvider: 'yandex#search'
        }),

    // Создаем геообъект с типом геометрии "Точка".
        myGeoObject = new ymaps.GeoObject({
            // Описание геометрии.
            geometry: {
                type: "Point",
                coordinates: [55.9941, 36.2714]
            },
            // Свойства.
            properties: {
                // Контент метки.
                iconContent: 'Raceway',
            }
        }, {
            // Опции.
            // Иконка метки будет растягиваться под размер ее содержимого.
            preset: 'islands#blackStretchyIcon',
            // Метку можно перемещать.
            draggable: true
        });
    myMap.geoObjects.add(myGeoObject);
}
