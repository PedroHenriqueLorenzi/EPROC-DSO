from usuario import Usuario
from sentenca import Sentenca
class Juiz(Usuario):
    def __init__(self, id, nome):
        super().__init__(id, nome)
        self._processos = []

    def processos(self):
        return self._processos

    def emitir_sentenca(self, processo, conteudo):
        
        sentenca = Sentenca(conteudo, self)
        processo.receber_sentenca(sentenca)
        print(f"Sentença emitida por {self.nome()}: {conteudo}")