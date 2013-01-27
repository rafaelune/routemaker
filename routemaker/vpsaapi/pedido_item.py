class PedidoItem(object):
	# get id_produto
    @property
    def id_produto(self):
        return self.__id_produto
    # set id_produto
    @id_produto.setter
    def id_produto(self, id_produto):
        self.__id_produto = id_produto
    # get descricao
    @property
    def descricao(self):
        return self.__descricao
    # set descricao
    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao
    # get unidade
    @property
    def unidade(self):
        return self.__unidade
    # set unidade
    @unidade.setter
    def unidade(self, unidade):
        self.__unidade = unidade
    # get quantidade
    @property
    def quantidade(self):
        return self.__quantidade
    # set quantidade
    @quantidade.setter
    def quantidade(self, quantidade):
        self.__quantidade = quantidade