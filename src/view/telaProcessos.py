
class TelaProcessos:
    def mostrar_menu(self) -> int:
        print("\n=== MENU DE PROCESSOS ===")
        print("1 - Criar novo processo")
        print("2 - Listar processos")
        print("3 - Adicionar documento")
        print("4 - Encerrar processo")
        print("5 - Gerar relatório")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def mostrar_mensagem(self, mensagem: str):
        print(f">>> {mensagem}")

    def ler_dados_processo(self) -> dict:
        print("\n--- Cadastro de Processo ---")
        numero = int(input("Número do processo: "))
        data_abertura = input("Data de abertura (AAAA-MM-DD): ")
        juiz = input("Juiz responsável (objeto esperado): ")
        advogados = input("Advogados (lista de objetos esperada): ")
        partes = input("Partes (lista de objetos esperada): ")
        return {
            "numero": numero,
            "data_abertura": data_abertura,
            "juiz": juiz,
            "advogados": advogados,
            "partes": partes
        }

    def selecionar_tribunal(self, tribunais: list):
        print("\n--- Selecionar Tribunal ---")
        for t in tribunais:
            print(f"{t.id} - {t.nome} ({t.localidade})")
        try:
            id_escolhido = int(input("Digite o ID do tribunal: "))
            for t in tribunais:
                if t.id == id_escolhido:
                    return t
        except ValueError:
            pass
        return None

    def exibir_lista_processos(self, lista: list):
        print("\n--- Lista de Processos ---")
        for item in lista:
            print(item)

    def selecionar_numero_processo(self) -> int:
        try:
            return int(input("Digite o número do processo: "))
        except ValueError:
            return -1

    def ler_dados_documento(self):
        print("\n--- Adicionar Documento ---")
        tipo = input("Tipo de documento (acusacao/defesa/audiencia/sentenca): ").lower()
        id_doc = int(input("ID do documento: "))
        titulo = input("Título: ")
        descricao = input("Descrição: ")
        data_envio = input("Data de envio (AAAA-MM-DD): ")
        return tipo, {
            "id": id_doc,
            "titulo": titulo,
            "descricao": descricao,
            "data_envio": data_envio
        }

    def exibir_relatorio(self, linhas: list):
        print("\n--- RELATÓRIO ---")
        if not linhas:
            print("Nenhum dado encontrado.")
        for linha in linhas:
            print(linha)

    def mostrar_menu_relatorio(self) -> int:
        print("\n--- Relatórios Disponíveis ---")
        print("1 - Por status")
        print("2 - Por juiz")
        print("3 - Sem audiência")
        print("4 - Com sentença")
        print("0 - Voltar")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def solicitar_status(self) -> str:
        return input("Digite o status (Ativo/Encerrado): ")

    def solicitar_nome_juiz(self) -> str:
        return input("Digite o nome do juiz: ")
