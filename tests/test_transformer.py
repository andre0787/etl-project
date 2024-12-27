"""
Testes para o módulo transformer
"""
import logging
import pytest
import pandas as pd
from etl_project.transformers.vendas_transformer import VendasTransformer

@pytest.fixture
def sample_data():
    df = pd.DataFrame({
        'data': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02']),
        'produto': ['Produto A', 'Produto B', 'Produto A', 'Produto C'],
        'quantidade': [10, 5, 8, 15],
        'preco_unitario': [100.50, 50.25, 100.50, 75.00]
    })
    return {'data': df}

def test_transform_calcula_valor_total(sample_data, caplog):
    """Testa se o valor total é calculado corretamente"""
    caplog.set_level(logging.DEBUG)
    
    transformer = VendasTransformer()
    result = transformer.transform(sample_data)
    
    df_detalhado = result['detalhado']
    assert 'valor_total' in df_detalhado.columns
    assert df_detalhado.loc[0, 'valor_total'] == 1005.00  # 10 * 100.50
    assert df_detalhado.loc[1, 'valor_total'] == 251.25   # 5 * 50.25
    
    # Verificar logs
    assert "Calculando valor total das vendas" in caplog.text

def test_transform_agrega_por_produto(sample_data, caplog):
    """Testa se a agregação por produto está correta"""
    caplog.set_level(logging.DEBUG)
    
    transformer = VendasTransformer()
    result = transformer.transform(sample_data)
    
    df_resumo = result['resumo_produto']
    assert len(df_resumo) == 3  # 3 produtos únicos
    
    # Produto A: 10 + 8 = 18 unidades, valor = (10 * 100.50) + (8 * 100.50)
    produto_a = df_resumo[df_resumo['produto'] == 'Produto A'].iloc[0]
    assert produto_a['quantidade'] == 18
    assert produto_a['valor_total'] == 1809.00
    
    # Verificar logs
    assert "Criando resumo por produto" in caplog.text

def test_transform_agrega_por_data(sample_data, caplog):
    """Testa se a agregação por data está correta"""
    caplog.set_level(logging.DEBUG)
    
    transformer = VendasTransformer()
    result = transformer.transform(sample_data)
    
    df_resumo = result['resumo_diario']
    assert len(df_resumo) == 2  # 2 datas únicas
    
    # 2024-01-01: quantidade = 15 (10 + 5), valor = 1005.00 + 251.25
    dia_1 = df_resumo[df_resumo['data'] == pd.Timestamp('2024-01-01')].iloc[0]
    assert dia_1['quantidade'] == 15
    assert abs(dia_1['valor_total'] - 1256.25) < 0.01
    
    # Verificar logs
    assert "Criando resumo diário" in caplog.text
