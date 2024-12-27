"""
Loader para salvar dados em Excel
"""
import os
from pathlib import Path
import pandas as pd
from typing import Dict, Any
from etl_project.loaders.base_loader import BaseLoader

class ExcelLoader(BaseLoader):
    """
    Loader para salvar dados em diferentes abas de um arquivo Excel
    """
    
    def __init__(self, filepath: str):
        """
        Inicializa o loader Excel.
        
        Args:
            filepath: Caminho para salvar o arquivo Excel
        """
        self.filepath = filepath
        
    def load(self, data_dict: Dict[str, Any]) -> None:
        """
        Carrega os dados em um arquivo Excel.
        
        Args:
            data_dict (dict): Dicionário com os DataFrames a serem salvos
            
        Raises:
            Exception: Se houver erro ao salvar o arquivo
        """
        try:
            # Verifica se o diretório pai existe e tenta criar
            parent_dir = os.path.dirname(os.path.abspath(self.filepath))
            os.makedirs(parent_dir, exist_ok=True)
            
            with pd.ExcelWriter(self.filepath, engine='openpyxl') as writer:
                # Salvar dados detalhados
                data_dict['detalhado'].to_excel(writer, sheet_name='Detalhado', index=False)
                
                # Salvar resumo por produto
                data_dict['resumo_produto'].to_excel(writer, sheet_name='Resumo por Produto', index=False)
                
                # Salvar resumo diário
                data_dict['resumo_diario'].to_excel(writer, sheet_name='Resumo Diário', index=False)
                
        except PermissionError as e:
            raise Exception(f"Erro ao salvar arquivo Excel: Sem permissão para criar diretório ou arquivo")
        except Exception as e:
            raise Exception(f"Erro ao salvar arquivo Excel: {str(e)}")
