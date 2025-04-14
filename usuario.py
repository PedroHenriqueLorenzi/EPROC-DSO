#usuario

from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, ide: int, nome: str, cpf: int, data_nascimento: str):
        self.__ide = ide
        self.__nome = nome
        self.__cpf = cpf
        self.__data_nascimento = data_nascimento


    #getters e setters....


    @abstractmethod
    def registrar_movimentacao(self, processo, movimentacao):
        pass

    @abstractmethod
    def adicionar_documento(self, documento):
        pass

    @abstractmethod
    def emitir_sentenca(self, processo, conteudo):
        pass