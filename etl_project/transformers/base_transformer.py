from abc import ABC, abstractmethod

class BaseTransformer(ABC):
    """Base class for all transformers"""
    
    @abstractmethod
    def transform(self, data):
        """Transform the extracted data"""
        pass
