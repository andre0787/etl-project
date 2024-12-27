"""
Módulo para validação dos dados de vendas
"""
import logging
from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator

logger = logging.getLogger(__name__)

class VendaModel(BaseModel):
    """
    Modelo para validação dos dados de uma venda
    """
    date: datetime
    product: str
    quantity: int
    price: float
    total_value: float | None = None

    @field_validator('product')
    @classmethod
    def validate_product(cls, v: str) -> str:
        """
        Valida o nome do produto
        """
        if not v.strip():
            raise ValueError("Nome do produto não pode estar vazio")
        return v.strip()

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v: int) -> int:
        """
        Valida a quantidade
        """
        if v <= 0:
            raise ValueError("Input should be greater than 0")
        return v

    @field_validator('price')
    @classmethod
    def validate_price(cls, v: float) -> float:
        """
        Valida o preço
        """
        if v <= 0:
            raise ValueError("Input should be greater than 0")
        return v

    @model_validator(mode='after')
    def calculate_total_value(self) -> 'VendaModel':
        """
        Calcula o valor total se não fornecido
        """
        if self.total_value is None:
            self.total_value = self.quantity * self.price
        return self

class VendasValidator:
    """
    Classe para validação dos dados de vendas
    """
    def __init__(self):
        """
        Inicializa o validador
        """
        logger.info("Inicializando VendasValidator")

    def validate(self, data: dict) -> dict:
        """
        Valida os dados de uma venda

        Args:
            data: Dicionário com os dados da venda

        Returns:
            Dicionário com os dados validados

        Raises:
            ValidationError: Se os dados forem inválidos
        """
        try:
            logger.debug(f"Validando dados: {data}")
            venda = VendaModel(**data)
            return venda.model_dump()
        except Exception as e:
            logger.error(f"Erro na validação dos dados: {str(e)}")
            raise
