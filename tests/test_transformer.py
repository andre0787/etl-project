"""
Testes para o módulo transformer
"""
import pytest
import pandas as pd
from datetime import datetime
from etl_project.transformers.vendas_transformer import VendasTransformer

@pytest.fixture
def sample_data():
    """
    Fixture que retorna dados de exemplo para teste
    """
    return pd.DataFrame({
        'data': [datetime(2024, 1, 1), datetime(2024, 1, 1), 
                datetime(2024, 1, 2), datetime(2024, 1, 2)],
        'produto': ['A', 'B', 'A', 'B'],
        'quantidade': [2, 3, 4, 1],
        'preco_unitario': [10.0, 20.0, 10.0, 20.0]
    })

def test_transform_success(sample_data, caplog):
    """
    Testa a transformação bem sucedida dos dados
    """
    transformer = VendasTransformer()
    df, product_summary, date_summary = transformer.transform(sample_data)
    
    # Verificar colunas renomeadas
    assert 'date' in df.columns
    assert 'product' in df.columns
    assert 'quantity' in df.columns
    assert 'price' in df.columns
    assert 'total_value' in df.columns
    
    # Verificar cálculo do valor total
    assert df['total_value'].iloc[0] == 20.0  # 2 * 10.0
    assert df['total_value'].iloc[1] == 60.0  # 3 * 20.0
    
    # Verificar resumo por produto
    assert len(product_summary) == 2
    product_a = product_summary[product_summary['product'] == 'A']
    assert product_a['quantity'].iloc[0] == 6  # 2 + 4
    assert product_a['total_value'].iloc[0] == 60.0  # (2 * 10.0) + (4 * 10.0)
    
    # Verificar resumo por data
    assert len(date_summary) == 2
    day_1 = date_summary[date_summary['date'] == datetime(2024, 1, 1)]
    assert day_1['quantity'].iloc[0] == 5  # 2 + 3
    assert day_1['total_value'].iloc[0] == 80.0  # (2 * 10.0) + (3 * 20.0)

def test_group_by_product(sample_data):
    """
    Testa o agrupamento por produto
    """
    transformer = VendasTransformer()
    df, _, _ = transformer.transform(sample_data)
    product_summary = transformer.group_by_product(df)
    
    assert len(product_summary) == 2
    product_a = product_summary[product_summary['product'] == 'A']
    assert product_a['quantity'].iloc[0] == 6
    assert product_a['total_value'].iloc[0] == 60.0
    assert product_a['average_price'].iloc[0] == 10.0

def test_group_by_date(sample_data):
    """
    Testa o agrupamento por data
    """
    transformer = VendasTransformer()
    df, _, _ = transformer.transform(sample_data)
    date_summary = transformer.group_by_date(df)
    
    assert len(date_summary) == 2
    day_1 = date_summary[date_summary['date'] == datetime(2024, 1, 1)]
    assert day_1['quantity'].iloc[0] == 5
    assert day_1['total_value'].iloc[0] == 80.0
    assert day_1['total_products'].iloc[0] == 2
    assert day_1['average_ticket'].iloc[0] == 40.0  # 80.0 / 2

def test_transform_with_missing_price_column(caplog):
    """
    Testa a transformação quando a coluna de preço está ausente
    """
    data = pd.DataFrame({
        'data': [datetime(2024, 1, 1)],
        'produto': ['A'],
        'quantidade': [2],
        'preco_unitario': [10.0]
    })
    
    transformer = VendasTransformer()
    df, product_summary, date_summary = transformer.transform(data)
    
    assert df['total_value'].iloc[0] == 20.0  # 2 * 10.0
    assert product_summary['total_value'].iloc[0] == 20.0
    assert date_summary['total_value'].iloc[0] == 20.0
