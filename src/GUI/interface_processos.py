import PySimpleGUI as sg

class InterfaceProcessosGUI:
    def __init__(self, controlador):
        self.__controlador = controlador

    def abre_tela(self):
        sg.theme("DarkBlue3")

        layout = [
            [sg.Text("GERENCIAR PROCESSOS", font=("Helvetica", 20), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button("➕  Cadastrar Processo", size=(30, 2))],
            [sg.Button("✏️  Editar Processo", size=(30, 2))],
            [sg.Button("🗑️  Remover Processo", size=(30, 2))],
            [sg.Button("📋  Listar Processos", size=(30, 2))],
            [sg.Button("🔙  Voltar", size=(30, 2))]
        ]

        janela = sg.Window("MiniEPROC - Processos", layout, element_justification="center")

        while True:
            evento, _ = janela.read()
            if evento in (sg.WINDOW_CLOSED, "🔙  Voltar"):
                break
            elif evento == "➕  Cadastrar Processo":
                self._cadastrar_processo()
            elif evento == "✏️  Editar Processo":
                self._editar_processo()
            elif evento == "🗑️  Remover Processo":
                self._remover_processo()
            elif evento == "📋  Listar Processos":
                self._listar_processos()

        janela.close()

    def _cadastrar_processo(self):
        sg.popup("Abrir tela de cadastro de processo (a implementar)")

    def _editar_processo(self):
        sg.popup("Abrir edição de processo (a implementar)")

    def _remover_processo(self):
        sg.popup("Abrir remoção de processo (a implementar)")

    def _listar_processos(self):
        sg.popup("Abrir listagem de processos (a implementar)")