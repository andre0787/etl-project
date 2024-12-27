"""
Extrator de dados de arquivos CSV
"""
import pandas as pd
import os
from typing import Optional
from etl_project.extractors.base_extractor import BaseExtractor

class CSVExtractor(BaseExtractor):
    """
    Extrator para arquivos CSV
    """
    
    def __init__(self, filepath: str, encoding: str = 'utf-8', **kwargs):
        """
        Inicializa o extrator CSV.
        
        Args:
            filepath: Caminho para o arquivo CSV
            encoding: Encoding do arquivo (default: utf-8)
            **kwargs: Argumentos adicionais para pd.read_csv
        """
        self.filepath = filepath
        self.encoding = encoding
        self.kwargs = kwargs
        
    def extract(self) -> pd.DataFrame:
        """
        Extrai dados do arquivo CSV.
        
        Returns:
            DataFrame com os dados do CSV
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            Exception: Para outros erros de leitura
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Arquivo não encontrado: {self.filepath}")
            
        try:
            df = pd.read_csv(
                self.filepath,
                encoding=self.encoding,
                **self.kwargs
            )
            
            # Converter tipos básicos
            if 'data' in df.columns:
                df['data'] = pd.to_datetime(df['data'])
            
            return df
            
        except Exception as e:
            raise Exception(f"Erro ao ler arquivo CSV: {str(e)}")
