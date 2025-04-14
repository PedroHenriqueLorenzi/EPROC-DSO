#usuario

from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, ide: int, nome: str, cpf: int, data_nascimento: int):
        self.__ide = ide
        self.__nome = nome
        self.__cpf = cpf
        self.__data_nasciemnto = data_nascimento


    #setters e getters....


    @abstractmethod
    def registrar_movimentacao(self, processo, movimentacao):
        pass

    @abstractmethod
    def adcicionar_documento(self, documento):
        pass

    @abstractmethod
    def emitir_sentenca(processo, conteudo):
        pass