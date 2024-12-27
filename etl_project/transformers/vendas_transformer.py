"""
Transformador de dados de vendas
"""
import pandas as pd
from typing import Dict, Any
from etl_project.transformers.base_transformer import BaseTransformer
from etl_project.utils.math_utils import calcular_estatisticas_basicas

class VendasTransformer(BaseTransformer):
    """
    Transformador específico para dados de vendas
    """
    
    def transform(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Transforma os dados de vendas.
        
        Args:
            data: DataFrame com dados brutos
            
        Returns:
            Dicionário com DataFrames transformados
        """
        # Criar uma cópia para não modificar o original
        df = data.copy()
        
        # Converter tipos
        df['data'] = pd.to_datetime(df['data'])
        df['quantidade'] = pd.to_numeric(df['quantidade'])
        df['preco_unitario'] = pd.to_numeric(df['preco_unitario'])
        
        # Calcular valor total
        df['valor_total'] = df['quantidade'] * df['preco_unitario']
        
        # Criar resumos
        resumo_produto = df.groupby('produto').agg({
            'quantidade': 'sum',
            'valor_total': 'sum'
        }).reset_index()
        
        resumo_diario = df.groupby('data').agg({
            'quantidade': 'sum',
            'valor_total': 'sum'
        }).reset_index()
        
        return {
            'detalhado': df,
            'resumo_produto': resumo_produto,
            'resumo_diario': resumo_diario
        }
