from abstractDocumento import Documento, Usuario

class Audiencia(Documento):
    def __init__(self, ide, titulo, descricao, data_envio, autor: Usuario, conteudo, juiz_responsavel: Juiz):
        super().__init__(ide, titulo, descricao, data_envio, autor, conteudo)
        self.__juiz_responsavel = juiz_responsavel 
        self.__partes_envolvidas = [] 
    
    @property
    def juiz_responsavel(self):
        return self.__juiz_responsavel
    
    @juiz_responsavel.setter
    def juiz_responsavel(self, juiz_responsavel: Usuario):
        self.__juiz_responsavel = juiz_responsavel
    
    @property
    def partes_envolvidas(self):
        return self.__partes_envolvidas
