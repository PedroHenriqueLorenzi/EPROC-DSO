from module.usuario.abstractUsuario import Usuario

class Parte(Usuario):
    def __init__(self, id: int, nome: str, cpf: int, data_nascimento: str):
        super().__init__(id= id, nome= nome, cpf= cpf, data_nascimento= data_nascimento)