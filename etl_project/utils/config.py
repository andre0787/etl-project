"""
Módulo para gerenciamento de configurações do projeto
"""
import os
from pathlib import Path
from typing import Dict, Any
import yaml
from etl_project.utils.logger import setup_logger

logger = setup_logger(__name__)

class Config:
    def __init__(self, config_path: str = None):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            config_path: Caminho para o arquivo de configuração YAML.
                        Se None, usa o arquivo padrão config.yaml
        """
        if config_path is None:
            config_path = os.path.join(os.getcwd(), 'config.yaml')
            
        self.config_path = config_path
        self._config = None
        logger.info(f"Inicializando configurações a partir de: {config_path}")
        
    def load(self) -> Dict[str, Any]:
        """
        Carrega as configurações do arquivo YAML.
        
        Returns:
            Dicionário com as configurações
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
            yaml.YAMLError: Se houver erro no formato do arquivo
        """
        try:
            logger.debug(f"Carregando configurações de: {self.config_path}")
            
            if not os.path.exists(self.config_path):
                logger.error(f"Arquivo de configuração não encontrado: {self.config_path}")
                raise FileNotFoundError(f"Arquivo não encontrado: {self.config_path}")
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
                
            logger.info("Configurações carregadas com sucesso")
            return self._config
            
        except yaml.YAMLError as e:
            logger.error(f"Erro ao parsear arquivo YAML: {str(e)}")
            raise
        
    @property
    def config(self) -> Dict[str, Any]:
        """
        Retorna as configurações carregadas.
        
        Returns:
            Dicionário com as configurações
        """
        if self._config is None:
            self._config = self.load()
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Retorna um valor específico das configurações.
        
        Args:
            key: Chave da configuração
            default: Valor padrão se a chave não existir
            
        Returns:
            Valor da configuração ou default
        """
        try:
            value = self.config.get(key, default)
            logger.debug(f"Obtendo configuração {key}: {value}")
            return value
        except Exception as e:
            logger.warning(f"Erro ao obter configuração {key}: {str(e)}")
            return default
    
    def validate(self) -> bool:
        """
        Valida se todas as configurações necessárias estão presentes.
        
        Returns:
            True se todas as configurações estiverem válidas
            
        Raises:
            ValueError: Se alguma configuração obrigatória estiver faltando
        """
        required_keys = {
            'input': {
                'directory': str,
                'filename': str,
                'date_format': str,
                'columns': {
                    'date': str,
                    'product': str,
                    'quantity': str,
                    'price': str
                }
            },
            'output': {
                'directory': str
            },
            'logging': {
                'level': str,
                'file': str
            }
        }
        
        try:
            logger.debug("Validando configurações")
            self._validate_dict(self.config, required_keys)
            logger.info("Configurações validadas com sucesso")
            return True
            
        except ValueError as e:
            logger.error(f"Erro na validação das configurações: {str(e)}")
            raise
    
    def _validate_dict(self, config: Dict, schema: Dict, path: str = "") -> None:
        """
        Valida recursivamente um dicionário de configurações.
        
        Args:
            config: Dicionário de configurações
            schema: Schema para validação
            path: Caminho atual na validação recursiva
        """
        for key, value_type in schema.items():
            current_path = f"{path}.{key}" if path else key
            
            if key not in config:
                raise ValueError(f"Configuração obrigatória ausente: {current_path}")
                
            if isinstance(value_type, dict):
                if not isinstance(config[key], dict):
                    raise ValueError(
                        f"Configuração {current_path} deve ser um dicionário"
                    )
                self._validate_dict(config[key], value_type, current_path)
            else:
                if not isinstance(config[key], value_type):
                    raise ValueError(
                        f"Configuração {current_path} deve ser do tipo {value_type.__name__}"
                    )
