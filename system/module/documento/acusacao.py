from abstractDocumento import Documento, Usuario

class Acusacao(Documento):

    def __init__(self, id, titulo, descricao, data_envio, autor, parte_ativa: Usuario, advogado_responsavel: Usuario):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self.__parte_ativa = parte_ativa
        self.__advogado_responsavel = advogado_responsavel

    @property 
    def parte_ativa(self):
        return self.__parte_ativa
    
    @property 
    def advogado_responsavel(self):
        return self.__advogado_responsavel
    
    

    

