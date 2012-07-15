// Requires gmaps.js, google maps api and geoip.js framework to works
var Mapper = function() {
    var self = this;
    
    var _mapContainer = '';
    var _startLatitude = -23.17908;
    var _startLongitude = -45.887248;
    var _map;

    this.getMap = function() {
        return _map;
    }

    this.getStartLatitude = function() {
        return _startLongitude;
    }

    this.getStartLongitude = function() {
        return _startLongitude;
    }
    
    this.getUserPosition = function() {
        
        GMaps.geolocate({
            success: function(position) {
                self.setCenter(position.coords.latitude, position.coords.longitude);
            },
            error: function(error) {
                // use MaxMind IP to location API fallback
                self.setCenter(geoip_latitude(), geoip_longitude());
            },
            not_supported: function() {
                // use MaxMind IP to location API fallback
                self.setCenter(geoip_latitude(), geoip_longitude());
            }
        });
        
    }

    this.setCenter = function(latitude, longitude) {

        if (_map != null) {
            _startLatitude = latitude;
            _startLongitude = longitude;

            // inits the map
            _map = new GMaps({
                div: _mapContainer,
                lat: _startLatitude,
                lng: _startLongitude
            });

        }

    }
    
    this.startMap = function(mapContainer) {
    
        _mapContainer = mapContainer; // saves the mapContainer, '# map for example

        // inits the map
        _map = new GMaps({
            div: _mapContainer,
            lat: _startLatitude,
            lng: _startLongitude
        });

        // try to get user position
        self.getUserPosition();
    }

    this.drawRoute = function(starts, ends, instructionsContainer) {
        _map.travelRoute({
          //origin: [-12.044012922866312, -77.02470665341184],
          //destination: [-12.090814532191756, -77.02271108990476],
          origin: starts,
          destination: ends,
          travelMode: 'driving',
          step: function(e) {

            //$('#instructions').append('<li>'+e.instructions+'</li>');
            $(instructionsContainer).append('<li>'+e.instructions+'</li>');
            
            //$('#instructions li:eq(' + e.step_number + ')').delay(450 * e.step_number).fadeIn(200, function() {
            $(instructionsContainer + ' li:eq(' + e.step_number + ')').delay(450 * e.step_number).fadeIn(200, function() {
              _map.drawPolyline({
                path: e.path,
                strokeColor: '#131540',
                strokeOpacity: 0.6,
                strokeWeight: 6
              });  
            });
          }
        });
    }

}

var mapper = new Mapper();