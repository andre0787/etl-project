import os
import pytest
import pandas as pd
import openpyxl
from etl_project.loaders.excel_loader import ExcelLoader

@pytest.fixture
def sample_data():
    return {
        'detalhado': pd.DataFrame({
            'data': pd.to_datetime(['2024-01-01', '2024-01-02']),
            'produto': ['Produto A', 'Produto B'],
            'quantidade': [10, 5],
            'valor_total': [1005.00, 251.25]
        }),
        'resumo_produto': pd.DataFrame({
            'produto': ['Produto A', 'Produto B'],
            'quantidade': [10, 5],
            'valor_total': [1005.00, 251.25]
        }),
        'resumo_diario': pd.DataFrame({
            'data': pd.to_datetime(['2024-01-01', '2024-01-02']),
            'quantidade': [10, 5],
            'valor_total': [1005.00, 251.25]
        })
    }

@pytest.fixture
def temp_excel_file(tmp_path):
    return os.path.join(tmp_path, 'test_output.xlsx')

def test_excel_loader_save_success(sample_data, temp_excel_file):
    """Testa se o loader salva corretamente o arquivo Excel"""
    loader = ExcelLoader(temp_excel_file)
    loader.load(sample_data)
    
    assert os.path.exists(temp_excel_file)
    
    # Verifica se todas as abas foram criadas
    excel_file = pd.ExcelFile(temp_excel_file)
    expected_sheets = ['Detalhado', 'Resumo por Produto', 'Resumo Diário']
    assert all(sheet in excel_file.sheet_names for sheet in expected_sheets)

def test_excel_loader_invalid_path(sample_data):
    """Testa se o loader lida corretamente com caminho inválido"""
    # No Windows, usar um caminho que sabemos que não teremos permissão
    loader = ExcelLoader('C:/Windows/System32/teste.xlsx')
    with pytest.raises(Exception, match="Erro ao salvar arquivo Excel"):
        loader.load(sample_data)

def test_excel_loader_data_integrity(sample_data, temp_excel_file):
    """Testa se os dados são mantidos corretamente após salvar"""
    loader = ExcelLoader(temp_excel_file)
    loader.load(sample_data)
    
    # Lê os dados salvos
    df_salvo = pd.read_excel(temp_excel_file, sheet_name='Detalhado')
    
    # Verifica se os dados estão corretos
    assert len(df_salvo) == len(sample_data['detalhado'])
    assert all(col in df_salvo.columns for col in sample_data['detalhado'].columns)
