from module.documento.abstractDocumento import Documento

class Sentenca(Documento):
    def __init__(self, id, titulo, descricao, data_envio, autor, reu, vitima):
        super().__init__(id, titulo, descricao, data_envio, autor)  
        self.__reu = reu
        self.__vitima = vitima          

    @property
    def reu(self):
        return self.__reu
    @reu.setter
    def reu(self, reu):
        self.__reu = reu

    @property
    def vitima(self):
        return self.__vitima
    @vitima.setter
    def vitima(self, vitima):
        self.__vitima = vitima