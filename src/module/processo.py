#processo

class Processo:
    def __init__(self, numero_processo: str, data_abertura_processo: str, juiz_responsavel, MP):
        self.__numero_processo = numero_processo
        self.__data_abertura_processo = data_abertura_processo
        #MP
        self.__juiz_responsavel = juiz_responsavel
        self.__processo_encerrado = False
        self.__advogados = []
        self.__partes = []
        self.__documentos = []
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
        pass

    def adicionar_vitima(self, vitima):
        pass

    def adicionar_advogado(self, advogado):
        pass

    def trocar_juiz_responsavel(self, juiz):
        pass

    def adicionar_acusacao(self, documento):
        pass

    def adicionar_audiencia(self, audiencia):
        pass

    def adicionar_defesa(self, defesa):
        pass

    #def registrar_movimentacao(self, movimentacao):
        #pass

    def adicionar_sentenca(self, sentenca):
        pass

    def adicionar_arquivamento(self):
        pass
