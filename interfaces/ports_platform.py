import abc


class AbstractPlatform(abc.ABC):
    def __init__(self):
        super().__init__()

    def connect(self):
        pass
