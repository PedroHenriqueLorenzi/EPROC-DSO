from src.module.usuario.abstractUsuario import Usuario
from src.module.usuario.juiz import Juiz
from src.module.usuario.advogado import Advogado
from src.view.telaProcessos import TelaProcessos
from src.module.processo import Processo
from src.module.documento.acusacao import Acusacao
from src.module.documento.defesa import Defesa
from src.module.documento.audiencia import Audiencia
from src.module.documento.sentenca import Sentenca
from src.module.arquivamento import Arquivamento
from src.module.tribunal import Tribunal
from datetime import date

class ControladorProcessos:
    def __init__(self):
        self.__processos = []
        self.__tribunais = self.__carregar_tribunais()
        self.__tela = TelaProcessos()
        self.__usuario_logado = None

    def set_usuario_logado(self, usuario: Usuario):
        self.__usuario_logado = usuario

    def __carregar_tribunais(self):
        return [
            Tribunal(1, "TJSC", "Santa Catarina", "Tribunal de Justiça de SC"),
            Tribunal(2, "TRF4", "Região Sul", "Tribunal Regional Federal da 4ª Região")
        ]

    def abrir_tela(self):
        while True:
            opcao = self.__tela.mostrar_menu()
            if opcao == 1:
                self.criar_processo()
            elif opcao == 2:
                self.listar_processos()
            elif opcao == 3:
                self.adicionar_documento()
            elif opcao == 4:
                self.encerrar_processo()
            elif opcao == 5:
                self.gerar_relatorio()
            elif opcao == 0:
                break
            else:
                self.__tela.mostrar_mensagem("Opção inválida.")

    def criar_processo(self):
        dados = self.__tela.ler_dados_processo()
        tribunal = self.__tela.selecionar_tribunal(self.__tribunais)
        if not tribunal:
            self.__tela.mostrar_mensagem("Tribunal não encontrado.")
            return

        processo = Processo(
            numero=dados["numero"],
            data_abertura=dados["data_abertura"],
            status="Ativo",
            juiz_responsavel=dados["juiz"],
            advogados=dados["advogados"],
            partes=dados["partes"],
            tribunal=tribunal
        )
        self.__processos.append(processo)
        self.__tela.mostrar_mensagem("Processo criado com sucesso.")

    def listar_processos(self):
        lista_str = [f"{p.numero()} - Status: {p.status()} - Tribunal: {p.tribunal().nome()}" for p in self.__processos]
        self.__tela.exibir_lista_processos(lista_str)

    def selecionar_processo(self):
        numero = self.__tela.selecionar_numero_processo()
        for processo in self.__processos:
            if processo.numero() == numero:
                return processo
        self.__tela.mostrar_mensagem("Processo não encontrado.")
        return None

    def adicionar_documento(self):
        processo = self.selecionar_processo()
        if not processo:
            return

        if processo.status().lower() != "ativo":
            self.__tela.mostrar_mensagem("Não é possível adicionar documentos a um processo encerrado.")
            return

        tipo, dados_doc = self.__tela.ler_dados_documento()
        dados_doc["autor"] = self.__usuario_logado 
        doc = None

        if tipo == "sentenca":
            if not isinstance(self.__usuario_logado, Juiz):
                self.__tela.mostrar_mensagem("Apenas juízes podem emitir sentenças.")
                return
            doc = Sentenca(**dados_doc)

        else:
            doc_class = {
                "acusacao": Acusacao,
                "defesa": Defesa,
                "audiencia": Audiencia,
                "arquivamento": Arquivamento
            }.get(tipo)
            if doc_class:
                doc = doc_class(**dados_doc)
            else:
                self.__tela.mostrar_mensagem("Tipo de documento inválido.")
                return

        processo.adicionar_documento(doc)
        self.__tela.mostrar_mensagem(f"{tipo.capitalize()} adicionada ao processo.")

    def encerrar_processo(self):
        processo = self.selecionar_processo()
        if processo:
            processo.encerrar()
            self.__tela.mostrar_mensagem("Processo encerrado com sucesso.")

    def gerar_relatorio(self):
        relatorio = []
        for p in self.__processos:
            relatorio.append(
                f"Processo {p.numero()} - Status: {p.status()} - Juiz: {p.juiz_responsavel().nome()} - Tribunal: {p.tribunal().nome()}"
            )
        self.__tela.exibir_relatorio(relatorio)
