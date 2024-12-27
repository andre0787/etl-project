import pandas as pd
import pytest
from etl_project.transformers.vendas_transformer import VendasTransformer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'data': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02']),
        'produto': ['Produto A', 'Produto B', 'Produto A', 'Produto C'],
        'quantidade': [10, 5, 8, 15],
        'preco_unitario': [100.50, 50.25, 100.50, 75.00]
    })

def test_transform_calcula_valor_total(sample_data):
    """Testa se o valor total é calculado corretamente"""
    transformer = VendasTransformer()
    result = transformer.transform(sample_data)
    
    assert 'valor_total' in result['detalhado'].columns
    # Produto A, dia 1: 10 * 100.50 = 1005.00
    expected_total = 1005.00
    assert result['detalhado'].loc[0, 'valor_total'] == expected_total

def test_transform_agrega_por_produto(sample_data):
    """Testa se a agregação por produto está correta"""
    transformer = VendasTransformer()
    result = transformer.transform(sample_data)
    
    resumo_produto = result['resumo_produto']
    
    # Produto A total: (10 + 8) = 18 unidades
    produto_a = resumo_produto[resumo_produto['produto'] == 'Produto A']
    assert produto_a['quantidade'].iloc[0] == 18

def test_transform_agrega_por_data(sample_data):
    """Testa se a agregação por data está correta"""
    transformer = VendasTransformer()
    result = transformer.transform(sample_data)
    
    resumo_data = result['resumo_diario']
    
    # Dia 1 total: 10 + 5 = 15 unidades
    dia_1 = resumo_data[resumo_data['data'] == pd.Timestamp('2024-01-01')]
    assert dia_1['quantidade'].iloc[0] == 15
