#documento

class Documento:
    def __init__(self, ide: int, titulo: str, descricao: str, data_envio: str, autor):
        self.__ide = ide
        self.__titulo = titulo
        self.__descricao = descricao
        self.__data_envio = data_envio
        self.__autor = autor


    #getters e setters....