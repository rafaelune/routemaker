class TokenAcesso(object):
    # get access_token
    @property
    def access_token(self):
        return self.__access_token
    # set access_token
    @access_token.setter
    def access_token(self, access_token):
        self.__access_token = access_token

    # get expires_in
    @property
    def expires_in(self):
        return self.__expires_in
    # set expires_in
    @expires_in.setter
    def expires_in(self, expires_in):
        self.__expires_in = expires_in

    # get refresh_token
    @property
    def refresh_token(self):
        return self.__refresh_token
    # set refresh_token
    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self.__refresh_token = refresh_token

    # get cnpj_empresa
    @property
    def cnpj_empresa(self):
        return self.__cnpj_empresa
    # set cnpj_empresa
    @cnpj_empresa.setter
    def cnpj_empresa(self, cnpj_empresa):
        self.__cnpj_empresa = cnpj_empresa

    # get terceiro_id
    @property
    def terceiro_id(self):
        return self.__terceiro_id
    # set terceiro_id
    @terceiro_id.setter
    def terceiro_id(self, terceiro_id):
        self.__terceiro_id = terceiro_id

    # get terceiro_nome
    @property
    def terceiro_nome(self):
        return self.__terceiro_nome
    # set terceiro_nome
    @terceiro_nome.setter
    def terceiro_nome(self, terceiro_nome):
        self.__terceiro_nome = terceiro_nome