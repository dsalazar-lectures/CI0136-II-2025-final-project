# component interface
from abc import ABC, abstractmethod


class IFilter(ABC):

    @abstractmethod
    def filter(self, criteria):
        pass
