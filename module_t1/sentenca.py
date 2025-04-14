class Sentenca:
    def __init__(self, conteudo, juiz):
        self._conteudo = conteudo
        self._juiz = juiz

    def conteudo(self):
        return self._conteudo

    def juiz(self):
        return self._juiz