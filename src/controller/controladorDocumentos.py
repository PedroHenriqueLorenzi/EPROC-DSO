from module.documento.acusacao import Acusacao
from module.documento.defesa import Defesa
from module.documento.audiencia import Audiencia
from module.documento.sentenca import Sentenca
from module.usuario.juiz import Juiz
from module.usuario.advogado import Advogado
from view.telaDocumentos import TelaDocumentos

class ControladorDocumentos:
    def __init__(self, processo_dao):
        self.__tela_documentos = TelaDocumentos()
        self.__processo_dao = processo_dao

    def adicionar_documento_ao_processo(self, processo, documento):
        processo.adicionar_documento(documento)
        self.__processo_dao.update(processo.numero, processo)

    def abrir_tela_documento(self, usuario_logado, processo, lista_usuarios):
        tipo = self.__tela_documentos.mostrar_menu_documentos()
        if not tipo:
            print(">>> Operação cancelada.")
            return

        dados_basicos = self.__tela_documentos.solicitar_dados_basicos()
        if not dados_basicos:
            print(">>> Falha ao obter dados básicos.")
            return

        dados_extra = self.__tela_documentos.solicitar_dados_extra(tipo, processo, processo.advogados)

        if dados_extra is None:
            print(">>> Falha ao obter dados específicos.")
            return

        dados_doc = {**dados_basicos, **dados_extra}

        try:
            documento = self.criar_documento(tipo, dados_doc, usuario_logado, processo)
            processo.adicionar_documento(documento)
            self.__controlador_processos.get_processo_dao().update(processo.numero, processo)
            print(f">>> {tipo.capitalize()} adicionada ao processo.")
        except (PermissionError, ValueError) as e:
            print(f">>> Erro: {str(e)}")

    def criar_documento(self, tipo, dados: dict, autor, processo):
        if tipo == "sentenca":
            if autor.__class__.__name__.lower() != "juiz":
                raise PermissionError("Apenas juízes podem emitir sentenças.")
            if "reu" not in dados or "vitima" not in dados:
                raise ValueError("Sentenças exigem réu e vítima.")
            return Sentenca(**dados, autor=autor)

        elif tipo == "acusacao":
            if autor.__class__.__name__.lower() != "advogado":
                raise PermissionError("Apenas advogados podem emitir acusações.")
            if "vitima" not in dados:
                raise ValueError("Acusações exigem uma vítima.")
            return Acusacao(**dados, autor=autor)

        elif tipo == "defesa":
            if autor.__class__.__name__.lower() != "advogado":
                raise PermissionError("Apenas advogados podem emitir defesas.")
            if "reu" not in dados:
                raise ValueError("Defesas exigem um réu.")
            return Defesa(**dados, autor=autor)

        elif tipo == "audiencia":
            if autor.__class__.__name__.lower() != "juiz":
                raise PermissionError("Apenas juízes podem marcar audiências.")
            if "data_audiencia" not in dados or "advogado" not in dados:
                raise ValueError("Audiências exigem um advogado e uma data.")
            
            juiz_responsavel = autor
            advogado_responsavel = dados.pop("advogado")
            data_audiencia = dados.pop("data_audiencia")

            return Audiencia(
                id=dados["id"],
                titulo=dados["titulo"],
                descricao=dados["descricao"],
                data_envio=dados["data_envio"],
                autor=advogado_responsavel,
                juiz_responsavel=juiz_responsavel,
                data=data_audiencia
            )

        elif tipo == "arquivamento":
            raise PermissionError("Arquivamentos são gerados automaticamente ao encerrar o processo.")

        else:
            raise ValueError("Tipo de documento inválido.")

    def get_proximo_id(self, processo):
        if not processo.documentos:
            return 1
        return max(doc.id for doc in processo.documentos) + 1
    
    def validar_permissao_documento(self, tipo: str, usuario):

        if tipo == "sentenca" and not isinstance(usuario, Juiz):
            raise PermissionError("Apenas juízes podem emitir sentenças.")
        elif tipo in ("acusacao", "defesa") and not isinstance(usuario, Advogado):
            raise PermissionError("Apenas advogados podem criar acusações ou defesas.")
        elif tipo == "audiencia" and not isinstance(usuario, Juiz):
            raise PermissionError("Apenas juízes podem marcar audiências.")
