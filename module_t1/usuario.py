from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, id, nome):
        self._id = id
        self._nome = nome

    def id(self):
        return self._id
    
    def nome(self):
        return self._nome

    @abstractmethod
    def emitir_sentenca(self, processo, conteudo):
        pass
