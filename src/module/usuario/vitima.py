from module.usuario.abstractParte import Parte

class Vitima(Parte):
    def __init__(self, id: int, nome: str, cpf: int, data_nascimento: str):
        super().__init__(id= id, nome= nome, cpf= cpf, data_nascimento= data_nascimento)