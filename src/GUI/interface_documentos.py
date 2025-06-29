import PySimpleGUI as sg
from datetime import datetime

class InterfaceDocumentosGUI:
    def __init__(self, controlador_documentos):
        self.__controlador = controlador_documentos

    def abre_tela(self, usuario_logado, processo, lista_usuarios):
        tipos = [
            ("Acusação", "acusacao"),
            ("Defesa", "defesa"),
            ("Audiência", "audiencia"),
            ("Sentença", "sentenca"),
        ]
        sg.theme("DarkBlue3")
        layout_tipo = [
            [sg.Text("Novo Documento no Processo", font=("Helvetica", 18), justification="center", expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Text("Selecione o tipo de documento:", font=("Helvetica", 13))],
            [sg.Listbox([t[0] for t in tipos], key="tipo", size=(28, 4), font=("Helvetica", 12), expand_x=True)],
            [sg.Push(), sg.Button("Avançar", size=(12, 1)), sg.Button("Cancelar", size=(12, 1)), sg.Push()]
        ]
        window = sg.Window("Adicionar Documento", layout_tipo, element_justification="center")
        evento, valores = window.read()
        window.close()
        if evento != "Avançar" or not valores["tipo"]:
            return
        tipo_nome = valores["tipo"][0]
        tipo = dict(tipos)[tipo_nome]

        while True:
            layout_dados = [
                [sg.Text("Dados Básicos do Documento", font=("Helvetica", 15), justification="center", expand_x=True)],
                [sg.HorizontalSeparator()],
                [sg.Text("Título:", size=(15,1)), sg.Input(key="titulo", size=(40,1))],
                [sg.Text("Descrição:", size=(15,1)), sg.Input(key="descricao", size=(40,1))],
                [sg.Text("Data de envio:", size=(15,1)), sg.Input(key="data_envio", size=(20,1)), sg.Text("AAAA-MM-DD", font=("Helvetica", 9, "italic"))],
                [sg.Push(), sg.Button("Avançar", size=(12, 1)), sg.Button("Cancelar", size=(12, 1)), sg.Push()]
            ]
            window = sg.Window("Dados Básicos do Documento", layout_dados, element_justification="center")
            evento, valores = window.read()
            window.close()
            if evento != "Avançar":
                return

            titulo = valores["titulo"]
            descricao = valores["descricao"]
            data_envio = valores["data_envio"]

            try:
                datetime.strptime(data_envio, "%Y-%m-%d")
                break
            except ValueError:
                sg.popup_error("Formato de data inválido. Use AAAA-MM-DD.")

        id_doc = self.__controlador.get_proximo_id(processo)
        dados_extra = {}

        if tipo == "acusacao":
            vitimas = [p for p in processo.partes if p.__class__.__name__.lower() == "vitima"]
            if not vitimas:
                sg.popup_error("Nenhuma vítima encontrada no processo.")
                return
            nomes = [f"{v.id} - {v.nome}" for v in vitimas]
            layout = [
                [sg.Text("Vítima Relacionada", font=("Helvetica", 15), justification="center", expand_x=True)],
                [sg.HorizontalSeparator()],
                [sg.Text("Selecione a vítima:", font=("Helvetica", 12))],
                [sg.Listbox(nomes, key="sel", size=(30, min(5, len(nomes))), font=("Helvetica", 12), expand_x=True)],
                [sg.Push(), sg.Button("Ok", size=(12, 1)), sg.Button("Cancelar", size=(12, 1)), sg.Push()]
            ]
            window = sg.Window("Selecionar Vítima", layout, element_justification="center")
            evento, valores = window.read()
            window.close()
            if evento != "Ok" or not valores["sel"]:
                return
            id_vitima = int(valores["sel"][0].split(" - ")[0])
            dados_extra["vitima"] = next(v for v in vitimas if v.id == id_vitima)

        elif tipo == "defesa":
            reus = [p for p in processo.partes if p.__class__.__name__.lower() == "reu"]
            if not reus:
                sg.popup_error("Nenhum réu encontrado no processo.")
                return
            nomes = [f"{r.id} - {r.nome}" for r in reus]
            layout = [
                [sg.Text("Réu Relacionado", font=("Helvetica", 15), justification="center", expand_x=True)],
                [sg.HorizontalSeparator()],
                [sg.Text("Selecione o réu:", font=("Helvetica", 12))],
                [sg.Listbox(nomes, key="sel", size=(30, min(5, len(nomes))), font=("Helvetica", 12), expand_x=True)],
                [sg.Push(), sg.Button("Ok", size=(12, 1)), sg.Button("Cancelar", size=(12, 1)), sg.Push()]
            ]
            window = sg.Window("Selecionar Réu", layout, element_justification="center")
            evento, valores = window.read()
            window.close()
            if evento != "Ok" or not valores["sel"]:
                return
            id_reu = int(valores["sel"][0].split(" - ")[0])
            dados_extra["reu"] = next(r for r in reus if r.id == id_reu)

        elif tipo == "sentenca":
            reus = [p for p in processo.partes if p.__class__.__name__.lower() == "reu"]
            vitimas = [p for p in processo.partes if p.__class__.__name__.lower() == "vitima"]
            if not reus or not vitimas:
                sg.popup_error("O processo precisa de ao menos um réu e uma vítima.")
                return
            dados_extra["reu"] = reus[0]
            dados_extra["vitima"] = vitimas[0]

        elif tipo == "audiencia":
            while True:
                layout = [
                    [sg.Text("Audiência", font=("Helvetica", 15), justification="center", expand_x=True)],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Data da audiência:", size=(18,1)), sg.Input(key="data_audiencia", size=(20,1)), sg.Text("AAAA-MM-DD", font=("Helvetica", 9, "italic"))],
                    [sg.Push(), sg.Button("Avançar", size=(12, 1)), sg.Button("Cancelar", size=(12, 1)), sg.Push()]
                ]
                window = sg.Window("Data da Audiência", layout, element_justification="center")
                evento, valores = window.read()
                window.close()
                if evento != "Avançar":
                    return

                data_audiencia = valores["data_audiencia"]
                try:
                    datetime.strptime(data_audiencia, "%Y-%m-%d")
                    break
                except ValueError:
                    sg.popup_error("Formato de data inválido. Use AAAA-MM-DD.")

            dados_extra["data_audiencia"] = data_audiencia

            advogados = [u for u in lista_usuarios if u.__class__.__name__.lower() == "advogado"]
            if not advogados:
                sg.popup_error("Nenhum advogado disponível.")
                return
            nomes = [f"{a.id} - {a.nome}" for a in advogados]
            layout = [
                [sg.Text("Advogado Responsável", font=("Helvetica", 15), justification="center", expand_x=True)],
                [sg.HorizontalSeparator()],
                [sg.Text("Selecione o advogado:", font=("Helvetica", 12))],
                [sg.Listbox(nomes, key="sel", size=(30, min(5, len(nomes))), font=("Helvetica", 12), expand_x=True)],
                [sg.Push(), sg.Button("Ok", size=(12, 1)), sg.Button("Cancelar", size=(12, 1)), sg.Push()]
            ]
            window = sg.Window("Selecionar Advogado", layout, element_justification="center")
            evento, valores = window.read()
            window.close()
            if evento != "Ok" or not valores["sel"]:
                return
            id_adv = int(valores["sel"][0].split(" - ")[0])
            dados_extra["advogado"] = next(a for a in advogados if a.id == id_adv)

        dados_doc = {
            "id": id_doc,
            "titulo": titulo,
            "descricao": descricao,
            "data_envio": data_envio,
            **dados_extra
        }
        try:
            documento = self.__controlador.criar_documento(tipo, dados_doc, usuario_logado, processo)
            processo.adicionar_documento(documento)
            sg.popup(f"{tipo_nome} adicionada ao processo com sucesso!")
        except (PermissionError, ValueError) as e:
            sg.popup_error(str(e))
        except Exception as e:
            sg.popup_error(f"Erro ao adicionar documento: {e}")
