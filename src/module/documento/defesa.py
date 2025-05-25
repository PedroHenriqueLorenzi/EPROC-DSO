from abstractDocumento import Documento, Usuario

class Defesa(Documento):
    def __init__(self, id, titulo, descricao, data_envio, autor, parte_defendida: Usuario, advogado_responsavel: Usuario):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self.__parte_defendida = parte_defendida  
        self.__advogado_responsavel = advogado_responsavel  

    def parte_defendida(self):
        return self.__parte_defendida

    def advogado_responsavel(self):
        return self.__advogado_responsavel
