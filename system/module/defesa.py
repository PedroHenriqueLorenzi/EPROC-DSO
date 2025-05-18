from abstractDocumento import Documento, Usuario

class Defesa(Documento):
    def __init__(self, id, titulo, descricao, data_envio, autor, parte_defendida, advogado_responsavel):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self._parte_defendida = parte_defendida  
        self._advogado_responsavel = advogado_responsavel  

    def parte_defendida(self):
        return self._parte_defendida

    def advogado_responsavel(self):
        return self._advogado_responsavel
    
    
    

    

