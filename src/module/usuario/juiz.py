from src.module.usuario.abstractUsuario import Usuario

class Juiz(Usuario):
    def __init__(self, ide: int, nome: str, cpf: int, data_nascimento: str, tribunal_atribuido: str):
        super().__init__(ide= ide, nome= nome, cpf= cpf, data_nascimento= data_nascimento)
        self.__tribunal_atribudio = tribunal_atribuido
        self.__processos = []


    #getters e setters...


    def registrar_movimentacao(self, processo, movimentacao):
        pass

    def adicionar_documento(self, documento):
        pass

    def emitir_sentenca(self, processo, conteudo):
        pass