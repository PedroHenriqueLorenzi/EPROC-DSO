from module.usuario.abstractUsuario import Usuario

class Juiz(Usuario):
    def __init__(self, id: int, nome: str, cpf: int, data_nascimento: str, tribunal_atribuido: str):
        super().__init__(id= id, nome= nome, cpf= cpf, data_nascimento= data_nascimento)
      