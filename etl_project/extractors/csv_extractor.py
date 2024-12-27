"""
Extrator de dados de arquivos CSV
"""
import pandas as pd
from pathlib import Path
from typing import Dict, Any
from etl_project.extractors.base_extractor import BaseExtractor
from etl_project.utils.logger import setup_logger

logger = setup_logger(__name__)

class CSVExtractor(BaseExtractor):
    def __init__(self, filepath: str):
        """
        Inicializa o extrator CSV.
        
        Args:
            filepath: Caminho para o arquivo CSV
        """
        self.filepath = filepath
        logger.info(f"Inicializando CSVExtractor para o arquivo: {filepath}")
    
    def extract(self) -> Dict[str, Any]:
        """
        Extrai dados do arquivo CSV.
        
        Returns:
            Dicionário com os dados extraídos
            
        Raises:
            FileNotFoundError: Se o arquivo não for encontrado
        """
        try:
            logger.debug(f"Iniciando extração do arquivo: {self.filepath}")
            
            if not Path(self.filepath).exists():
                logger.error(f"Arquivo não encontrado: {self.filepath}")
                raise FileNotFoundError(f"Arquivo não encontrado: {self.filepath}")
            
            df = pd.read_csv(self.filepath)
            
            # Converter coluna de data
            if 'data' in df.columns:
                logger.debug("Convertendo coluna 'data' para datetime")
                df['data'] = pd.to_datetime(df['data'], errors='coerce')
                logger.debug("Conversão da coluna 'data' concluída")
            
            logger.info(f"Extração concluída com sucesso. {len(df)} registros carregados.")
            return {'data': df}
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados do arquivo CSV: {str(e)}")
            raise
