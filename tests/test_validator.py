"""
Testes para o módulo de validação de vendas
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from etl_project.validators.vendas_validator import VendasValidator

@pytest.fixture
def validator():
    """
    Fixture que retorna um validador de vendas
    """
    return VendasValidator()

@pytest.fixture
def valid_data():
    """
    Fixture que retorna dados válidos para uma venda
    """
    return {
        'date': datetime(2024, 1, 1),
        'product': 'Produto A',
        'quantity': 10,
        'price': 100.50
    }

def test_validate_success(validator, valid_data):
    """
    Testa validação com dados válidos
    """
    result = validator.validate(valid_data)
    assert result['product'] == 'Produto A'
    assert result['quantity'] == 10
    assert result['price'] == 100.50
    assert result['total_value'] == 1005.0

def test_validate_empty_product(validator, valid_data):
    """
    Testa validação com produto vazio
    """
    valid_data['product'] = ''
    with pytest.raises(ValidationError, match="Nome do produto não pode estar vazio"):
        validator.validate(valid_data)

def test_validate_invalid_quantity(validator, valid_data):
    """
    Testa validação com quantidade inválida
    """
    valid_data['quantity'] = 0
    with pytest.raises(ValidationError, match="Input should be greater than 0"):
        validator.validate(valid_data)

def test_validate_invalid_price(validator, valid_data):
    """
    Testa validação com preço inválido
    """
    valid_data['price'] = -1
    with pytest.raises(ValidationError, match="Input should be greater than 0"):
        validator.validate(valid_data)

def test_validate_missing_field(validator, valid_data):
    """
    Testa validação com campo faltando
    """
    del valid_data['product']
    with pytest.raises(ValidationError, match="Field required"):
        validator.validate(valid_data)

def test_validate_extra_field(validator, valid_data):
    """
    Testa validação com campo extra
    """
    valid_data['extra'] = 'extra'
    result = validator.validate(valid_data)
    assert 'extra' not in result

def test_validate_whitespace_product(validator, valid_data):
    """
    Testa validação com produto contendo apenas espaços
    """
    valid_data['product'] = '   '
    with pytest.raises(ValidationError, match="Nome do produto não pode estar vazio"):
        validator.validate(valid_data)

def test_validate_total_value_provided(validator, valid_data):
    """
    Testa validação com valor total fornecido
    """
    valid_data['total_value'] = 2000.0
    result = validator.validate(valid_data)
    assert result['total_value'] == 2000.0
