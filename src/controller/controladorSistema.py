from view.telaSistema import TelaSistema
from controller.controladorUsuarios import ControladorUsuarios
from controller.controladorProcessos import ControladorProcessos

class ControladorSistema:
    def __init__(self):
        self.__tela = TelaSistema()
        self.__controlador_usuarios = ControladorUsuarios(self.get_tribunais())
        self.__controlador_processos = ControladorProcessos(self.__controlador_usuarios)

    def get_tribunais(self):
        from module.tribunal import Tribunal
        return [
            Tribunal(1, "TJSC", "Santa Catarina", "Tribunal de Justiça de SC", "1ª Instância"),
            Tribunal(2, "TRF4", "Região Sul", "Tribunal Regional Federal da 4ª Região", "2ª Instância")
        ]
    def inicializar(self):
        while True:
            opcao = self.__tela.mostrar_menu()
            if opcao == 1:
                self.__controlador_usuarios.abrir_tela()

            elif opcao == 2:
                id_usuario = self.__tela.solicitar_id_usuario()
                usuario_logado = self.__controlador_usuarios.buscar_usuario_por_id(id_usuario)

                if usuario_logado:
                    tipo = usuario_logado.__class__.__name__.lower()
                    if tipo in ["juiz", "advogado", "promotor"]:
                        self.__controlador_processos.set_usuario_logado(usuario_logado)
                        self.__controlador_processos.abrir_tela()
                    else:
                        self.__tela.mostrar_mensagem(f"Usuário do tipo '{tipo}' não tem permissão para acessar processos.")
                else:
                    self.__tela.mostrar_mensagem("Usuário não encontrado.")

            elif opcao == 0:
                self.__tela.mostrar_mensagem("Saindo do sistema...")
                break

            else:
                self.__tela.mostrar_mensagem("Opção inválida.")