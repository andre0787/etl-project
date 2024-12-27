"""
Testes para o módulo extractor
"""
import os
import pandas as pd
import pytest
from datetime import datetime
from etl_project.extractors.csv_extractor import CSVExtractor
from etl_project.utils.config import Config
from pydantic import ValidationError

@pytest.fixture
def config():
    """
    Fixture que retorna uma instância da configuração
    """
    return Config()

@pytest.fixture
def temp_csv_file(tmp_path):
    """
    Fixture que cria um arquivo CSV temporário com dados válidos
    """
    filepath = os.path.join(tmp_path, "vendas.csv")
    df = pd.DataFrame({
        'data': ['2024-01-01', '2024-01-02'],
        'produto': ['Produto A', 'Produto B'],
        'quantidade': [10, 5],
        'preco_unitario': [100.50, 50.25]
    })
    df.to_csv(filepath, index=False)
    return filepath

@pytest.fixture
def temp_csv_invalid(tmp_path):
    """
    Fixture que cria um arquivo CSV temporário com dados inválidos
    """
    filepath = os.path.join(tmp_path, "vendas_invalido.csv")
    df = pd.DataFrame({
        'data': ['2024-01-01', '2024-01-02'],
        'produto': ['', 'Produto B'],  # Produto vazio
        'quantidade': [0, 5],  # Quantidade inválida
        'preco_unitario': [-1, 50.25]  # Preço inválido
    })
    df.to_csv(filepath, index=False)
    return filepath

def test_csv_extractor_read_success(temp_csv_file):
    """
    Testa se o extrator lê corretamente o arquivo CSV
    """
    extractor = CSVExtractor(temp_csv_file)
    df = extractor.extract()
    
    assert len(df) == 2
    assert 'date' in df.columns
    assert 'product' in df.columns
    assert 'quantity' in df.columns
    assert 'price' in df.columns
    assert 'total_value' in df.columns
    
    assert isinstance(df['date'].iloc[0], datetime)
    assert df['quantity'].iloc[0] == 10
    assert df['price'].iloc[0] == 100.50
    assert df['total_value'].iloc[0] == 1005.0

def test_csv_extractor_file_not_found():
    """
    Testa se o extrator lida corretamente com arquivo inexistente
    """
    extractor = CSVExtractor("arquivo_inexistente.csv")
    with pytest.raises(FileNotFoundError):
        extractor.extract()

def test_csv_extractor_invalid_data(temp_csv_invalid):
    """
    Testa se o extrator lida corretamente com dados inválidos
    """
    extractor = CSVExtractor(temp_csv_invalid)
    with pytest.raises(ValidationError):
        extractor.extract()

def test_csv_extractor_data_types(temp_csv_file):
    """
    Testa se os tipos de dados são convertidos corretamente
    """
    extractor = CSVExtractor(temp_csv_file)
    df = extractor.extract()
    
    assert pd.api.types.is_datetime64_any_dtype(df['date'])
    assert pd.api.types.is_string_dtype(df['product'])
    assert pd.api.types.is_integer_dtype(df['quantity'])
    assert pd.api.types.is_float_dtype(df['price'])
    assert pd.api.types.is_float_dtype(df['total_value'])
