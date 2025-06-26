from GUI.interface_principal import InterfacePrincipalGUI
from controller.controladorUsuarios import ControladorUsuarios
from controller.controladorProcessos import ControladorProcessos
from controller.controladorDocumentos import ControladorDocumentos

class ControladorSistema:
    def __init__(self):
        self.__tela = InterfacePrincipalGUI(self)
        self.__controlador_documentos = ControladorDocumentos()
        self.__controlador_usuarios = ControladorUsuarios(self.get_tribunais())
        self.__controlador_processos = ControladorProcessos(self.__controlador_usuarios, self.__controlador_documentos)

    def get_tribunais(self):
        from module.tribunal import Tribunal
        return [
            Tribunal(1, "TJSC", "Santa Catarina", "Tribunal de Justiça de SC", "1ª Instância"),
            Tribunal(2, "TRF4", "Região Sul", "Tribunal Regional Federal da 4ª Região", "2ª Instância")
        ]

    def inicializar(self):
        self.__tela.abre_tela()

    def abrir_usuarios(self):
        self.__controlador_usuarios.abrir_tela()

    def abrir_processos_com_usuario(self, usuario):
        self.__controlador_processos.set_usuario_logado(usuario)
        self.__controlador_processos.abrir_tela()
