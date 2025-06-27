import PySimpleGUI as sg

def tela_documentos():
    sg.theme("DarkBlue")

    layout = [
        [sg.Text("Gerenciar Documentos", font=("Helvetica", 16))],
        [sg.Button("Cadastrar Documento", size=(25, 2))],
        [sg.Button("Listar Documentos", size=(25, 2))],
        [sg.Button("Voltar", size=(25, 2))]
    ]

    janela = sg.Window("MiniEPROC - Documentos", layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WINDOW_CLOSED or evento == "Voltar":
            break
        elif evento == "Cadastrar Documento":
            sg.popup("Abrir tela de cadastro de documento (a implementar)")
        elif evento == "Listar Documentos":
            sg.popup("Abrir listagem de documentos (a implementar)")

    janela.close()

if __name__ == "__main__":
    tela_documentos()