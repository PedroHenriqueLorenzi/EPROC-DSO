class TelaProcessos:
    def mostrar_menu(self) -> int:
        print("\n--- MENU DE PROCESSOS ---")
        print("1 - Criar novo processo")
        print("2 - Listar processos")
        print("3 - Adicionar documento a processo")
        print("4 - Encerrar processo")
        print("5 - Gerar relatório de processos")
        print("0 - Voltar ao menu principal")
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    def mostrar_mensagem(self, mensagem: str):
        print(f">>> {mensagem}")

    def ler_dados_processo(self) -> dict:
        print("\n--- Cadastro de Processo ---")
        numero = input("Número do processo: ").strip()
        data_abertura = input("Data de abertura (AAAA-MM-DD): ").strip()
        juiz = input("Nome do juiz responsável: ").strip()  # será substituído no controlador
        advogados = input("Nomes dos advogados (separados por vírgula): ").split(",")
        partes = input("Nomes das partes (separados por vírgula): ").split(",")

        return {
            "numero": numero,
            "data_abertura": data_abertura,
            "juiz": juiz,
            "advogados": [a.strip() for a in advogados if a.strip()],
            "partes": [p.strip() for p in partes if p.strip()]
        }

    def exibir_lista_processos(self, lista: list[str]):
        print("\n--- Lista de Processos ---")
        if not lista:
            print("Nenhum processo encontrado.")
        else:
            for item in lista:
                print(item)

    def selecionar_numero_processo(self) -> str:
        return input("Digite o número do processo: ").strip()

    def ler_dados_documento(self) -> tuple[str, dict]:
        print("\n--- Adicionar Documento ---")
        tipo = input("Tipo de documento (acusacao / defesa / audiencia / sentenca / arquivamento): ").strip().lower()
        id_doc = int(input("ID do documento: ").strip())
        titulo = input("Título do documento: ").strip()
        descricao = input("Descrição: ").strip()
        data_envio = input("Data de envio (AAAA-MM-DD): ").strip()

        dados = {
            "id": id_doc,
            "titulo": titulo,
            "descricao": descricao,
            "data_envio": data_envio
            # o autor será definido pelo controlador
        }

        # Campos específicos opcionais
        if tipo == "arquivamento":
            dados["motivo"] = input("Motivo do arquivamento: ").strip()
        elif tipo == "audiencia":
            dados["data"] = input("Data da audiência (AAAA-MM-DD): ").strip()

        return tipo, dados

    def exibir_relatorio(self, relatorio: list[str]):
        print("\n--- Relatório de Processos ---")
        if not relatorio:
            print("Nenhum dado encontrado.")
        else:
            for linha in relatorio:
                print(linha)

    def selecionar_tribunal(self, tribunais: list):
        print("\n--- Tribunais Disponíveis ---")
        for t in tribunais:
            print(f"{t.id()} - {t.nome()} ({t.localidade()})")
        try:
            id_escolhido = int(input("Digite o ID do tribunal a ser vinculado: "))
            for t in tribunais:
                if t.id() == id_escolhido:
                    return t
        except ValueError:
            return None
        return None