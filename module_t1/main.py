# main.py
from juiz import Juiz
from processo import Processo

if __name__ == "__main__":
    juiz = Juiz(1, "Dr. Carlos")
    processo = Processo("0001/2025", juiz)

    processo.exibir()
    juiz.emitir_sentenca(processo, "Condenado a 2 anos de prisão.")
    processo.exibir()