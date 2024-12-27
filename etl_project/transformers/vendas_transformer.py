"""
Módulo para transformação dos dados de vendas
"""
import pandas as pd
from etl_project.utils.logger import setup_logger
from etl_project.utils.config import Config

logger = setup_logger(__name__)

class VendasTransformer:
    """
    Classe para transformação dos dados de vendas
    """
    
    def __init__(self):
        """
        Inicializa o transformador de vendas
        """
        logger.info("Inicializando VendasTransformer")
        self.config = Config()
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforma os dados de vendas
        
        Args:
            df: DataFrame com os dados de vendas
            
        Returns:
            DataFrame transformado
        """
        try:
            logger.debug("Iniciando transformação dos dados de vendas")
            
            # Calcular valor total
            logger.debug("Calculando valor total das vendas")
            try:
                df['total_value'] = df['quantity'] * df['price']
            except KeyError:
                logger.warning("Coluna 'price' não encontrada, usando price_unit")
                df['total_value'] = df['quantity'] * df['price_unit']
            
            logger.info("Transformação concluída com sucesso")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao transformar dados: {str(e)}")
            raise
    
    def group_by_product(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrupa os dados por produto
        
        Args:
            df: DataFrame com os dados de vendas
            
        Returns:
            DataFrame agrupado por produto
        """
        try:
            logger.debug("Criando resumo por produto")
            
            # Agrupar por produto
            df_produto = df.groupby('product').agg({
                'quantity': 'sum',
                'total_value': 'sum'
            }).reset_index()
            
            # Calcular preço médio
            df_produto['average_price'] = df_produto['total_value'] / df_produto['quantity']
            
            logger.debug("Resumo por produto criado com sucesso")
            return df_produto
            
        except Exception as e:
            logger.error(f"Erro ao agrupar por produto: {str(e)}")
            raise
    
    def group_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrupa os dados por data
        
        Args:
            df: DataFrame com os dados de vendas
            
        Returns:
            DataFrame agrupado por data
        """
        try:
            logger.debug("Criando resumo diário")
            
            # Agrupar por data
            df_diario = df.groupby('date').agg({
                'quantity': 'sum',
                'total_value': 'sum',
                'product': 'count'
            }).reset_index()
            
            # Renomear coluna de contagem
            df_diario = df_diario.rename(columns={'product': 'total_products'})
            
            # Calcular ticket médio
            df_diario['average_ticket'] = df_diario['total_value'] / df_diario['total_products']
            
            logger.debug("Resumo diário criado com sucesso")
            return df_diario
            
        except Exception as e:
            logger.error(f"Erro ao agrupar por data: {str(e)}")
            raise
