
""" 
ControladorUsuarios
-------------------
Responsável por:
- Gerenciar instâncias de usuários (Advogado, Juiz, Parte)
- Encaminhar interações para a tela correspondente
- Permitir extração de dados para relatórios (ex: listar por tipo)
"""

from src.view.telaUsuario import TelaUsuarios
from src.module.usuario.advogado import Advogado
from src.module.usuario.juiz import Juiz
from src.module.usuario.reu import Reu
from src.module.usuario.vitima import Vitima

class ControladorUsuarios:
    def __init__(self):
        self.__usuarios = []  # Lista única contendo todas as instâncias de usuários
        self.__tela = TelaUsuarios()

    def abrir__tela(self):
        while True:
            opcao = self.__tela.mostrar_menu()
            if opcao == 1:
                self.incluir_usuario()
            elif opcao == 2:
                self.remover_usuario()
            elif opcao == 3:
                self.alterar_usuario()
            elif opcao == 4:
                self.listar_usuarios()
            elif opcao == 5:
                self.listar_por_tipo()
            elif opcao == 0:
                break
            else:
                self.__tela.mostrar_mensagem("Opção inválida.")

    def incluir_usuario(self):
        dados = self.__tela.ler_dados_usuario()
        tipo = dados["tipo"]
        if tipo == "advogado":
            usuario = Advogado(**dados)
        elif tipo == "juiz":
            usuario = Juiz(**dados)
        elif tipo == "reu":
            usuario = Reu(**dados)
        elif tipo == "vitima":
            usuario = Vitima(**dados)
        else:
            self.__tela.mostrar_mensagem("Tipo inválido.")
            return
        self.__usuarios.append(usuario)
        self.__tela.mostrar_mensagem("Usuário cadastrado com sucesso.")

    def remover_usuario(self):
        id_usuario = self.__tela.selecionar_usuario(self.__usuarios)
        for usuario in self.__usuarios:
            if usuario.id() == id_usuario:
                self.__usuarios.remove(usuario)
                self.__tela.mostrar_mensagem("Usuário removido.")
                return
        self.__tela.mostrar_mensagem("Usuário não encontrado.")

    def alterar_usuario(self):
        id_usuario = self.__tela.selecionar_usuario(self.__usuarios)
        for i, usuario in enumerate(self.__usuarios):
            if usuario.id() == id_usuario:
                novos_dados = self.__tela.ler_dados_usuario()
                novo_usuario = type(usuario)(**novos_dados)
                self.__usuarios[i] = novo_usuario
                self.__tela.mostrar_mensagem("Usuário alterado com sucesso.")
                return
        self.__tela.mostrar_mensagem("Usuário não encontrado.")

    def listar_usuarios(self):
        lista_str = [f"{u.id()} - {u.nome()} ({type(u).__name__})" for u in self.__usuarios]
        self.__tela.exibir_lista_usuarios(lista_str)

    def listar_por_tipo(self):
        tipo = self.__tela.selecionar_tipo_usuario()
        lista_filtrada = [
            f"{u.id()} - {u.nome()} ({type(u).__name__})" 
            for u in self.__usuarios if type(u).__name__.lower() == tipo.lower()
        ]
        self.__tela.exibir_lista_usuarios(lista_filtrada)
