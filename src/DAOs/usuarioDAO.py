from DAOs.abstractDAO import AbstractDAO

class UsuarioDAO(AbstractDAO):
    def __init__(self):
        super().__init__('users.pkl')