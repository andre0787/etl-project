"""
Testes para o módulo de transformação
"""
import pandas as pd
import pytest
from datetime import datetime
from etl_project.transformers.vendas_transformer import VendasTransformer

@pytest.fixture
def sample_data():
    """
    Fixture com dados de exemplo para testes
    """
    return pd.DataFrame({
        'data': [
            datetime(2024, 1, 1),
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
            datetime(2024, 1, 2)
        ],
        'produto': ['A', 'B', 'A', 'B'],
        'quantidade': [2, 3, 4, 1],
        'preco_unitario': [10.0, 20.0, 10.0, 20.0]
    })

def test_transform_success(sample_data, caplog):
    """
    Testa a transformação bem sucedida dos dados
    """
    transformer = VendasTransformer()
    result = transformer.transform(sample_data)
    
    # Verificar se o valor total foi calculado corretamente
    assert 'valor_total' in result.columns
    assert result['valor_total'].tolist() == [20.0, 60.0, 40.0, 20.0]
    
    # Verificar logs
    assert "Iniciando transformação dos dados de vendas" in caplog.text
    assert "Transformação concluída com sucesso" in caplog.text

def test_group_by_product(sample_data):
    """
    Testa o agrupamento por produto
    """
    transformer = VendasTransformer()
    df = transformer.transform(sample_data)
    result = transformer.group_by_product(df)
    
    # Verificar estrutura do resultado
    assert set(result.columns) == {'produto', 'quantidade', 'valor_total', 'preco_medio'}
    
    # Verificar valores
    assert len(result) == 2  # Dois produtos
    
    # Produto A
    produto_a = result[result['produto'] == 'A'].iloc[0]
    assert produto_a['quantidade'] == 6  # 2 + 4
    assert produto_a['valor_total'] == 60.0  # (2 * 10) + (4 * 10)
    assert produto_a['preco_medio'] == 10.0  # 60 / 6
    
    # Produto B
    produto_b = result[result['produto'] == 'B'].iloc[0]
    assert produto_b['quantidade'] == 4  # 3 + 1
    assert produto_b['valor_total'] == 80.0  # (3 * 20) + (1 * 20)
    assert produto_b['preco_medio'] == 20.0  # 80 / 4

def test_group_by_date(sample_data):
    """
    Testa o agrupamento por data
    """
    transformer = VendasTransformer()
    df = transformer.transform(sample_data)
    result = transformer.group_by_date(df)
    
    # Verificar estrutura do resultado
    assert set(result.columns) == {
        'data', 'quantidade', 'valor_total', 'total_produtos', 'ticket_medio'
    }
    
    # Verificar valores
    assert len(result) == 2  # Dois dias
    
    # Dia 1
    dia_1 = result[result['data'] == datetime(2024, 1, 1)].iloc[0]
    assert dia_1['quantidade'] == 5  # 2 + 3
    assert dia_1['valor_total'] == 80.0  # (2 * 10) + (3 * 20)
    assert dia_1['total_produtos'] == 2  # 2 produtos
    assert dia_1['ticket_medio'] == 40.0  # 80 / 2
    
    # Dia 2
    dia_2 = result[result['data'] == datetime(2024, 1, 2)].iloc[0]
    assert dia_2['quantidade'] == 5  # 4 + 1
    assert dia_2['valor_total'] == 60.0  # (4 * 10) + (1 * 20)
    assert dia_2['total_produtos'] == 2  # 2 produtos
    assert dia_2['ticket_medio'] == 30.0  # 60 / 2

def test_transform_with_missing_price_column(caplog):
    """
    Testa a transformação quando a coluna de preço está ausente
    """
    # Dados sem a coluna preco
    data = pd.DataFrame({
        'data': [datetime(2024, 1, 1)],
        'produto': ['A'],
        'quantidade': [2],
        'preco_unitario': [10.0]
    })
    
    transformer = VendasTransformer()
    result = transformer.transform(data)
    
    # Verificar se usou preco_unitario
    assert "Coluna 'preco' não encontrada, usando preco_unitario" in caplog.text
    assert result['valor_total'].iloc[0] == 20.0  # 2 * 10.0
