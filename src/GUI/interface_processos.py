import PySimpleGUI as sg

def tela_processos():
    sg.theme("DarkBlue")

    layout = [
        [sg.Text("Gerenciar Processos", font=("Helvetica", 16))],
        [sg.Button("Cadastrar Processo", size=(25, 2))],
        [sg.Button("Listar Processos", size=(25, 2))],
        [sg.Button("Voltar", size=(25, 2))],
    ]

    janela = sg.Window("MiniEPROC - Processos", layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WINDOW_CLOSED or evento == "Voltar":
            break
        elif evento == "Cadastrar Processo":
            sg.popup("Abrir tela de cadastro de processo (a implementar)")
        elif evento == "Listar Processos":
            sg.popup("Abrir listagem de processos (a implementar)")

    janela.close()

if __name__ == "__main__":
    tela_processos()