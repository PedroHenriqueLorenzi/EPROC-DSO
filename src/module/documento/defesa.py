from abstractDocumento import Documento, Usuario

class Defesa(Documento):
    def __init__(self, ide, titulo, descricao, data_envio, autor, conteudo, reu):
        super().__init__(ide, titulo, descricao, data_envio, autor, conteudo)
        self.__reu = reu
