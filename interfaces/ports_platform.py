import abc


class AbstractPlatform(abc.ABC):
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError
