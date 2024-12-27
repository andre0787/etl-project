import os
import pytest
import pandas as pd
from etl_project.extractors.csv_extractor import CSVExtractor

@pytest.fixture
def test_data_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'test_data', 'dados_vendas_teste.csv')

def test_csv_extractor_read_success(test_data_path):
    """Testa se o extrator lê corretamente um arquivo CSV válido"""
    extractor = CSVExtractor(test_data_path)
    data = extractor.extract()
    
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 4
    assert all(col in data.columns for col in ['data', 'produto', 'quantidade', 'preco_unitario'])

def test_csv_extractor_file_not_found():
    """Testa se o extrator lida corretamente com arquivo inexistente"""
    extractor = CSVExtractor('arquivo_inexistente.csv')
    with pytest.raises(FileNotFoundError):
        extractor.extract()

def test_csv_extractor_data_types(test_data_path):
    """Testa se os tipos de dados estão corretos após a extração"""
    extractor = CSVExtractor(test_data_path)
    data = extractor.extract()
    
    assert pd.api.types.is_datetime64_any_dtype(data['data'])
    assert pd.api.types.is_numeric_dtype(data['quantidade'])
    assert pd.api.types.is_numeric_dtype(data['preco_unitario'])
