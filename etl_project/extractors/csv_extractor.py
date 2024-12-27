"""
Módulo para extração de dados de arquivos CSV
"""
import pandas as pd
from etl_project.utils.logger import setup_logger
from etl_project.utils.config import Config

logger = setup_logger(__name__)

class CSVExtractor:
    """
    Classe para extrair dados de arquivos CSV
    """
    
    def __init__(self, filepath: str):
        """
        Inicializa o extrator CSV
        
        Args:
            filepath: Caminho para o arquivo CSV
        """
        logger.info(f"Inicializando CSVExtractor para o arquivo: {filepath}")
        self.filepath = filepath
        self.config = Config()
    
    def extract(self) -> pd.DataFrame:
        """
        Extrai dados do arquivo CSV
        
        Returns:
            DataFrame com os dados extraídos
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        try:
            logger.debug(f"Iniciando extração do arquivo: {self.filepath}")
            
            # Ler arquivo CSV
            df = pd.read_csv(self.filepath)
            
            # Obter configurações das colunas
            columns = self.config.get('input')['columns']
            
            # Converter coluna de data
            logger.debug("Convertendo coluna 'data' para datetime")
            date_format = self.config.get('input')['date_format']
            df[columns['date']] = pd.to_datetime(df[columns['date']], format=date_format)
            logger.debug("Conversão da coluna 'data' concluída")
            
            # Renomear colunas para o padrão interno
            column_mapping = {v: k for k, v in columns.items()}
            df = df.rename(columns=column_mapping)
            
            logger.info(f"Extração concluída com sucesso. {len(df)} registros carregados.")
            return df
            
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {self.filepath}")
            raise
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {str(e)}")
            raise
