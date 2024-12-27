"""
Loader para salvar dados em arquivos Excel
"""
import pandas as pd
from pathlib import Path
from typing import Union
from etl_project.utils.logger import setup_logger

logger = setup_logger(__name__)

class ExcelLoader:
    def __init__(self, output_dir: Union[str, Path]):
        """
        Inicializa o loader Excel.
        
        Args:
            output_dir: Diretório onde os arquivos serão salvos
        """
        self.output_dir = Path(output_dir)
        logger.info(f"Inicializando ExcelLoader para o arquivo: {output_dir}")
        
    def save(self, df: pd.DataFrame, filename: str) -> None:
        """
        Salva o DataFrame em um arquivo Excel.
        
        Args:
            df: DataFrame a ser salvo
            filename: Nome do arquivo Excel
        """
        try:
            # Garantir que o diretório existe
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # Construir caminho completo
            filepath = self.output_dir / filename
            
            logger.debug(f"Salvando DataFrame em: {filepath}")
            df.to_excel(filepath, index=False)
            logger.info(f"Arquivo salvo com sucesso: {filepath}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo Excel: {str(e)}")
            raise
