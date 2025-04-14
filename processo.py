#processo

class Processo:
    def __init__(self, numero_processo: str, data_abertura_processo: int, juiz_responsavel):
        self.__numero_processo = numero_processo
        self.__data_abertura_processo = data_abertura_processo
        self.__juiz_responsavel = juiz_responsavel
        self.__processo_encerrado = False
        self.__advogados = []
        self.__partes = []
        self.__documentos = []
        self.__movimentacoes = []
        if self.__processo_encerrado == False:
            self.__sentenca = None


    #setters e getters...

    def adicionar_parte(self, parte):
        pass

    def adicionar_advogado(self, advogado):
        pass

    def adicionar_documento(self, documento):
        pass

    def registrar_movimentacao(self, movimentacao):
        pass

    def emitir_sentenca(self, sentenca):
        pass

    def encerrar_processo(self):
        if self.__processo_encerrado == False: self.__processo_encerrado = True
