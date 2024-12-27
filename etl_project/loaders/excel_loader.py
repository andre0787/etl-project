"""
Módulo para carregar dados em arquivos Excel
"""
import os
import pandas as pd
from etl_project.utils.logger import setup_logger

logger = setup_logger(__name__)

class ExcelLoader:
    """
    Classe para carregar dados em arquivos Excel
    """
    
    def __init__(self, output_dir: str):
        """
        Inicializa o loader de Excel
        
        Args:
            output_dir: Diretório de saída para os arquivos Excel
        """
        logger.info(f"Inicializando ExcelLoader para o arquivo: {output_dir}")
        self.output_dir = output_dir
    
    def save(self, df: pd.DataFrame, filename: str) -> None:
        """
        Salva um DataFrame em um arquivo Excel
        
        Args:
            df: DataFrame para salvar
            filename: Nome do arquivo Excel
            
        Raises:
            Exception: Se houver erro ao salvar o arquivo
        """
        try:
            # Criar diretório se não existir
            os.makedirs(self.output_dir, exist_ok=True)
            
            # Caminho completo do arquivo
            filepath = os.path.join(self.output_dir, filename)
            logger.debug(f"Salvando DataFrame em: {filepath}")
            
            # Salvar arquivo
            df.to_excel(filepath, index=False)
            logger.info(f"Arquivo salvo com sucesso: {filepath}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo Excel: {str(e)}")
            raise Exception(f"Erro ao salvar arquivo Excel: {str(e)}")
