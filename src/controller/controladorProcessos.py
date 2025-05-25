from module.usuario.abstractUsuario import Usuario
from module.usuario.juiz import Juiz
from module.usuario.advogado import Advogado
from view.telaProcessos import TelaProcessos
from module.processo import Processo
from module.documento.acusacao import Acusacao
from module.documento.defesa import Defesa
from module.documento.audiencia import Audiencia
from module.documento.sentenca import Sentenca
from module.documento.arquivamento import Arquivamento
from module.tribunal import Tribunal
from datetime import date

class ControladorProcessos:
    def __init__(self, controlador_usuarios):
        self.__controlador_usuarios = controlador_usuarios
        self.__processos = []
        self.__tribunais = self.__carregar_tribunais()
        self.__tela = TelaProcessos()
        self.__usuario_logado = None


    def set_usuario_logado(self, usuario: Usuario):
        self.__usuario_logado = usuario

    def __carregar_tribunais(self):
        return [
            Tribunal(1, "TJSC", "Santa Catarina", "Tribunal de Justiça de SC", "1ª Instância"),
            Tribunal(2, "TRF4", "Região Sul", "Tribunal Regional Federal da 4ª Região", "2ª Instância")
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

        # Seleção de advogados
        advogados = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() == "advogado"]
        if not advogados:
            self.__tela.mostrar_mensagem("Nenhum advogado cadastrado.")
            if self.__tela.perguntar_sim_ou_nao("Deseja cadastrar um advogado agora? (s/n): "):
                self.__controlador_usuarios.incluir_usuario()
                advogados = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() == "advogado"]
        advogados_selecionados = self.__tela.selecionar_usuarios_por_id(advogados, "advogado")

        # Seleção de partes
        partes = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() in ["reu", "vitima"]]
        if not partes:
            self.__tela.mostrar_mensagem("Nenhuma parte cadastrada.")
            if self.__tela.perguntar_sim_ou_nao("Deseja cadastrar uma parte agora? (s/n): "):
                self.__controlador_usuarios.incluir_usuario()
                partes = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() in ["reu", "vitima"]]
        partes_selecionadas = self.__tela.selecionar_usuarios_por_id(partes, "parte")

        processo = Processo(
            numero=dados["numero"],
            data_abertura=dados["data_abertura"],
            status="Ativo",
            juiz_responsavel=dados["juiz"],
            advogados=advogados_selecionados,
            partes=partes_selecionadas,
            tribunal=tribunal
        )
        self.__processos.append(processo)
        self.__tela.mostrar_mensagem("Processo criado com sucesso.")

    def listar_processos(self):
        processos_usuario = []

        for p in self.__processos:
            if p.juiz_responsavel == self.__usuario_logado or \
            self.__usuario_logado in p.advogados or \
            self.__usuario_logado in p.partes:
                processos_usuario.append(p)

        if not processos_usuario:
            self.__tela.mostrar_mensagem("Nenhum processo relacionado ao usuário atual.")
            return

        lista_str = [f"{p.numero} - Status: {p.status} - Tribunal: {p.tribunal.nome}" for p in processos_usuario]
        self.__tela.exibir_lista_processos(lista_str)


    def selecionar_processo(self):
        numero = self.__tela.selecionar_numero_processo()
        for processo in self.__processos:
            if processo.numero == numero:
                return processo
        self.__tela.mostrar_mensagem("Processo não encontrado.")
        return None

    def adicionar_documento(self):
        processo = self.selecionar_processo()
        if not processo:
            return

        if processo.status.lower() != "ativo":
            self.__tela.mostrar_mensagem("Não é possível adicionar documentos a um processo encerrado.")
            return

        if any(isinstance(d, Sentenca) for d in processo.documentos):
            self.__tela.mostrar_mensagem("Este processo já possui sentença. Não é possível adicionar novos documentos.")
            return

        tipo, dados_doc = self.__tela.ler_dados_documento()
        dados_doc["autor"] = self.__usuario_logado 
        doc = None

        if tipo == "sentenca":
            if not isinstance(self.__usuario_logado, Juiz):
                self.__tela.mostrar_mensagem("Apenas juízes podem emitir sentenças.")
                return
            doc = Sentenca(**dados_doc)

        elif tipo == "acusacao":
            if not isinstance(self.__usuario_logado, Advogado):
                self.__tela.mostrar_mensagem("Apenas advogados podem emitir acusações.")
                return
            if not self._possui_audiencia_realizada(processo):
                self.__tela.mostrar_mensagem("A acusação só pode ocorrer após a audiência.")
                return
            doc = Acusacao(**dados_doc)

        elif tipo == "defesa":
            if not isinstance(self.__usuario_logado, Advogado):
                self.__tela.mostrar_mensagem("Apenas advogados podem apresentar defesa.")
                return
            if not self._possui_audiencia_realizada(processo):
                self.__tela.mostrar_mensagem("A defesa só pode ocorrer após a audiência.")
                return
            doc = Defesa(**dados_doc)

        elif tipo == "audiencia":
            if not isinstance(self.__usuario_logado, Juiz):
                self.__tela.mostrar_mensagem("Apenas juízes podem marcar audiências.")
                return
            dados_doc["data"] = date.today().isoformat()
            doc = Audiencia(**dados_doc)

        elif tipo == "arquivamento":
            self.__tela.mostrar_mensagem("Arquivamentos são gerados automaticamente ao encerrar o processo.")
            return

        else:
            self.__tela.mostrar_mensagem("Tipo de documento inválido.")
            return

        processo.adicionar_documento(doc)
        self.__tela.mostrar_mensagem(f"{tipo.capitalize()} adicionada ao processo.")

    def encerrar_processo(self):
        processo = self.selecionar_processo()
        if not processo:
            return

        if not any(isinstance(d, Audiencia) for d in processo.documentos):
            self.__tela.mostrar_mensagem("Não é possível encerrar o processo sem uma audiência.")
            return

        if not any(isinstance(d, Sentenca) for d in processo.documentos):
            self.__tela.mostrar_mensagem("Não é possível encerrar o processo sem uma sentença.")
            return

        processo.encerrar()
        self.__tela.mostrar_mensagem("Processo encerrado com sucesso.")

    def gerar_relatorio(self):
        while True:
            opcao = self.__tela.mostrar_menu_relatorio()
            if opcao == 1:
                self._relatorio_por_status()
            elif opcao == 2:
                self._relatorio_por_juiz()
            elif opcao == 3:
                self._relatorio_sem_audiencia()
            elif opcao == 4:
                self._relatorio_com_sentenca()
            elif opcao == 0:
                break
            else:
                self.__tela.mostrar_mensagem("Opção inválida.")

    def _relatorio_por_status(self):
        status = self.__tela.solicitar_status()
        lista = [p for p in self.__processos if p.status.lower() == status.lower()]
        self.__tela.exibir_relatorio([f"{p.numero} - {p.status}" for p in lista])

    def _relatorio_por_juiz(self):
        nome = self.__tela.solicitar_nome_juiz()
        lista = [p for p in self.__processos if p.juiz_responsavel.nome.lower() == nome.lower()]
        self.__tela.exibir_relatorio([f"{p.numero} - Juiz: {p.juiz_responsavel.nome}" for p in lista])

    def _relatorio_sem_audiencia(self):
        lista = []
        for p in self.__processos:
            if not any(isinstance(d, Audiencia) for d in p.documentos):
                lista.append(p)
        self.__tela.exibir_relatorio([f"{p.numero} - Sem audiência" for p in lista])

    def _relatorio_com_sentenca(self):
        lista = []
        for p in self.__processos:
            if any(isinstance(d, Sentenca) for d in p.documentos):
                lista.append(p)
        self.__tela.exibir_relatorio([f"{p.numero} - Contém sentença" for p in lista])

    def _possui_audiencia_realizada(self, processo):
        for doc in processo.documentos:
            if isinstance(doc, Audiencia) and doc.data <= date.today().isoformat():
                return True
        return False
    
    def get_tribunais(self):
        return self.__tribunais
