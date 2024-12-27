from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """Base class for all loaders"""
    
    @abstractmethod
    def load(self, data):
        """Load the transformed data to destination"""
        pass
