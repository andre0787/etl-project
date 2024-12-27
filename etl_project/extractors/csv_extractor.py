"""
Módulo para extração de dados de arquivos CSV
"""
import pandas as pd
from etl_project.utils.logger import setup_logger
from etl_project.utils.config import Config
from etl_project.validators.vendas_validator import VendasValidator

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
        self.validator = VendasValidator()
    
    def extract(self) -> pd.DataFrame:
        """
        Extrai dados do arquivo CSV
        
        Returns:
            DataFrame com os dados extraídos
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            ValidationError: Se os dados forem inválidos
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
            
            # Validar cada linha
            logger.debug("Iniciando validação dos dados")
            validated_data = []
            for _, row in df.iterrows():
                data = row.to_dict()
                validated_row = self.validator.validate(data)
                validated_data.append(validated_row)
            
            # Criar novo DataFrame com dados validados
            df_validated = pd.DataFrame(validated_data)
            
            logger.info(f"Extração e validação concluídas com sucesso. {len(df_validated)} registros carregados.")
            return df_validated
            
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {self.filepath}")
            raise
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados: {str(e)}")
            raise
