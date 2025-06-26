from DAOs.abstractDAO import AbstractDAO

class ProcessoDAO(AbstractDAO):
    def __init__(self):
        super().__init__('processos.pkl')
