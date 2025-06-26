from src.module.documento.abstractDocumento import Documento
from src.module.usuario.abstractUsuario import Usuario
from src.module.usuario.juiz import Juiz

class Audiencia(Documento):
    def __init__(self, id, titulo, descricao, data_envio, autor: Usuario, juiz_responsavel: Juiz, data):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self.__juiz_responsavel = juiz_responsavel
        self.__data = data
        self.__partes_envolvidas = []


    @property
    def juiz_responsavel(self):
        return self.__juiz_responsavel

    @juiz_responsavel.setter
    def juiz_responsavel(self, juiz_responsavel: Usuario):
        self.__juiz_responsavel = juiz_responsavel

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, nova_data):
        self.__data = nova_data

    @property
    def partes_envolvidas(self):
        return self.__partes_envolvidas

    def adicionar_parte(self, parte):
        self.__partes_envolvidas.append(parte)