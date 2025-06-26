from src.view.telaUsuario import TelaUsuarios
from src.module.usuario.advogado import Advogado
from src.module.usuario.juiz import Juiz
from src.module.usuario.reu import Reu
from src.module.usuario.vitima import Vitima
from src.DAOs.usuarioDAO import UsuarioDAO

class ControladorUsuarios:
    def __init__(self, tribunais: list):
        self.__tela = TelaUsuarios()
        self.__tribunais = tribunais
        self.__user_dao = UsuarioDAO()

    def abrir_tela(self):
        while True:
            opcao = self.__tela.mostrar_menu()
            if opcao == 1:
                self.incluir_usuario()
            elif opcao == 2:
                self.listar_usuarios()
            elif opcao == 3:
                self.listar_por_tipo()
            elif opcao == 4:
                self.remover_usuario()
            elif opcao == 0:
                break
            else:
                self.__tela.mostrar_mensagem("Opção inválida.")

    def incluir_usuario(self):
        usuarios_existentes = list(self.__user_dao.get_all())
        dados = self.__tela.ler_dados_usuario(usuarios_existentes, self.__tribunais)
        if not dados:
            return

        if any(u.id == dados["id"] or u.cpf == dados["cpf"] for u in usuarios_existentes):
            self.__tela.mostrar_mensagem("ID ou CPF já cadastrado.")
            return

        tipo = dados["tipo"]
        del dados["tipo"]

        if tipo == "juiz":
            tribunal = self.__tela.selecionar_tribunal(self.__tribunais)
            if tribunal is None:
                self.__tela.mostrar_mensagem("Tribunal inválido. Operação cancelada.")
                return
            dados["tribunal_atribuido"] = tribunal
            novo_usuario = Juiz(**dados)

        elif tipo == "advogado":
            dados["oab"] = input("Digite o número da OAB do advogado: ")
            novo_usuario = Advogado(**dados)

        elif tipo == "vitima":
            novo_usuario = Vitima(**dados)

        elif tipo == "reu":
            novo_usuario = Reu(**dados)

        else:
            self.__tela.mostrar_mensagem("Tipo inválido.")
            return

        self.__user_dao.add(novo_usuario.id, novo_usuario)
        self.__tela.mostrar_mensagem(f"{tipo.capitalize()} cadastrado com sucesso.")

    def listar_usuarios(self):
        usuarios = list(self.__user_dao.get_all())
        lista = [f"{u.id} - {u.nome} ({u.__class__.__name__})" for u in usuarios]
        self.__tela.exibir_usuarios(lista)

    def listar_por_tipo(self):
        tipo = self.__tela.solicitar_tipo()
        usuarios = list(self.__user_dao.get_all())
        lista = [f"{u.id} - {u.nome} ({u.__class__.__name__})" for u in usuarios if u.__class__.__name__.lower() == tipo.lower()]
        self.__tela.exibir_usuarios(lista)

    def remover_usuario(self):
        id_remover = self.__tela.solicitar_id()
        if self.__user_dao.get(id_remover):
            self.__user_dao.remove(id_remover)
            self.__tela.mostrar_mensagem("Usuário removido.")
        else:
            self.__tela.mostrar_mensagem("Usuário não encontrado.")

    def buscar_usuario_por_id(self, id_usuario):
        return self.__user_dao.get(id_usuario)

    def get_usuarios(self):
        return list(self.__user_dao.get_all())
