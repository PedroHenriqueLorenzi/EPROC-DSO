from abc import ABC,abstractmethod
from src.module.usuario.abstractUsuario import Usuario
class Documento(ABC):
    @abstractmethod
    def __init__(self, id: int, titulo: str, descricao: str, data_envio: str, autor: Usuario):
        self.__id = id
        self.__titulo = titulo
        self.__descricao = descricao
        self.__data_envio = data_envio
        self.__autor = autor

    @property
    def ide(self):
        return self.__id

    @ide.setter
    def ide(self, id: int):
        if isinstance(id, int): self.__id = id

    @property
    def titulo(self):
        return self.__titulo
    
    @titulo.setter
    def titulo(self, titulo: str):
        if isinstance(titulo, str): self.__titulo = titulo

    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def data_envio(self, str):
        return self.__data_envio
    
    @data_envio.setter
    def data_envio(self, data_envio: str):
        self.__data_envio = data_envio

    @property
    def autor(self):
        return self.__autor
    
