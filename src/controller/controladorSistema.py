import PySimpleGUI as sg
from GUI.interface_principal import InterfacePrincipalGUI
from GUI.interface_usuarios import InterfaceUsuariosGUI
from GUI.interface_processos import InterfaceProcessosGUI
from controller.controladorUsuarios import ControladorUsuarios
from controller.controladorProcessos import ControladorProcessos
from controller.controladorDocumentos import ControladorDocumentos
from module.tribunal import Tribunal
from DAOs.processoDAO import ProcessoDAO

class ControladorSistema:
    def __init__(self):
        self.__processo_dao = ProcessoDAO()
        self.__controlador_documentos = ControladorDocumentos(self.__processo_dao)
        self.__controlador_usuarios = ControladorUsuarios(self.get_tribunais())
        self.__controlador_processos = ControladorProcessos(
            self.__controlador_usuarios, self.__controlador_documentos, self.__processo_dao
        )
        self.__tela = InterfacePrincipalGUI(self)

    def get_tribunais(self):
        return [
            Tribunal(1, "TJSC", "Santa Catarina", "Tribunal de Justiça de SC", "1ª Instância"),
            Tribunal(2, "TRF4", "Região Sul", "Tribunal Regional Federal da 4ª Região", "2ª Instância")
        ]

    def inicializar(self):
        while True:
            acao = self.__tela.abre_tela()

            if acao == "usuarios":
                gui = InterfaceUsuariosGUI(self.__controlador_usuarios)
                gui.abre_tela()
            elif acao == "processos":
                id_str = sg.popup_get_text("Digite o ID do usuário:", title="Acesso aos Processos")
                if id_str and id_str.isdigit():
                    id_usuario = int(id_str)
                    usuario = self.__controlador_usuarios.buscar_usuario_por_id(id_usuario)

                    if usuario:
                        try:
                            self.__controlador_processos.set_usuario_logado(usuario)
                            gui = InterfaceProcessosGUI(self.__controlador_processos, self.__controlador_documentos)
                            gui.abre_tela()
                        except PermissionError as e:
                            sg.popup_error(str(e))
                            
                    else:
                        sg.popup_error("Usuário não encontrado.")
                else:
                    sg.popup_error("ID inválido.")
            else:
                break

