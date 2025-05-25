from abstractDocumento import Documento, Usuario

class Defesa(Documento):
    def __init__(self, id, titulo, descricao, data_envio, autor, reu):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self.__reu = reu

    @property
    def reu(self):
        return self.__reu
    @reu.setter
    def reu(self, reu):
        self.__reu = reu

