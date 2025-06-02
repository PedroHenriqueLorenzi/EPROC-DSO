from module.usuario.abstractUsuario import Usuario

class Promotor(Usuario):
    def __init__(self, id: int, nome: str, cpf: int, data_nascimento: str, area_atuacao):
        super().__init__(id= id, nome= nome, cpf= cpf, data_nascimento= data_nascimento)
        self.__area_atuacao = area_atuacao
