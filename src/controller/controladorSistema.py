from src.view.telaSistema import TelaSistema
from src.controller.controladorUsuarios import ControladorUsuarios
from src.controller.controladorProcessos import ControladorProcessos

class ControladorSistema:
    def __init__(self):
        self.__tela = TelaSistema()
        self.__controlador_usuarios = ControladorUsuarios()
        self.__controlador_processos = ControladorProcessos()

    def inicializar(self):
        self.__controlador_usuarios.abrir_tela()

        id_usuario = self.__tela.solicitar_id_usuario()
        usuario_logado = self.__controlador_usuarios.buscar_usuario_por_id(id_usuario)

        if usuario_logado:
            self.__controlador_processos.set_usuario_logado(usuario_logado)
            self.__controlador_processos.abrir_tela()
        else:
            self.__tela.mostrar_mensagem("Usuário não encontrado.")