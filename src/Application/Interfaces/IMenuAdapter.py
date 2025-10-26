from abc import ABC, abstractmethod


class IMenuAdapter(ABC):
    @abstractmethod
    def generateContentFile(self):
        pass

    @abstractmethod
    def getFileExtension(self):
        pass