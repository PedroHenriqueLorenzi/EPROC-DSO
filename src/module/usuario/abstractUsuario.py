from abc import ABC, abstractmethod

class Usuario(ABC):
    @abstractmethod
    def __init__(self, ide: int, nome: str, cpf: int, data_nascimento: str):
        self.__ide = ide
        self.__nome = nome
        self.__cpf = cpf
        self.__data_nascimento = data_nascimento

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


    def realizar_audiencia(self, audiencia):
        pass



    #@abstractmethod
    #def registrar_movimentacao(self, processo, movimentacao):
        #pass

    @abstractmethod
    def apresentar_defesa(self, defesa):
        pass

    @abstractmethod
    def emitir_acusacao(self, acusacao):
        pass

    @abstractmethod
    def emitir_sentenca(self, processo):
        pass



    @abstractmethod
    def emitir_arquivamento(self, arquivamento):
        pass