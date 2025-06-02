from src.module.usuario.abstractUsuario import Usuario
from src.module.documento.sentenca import Sentenca
from src.module.arquivamento import Arquivamento
from src.module.documento.audiencia import Audiencia

class Juiz(Usuario):
    def __init__(self, ide: int, nome: str, cpf: int, data_nascimento: str, tribunal_atribuido: str):
        super().__init__(ide= ide, nome= nome, cpf= cpf, data_nascimento= data_nascimento)
        self.__tribunal_atribudio = tribunal_atribuido
        self.__processos = []
        self.__ultima_sentenca = None
        self.__ultimo_arquivamento = None

    @property
    def ide(self):
        return self.__ide
    @ide.setter
    def ide(self, nova_ide):
        if isinstance(nova_ide, int): self.__ide = nova_ide

    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self, novo_nome):
        if isinstance(novo_nome, str): self.__nome = novo_nome

    @property
    def cpf(self):
        return self.__cpf
    @cpf.setter
    def cpf(self, novo_cpf):
        if isinstance(novo_cpf, int): self.__cpf = novo_cpf

    @property
    def data_nascimento(self):
        return self.__data_nascimento
    @data_nascimento.setter
    def data_nascimento(self, nova_data_nascimento):
        if isinstance(nova_data_nascimento, str): self.__data_nascimento = nova_data_nascimento



    #def registrar_movimentacao(self, processo, movimentacao):
        #pass

    def emitir_sentenca(self, sentenca):
        pass

    def emitir_arquivamento(self, arquivamento):
        pass

    def realizar_audiencia(self, audiencia):
        pass