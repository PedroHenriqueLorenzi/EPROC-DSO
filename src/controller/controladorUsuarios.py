from view.telaUsuario import TelaUsuarios
from module.usuario.advogado import Advogado
from module.usuario.juiz import Juiz
from module.usuario.reu import Reu
from module.usuario.vitima import Vitima
from DAOs.usuarioDAO import UsuarioDAO

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

    def remover_usuario(self, id_remover=None):
        if id_remover is None:
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


    def criar_usuario(self, nome, cpf, nascimento, tipo, oab=None, tribunal_index=None, parte_tipo=None):
        novo_id = max([u.id for u in self.__user_dao.get_all()] + [0]) + 1

        if tipo.lower() == "juiz":
            if tribunal_index is None or not (0 <= tribunal_index < len(self.__tribunais)):
                raise ValueError("Tribunal inválido.")
            tribunal = self.__tribunais[tribunal_index]
            novo_usuario = Juiz(novo_id, nome, cpf, nascimento, tribunal)

        elif tipo.lower() == "advogado":
            if not oab:
                raise ValueError("Número da OAB é obrigatório para advogados.")
            novo_usuario = Advogado(novo_id, nome, cpf, nascimento, oab)

        elif tipo.lower() == "parte":
            if parte_tipo == "reu":
                novo_usuario = Reu(novo_id, nome, cpf, nascimento)
            elif parte_tipo == "vitima":
                novo_usuario = Vitima(novo_id, nome, cpf, nascimento)
            else:
                raise ValueError("Tipo de parte inválido.")

        else:
            raise ValueError("Tipo de usuário inválido")

        self.__user_dao.add(novo_id, novo_usuario)


    def editar_usuario(self, id, novo_nome, novo_nascimento=None, nova_oab=None):
        usuario = self.__user_dao.get(id)
        if usuario:
            usuario.nome = novo_nome
            if novo_nascimento:
                usuario.data_nascimento = novo_nascimento 
            if hasattr(usuario, "oab") and nova_oab is not None:
                usuario.oab = nova_oab
            self.__user_dao.update(id, usuario)

    def get_todos_usuarios(self):
        return list(self.__user_dao.get_all())

    def get_usuarios_por_tipo(self, tipo):
        return [u for u in self.__user_dao.get_all() if u.__class__.__name__.lower() == tipo.lower()]
