from datetime import datetime
from src.module.usuario.advogado import Advogado
from src.module.usuario.juiz import Juiz

class TelaDocumentos:
    def mostrar_menu_documentos(self):
        print("\n--- Tipos de Documentos ---")
        print("1 - Acusação")
        print("2 - Defesa")
        print("3 - Audiência")
        print("4 - Sentença")
        print("0 - Cancelar")
        try:
            opcao = int(input("Escolha o tipo de documento: "))
        except ValueError:
            opcao = -1

        tipos = {1: "acusacao", 2: "defesa", 3: "audiencia", 4: "sentenca"}
        return tipos.get(opcao, None)

    def solicitar_dados_basicos(self):
        try:
            id_doc = int(input("ID do documento: "))
        except ValueError:
            print("ID inválido.")
            return None

        titulo = input("Título: ")
        descricao = input("Descrição: ")

        while True:
            data_envio = input("Data de envio (AAAA-MM-DD): ").strip()
            try:
                datetime.strptime(data_envio, "%Y-%m-%d")
                break
            except ValueError:
                print("Data inválida.")

        return {
            "id": id_doc,
            "titulo": titulo,
            "descricao": descricao,
            "data_envio": data_envio
        }

    def solicitar_dados_extra(self, tipo, processo, usuarios_disponiveis):
        dados_extra = {}

        if tipo == "acusacao":
            vitimas = [p for p in processo.partes if p.__class__.__name__.lower() == "vitima"]
            if not vitimas:
                print("Nenhuma vítima encontrada no processo.")
                return None
            print("Vítimas disponíveis:")
            for v in vitimas:
                print(f"{v.id} - {v.nome}")
            try:
                id_vitima = int(input("Escolha o ID da vítima: "))
                selecionado = next((v for v in vitimas if v.id == id_vitima), None)
                if not selecionado:
                    print("Vítima não encontrada.")
                    return None
                dados_extra["vitima"] = selecionado
            except ValueError:
                print("ID inválido.")
                return None

        elif tipo == "defesa":
            reus = [p for p in processo.partes if p.__class__.__name__.lower() == "reu"]
            if not reus:
                print("Nenhum réu encontrado no processo.")
                return None
            print("Réus disponíveis:")
            for r in reus:
                print(f"{r.id} - {r.nome}")
            try:
                id_reu = int(input("Escolha o ID do réu: "))
                selecionado = next((r for r in reus if r.id == id_reu), None)
                if not selecionado:
                    print("Réu não encontrado.")
                    return None
                dados_extra["reu"] = selecionado
            except ValueError:
                print("ID inválido.")
                return None

        elif tipo == "sentenca":
            reus = [p for p in processo.partes if p.__class__.__name__.lower() == "reu"]
            vitimas = [p for p in processo.partes if p.__class__.__name__.lower() == "vitima"]

            if not reus or not vitimas:
                print("Processo precisa de ao menos um réu e uma vítima.")
                return None

            dados_extra["reu"] = reus[0]
            dados_extra["vitima"] = vitimas[0]

        elif tipo == "audiencia":
            data_audiencia = input("Data da audiência (AAAA-MM-DD): ")
            dados_extra["data"] = data_audiencia

            juizes = [u for u in usuarios_disponiveis if isinstance(u, Juiz)]
            advogados = [u for u in usuarios_disponiveis if isinstance(u, Advogado)]

            if not advogados:
                print("Nenhum advogado disponível.")
                return None

            print("\nAdvogados disponíveis:")
            for adv in advogados:
                print(f"{adv.id} - {adv.nome}")
            try:
                id_adv = int(input("Escolha o ID do advogado responsável: "))
                selecionado = next((a for a in advogados if a.id == id_adv), None)
                if not selecionado:
                    print("Advogado não encontrado.")
                    return None
                dados_extra["advogado_responsavel"] = selecionado
            except ValueError:
                print("ID inválido.")
                return None

        return dados_extra
