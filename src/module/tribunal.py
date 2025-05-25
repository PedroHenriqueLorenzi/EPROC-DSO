class Tribunal:
    def __init__(self, id, nome, localidade, atribuicao, instancia):
        self.__id = id
        self.__nome = nome
        self.__localidade = localidade
        self.__atribuicao = atribuicao
        self.__instancia = instancia

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, nova_id: int):
        if isinstance(nova_id, int): self.__id = nova_ide

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, novo_nome):
        if isinstance(novo_nome, str): self.__nome = novo_nome

    @property
    def localidade(self):
        return self.__localidade
    @localidade.setter
    def localidade(self, nova_localidade):
        if isinstance(nova_localidade, str): self.__localidade = nova_localidade

    @property
    def atribuicao(self):
        return self.__atribuicao
    @atribuicao.setter
    def atribuicao(self, nova_atribucao):
        if isinstance(nova_atribucao, str): self.__atribuicao = nova_atribucao
    
    @property
    def instancia(self):
        return self.__instancia
    @instancia.setter
    def instancia(self, nova_instancia):
        if isinstance(nova_instancia, str): self.__instancia = nova_instancia