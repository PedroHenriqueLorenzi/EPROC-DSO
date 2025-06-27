import PySimpleGUI as sg

class InterfaceDocumentosGUI:
    def __init__(self, controlador):
        self.__controlador = controlador

    def abre_tela(self):
        sg.theme("DarkBlue3")

        layout = [
            [sg.Text("GERENCIAR DOCUMENTOS", font=("Helvetica", 20), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button("➕  Adicionar Documento", size=(30, 2))],
            [sg.Button("✏️  Editar Documento", size=(30, 2))],
            [sg.Button("🗑️  Remover Documento", size=(30, 2))],
            [sg.Button("📋  Listar Documentos", size=(30, 2))],
            [sg.Button("🔍  Buscar Documento", size=(30, 2))],
            [sg.Button("🔙  Voltar", size=(30, 2))]
        ]

        janela = sg.Window("MiniEPROC - Documentos", layout, element_justification="center")

        while True:
            evento, _ = janela.read()

            if evento in (sg.WINDOW_CLOSED, "🔙  Voltar"):
                break
            elif evento == "➕  Adicionar Documento":
                self._adicionar_documento()
            elif evento == "✏️  Editar Documento":
                self._editar_documento()
            elif evento == "🗑️  Remover Documento":
                self._remover_documento()
            elif evento == "📋  Listar Documentos":
                self._listar_documentos()
            elif evento == "🔍  Buscar Documento":
                self._buscar_documento()

        janela.close()

    def _adicionar_documento(self):
        sg.popup("Abrir formulário de novo documento (a implementar)")

    def _editar_documento(self):
        sg.popup("Abrir edição de documento (a implementar)")

    def _remover_documento(self):
        sg.popup("Abrir remoção de documento (a implementar)")

    def _listar_documentos(self):
        sg.popup("Listagem de todos os documentos (a implementar)")

    def _buscar_documento(self):
        sg.popup("Tela de busca por documento (a implementar)")