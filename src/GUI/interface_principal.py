import PySimpleGUI as sg

class InterfacePrincipalGUI:
    def __init__(self, controlador):
        self.__controlador = controlador

    def abre_tela(self):
        sg.theme("DarkBlue3")

        layout = [
            [sg.Text("SISTEMA MINI-EPROC", font=("Helvetica", 20), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button("👤  Gerenciar Usuários", size=(30, 2), font=("Helvetica", 12)), sg.Push()],
            [sg.Push(), sg.Button("📂  Gerenciar Processos", size=(30, 2), font=("Helvetica", 12)), sg.Push()],
            [sg.Push(), sg.Button("❌  Sair", size=(30, 2), font=("Helvetica", 12)), sg.Push()]
        ]

        janela = sg.Window("MiniEPROC - Menu Principal", layout, element_justification="center")

        while True:
            evento, _ = janela.read()
            if evento in (sg.WINDOW_CLOSED, "❌  Sair"):
                sg.popup_ok("Saindo do sistema...", title="Encerrando")
                break

            elif evento == "👤  Gerenciar Usuários":
                # self.__controlador.controlador_usuarios.abrir_tela()
                sg.popup_ok("Redirecionando para terminal...", title="Modo Texto")
                janela.close()
                self.__controlador.abrir_usuarios()
                break


            elif evento == "📂  Gerenciar Processos":
                id_str = sg.popup_get_text("Digite o ID do usuário:", title="Acesso aos Processos")
                if id_str and id_str.isdigit():
                    id_usuario = int(id_str)
                    usuario = self.__controlador.controlador_usuarios.buscar_usuario_por_id(id_usuario)

                    if usuario:
                        tipo = usuario.__class__.__name__.lower()
                        if tipo in ["juiz", "advogado", "promotor"]:
                            self.__controlador.controlador_processos.set_usuario_logado(usuario)
                            sg.popup_ok("Redirecionando para terminal...", title="Modo Texto")
                            janela.close()
                            self.__controlador.abrir_processos_com_usuario(usuario)
                            break
                            # self.__controlador.controlador_processos.set_usuario_logado(usuario)
                            # self.__controlador.controlador_processos.abrir_tela()
                        else:
                            sg.popup_error(f"Usuário do tipo '{tipo}' não tem permissão para acessar processos.")
                    else:
                        sg.popup_error("Usuário não encontrado.")
                else:
                    sg.popup_error("ID inválido.")

        janela.close()
