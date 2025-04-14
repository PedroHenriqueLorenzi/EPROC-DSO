class Processo:
    def __init__(self, numero, juiz):
        self._numero = numero
        self._juiz = juiz
        self._sentenca = None

    def numero(self):
        return self._numero

    def juiz_responsavel(self):
        return self._juiz

    def receber_sentenca(self, sentenca):
        self._sentenca = sentenca

    def exibir(self):
        print(f"Processo {self._numero}")
        if self._sentenca:
            print(f"Sentença: {self._sentenca.conteudo()} (Juiz: {self._sentenca.juiz().nome()})")
        else:
            print("Ainda sem sentença.")