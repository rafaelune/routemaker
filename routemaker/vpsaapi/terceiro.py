class Terceiro(object):
    def __init__(self):
        self.__geolocated = False

    # get id
    @property
    def id(self):
        return self.__id
    # set id
    @id.setter
    def id(self, id):
        self.__id = id
    # get identificacao
    @property
    def identificacao(self):
        return self.__identificacao
    # set identificacao
    @identificacao.setter
    def identificacao(self, identificacao):
        self.__identificacao = identificacao
    # get nome
    @property
    def nome(self):
        return self.__nome
    # set nome
    @nome.setter
    def nome(self, nome):
        self.__nome = nome
    # get email
    @property
    def email(self):
        return self.__email
    # set email
    @email.setter
    def email(self, email):
        self.__email = email
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
    # get cidade
    @property
    def cidade(self):
        return self.__cidade
    # set cidade
    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade
    # get estado
    @property
    def estado(self):
        return self.__estado
    # set estado
    @estado.setter
    def estado(self, estado):
        self.__estado = estado
    # get bairro
    @property
    def bairro(self):
        return self.__bairro
    # set bairro
    @bairro.setter
    def bairro(self, bairro):
        self.__bairro = bairro
    # get logradouro
    @property
    def logradouro(self):
        return self.__logradouro
    # set logradouro
    @logradouro.setter
    def logradouro(self, logradouro):
        self.__logradouro = logradouro
    # get geolocated
    @property
    def geolocated(self):
        return self.__geolocated
    # set geolocated
    @geolocated.setter
    def geolocated(self, geolocated):
        self.__geolocated = geolocated

    def set_geolocation(self, lat, lng):
        if lat != None and lng != None:
            self.__geolocated = True

        self.__lat = lat
        self.__lng = lng

    def get_full_address(self):
        return '{0}, {1}, {2}-{3}'.format(
            self.logradouro,
            self.bairro,
            self.cidade,
            self.estado
        )