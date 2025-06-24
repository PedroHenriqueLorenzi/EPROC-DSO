import pickle
import os
from abc import ABC, abstractmethod

class AbstractDAO(ABC):
    @abstractmethod
    def __init__(self, filename=''):
        self.__datasource = os.path.join('src', 'database', filename)
        self.__cache = {}

        if not os.path.exists(os.path.dirname(self.__datasource)):
            os.makedirs(os.path.dirname(self.__datasource))

        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        with open(self.__datasource, 'wb') as file:
            pickle.dump(self.__cache, file)

    def __load(self):
        with open(self.__datasource, 'rb') as file:
            self.__cache = pickle.load(file)

    def add(self, key, obj):
        self.__cache[key] = obj
        self.__dump()

    def update(self, key, obj):
        try:
            if self.__cache[key] is not None:
                self.__cache[key] = obj
                self.__dump()
        except KeyError:
            pass 

    def get(self, key):
        try:
            return self.__cache[key]
        except KeyError:
            pass 

    def remove(self, key):
        try:
            self.__cache.pop(key)
            self.__dump()
        except KeyError:
            pass

    def get_all(self):
        return self.__cache.values()
