from module.usuario.abstractUsuario import Usuario
from module.usuario.juiz import Juiz
from module.usuario.advogado import Advogado
from view.telaProcessos import TelaProcessos
from module.processo import Processo
from module.documento.audiencia import Audiencia
from module.documento.sentenca import Sentenca
from module.tribunal import Tribunal
from datetime import datetime
from DAOs.processoDAO import ProcessoDAO

class ControladorProcessos:
    def __init__(self, controlador_usuarios, controlador_documentos, processo_dao):
        self.__controlador_usuarios = controlador_usuarios
        self.__controlador_documentos = controlador_documentos
        self.__tribunais = self.__carregar_tribunais()
        self.__tela = TelaProcessos()
        self.__usuario_logado = None
        self.__processo_dao = processo_dao
        self.__processo_dao = ProcessoDAO()

    def set_usuario_logado(self, usuario):
        if usuario.__class__.__name__.lower() not in ["juiz", "advogado"]:
            raise PermissionError("Apenas juízes e advogados têm acesso aos processos.")
        self.__usuario_logado = usuario
    
    def get_usuario_logado(self):
        return self.__usuario_logado


    def __carregar_tribunais(self):
        return [
            Tribunal(1, "TJSC", "Santa Catarina", "Tribunal de Justiça de SC", "1ª Instância"),
            Tribunal(2, "TRF4", "Região Sul", "Tribunal Regional Federal da 4ª Região", "2ª Instância")
        ]

    def abrir_tela(self):
        while True:
            opcao = self.__tela.mostrar_menu(self.__usuario_logado)
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
            elif opcao == 6:
                self.editar_processo()
            elif opcao == 7:
                self.exibir_detalhes_processo()
            elif opcao == 0:
                break
            else:
                self.__tela.mostrar_mensagem("Opção inválida.")

        numero = self.__tela.solicitar_numero_processo()
        data_abertura = self.__tela.solicitar_data_processo()
        juiz = self.__tela.solicitar_juiz(self.__controlador_usuarios.get_usuarios())
        if not juiz:
            self.__tela.mostrar_mensagem("Juiz não encontrado.")
            return

        tribunal = self.__tela.selecionar_tribunal(self.__tribunais)
        if not tribunal:
            self.__tela.mostrar_mensagem("Tribunal não encontrado.")
            return

        advogados = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() == "advogado"]
        if not advogados:
            self.__tela.mostrar_mensagem(">>> Nenhum advogado cadastrado.")
            if self.__tela.confirmar("Deseja cadastrar um advogado agora? (s/n): "):
                self.__controlador_usuarios.incluir_usuario()
                advogados = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() == "advogado"]
            else:
                self.__tela.mostrar_mensagem("Operação cancelada.")
                return

        selecionados = self.__tela.selecionar_usuarios_por_id(advogados, "advogado")
        if not selecionados:
            self.__tela.mostrar_mensagem("Nenhum advogado selecionado.")
            return

        partes = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() in ["reu", "vitima"]]
        if not partes:
            self.__tela.mostrar_mensagem(">>> Nenhuma parte cadastrada.")
            if self.__tela.confirmar("Deseja cadastrar uma parte agora? (s/n): "):
                self.__controlador_usuarios.incluir_usuario()
                partes = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() in ["reu", "vitima"]]
            else:
                self.__tela.mostrar_mensagem("Operação cancelada.")
                return

        partes_selecionadas = self.__tela.selecionar_usuarios_por_id(partes, "parte")
        if not partes_selecionadas:
            self.__tela.mostrar_mensagem("Nenhuma parte selecionada.")
            return

        processo = Processo(
            numero=numero,
            data_abertura=data_abertura,
            status="Ativo",
            juiz_responsavel=juiz,
            advogados=selecionados,
            partes=partes_selecionadas,
            tribunal=tribunal
        )
        self.__processo_dao.add(numero, processo)
        self.__tela.mostrar_mensagem(">>> Processo criado com sucesso.")

    def listar_processos(self):       
        processos_usuario = []
        id_logado = self.__usuario_logado.id

        for p in self.__processo_dao.get_all():
            if p.juiz_responsavel.id == id_logado or \
            any(adv.id == id_logado for adv in p.advogados) or \
            any(parte.id == id_logado for parte in p.partes):
                processos_usuario.append(p)

        if not processos_usuario:
            self.__tela.mostrar_mensagem("Nenhum processo relacionado ao usuário atual.")
            return

        lista_str = [f"{p.numero} - Status: {p.status} - Tribunal: {p.tribunal.nome}" for p in processos_usuario]
        self.__tela.exibir_lista_processos(lista_str)


    def selecionar_processo(self):
        numero = self.__tela.selecionar_numero_processo()
        return self.__processo_dao.get(numero)

    def adicionar_documento(self):
        processo = self.selecionar_processo()
        if not processo:
            return

        if isinstance(self.__usuario_logado, Juiz) and self.__usuario_logado.id != processo.juiz_responsavel.id:
            self.__tela.mostrar_mensagem("Você não é o juiz responsável por este processo.")
            return

        if isinstance(self.__usuario_logado, Advogado) and self.__usuario_logado not in processo.advogados:
            self.__tela.mostrar_mensagem("Você não é advogado deste processo.")
            return

        if processo.status.lower() != "ativo":
            self.__tela.mostrar_mensagem("Não é possível adicionar documentos a um processo encerrado.")
            return

        if any(isinstance(d, Sentenca) for d in processo.documentos):
            self.__tela.mostrar_mensagem("Este processo já possui sentença. Não é possível adicionar novos documentos.")
            return
        
        documento = self.__controlador_documentos.criar_documento_pela_tela(
            self.__usuario_logado,
            processo,
            self.__controlador_usuarios.get_usuarios()
        )
        if documento:
            self.__controlador_documentos.adicionar_documento_ao_processo(processo, documento)
            self.__tela.mostrar_mensagem("Documento adicionado com sucesso!")
        else:
            self.__tela.mostrar_mensagem("Operação cancelada ou inválida.")


    def editar_processo(self):
        processo = self.selecionar_processo()
        if not processo:
            return

        while True:
            opcao = self.__tela.mostrar_menu_edicao()

            if opcao == 1:
                advogados = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() == "advogado"]
                if not advogados:
                    self.__tela.mostrar_mensagem("Nenhum advogado cadastrado.")
                    continue
                novos = self.__tela.selecionar_usuarios_por_id(advogados, "advogado")
                for a in novos:
                    if a not in processo.advogados:
                        processo.adicionar_advogado(a)
                self.__tela.mostrar_mensagem("Advogado(s) adicionados com sucesso.")

            elif opcao == 2:
                partes = [u for u in self.__controlador_usuarios.get_usuarios() if u.__class__.__name__.lower() in ["reu", "vitima"]]
                if not partes:
                    self.__tela.mostrar_mensagem("Nenhuma parte cadastrada.")
                    continue
                novos = self.__tela.selecionar_usuarios_por_id(partes, "parte")
                for p in novos:
                    if p not in processo.partes:
                        processo.adicionar_parte(p)
                self.__tela.mostrar_mensagem("Parte(s) adicionadas com sucesso.")

            elif opcao == 3:
                if not processo.advogados:
                    self.__tela.mostrar_mensagem("Nenhum advogado para remover.")
                    continue
                remover = self.__tela.selecionar_usuarios_por_id(processo.advogados, "advogado")
                for a in remover:
                    processo.remover_advogado(a)
                self.__tela.mostrar_mensagem("Advogado(s) removidos com sucesso.")

            elif opcao == 4:
                if not processo.partes:
                    self.__tela.mostrar_mensagem("Nenhuma parte para remover.")
                    continue
                remover = self.__tela.selecionar_usuarios_por_id(processo.partes, "parte")
                for p in remover:
                    processo.remover_parte(p)
                self.__tela.mostrar_mensagem("Parte(s) removidas com sucesso.")

            elif opcao == 0:
                break
            else:
                self.__tela.mostrar_mensagem("Opção inválida.")

        self.__processo_dao.update(processo.numero, processo)

    def exibir_detalhes_processo(self):
        processo = self.selecionar_processo()
        if not processo:
            self.__tela.mostrar_mensagem("Processo não encontrado.")
            return

        print(f"Número: {processo.numero}")
        print(f"Data de Abertura: {processo.data_abertura}")
        print(f"Status: {processo.status}")
        print(f"Tribunal: {processo.tribunal.nome} ({processo.tribunal.localidade})")
        print(f"Juiz Responsável: {processo.juiz_responsavel.nome} (ID {processo.juiz_responsavel.id})")
        print("\nAdvogados:")
        for adv in processo.advogados:
            print(f"- {adv.nome} (ID {adv.id})")

        print("\nPartes:")
        for parte in processo.partes:
            print(f"- {parte.nome} ({parte.__class__.__name__}) (ID {parte.id})")

        print("\nDocumentos:")
        if not processo.documentos:
            print("Nenhum documento anexado.")
        else:
            for doc in processo.documentos:
                print(f"- {doc.__class__.__name__}: {doc.titulo} (ID {doc.id})")

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
            elif opcao == 5:
                self._relatorio_tempo_medio()
            elif opcao == 6:
                self._relatorio_documentos_por_processo()
            elif opcao == 0:
                break
            else:
                self.__tela.mostrar_mensagem("Opção inválida.")


    def _relatorio_por_status(self):
        status = self.__tela.solicitar_status()
        lista = [p for p in self.__processo_dao.get_all() if p.status.lower() == status.lower()]
        self.__tela.exibir_relatorio([f"{p.numero} - {p.status}" for p in lista])

    def _relatorio_por_juiz(self):
        try:
            id_juiz = self.__tela.solicitar_id()
        except ValueError:
            self.__tela.mostrar_mensagem("ID inválido.")
            return

        lista = [p for p in self.__processo_dao.get_all() if p.juiz_responsavel.id == id_juiz]
        
        if not lista:
            self.__tela.mostrar_mensagem("Nenhum processo encontrado para o juiz informado.")
            return

        linhas = [f"{p.numero} - Status: {p.status} - Tribunal: {p.tribunal.nome}" for p in lista]
        self.__tela.exibir_relatorio(linhas)

    def _relatorio_sem_audiencia(self):
        lista = []
        for p in self.__processo_dao.get_all():
            if not any(isinstance(d, Audiencia) for d in p.documentos):
                lista.append(p)
        self.__tela.exibir_relatorio([f"{p.numero} - Sem audiência" for p in lista])

    def _relatorio_com_sentenca(self):
        lista = []
        for p in self.__processo_dao.get_all():
            if any(isinstance(d, Sentenca) for d in p.documentos):
                lista.append(p)
        self.__tela.exibir_relatorio([f"{p.numero} - Contém sentença" for p in lista])

    
    def encerrar_processo(self):
        processo = self.selecionar_processo()
        if not processo:
            return

        try:
            processo.encerrar()
            self.__processo_dao.update(processo.numero, processo)
            self.__tela.mostrar_mensagem("Processo encerrado com sucesso e arquivamento gerado.")
        except ValueError as e:
            self.__tela.mostrar_mensagem(str(e))

    def _relatorio_tempo_medio(self):
        encerrados = [p for p in self.__processo_dao.get_all() if p.status.lower() == "encerrado"]
        if not encerrados:
            self.__tela.mostrar_mensagem("Nenhum processo encerrado encontrado.")
            return

        total_dias = 0
        count = 0

        for p in encerrados:
            try:
                data_inicio = datetime.strptime(p.data_abertura, "%Y-%m-%d")
                data_fim = max(datetime.strptime(d.data_envio, "%Y-%m-%d") for d in p.documentos)
                total_dias += (data_fim - data_inicio).days
                count += 1
            except:
                continue

        media = total_dias / count if count else 0
        self.__tela.mostrar_mensagem(f"Tempo médio de tramitação: {media:.1f} dias")

    def _relatorio_documentos_por_processo(self):
        linhas = []
        for p in self.__processo_dao.get_all():
            linha = f"Processo {p.numero}: {len(p.documentos)} documento(s)"
            linhas.append(linha)
        self.__tela.exibir_relatorio(linhas)

    def get_usuarios(self):
        return self.__controlador_usuarios.get_usuarios()

    def get_tribunais(self):
        return self.__tribunais

    def get_todos_processos(self):
        return list(self.__processo_dao.get_all())

    def get_lista_processos_gui(self):
        return [f"{p.numero} - Status: {p.status} - Tribunal: {p.tribunal.nome}" for p in self.__processo_dao.get_all()]

    def criar_processo(self, numero, data_abertura, juiz, tribunal, advogados, partes, status="Ativo"):
        if self.__processo_dao.get(numero) is not None:
            raise ValueError(f"Já existe um processo com o número {numero}.")
        processo = Processo(
            numero=numero,
            data_abertura=data_abertura,
            status=status,
            juiz_responsavel=juiz,
            advogados=advogados,
            partes=partes,
            tribunal=tribunal
        )
        self.__processo_dao.add(numero, processo)


    def remover_processo(self, numero):
        self.__processo_dao.remove(numero)

    def atualizar_processo(self, processo):
        self.__processo_dao.update(processo.numero, processo)

    # RELATÓRIOS

    def relatorio_por_status(self, status):
        lista = [p for p in self.__processo_dao.get_all() if p.status.lower() == status.lower()]
        return [f"{p.numero} - {p.status}" for p in lista]

    def relatorio_por_juiz(self, id_juiz):
        lista = [p for p in self.__processo_dao.get_all() if p.juiz_responsavel.id == id_juiz]
        return [f"{p.numero} - Status: {p.status} - Tribunal: {p.tribunal.nome}" for p in lista]

    def relatorio_sem_audiencia(self):
        return [f"{p.numero} - Sem audiência"
                for p in self.__processo_dao.get_all()
                if not any(isinstance(d, Audiencia) for d in p.documentos)]

    def relatorio_com_sentenca(self):
        return [f"{p.numero} - Contém sentença"
                for p in self.__processo_dao.get_all()
                if any(isinstance(d, Sentenca) for d in p.documentos)]

    def relatorio_tempo_medio(self):
        encerrados = [p for p in self.__processo_dao.get_all() if p.status.lower() == "encerrado"]
        if not encerrados:
            return 0
        total_dias = 0
        count = 0
        for p in encerrados:
            try:
                data_inicio = datetime.strptime(p.data_abertura, "%Y-%m-%d")
                data_fim = max(datetime.strptime(d.data_envio, "%Y-%m-%d") for d in p.documentos)
                total_dias += (data_fim - data_inicio).days
                count += 1
            except Exception:
                continue
        return total_dias / count if count else 0

    def relatorio_documentos_por_processo(self):
        return [f"Processo {p.numero}: {len(p.documentos)} documento(s)"
                for p in self.__processo_dao.get_all()]
    def relatorio_com_audiencia(self):
   
        return [f"{p.numero} - Contém audiência"
            for p in self.__processo_dao.get_all()
            if any(isinstance(d, Audiencia) for d in p.documentos)]
    def get_processo_dao(self):
        return self.__processo_dao
    
    def get_processos_do_usuario(self):
        todos = self.__processo_dao.get_all()
        usuario = self.__usuario_logado

        if usuario.__class__.__name__.lower() == "juiz":
            return [p for p in todos if p.juiz_responsavel.id == usuario.id]

        elif usuario.__class__.__name__.lower() == "advogado":
            return [p for p in todos if any(adv.id == usuario.id for adv in p.advogados)]

        elif usuario.__class__.__name__.lower() == "parte":
            return [p for p in todos if any(parte.id == usuario.id for parte in p.partes)]

        else:
            return []

