import PySimpleGUI as sg
from src.controller.controladorSistema import ControladorSistema

def interface_principal():
    sg.theme("DarkBlue")

    controlador = ControladorSistema()

    layout = [
        [sg.Text("=== SISTEMA MINI-EPROC ===", font=("Helvetica", 16))],
        [sg.Button("Gerenciar Usuários", size=(25, 2))],
        [sg.Button("Gerenciar Processos", size=(25, 2))],
        [sg.Button("Sair", size=(25, 2))]
    ]

    janela = sg.Window("MiniEPROC - Menu Principal", layout)

    while True:
        evento, valores = janela.read()
        if evento == sg.WINDOW_CLOSED or evento == "Sair":
            break
        elif evento == "Gerenciar Usuários":
            janela.hide()
            controlador.controlador_usuarios.abre_tela()
            janela.un_hide()
        elif evento == "Gerenciar Processos":
            janela.hide()
            controlador.controlador_processos.abre_tela()
            janela.un_hide()

    janela.close()

if __name__ == "__main__":
    interface_principal()