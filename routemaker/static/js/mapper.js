// Requires gmaps.js, google maps api and geoip.js framework to works
var Mapper = function() {
    var self = this;
    
    _mapContainer = '';
    _startLatitude = 0;
    _startLongitude = 0;
    
    this.getUserPosition = function(mapContainer) {
        _mapContainer = mapContainer;
        
        GMaps.geolocate({
            success: function(position) {
                self.startMap(position.coords.latitude, position.coords.longitude);
            },
            error: function(error) {
                // use MaxMind IP to location API fallback
                self.startMap(geoip_latitude(), geoip_longitude());
            },
            not_supported: function() {
                // use MaxMind IP to location API fallback
                self.startMap(geoip_latitude(), geoip_longitude());
            }
        });
        
    }
    
    this.startMap = function(latitude, longitude) {
        map = new GMaps({
            div: _mapContainer, //'#map',
            lat: latitude,
            lng: longitude
        });
        
        _startLatitude = latitude;
        _startLongitude = longitude;
    }
}

var mapper = new Mapper();