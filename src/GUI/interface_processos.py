import PySimpleGUI as sg
from GUI.interface_documentos import InterfaceDocumentosGUI

class InterfaceProcessosGUI:
    def __init__(self, controlador, controlador_documentos=None):
        self.__controlador = controlador
        self.__controlador_documentos = controlador_documentos

    def abre_tela(self):
        sg.theme("DarkBlue3")
        while True:
            layout = [
                [sg.Text("GERENCIAR PROCESSOS", font=("Helvetica", 20), justification="center", expand_x=True)],
                [sg.HorizontalSeparator()],
                [sg.Button("➕  Cadastrar Processo", size=(30, 2))],
                [sg.Button("📋  Listar Processos", size=(30, 2))],
                [sg.Button("✏️  Editar Processo", size=(30, 2))],
                [sg.Button("🗑️  Remover Processo", size=(30, 2))],
                [sg.Button("📂  Adicionar Documentos", size=(30, 2))],
                [sg.Button("🧾  Relatórios", size=(30, 2))],
                [sg.Button("🔎  Detalhes do Processo", size=(30, 2))],
                [sg.Button("🔙  Voltar", size=(30, 2))]
            ]
            window = sg.Window("MiniEPROC - Processos", layout, element_justification="center")
            evento, _ = window.read()
            window.close()

            if evento in (sg.WINDOW_CLOSED, "🔙  Voltar"):
                break
            elif evento == "➕  Cadastrar Processo":
                self._cadastrar_processo()
            elif evento == "📋  Listar Processos":
                self._listar_processos()
            elif evento == "✏️  Editar Processo":
                self._editar_processo()
            elif evento == "🗑️  Remover Processo":
                self._remover_processo()
            elif evento == "📂  Adicionar Documentos":
                self._adicionar_documento()
            elif evento == "🔎  Detalhes do Processo":
                self._exibir_detalhes_processo()
            elif evento == "🧾  Relatórios":
                self._menu_relatorios()

    def _cadastrar_processo(self):
        usuarios = self.__controlador.get_usuarios()
        tribunais = self.__controlador.get_tribunais()
        usuario_logado = getattr(self.__controlador, "_ControladorProcessos__usuario_logado", None)
        if not usuario_logado or usuario_logado.__class__.__name__.lower() not in ["juiz", "advogado", "promotor"]:
            sg.popup_error("Você não tem permissão para criar processos.")
            return

        while True:
            layout_num = [
                [sg.Text("Número do Processo:"), sg.Input(key="numero")],
                [sg.Button("Avançar"), sg.Button("Cancelar")]
            ]
            window = sg.Window("Cadastrar Processo", layout_num)
            evento, valores = window.read()
            window.close()
            if evento != "Avançar":
                return
            try:
                numero = int(valores["numero"])
            except ValueError:
                sg.popup_error("Número inválido.")
                continue
            if any(p.numero == numero for p in self.__controlador.get_todos_processos()):
                sg.popup_error(f"Já existe um processo com o número {numero}.")
                continue
            break

        layout = [
            [sg.Text("Data de Abertura (YYYY-MM-DD):"), sg.Input(key="data_abertura")],
            [sg.Button("Avançar"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Cadastrar Processo", layout)
        evento, valores_2 = window.read()
        window.close()
        if evento != "Avançar":
            return
        data_abertura = valores_2["data_abertura"]

        juizes = [u for u in usuarios if u.__class__.__name__.lower() == "juiz"]
        if not juizes:
            sg.popup_error("Nenhum juiz cadastrado.")
            return
        juiz_nomes = [f"{j.id} - {j.nome}" for j in juizes]
        window = sg.Window("Selecionar Juiz", [
            [sg.Text("Selecione o Juiz responsável:")],
            [sg.Listbox(juiz_nomes, key="sel", size=(30, min(10, len(juiz_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["sel"]:
            return
        juiz_id = int(valores["sel"][0].split(" - ")[0])
        juiz = next(j for j in juizes if j.id == juiz_id)

        tribunal_nomes = [f"{t.id} - {t.nome}" for t in tribunais]
        window = sg.Window("Selecionar Tribunal", [
            [sg.Text("Selecione o Tribunal:")],
            [sg.Listbox(tribunal_nomes, key="sel", size=(30, min(10, len(tribunal_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["sel"]:
            return
        tribunal_id = int(valores["sel"][0].split(" - ")[0])
        tribunal = next(t for t in tribunais if t.id == tribunal_id)

        advogados = [u for u in usuarios if u.__class__.__name__.lower() == "advogado"]
        if not advogados:
            sg.popup_error("Nenhum advogado cadastrado.")
            return
        adv_nomes = [f"{a.id} - {a.nome}" for a in advogados]
        window = sg.Window("Selecionar Advogados", [
            [sg.Text("Selecione os advogados (CTRL para múltiplo):")],
            [sg.Listbox(adv_nomes, key="sel", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, min(10, len(adv_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["sel"]:
            return
        adv_ids = [int(n.split(" - ")[0]) for n in valores["sel"]]
        advogados_sel = [a for a in advogados if a.id in adv_ids]

        partes = [u for u in usuarios if u.__class__.__name__.lower() in ["reu", "vitima"]]
        if not partes:
            sg.popup_error("Nenhuma parte cadastrada.")
            return
        partes_nomes = [f"{p.id} - {p.nome} ({p.__class__.__name__})" for p in partes]
        window = sg.Window("Selecionar Partes", [
            [sg.Text("Selecione as partes (CTRL para múltiplo):")],
            [sg.Listbox(partes_nomes, key="sel", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, min(10, len(partes_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["sel"]:
            return
        partes_ids = [int(n.split(" - ")[0]) for n in valores["sel"]]
        partes_sel = [p for p in partes if p.id in partes_ids]

        try:
            self.__controlador.criar_processo(
                numero=numero,
                data_abertura=data_abertura,
                juiz=juiz,
                tribunal=tribunal,
                advogados=advogados_sel,
                partes=partes_sel,
            )
            sg.popup("Processo cadastrado com sucesso!")
        except Exception as e:
            sg.popup_error(str(e))



    def _listar_processos(self):
        try:
            lista = self.__controlador.get_lista_processos_gui() if hasattr(self.__controlador, "get_lista_processos_gui") \
                else [f"{p.numero} - Status: {p.status} - Tribunal: {p.tribunal.nome}" for p in getattr(self.__controlador, "_ControladorProcessos__processo_dao").get_all()]
            sg.popup_scrolled("\n".join(lista) if lista else "Nenhum processo encontrado.", title="Processos")
        except Exception as e:
            sg.popup_error(f"Erro ao listar processos: {e}")

    def _editar_processo(self):
        processos = getattr(self.__controlador, "_ControladorProcessos__processo_dao").get_all()
        if not processos:
            sg.popup("Nenhum processo para editar.")
            return
        proc_nomes = [f"{p.numero} - {p.status}" for p in processos]
        window = sg.Window("Selecionar Processo", [
            [sg.Text("Selecione o processo a editar:")],
            [sg.Listbox(proc_nomes, key="sel", size=(40, min(10, len(proc_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["sel"]:
            return
        numero = int(valores["sel"][0].split(" - ")[0])
        processo = next(p for p in processos if p.numero == numero)

        opcoes = ["Adicionar Advogado", "Adicionar Parte", "Remover Advogado", "Remover Parte", "Cancelar"]
        window = sg.Window("Editar Processo", [
            [sg.Text("O que deseja fazer?")],
            [sg.Listbox(opcoes, key="op", size=(30, len(opcoes)))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["op"]:
            return
        escolha = valores["op"][0]

        usuarios = self.__controlador.get_usuarios()
        if escolha == "Adicionar Advogado":
            advogados = [u for u in usuarios if u.__class__.__name__.lower() == "advogado"]
            adv_nomes = [f"{a.id} - {a.nome}" for a in advogados if a not in processo.advogados]
            if not adv_nomes:
                sg.popup("Nenhum advogado disponível para adicionar.")
                return
            window = sg.Window("Adicionar Advogado", [
                [sg.Text("Selecione os advogados:")],
                [sg.Listbox(adv_nomes, key="sel", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, min(10, len(adv_nomes))))],
                [sg.Button("Ok"), sg.Button("Cancelar")]
            ])
            evento, valores = window.read()
            window.close()
            if evento == "Ok" and valores["sel"]:
                adv_ids = [int(n.split(" - ")[0]) for n in valores["sel"]]
                for a in advogados:
                    if a.id in adv_ids and a not in processo.advogados:
                        processo.adicionar_advogado(a)
                self.__controlador.atualizar_processo(processo)  # Salva tudo de uma vez!
                sg.popup("Advogado(s) adicionado(s)!")
        elif escolha == "Adicionar Parte":
            partes = [u for u in usuarios if u.__class__.__name__.lower() in ["reu", "vitima"]]
            partes_nomes = [f"{p.id} - {p.nome} ({p.__class__.__name__})" for p in partes if p not in processo.partes]
            if not partes_nomes:
                sg.popup("Nenhuma parte disponível para adicionar.")
                return
            window = sg.Window("Adicionar Parte", [
                [sg.Text("Selecione as partes:")],
                [sg.Listbox(partes_nomes, key="sel", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, min(10, len(partes_nomes))))],
                [sg.Button("Ok"), sg.Button("Cancelar")]
            ])
            evento, valores = window.read()
            window.close()
            if evento == "Ok" and valores["sel"]:
                partes_ids = [int(n.split(" - ")[0]) for n in valores["sel"]]
                for p in partes:
                    if p.id in partes_ids and p not in processo.partes:
                        processo.adicionar_parte(p)
                self.__controlador.atualizar_processo(processo)
                sg.popup("Parte(s) adicionada(s)!")
        elif escolha == "Remover Advogado":
            if not processo.advogados:
                sg.popup("Nenhum advogado para remover.")
                return
            adv_nomes = [f"{a.id} - {a.nome}" for a in processo.advogados]
            window = sg.Window("Remover Advogado", [
                [sg.Text("Selecione os advogados:")],
                [sg.Listbox(adv_nomes, key="sel", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(30, min(10, len(adv_nomes))))],
                [sg.Button("Ok"), sg.Button("Cancelar")]
            ])
            evento, valores = window.read()
            window.close()
            if evento == "Ok" and valores["sel"]:
                adv_ids = [int(n.split(" - ")[0]) for n in valores["sel"]]
                for a in processo.advogados[:]:
                    if a.id in adv_ids:
                        processo.remover_advogado(a)
                self.__controlador.atualizar_processo(processo)
                sg.popup("Advogado(s) removido(s)!")
        elif escolha == "Remover Parte":
            if not processo.partes:
                sg.popup("Nenhuma parte para remover.")
                return
            partes_nomes = [f"{p.id} - {p.nome} ({p.__class__.__name__})" for p in processo.partes]
            window = sg.Window("Remover Parte", [
                [sg.Text("Selecione as partes:")],
                [sg.Listbox(partes_nomes, key="sel", select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(40, min(10, len(partes_nomes))))],
                [sg.Button("Ok"), sg.Button("Cancelar")]
            ])
            evento, valores = window.read()
            window.close()
            if evento == "Ok" and valores["sel"]:
                partes_ids = [int(n.split(" - ")[0]) for n in valores["sel"]]
                for p in processo.partes[:]:
                    if p.id in partes_ids:
                        processo.remover_parte(p)
                self.__controlador.atualizar_processo(processo)
                sg.popup("Parte(s) removida(s)!")


    def _remover_processo(self):
        processos = getattr(self.__controlador, "_ControladorProcessos__processo_dao").get_all()
        if not processos:
            sg.popup("Nenhum processo para remover.")
            return
        proc_nomes = [f"{p.numero} - {p.status}" for p in processos]
        idx, ok = sg.Window("Remover Processo", [
            [sg.Text("Selecione o processo para remover:")],
            [sg.Listbox(proc_nomes, key="sel", size=(40, min(10, len(proc_nomes))))],
            [sg.Button("Remover"), sg.Button("Cancelar")]
        ]).read(close=True)
        if ok and idx["sel"]:
            numero = int(idx["sel"][0].split(" - ")[0])
            self.__controlador.remover_processo(numero)
            sg.popup("Processo removido!")

    def _abrir_documentos_processo(self):
        # Se quiser, pode passar o processo selecionado para o controlador de documentos
        processos = getattr(self.__controlador, "_ControladorProcessos__processo_dao").get_all()
        if not processos:
            sg.popup("Nenhum processo disponível.")
            return
        proc_nomes = [f"{p.numero} - {p.status}" for p in processos]
        idx, ok = sg.Window("Selecionar Processo", [
            [sg.Text("Selecione o processo para ver os documentos:")],
            [sg.Listbox(proc_nomes, key="sel", size=(40, min(10, len(proc_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ]).read(close=True)
        if not ok or not idx["sel"]:
            return
        numero = int(idx["sel"][0].split(" - ")[0])
        processo = next(p for p in processos if p.numero == numero)
        if self.__controlador_documentos:
            self.__controlador_documentos.abrir_tela_documento(processo)
        else:
            sg.popup("Tela de documentos: funcionalidade a implementar.")

    def _menu_relatorios(self):
        relatorios = [
            "Por status",
            "Por juiz",
            "Sem audiência",
            "Com audiência",
            "Com sentença",
            "Tempo médio de tramitação",
            "Qtd de documentos por processo"
        ]
        layout = [
            [sg.Text("Selecione um relatório:")],
            [sg.Listbox(relatorios, key="rel", size=(40, len(relatorios)))],
            [sg.Button("Gerar"), sg.Button("Cancelar")]
        ]
        window = sg.Window("Relatórios", layout)
        evento, valores = window.read()
        window.close()
        if evento != "Gerar" or not valores["rel"]:
            return
        relatorio = valores["rel"][0]
        try:
            if relatorio == "Por status":
                status = sg.popup_get_text("Digite o status (Ativo/Encerrado):")
                if status:
                    linhas = self.__controlador.relatorio_por_status(status)
            elif relatorio == "Por juiz":
                usuarios = self.__controlador.get_usuarios()
                juizes = [u for u in usuarios if u.__class__.__name__.lower() == "juiz"]
                if not juizes:
                    sg.popup_error("Nenhum juiz cadastrado.")
                    return
                juiz_nomes = [f"{j.id} - {j.nome}" for j in juizes]
                window = sg.Window("Selecionar Juiz", [
                    [sg.Text("Selecione o juiz:")],
                    [sg.Listbox(juiz_nomes, key="sel", size=(30, min(10, len(juiz_nomes))))],
                    [sg.Button("Ok"), sg.Button("Cancelar")]
                ])
                evento, valores = window.read()
                window.close()
                if evento != "Ok" or not valores["sel"]:
                    return
                id_juiz = int(valores["sel"][0].split(" - ")[0])
                linhas = self.__controlador.relatorio_por_juiz(id_juiz)
                sg.popup_scrolled("\n".join(linhas) if linhas else "Nenhum dado encontrado.", title=relatorio)
            elif relatorio == "Sem audiência":
                linhas = self.__controlador.relatorio_sem_audiencia()
            elif relatorio == "Com audiência":
                linhas = self.__controlador.relatorio_com_audiencia()
            elif relatorio == "Com sentença":
                linhas = self.__controlador.relatorio_com_sentenca()
            elif relatorio == "Tempo médio de tramitação":
                media = self.__controlador.relatorio_tempo_medio()
                sg.popup(f"Tempo médio de tramitação: {media:.1f} dias")
                return
            elif relatorio == "Qtd de documentos por processo":
                linhas = self.__controlador.relatorio_documentos_por_processo()
            else:
                linhas = []
            sg.popup_scrolled("\n".join(linhas) if linhas else "Nenhum dado encontrado.", title=relatorio)
        except Exception as e:
            sg.popup_error(f"Erro ao gerar relatório: {e}")

    def _exibir_detalhes_processo(self):
        processos = self.__controlador.get_todos_processos()
        if not processos:
            sg.popup("Nenhum processo disponível.")
            return
        proc_nomes = [f"{p.numero} - {p.status}" for p in processos]
        window = sg.Window("Selecionar Processo", [
            [sg.Text("Selecione o processo para ver detalhes:")],
            [sg.Listbox(proc_nomes, key="sel", size=(40, min(10, len(proc_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["sel"]:
            return
        numero = int(valores["sel"][0].split(" - ")[0])
        processo = next(p for p in processos if p.numero == numero)
        # Monte o texto detalhado
        detalhes = f"Número: {processo.numero}\n"
        detalhes += f"Data de Abertura: {processo.data_abertura}\n"
        detalhes += f"Status: {processo.status}\n"
        detalhes += f"Tribunal: {processo.tribunal.nome} ({processo.tribunal.localidade})\n"
        detalhes += f"Juiz Responsável: {processo.juiz_responsavel.nome} (ID {processo.juiz_responsavel.id})\n\n"
        detalhes += "Advogados:\n"
        for adv in processo.advogados:
            detalhes += f"- {adv.nome} (ID {adv.id})\n"
        detalhes += "\nPartes:\n"
        for parte in processo.partes:
            detalhes += f"- {parte.nome} ({parte.__class__.__name__}) (ID {parte.id})\n"
        detalhes += "\nDocumentos:\n"
        if not processo.documentos:
            detalhes += "Nenhum documento anexado."
        else:
            for doc in processo.documentos:
                detalhes += f"- {doc.__class__.__name__}: {doc.titulo} (ID {doc.id})\n"
        sg.popup_scrolled(detalhes, title="Detalhes do Processo")

    def _adicionar_documento(self):
        processos = self.__controlador.get_todos_processos()
        if not processos:
            sg.popup("Nenhum processo disponível.")
            return
        proc_nomes = [f"{p.numero} - {p.status}" for p in processos]
        window = sg.Window("Selecionar Processo", [
            [sg.Text("Selecione o processo para adicionar documento:")],
            [sg.Listbox(proc_nomes, key="sel", size=(40, min(10, len(proc_nomes))))],
            [sg.Button("Ok"), sg.Button("Cancelar")]
        ])
        evento, valores = window.read()
        window.close()
        if evento != "Ok" or not valores["sel"]:
            return
        numero = int(valores["sel"][0].split(" - ")[0])
        processo = next(p for p in processos if p.numero == numero)
        usuario_logado = getattr(self.__controlador, "_ControladorProcessos__usuario_logado", None)

        InterfaceDocumentosGUI(self.__controlador_documentos).abre_tela(
            usuario_logado,
            processo,
            self.__controlador.get_usuarios()
        )
