class Pedido(object):
    # get id
    @property
    def id(self):
        return self.__id
    # set id
    @id.setter
    def id(self, id):
        self.__id = id
    # get data
    @property
    def data(self):
        return self.__data
    # set data
    @data.setter
    def data(self, data):
        self.__data = data
    # get numero
    @property
    def numero(self):
        return self.__numero
    # set numero
    @numero.setter
    def numero(self, numero):
        self.__numero = numero
    # get valor_total
    @property
    def valor_total(self):
        return self.__valor_total
    # set valor_total
    @valor_total.setter
    def valor_total(self, valor_total):
        self.__valor_total = valor_total
    # get plano_pagamento
    @property
    def plano_pagamento(self):
        return self.__plano_pagamento
    # set plano_pagamento
    @plano_pagamento.setter
    def plano_pagamento(self, plano_pagamento):
        self.__plano_pagamento = plano_pagamento
    # get representante
    @property
    def representante(self):
        return self.__representante
    # set representante
    @representante.setter
    def representante(self, representante):
        self.__representante = representante
    # get terceiro_id
    @property
    def terceiro_id(self):
        return self.__terceiro_id
    # set terceiro_id
    @terceiro_id.setter
    def terceiro_id(self, terceiro_id):
        self.__terceiro_id = terceiro_id
    # get terceiro
    @property
    def terceiro(self):
        return self.__terceiro
    # set terceiro
    @terceiro.setter
    def terceiro(self, terceiro):
        self.__terceiro = terceiro
    # get items
    @property
    def items(self):
        return self.__items
    # set items
    @items.setter
    def items(self, items):
        self.__items = items