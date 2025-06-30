from datetime import date
from module.documento.arquivamento import Arquivamento

from module.documento.audiencia import Audiencia
from module.documento.sentenca import Sentenca


class Processo:
    def __init__(self, numero: int, data_abertura: str, status: str, juiz_responsavel, advogados, partes, tribunal):
        self.__numero = numero
        self.__data_abertura = data_abertura
        self.__status = status
        self.__juiz_responsavel = juiz_responsavel
        self.__advogados = advogados or []
        self.__partes = partes or []
        self.__documentos = []
        self.__tribunal = tribunal
        self.__arquivamento = None

    @property
    def numero(self):
        return self.__numero

    @property
    def status(self):
        return self.__status

    @property
    def juiz_responsavel(self):
        return self.__juiz_responsavel

    @property
    def tribunal(self):
        return self.__tribunal

    @property
    def documentos(self):
        return self.__documentos

    @property
    def partes(self):
        return self.__partes

    @property
    def advogados(self):
        return self.__advogados
    
    @status.setter
    def status(self, novo_status):
        self.__status = novo_status

    @property
    def data_abertura(self):
        return self.__data_abertura

    def adicionar_documento(self, doc):
        self.__documentos.append(doc)

    def adicionar_parte(self, parte):
        self.__partes.append(parte)

    def adicionar_advogado(self, advogado):
        self.__advogados.append(advogado)
    
    def remover_advogado(self, advogado):
        if advogado in self.__advogados:
            self.__advogados.remove(advogado)
            
    def remover_parte(self, parte):
        if parte in self.__partes:
            self.__partes.remove(parte)

    def encerrar(self, motivo="Encerramento do processo."):
        if not any(isinstance(d, Audiencia) for d in self.documentos):
            raise ValueError("Não é possível encerrar o processo sem uma audiência.")

        if not any(isinstance(d, Sentenca) for d in self.documentos):
            raise ValueError("Não é possível encerrar o processo sem uma sentença.")

        arquivamento = Arquivamento(
            id=len(self.documentos) + 1,
            titulo=f"Arquivamento do processo {self.numero}",
            descricao=motivo,
            data_envio=date.today().isoformat(),
            autor=self.juiz_responsavel,
            motivo=motivo
        )

        self.adicionar_documento(arquivamento)
        self.status = "Encerrado"
        self.__arquivamento = arquivamento
