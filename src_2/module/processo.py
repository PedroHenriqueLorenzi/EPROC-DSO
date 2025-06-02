#processo

from src.module.usuario.juiz import Juiz
from src.module.usuario.advogado import Advogado
from src.module.usuario.promotor import Promotor
from src.module.usuario.reu import Reu
from src.module.usuario.vitima import Vitima
from src.module.tribunal import Tribunal

from src.module.documento.acusacao import Acusacao
from src.module.documento.defesa import Defesa
from src.module.documento.audiencia import Audiencia
from src.module.documento.sentenca import Sentenca

from src.module.arquivamento import Arquivamento


class Processo:
    def __init__(self, numero_processo: int, data_abertura_processo: str, juiz_responsavel: Juiz, promotor_responsavel, tribunal_responsavel):
        self.__numero_processo = numero_processo
        self.__data_abertura_processo = data_abertura_processo

        self.__promotor_responsavel = promotor_responsavel
        self.__juiz_responsavel = juiz_responsavel
        self.__arquivamento = None
        self.__processo_encerrado = False
        self.__advogados = []
        self.__partes = []
        self.__documentos = []
        self.__tribunal_responsavel = tribunal_responsavel
        #self.__movimentacoes = []

    @property
    
    @.setter

    @property
    
    @.setter

    @property
    
    @.setter

    @property
    
    @.setter

    @property
    
    @.setter

    def adicionar_reu(self, reu):
        if isinstance(reu, Reu) and not self.__processo_encerrado: self.__partes.append(reu)

    def adicionar_vitima(self, vitima):
        if isinstance(vitima, Vitima) and not self.__processo_encerrado: self.__partes.append(vitima)

    def adicionar_advogado(self, advogado):
        if isinstance(advogado, Advogado) and not self.__processo_encerrado: self.__advogados.append(advogado)

    def trocar_juiz_responsavel(self, juiz): ####
        if isinstance(juiz, Juiz) and not self.__processo_encerrado: self.__juiz_responsavel = juiz

    def trocar_promotor_responsavel(self, promotor): ####
        if isinstance(promotor, Promotor) and not self.__processo_encerrado: self.__promotor_responsavel = promotor

    def trocar_tribunal_responsavel(self, tribunal): ####
        if isinstance(tribunal, Tribunal) and not self.__processo_encerrado: self.__tribunal_responsavel = tribunal




    def adicionar_acusacao(self, acusacao):
        if isinstance(acusacao, Acusacao) and not self.__processo_encerrado: self.__documentos.append(acusacao)

    def adicionar_audiencia(self, audiencia):
        if isinstance(audiencia, Audiencia) and not self.__processo_encerrado: self.__documentos.append(audiencia)

    def adicionar_defesa(self, defesa):
        if isinstance(defesa, Defesa) and not self.__processo_encerrado: self.__documentos.append(defesa)

    #def registrar_movimentacao(self, movimentacao):
        #pass

    def adicionar_sentenca(self, sentenca):
        if isinstance(sentenca, Sentenca) and not self.__processo_encerrado: self.__documentos.append(sentenca)



    def adicionar_arquivamento(self, arquivamento):
        if isinstance(arquivamento, Arquivamento) and not self.__processo_encerrado:
            self.__arquivamento.append(arquivamento)
            self.__processo_encerrado = True