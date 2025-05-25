

from view.telaUsuario import TelaUsuarios
from module.usuario.advogado import Advogado
from module.usuario.juiz import Juiz
from module.usuario.reu import Reu
from module.usuario.vitima import Vitima

class ControladorUsuarios:
    def __init__(self, tribunais: list):
        self.__usuarios = []
        self.__tela = TelaUsuarios()
        self.__tribunais = tribunais

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
        dados = self.__tela.ler_dados_usuario(self.__tribunais)
        if not dados:
            return

        if any(u.id == dados["id"] or u.cpf == dados["cpf"] for u in self.__usuarios):
            self.__tela.mostrar_mensagem("ID ou CPF já cadastrado.")
            return

        tipo = dados["tipo"]
        del dados["tipo"]

        if tipo == "juiz":
            novo_usuario = Juiz(**dados)
        elif tipo == "advogado":
            novo_usuario = Advogado(**dados)
        elif tipo == "vitima":
            novo_usuario = Vitima(**dados)
        elif tipo == "reu":
            novo_usuario = Reu(**dados)
        else:
            self.__tela.mostrar_mensagem("Tipo inválido.")
            return

        self.__usuarios.append(novo_usuario)
        self.__tela.mostrar_mensagem(f"{tipo.capitalize()} cadastrado com sucesso.")


    def listar_usuarios(self):
        lista = [f"{u.id} - {u.nome} ({u.__class__.__name__})" for u in self.__usuarios]
        self.__tela.exibir_usuarios(lista)

    def listar_por_tipo(self):
        tipo = self.__tela.solicitar_tipo()
        lista = [f"{u.id} - {u.nome} ({u.__class__.__name__})" for u in self.__usuarios if u.__class__.__name__.lower() == tipo.lower()]
        self.__tela.exibir_usuarios(lista)

    def remover_usuario(self):
        id_remover = self.__tela.solicitar_id()
        for u in self.__usuarios:
            if u.id() == id_remover:
                self.__usuarios.remove(u)
                self.__tela.mostrar_mensagem("Usuário removido.")
                return
        self.__tela.mostrar_mensagem("Usuário não encontrado.")

    def buscar_usuario_por_id(self, id_usuario):
        for u in self.__usuarios:
            if u.id == id_usuario:
                return u
        return None