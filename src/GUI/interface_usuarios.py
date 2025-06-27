import PySimpleGUI as sg
from datetime import datetime

class InterfaceUsuariosGUI:
    def __init__(self, controlador):
        self.__controlador = controlador

    def abre_tela(self):
        sg.theme("DarkBlue3")

        layout = [
            [sg.Text("GERENCIAR USUÁRIOS", font=("Helvetica", 20), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Button("➕  Cadastrar Usuário", size=(30, 2))],
            [sg.Button("✏️  Editar Usuário", size=(30, 2))],
            [sg.Button("🗑️  Remover Usuário", size=(30, 2))],
            [sg.Button("📋  Listar Usuários", size=(30, 2))],
            [sg.Button("📈  Relatórios", size=(30, 2))],
            [sg.Button("🔙  Voltar", size=(30, 2))]
        ]

        janela = sg.Window("MiniEPROC - Usuários", layout, element_justification="center")

        while True:
            evento, _ = janela.read()

            if evento in (sg.WINDOW_CLOSED, "🔙  Voltar"):
                break
            elif evento == "➕  Cadastrar Usuário":
                self._cadastrar_usuario()
            elif evento == "✏️  Editar Usuário":
                self._editar_usuario()
            elif evento == "🗑️  Remover Usuário":
                self._remover_usuario()
            elif evento == "📋  Listar Usuários":
                self._listar_usuarios()
            elif evento == "📈  Relatórios":
                self._relatorios()

        janela.close()


    def _cadastrar_usuario(self):
        layout = [
            [sg.Text("Nome:"), sg.Input(key="nome")],
            [sg.Text("CPF (somente números, 11 dígitos):"), sg.Input(key="cpf", size=(20,1), enable_events=True)],
            [sg.Text("", key="cpf_status", size=(30,1), text_color="yellow")],
            [sg.Text("Data de Nascimento (DD-MM-AAAA):"), sg.Input(key="nascimento")],
            [sg.Text("Tipo:")],
            [sg.Radio("Juiz", "TIPO_USUARIO", key="tipo_juiz", enable_events=True),
             sg.Radio("Advogado", "TIPO_USUARIO", key="tipo_advogado", enable_events=True),
             sg.Radio("Parte", "TIPO_USUARIO", key="tipo_parte", enable_events=True)],
            [sg.Text("OAB (somente para Advogados):"), sg.Input(key="oab", visible=False)],
            [sg.Submit("Salvar"), sg.Cancel("Cancelar")]
        ]

        window = sg.Window("Cadastrar Usuário", layout, finalize=True)
        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, "Cancelar"):
                break

            if event == "cpf":
                texto = values["cpf"]
                if len(texto) > 11:
                    window["cpf"].update(texto[:11])
                elif len(texto) == 11:
                    window["cpf_status"].update("✔ CPF completo")
                else:
                    window["cpf_status"].update(f"{11 - len(texto)} dígito(s) faltando")

            if event in ("tipo_juiz", "tipo_advogado", "tipo_parte"):
                window["oab"].update(visible=values.get("tipo_advogado", False))

            if event == "Salvar":
                try:
                    nome = values["nome"].strip()
                    cpf = values["cpf"].strip()
                    nascimento = values["nascimento"].strip()
                    oab = values.get("oab", "").strip()

                    tipo = "Juiz" if values.get("tipo_juiz") else "Advogado" if values.get("tipo_advogado") else "Parte"

                    if len(cpf) != 11 or not cpf.isdigit():
                        sg.popup_error("CPF deve conter 11 dígitos numéricos.")
                        continue

                    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

                    try:
                        datetime.strptime(nascimento, "%d-%m-%Y")
                    except ValueError:
                        sg.popup_error("Data de nascimento deve estar no formato DD-MM-AAAA.")
                        continue

                    args = [nome, cpf_formatado, nascimento, tipo]
                    if tipo == "Advogado":
                        args.append(oab)

                    self.__controlador.criar_usuario(*args)
                    sg.popup_ok("Usuário cadastrado com sucesso!")
                    break
                except Exception as e:
                    sg.popup_error(f"Erro ao cadastrar: {str(e)}")
        window.close()

    def _editar_usuario(self):
        id_str = sg.popup_get_text("Digite o ID do usuário a editar:")
        if not id_str or not id_str.isdigit():
            sg.popup_error("ID inválido.")
            return
        usuario = self.__controlador.buscar_usuario_por_id(int(id_str))
        if not usuario:
            sg.popup("Usuário não encontrado.")
            return

        layout = [
            [sg.Text("Nome:"), sg.Input(default_text=usuario.nome, key="nome")],
            [sg.Text("Nascimento (DD-MM-AAAA):"), sg.Input(default_text=usuario.data_nascimento, key="nascimento")]
        ]

        if usuario.__class__.__name__.lower() == "advogado":
            layout.append([sg.Text("OAB:"), sg.Input(default_text=getattr(usuario, "oab", ""), key="oab")])

        layout.append([sg.Submit("Salvar"), sg.Cancel("Cancelar")])

        window = sg.Window("Editar Usuário", layout)
        event, values = window.read()
        if event == "Salvar":
            nome = values["nome"].strip()
            nascimento = values["nascimento"].strip()
            oab = values.get("oab", "").strip()
            try:
                self.__controlador.editar_usuario(usuario.id, nome, nascimento, oab)
                sg.popup("Usuário atualizado com sucesso.")
            except Exception as e:
                sg.popup_error(f"Erro ao atualizar: {str(e)}")
        window.close()

    def _remover_usuario(self):
        id_str = sg.popup_get_text("Digite o ID do usuário a remover:")
        if not id_str or not id_str.isdigit():
            sg.popup_error("ID inválido.")
            return
        usuario = self.__controlador.buscar_usuario_por_id(int(id_str))
        if not usuario:
            sg.popup("Usuário não encontrado.")
            return
        confirm = sg.popup_yes_no(f"Confirma a remoção de {usuario.nome}?")
        if confirm == "Yes":
            self.__controlador.remover_usuario(usuario.id)
            sg.popup("Usuário removido com sucesso.")

    def _listar_usuarios(self):
        usuarios = self.__controlador.get_todos_usuarios()
        if not usuarios:
            sg.popup("Nenhum usuário cadastrado.")
            return
        linhas = [f"{u.id} - {u.nome} ({u.__class__.__name__})" for u in usuarios]
        sg.popup_scrolled("\n".join(linhas), title="Usuários Cadastrados")

    def _relatorios(self):
        tipos = ["Juiz", "Advogado", "Parte"]
        tipo = sg.popup_get_text("Digite o tipo de usuário para filtrar (Juiz, Advogado, Parte):")
        if tipo and tipo in tipos:
            usuarios = self.__controlador.get_usuarios_por_tipo(tipo.lower())
            if usuarios:
                linhas = [f"{u.id} - {u.nome} ({tipo})" for u in usuarios]
                sg.popup_scrolled("\n".join(linhas), title=f"Relatório - {tipo}s")
            else:
                sg.popup("Nenhum usuário encontrado do tipo informado.")
        else:
            sg.popup("Tipo inválido.")