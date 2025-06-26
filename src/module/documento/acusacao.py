from src.module.documento.abstractDocumento import Documento

class Acusacao(Documento):

    def __init__(self, id, titulo, descricao, data_envio, autor, vitima):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self.__vitima = vitima

    @property
    def vitima(self):
        return self.__vitima
    
    @vitima.setter
    def vitima(self, vitima):
        self.__vitima = vitima


