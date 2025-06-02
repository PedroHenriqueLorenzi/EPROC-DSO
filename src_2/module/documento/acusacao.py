from abstractDocumento import Documento, Usuario

class Acusacao(Documento):

    def __init__(self, ide, titulo, descricao, data_envio, autor, conteudo, vitima):
        super().__init__(ide, titulo, descricao, data_envio, autor, conteudo)
        self.__vitima = vitima

