"""
Testes para o módulo loader
"""
import os
import pandas as pd
import pytest
from datetime import datetime
from etl_project.loaders.excel_loader import ExcelLoader

@pytest.fixture
def sample_data():
    """
    Fixture com dados de exemplo para testes
    """
    return pd.DataFrame({
        'data': [datetime(2024, 1, 1), datetime(2024, 1, 2)],
        'produto': ['A', 'B'],
        'quantidade': [10, 5],
        'valor_total': [100.0, 50.0]
    })

@pytest.fixture
def temp_dir(tmp_path):
    """
    Fixture que cria um diretório temporário para testes
    """
    return str(tmp_path)

def test_excel_loader_save_success(sample_data, temp_dir):
    """
    Testa se o loader salva corretamente o arquivo Excel
    """
    loader = ExcelLoader(temp_dir)
    filename = "test_output.xlsx"
    
    # Salvar arquivo
    loader.save(sample_data, filename)
    
    # Verificar se arquivo foi criado
    filepath = os.path.join(temp_dir, filename)
    assert os.path.exists(filepath)
    
    # Verificar conteúdo
    df_loaded = pd.read_excel(filepath)
    
    # Converter tipos para corresponder aos originais
    df_loaded['valor_total'] = df_loaded['valor_total'].astype(float)
    
    pd.testing.assert_frame_equal(df_loaded, sample_data)

def test_excel_loader_invalid_path(sample_data):
    """
    Testa se o loader lida corretamente com caminho inválido
    """
    # No Windows, usar um caminho que sabemos que não teremos permissão
    loader = ExcelLoader('C:/Windows/System32')
    
    with pytest.raises(Exception, match="Erro ao salvar arquivo Excel"):
        loader.save(sample_data, 'test.xlsx')

def test_excel_loader_create_directory(sample_data, temp_dir):
    """
    Testa se o loader cria o diretório de saída se não existir
    """
    # Criar um subdiretório que não existe
    output_dir = os.path.join(temp_dir, 'new_dir')
    
    loader = ExcelLoader(output_dir)
    filename = "test_output.xlsx"
    
    # Salvar arquivo
    loader.save(sample_data, filename)
    
    # Verificar se diretório e arquivo foram criados
    assert os.path.exists(output_dir)
    assert os.path.exists(os.path.join(output_dir, filename))

def test_excel_loader_empty_dataframe(temp_dir):
    """
    Testa se o loader lida corretamente com DataFrame vazio
    """
    loader = ExcelLoader(temp_dir)
    df_empty = pd.DataFrame()
    
    loader.save(df_empty, "empty.xlsx")
    
    # Verificar se arquivo foi criado
    filepath = os.path.join(temp_dir, "empty.xlsx")
    assert os.path.exists(filepath)
    
    # Verificar se está vazio
    df_loaded = pd.read_excel(filepath)
    assert df_loaded.empty
