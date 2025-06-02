from module.usuario.abstractUsuario import Usuario

class Advogado(Usuario):
    def __init__(self, id: int, nome: str, cpf: int, data_nascimento: str, oab: str):
        super().__init__(id= id, nome= nome, cpf= cpf, data_nascimento= data_nascimento)
        self.__oab = oab
        
    @property
    def oab(self):
        return self.__oab

    @oab.setter
    def oab(self, novo_oab):
        if isinstance(novo_oab, int):
            self.__oab = novo_oab
