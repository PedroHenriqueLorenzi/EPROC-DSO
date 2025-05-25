from abstractDocumento import Documento, Usuario

class Sentenca(Documento):
    def __init__(self, id, titulo, descricao, data_envio, autor, juiz_sentenciante, parte_afetada):
        super().__init__(id, titulo, descricao, data_envio, autor)
        self.__juiz_sentenciante = juiz_sentenciante    
        self.__parte_afetada = parte_afetada             

    def juiz_sentenciante(self):
        return self.__juiz_sentenciante

    def parte_afetada(self):
        return self.__parte_afetada