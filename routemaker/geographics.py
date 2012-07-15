import urllib3, json

class Location(object):
    def __init__(self, lat, lng):
        self.__lat = lat
        self.__lng = lng
    # get lat
    @property
    def lat(self):
        return self.__lat
    # set lat
    @lat.setter
    def lat(self, lat):
        self.__lat = lat
    # get lng
    @property
    def lng(self):
        return self.__lng
    # set lng
    @lng.setter
    def lng(self, lng):
        self.__lng = lng

class PositionApi(object):
    def get_location_by_address(self, address):
        base_url = 'http://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor=true'
        base_url = base_url.format(address.replace(" ", "+"))
        
        http = urllib3.PoolManager()
        request = http.request('GET', base_url)
        request_location = json.loads(request.data) # Parse JSON
        if request_location['status'] == 'OK':
            location_data = request_location['results'][0]['geometry']['location']
            
            location = Location(location_data['lat'], location_data['lng'])
            return location
        
        return None