from module.documento.abstractDocumento import Documento

class Arquivamento(Documento):
    def __init__(self, id, titulo, descricao, data_envio, autor, motivo):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self.__motivo = motivo

    @property
    def motivo(self):
        return self.__motivo

    @motivo.setter
    def motivo(self, novo_motivo):
        self.__motivo = novo_motivo
