"""
Transformer para processamento de dados de vendas
"""
import pandas as pd
from typing import Dict, Any
from etl_project.transformers.base_transformer import BaseTransformer
from etl_project.utils.logger import setup_logger

logger = setup_logger(__name__)

class VendasTransformer(BaseTransformer):
    def __init__(self):
        """
        Inicializa o transformer de vendas
        """
        logger.info("Inicializando VendasTransformer")
    
    def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transforma os dados de vendas.
        
        Args:
            data: Dicionário com DataFrame de vendas
            
        Returns:
            Dicionário com DataFrames transformados
        """
        try:
            logger.debug("Iniciando transformação dos dados de vendas")
            df = data['data']
            
            # Calcular valor total
            logger.debug("Calculando valor total das vendas")
            if 'preco' not in df.columns:
                logger.warning("Coluna 'preco' não encontrada, usando preco_unitario")
                preco_col = 'preco_unitario'
            else:
                preco_col = 'preco'
                
            df['valor_total'] = df['quantidade'] * df[preco_col]
            
            # Criar resumos
            logger.debug("Criando resumo por produto")
            resumo_produto = df.groupby('produto').agg({
                'quantidade': 'sum',
                'valor_total': 'sum'
            }).reset_index()
            
            logger.debug("Criando resumo diário")
            resumo_diario = df.groupby('data').agg({
                'quantidade': 'sum',
                'valor_total': 'sum'
            }).reset_index()
            
            resultado = {
                'detalhado': df,
                'resumo_produto': resumo_produto,
                'resumo_diario': resumo_diario
            }
            
            logger.info("Transformação concluída com sucesso")
            return resultado
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados: {str(e)}")
            raise
