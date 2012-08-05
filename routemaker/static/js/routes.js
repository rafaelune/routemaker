startsLat = -23.17908;
startsLng = -45.887248;

var map = null;

$(document).ready(function() {
    util.createExternalLinks();
    visual.configUserMenuOptions();

    // inits the map
    map = new GMaps({
        div: '#my-map',
        lat: startsLat,
        lng: startsLng
    });

    $('#buscar').click(function() {
        getMyPositionByAddress();
    });

    $('#obter-posicao').click(function() {
        getMyPosition();
    });

    // prepare Options Object 
    var options = { 
        target:     '#pedidos-placeholder', 
        url:        '/filtro/', 
        beforeSubmit: function(arr, $form, options) {
            // saves the entidade id selected
            $('#my-map').data('entidade', arr[1].value);
            visual.showLoading();
        },
        success: function() { 
            $('#pedidos-placeholder')
                .accordion({
                    header: "> div > h3",
                    active: false
                })
                .sortable({
                    connectWith: '#selected-pedidos-placeholder',
                    placeholder: 'ui-state-highlight',
                    handle: 'h3',
                    stop: function( event, ui ) {
                        /* IE doesn't register the blur when sorting
                            so trigger focusout handlers to remove .ui-state-focus
                        */
                        ui.item.children( 'h3' ).triggerHandler( 'focusout' );
                    }
                });
            $('#pedidos-placeholder').disableSelection();
            
            $('#selected-pedidos-placeholder')
                .accordion({
                    header: "> div > h3"
                })
                .sortable({
                    connectWith: '#pedidos-placeholder',
                    placeholder: 'ui-state-highlight',
                    handle: 'h3',
                    stop: function( event, ui ) {
                        /* IE doesn't register the blur when sorting
                            so trigger focusout handlers to remove .ui-state-focus
                        */
                        ui.item.children( 'h3' ).triggerHandler( 'focusout' );
                    }
                });
            $('#selected-pedidos-placeholder').disableSelection();

            $('#btnNext1').removeClass('disabled');
            $('#btnNext1').removeAttr('disabled');

            visual.closeLoading();
        } 
    };
    // pass options to ajaxForm 
    $('#filterForm').ajaxForm(options);
});

function getMyPositionByAddress() {
    GMaps.geocode({
        address: $('#endereco').val(),
        callback: function(results, status) {
            if (status == 'OK') {
                var geocode_location = results[0].geometry.location;
                
                startsLat = geocode_location.lat();
                startsLng = geocode_location.lng();

                map = new GMaps({
                    div: '#my-map',
                    lat: startsLat,
                    lng: startsLng
                });

                map.setCenter(geocode_location.lat(), geocode_location.lng());

                map.addMarker({
                    lat: geocode_location.lat(),
                    lng: geocode_location.lng(),
                    infoWindow: {
                        content: '<strong>Ponto de partida</strong>'
                    }
                });

                $('#btnNext2').removeClass('disabled');
                $('#btnNext2').removeAttr('disabled');
            }
        }
    });
}

function getMyPosition() {
    visual.showLoading();

    GMaps.geolocate({
        success: function(position) {
            startsLat = position.coords.latitude;
            startsLng = position.coords.longitude;

            map = new GMaps({
                div: '#my-map',
                lat: startsLat,
                lng: startsLng
            });

            map.setCenter(position.coords.latitude, position.coords.longitude);

            map.addMarker({
                lat: startsLat,
                lng: startsLng,
                infoWindow: {
                    content: '<strong>Ponto de partida</strong>'
                }
            });

            $('#btnNext2').removeClass('disabled');
            $('#btnNext2').removeAttr('disabled');

            visual.closeLoading();
        },
        error: function(error) {
            startsLat = geoip_latitude();
            startsLng = geoip_longitude();

            // use MaxMind IP to location API fallback
            map.setCenter(startsLat, startsLng);

            map = new GMaps({
                div: '#my-map',
                lat: startsLat,
                lng: startsLng
            });

            map.addMarker({
                lat: startsLat,
                lng: startsLng,
                infoWindow: {
                    content: '<strong>Ponto de partida</strong>'
                }
            });

            $('#btnNext2').removeClass('disabled');
            $('#btnNext2').removeAttr('disabled');

            visual.closeLoading();
        },
        not_supported: function() {
            startsLat = geoip_latitude();
            startsLng = geoip_longitude();

            // use MaxMind IP to location API fallback
            map.setCenter(startsLat, startsLng);

            map = new GMaps({
                div: '#my-map',
                lat: startsLat,
                lng: startsLng
            });

            map.addMarker({
                lat: startsLat,
                lng: startsLng,
                infoWindow: {
                    content: '<strong>Ponto de partida</strong>'
                }
            });

            $('#btnNext2').removeClass('disabled');
            $('#btnNext2').removeAttr('disabled');

            visual.closeLoading();
        }
    });
}

