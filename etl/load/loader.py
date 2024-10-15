"""
Loader Base Class
"""
from abc import ABC, abstractmethod

class Loader(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass