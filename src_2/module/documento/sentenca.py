from abstractDocumento import Documento, Usuario

class Sentenca(Documento):
    def __init__(self, ide, titulo, descricao, data_envio, autor, conteudo, reu, vitima):
        super().__init__(ide, titulo, descricao, data_envio, autor, conteudo)  
        self.__reu = reu
        self.__vitima = vitima          