function loadTab2() {
    visual.goToSecondTabFilter();
}

function loadTab3() {
    visual.goToThirdTabFilter();
    
    visual.showLoading();

    // get pedidos id
    var pedidos_list = $('#selected-pedidos-placeholder .sortable-item').map(
        function () {
            return $(this).attr('id');
        }
    ).get().join(',');

    var origin_lat = startsLat;
    var origin_lng = startsLng;
    var counter = 0;
    var pedidos_json = [];
    var locations = [];
    var routes = [];

    var drawRoutes = function() {

        if (counter==0) {
            origin_lat = startsLat;
            origin_lng = startsLng;
        }

        if (counter < pedidos_json.length) {
            var item = pedidos_json[counter];
            var location = locations[counter];
            var route = routes[counter];

            if (location != null) {

                map.addMarker({
                    lat: location.lat(),
                    lng: location.lng(),
                    infoWindow: {
                        content: "<p>" +
                                 "<strong>" + item._Pedido__terceiro._Terceiro__nome + "</strong><br/>" + 
                                 "<span>Pedido: " + item._Pedido__numero + "</span><br/>" +
                                 "<span>Endere&#231;o: " + item._Pedido__terceiro._Terceiro__logradouro + "</span>" +
                                 "</p>"
                    }
                });

                map.drawRoute({
                    origin: [origin_lat, origin_lng],
                    destination: [location.lat(), location.lng()],
                    travelMode: 'driving',
                    strokeColor: '#336699',
                    strokeOpacity: 0.5,
                    strokeWeight: 6
                });

                origin_lat = location.lat();
                origin_lng = location.lng();

                if (route.route.legs.length > 0) {
                    var steps = route.route.legs[0].steps;
                    for (var i=0, step; step=steps[i]; i++) {
                        $('#instructions').append('<li>'+step.instructions+'</li>');
                    }
                    $('#instructions').append('<li>Chegou em <strong>' + item._Pedido__terceiro._Terceiro__logradouro + 
                        ' - pedido: ' + item._Pedido__numero + ' de '+ item._Pedido__terceiro._Terceiro__nome +'</strong></li>');
                }
            } else {
                $('#instructions').append('<li>Endere&#231;o <strong>' + item._Pedido__terceiro._Terceiro__logradouro + 
                        ' - pedido: ' + item._Pedido__numero + ' de '+ item._Pedido__terceiro._Terceiro__nome +'</strong> n&#227;o encontrado</li>');
            }

            counter++;
            drawRoutes();
        } else {
            visual.closeLoading();
        }
    }

    var geolocatePedidos = function() {
        if (counter < pedidos_json.length) {

            var item = pedidos_json[counter];

            GMaps.geocode({
                address: item._Pedido__terceiro._Terceiro__logradouro
                    + ',' + item._Pedido__terceiro._Terceiro__bairro
                    + ',' + item._Pedido__terceiro._Terceiro__cidade
                    + ' - ' + item._Pedido__terceiro._Terceiro__estado,
                callback: function(results, status) {
                    if (status == 'OK') {
                        var latlng = results[0].geometry.location;
                        locations.push(latlng);
                        
                        map.getRoutes({
                            origin: [origin_lat, origin_lng],
                            destination: [latlng.lat(), latlng.lng()],
                            travelMode: 'driving',
                            callback: function(e) {
                                var route = new GMaps.Route({
                                    map: map,
                                    route: e[0],
                                    strokeColor: '#336699',
                                    strokeOpacity: 0.5,
                                    strokeWeight: 10
                                });
                                routes.push(route);
                                counter++;
                                geolocatePedidos(); // recursive method
                            }
                        });

                        origin_lat = latlng.lat();
                        origin_lng = latlng.lng();

                    } else {
                        locations.push(null);
                        routes.push(null);
                    }
                }
            });
        } else {
            counter=0;
            drawRoutes();
        }
    }

    $.getJSON(
        '/pedidos/', 
        { entidade: $('#my-map').data('entidade'), 'pedidos[]': [pedidos_list] }, 
        function(retorno) {
            if (retorno.length > 0) {
                pedidos_json = retorno;
                $('#instructions li').remove()
                geolocatePedidos();
            }
        }
    );
}