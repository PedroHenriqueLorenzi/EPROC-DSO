class Tribunal:
    def __init__(self, ide, nome, localidade, atribuicao, instancia):
        self.__ide = ide
        self.__nome = nome
        self.__localidade = localidade
        self.__atribuicao = atribuicao
        self.__instancia = instancia

    @property
    def ide(self):
        return self.__ide
    @ide.setter
    def ide(self, nova_ide: int):
        if isinstance(nova_ide, int): self.__ide = nova_ide

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
    def descricao(self, nova_atribucao):
        if isinstance(nova_atribucao, str): self.__atribuicao = nova_atribucao