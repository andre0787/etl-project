"""
Módulo para configuração do logger
"""
import logging
import os
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """
    Configura e retorna um logger com handlers para console e arquivo.
    
    Args:
        name: Nome do logger, geralmente __name__
        
    Returns:
        Logger configurado
    """
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Definir nível para DEBUG
    
    # Verificar se o logger já tem handlers para evitar duplicação
    if not logger.handlers:
        # Criar formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Definir nível para DEBUG
        console_handler.setFormatter(formatter)
        
        # Handler para arquivo
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(logs_dir / 'etl.log')
        file_handler.setLevel(logging.DEBUG)  # Definir nível para DEBUG
        file_handler.setFormatter(formatter)
        
        # Adicionar handlers ao logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger
