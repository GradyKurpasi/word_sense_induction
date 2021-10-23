"""
This module defines Ports (Interfaces) 

"""
import abc


class AbstractRepository(abc.ABC):
    def __init__(self):
        super().__init__()

    def add_symbol(self, symbol):
        self._add(symbol)
    
    def get_symbol(self, symbol):
        self._get(symbol)
    

class AbstractSource(abc.ABC):
    """
    Port/Interface for corpora (text, sound, video, etc).
    Used to stream input from text sources
    FUTURE: input from websites, audio, video sources etc.
    """

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def open(self):
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError
        
    @abc.abstractmethod
    def read(self):
        raise NotImplementedError


