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
        tribunais = self.__controlador.get_tribunais()
        sg.theme("DarkBlue4")
        layout = [
            [sg.Text("Nome:", size=(20,1)), sg.Input(key="nome", size=(40,1))],
            [sg.Text("CPF (somente números, 11 dígitos):", size=(30,1)), 
            sg.Input(key="cpf", size=(20,1), enable_events=True), 
            sg.Text("", key="cpf_feedback", size=(25,1), text_color="yellow")],
            [sg.Text("Data de Nascimento (DD-MM-AAAA):", size=(30,1)), sg.Input(key="nascimento", size=(20,1))],
            [sg.Text("Tipo de Usuário:")],
            [sg.Radio("Juiz", "tipo", key="tipo_juiz", enable_events=True),
            sg.Radio("Advogado", "tipo", key="tipo_advogado", enable_events=True),
            sg.Radio("Parte", "tipo", key="tipo_parte", enable_events=True)],
            [sg.Column([[sg.Text("Subtipo da Parte:"), sg.Combo(["Reu", "Vitima"], key="parte_tipo")]], key="col_parte", visible=False, pad=(0, 0))],
            [sg.Column([[sg.Text("OAB:"), sg.Input(key="oab")]], key="col_oab", visible=False, pad=(0, 0))],
            [sg.Column([[sg.Text("Tribunal:"), sg.Combo([t.nome for t in tribunais], key="tribunal")]], key="col_tribunal", visible=False, pad=(0, 0))],
            [sg.Button("Salvar"), sg.Button("Cancelar")]
        ]

        window = sg.Window("Cadastro de Usuário", layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, "Cancelar"):
                break

            if event == "cpf":
                cpf_input = values["cpf"]
                if len(cpf_input) < 11:
                    window["cpf_feedback"].update(f"Faltam {11 - len(cpf_input)} dígitos")
                elif len(cpf_input) > 11:
                    window["cpf_feedback"].update("CPF excede 11 dígitos", text_color="red")
                else:
                    window["cpf_feedback"].update("✔ CPF completo", text_color="green")

            if event in ("tipo_juiz", "tipo_advogado", "tipo_parte"):
                window["col_oab"].update(visible=values["tipo_advogado"])
                window["col_tribunal"].update(visible=values["tipo_juiz"])
                window["col_parte"].update(visible=values["tipo_parte"])

            if event == "Salvar":
                try:
                    nome = values["nome"].strip()
                    cpf = values["cpf"].strip()
                    nascimento = values["nascimento"].strip()
                    oab = values.get("oab", "").strip()
                    parte_tipo = values.get("parte_tipo")

                    if len(cpf) != 11 or not cpf.isdigit():
                        sg.popup_error("CPF deve conter 11 dígitos numéricos.")
                        continue

                    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
                    try:
                        datetime.strptime(nascimento, "%d-%m-%Y")
                    except ValueError:
                        sg.popup_error("Data de nascimento deve estar no formato DD-MM-AAAA.")
                        continue

                    if values["tipo_advogado"]:
                        self.__controlador.criar_usuario(nome, cpf_formatado, nascimento, "Advogado", oab=oab)

                    elif values["tipo_juiz"]:
                        nome_tribunal = values.get("tribunal")
                        if not nome_tribunal:
                            sg.popup_error("Selecione o tribunal.")
                            continue
                        tribunais_dict = {t.nome: i for i, t in enumerate(tribunais)}
                        self.__controlador.criar_usuario(nome, cpf_formatado, nascimento, "Juiz", tribunal_index=tribunais_dict[nome_tribunal])

                    elif values["tipo_parte"]:
                        if parte_tipo not in ("Reu", "Vitima"):
                            sg.popup_error("Selecione o subtipo da parte (Réu ou Vítima).")
                            continue
                        self.__controlador.criar_usuario(nome, cpf_formatado, nascimento, "Parte", parte_tipo=parte_tipo.lower())

                    else:
                        sg.popup_error("Selecione um tipo de usuário.")
                        continue

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