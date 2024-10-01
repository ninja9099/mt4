from abc import ABC, abstractmethod

class DataProvider(ABC):
    @abstractmethod
    def fetch_historic_data(self, symbol, start, end):
        pass
