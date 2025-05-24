#advogado

from src.module.usuario.abstractUsuario import Usuario

class Advogado(Usuario):
    def __init__(self, ide: int, nome: str, cpf: int, data_nascimento: str, oab: str):
        super().__init__(ide= ide, nome= nome, cpf= cpf, data_nascimento= data_nascimento)
        self.__oab = oab
        self.__processos = []


    #getters e setters...


    def registrar_movimentacao(self, processo, movimentacao):
        pass

    def adicionar_documento(self, documento):
        pass