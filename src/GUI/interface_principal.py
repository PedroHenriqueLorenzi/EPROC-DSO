import PySimpleGUI as sg

class InterfacePrincipalGUI:
    def __init__(self, controlador):
        self.__controlador = controlador

    def abre_tela(self):
        sg.theme("DarkBlue3")

        layout = [
            [sg.Text("SISTEMA MINI-EPROC", font=("Helvetica", 20), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button("👤  Gerenciar Usuários", key="usuarios", size=(30, 2), font=("Helvetica", 12)), sg.Push()],
            [sg.Push(), sg.Button("📂  Gerenciar Processos", key="processos", size=(30, 2), font=("Helvetica", 12)), sg.Push()],
            [sg.Push(), sg.Button("❌  Sair", key="sair", size=(30, 2), font=("Helvetica", 12)), sg.Push()]
        ]

        janela = sg.Window("MiniEPROC - Menu Principal", layout, element_justification="center")

        while True:
            evento, _ = janela.read()
            janela.close()

            if evento in (sg.WINDOW_CLOSED, "sair"):
                return "sair"
            elif evento == "usuarios":
                return "usuarios"
            elif evento == "processos":
                return "processos"
