"""
Testes para o módulo extractor
"""
import logging
import pytest
import pandas as pd
from pathlib import Path
from etl_project.extractors.csv_extractor import CSVExtractor

@pytest.fixture
def test_data_path():
    """Retorna o caminho para o arquivo de teste"""
    return str(Path(__file__).parent / 'test_data' / 'dados_vendas_teste.csv')

def test_csv_extractor_read_success(test_data_path):
    """Testa se o extrator lê o arquivo CSV com sucesso"""
    extractor = CSVExtractor(test_data_path)
    result = extractor.extract()
    
    assert isinstance(result, dict)
    assert 'data' in result
    assert isinstance(result['data'], pd.DataFrame)
    assert len(result['data']) > 0

def test_csv_extractor_file_not_found():
    """Testa se o extrator lança erro quando arquivo não existe"""
    with pytest.raises(FileNotFoundError):
        extractor = CSVExtractor('arquivo_inexistente.csv')
        extractor.extract()

def test_csv_extractor_data_types(caplog, test_data_path):
    """Testa se o extrator converte corretamente os tipos de dados"""
    # Configurar logging para capturar mensagens
    caplog.set_level(logging.DEBUG)
    
    # Criar e executar extrator
    extractor = CSVExtractor(test_data_path)
    result = extractor.extract()
    
    # Verificar conversão de tipos
    assert pd.api.types.is_datetime64_any_dtype(result['data']['data'])
    assert pd.api.types.is_numeric_dtype(result['data']['quantidade'])
    assert pd.api.types.is_numeric_dtype(result['data']['preco_unitario'])
    
    # Verificar logs
    assert "Convertendo coluna 'data' para datetime" in caplog.text
