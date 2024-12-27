"""
Testes para o módulo de configuração
"""
import os
import pytest
import yaml
from etl_project.utils.config import Config

def test_config_load_success(tmp_path):
    """Testa o carregamento bem sucedido das configurações"""
    # Cria um arquivo de configuração temporário
    config_data = {
        'input': {
            'directory': 'data/input',
            'filename': 'test.csv',
            'date_format': '%Y-%m-%d',
            'columns': {
                'date': 'data',
                'product': 'produto',
                'quantity': 'quantidade',
                'price': 'preco'
            }
        },
        'output': {
            'directory': 'data/output'
        },
        'logging': {
            'level': 'DEBUG',
            'file': 'logs/test.log'
        }
    }
    
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f)
    
    # Carrega e verifica as configurações
    config = Config(str(config_file))
    loaded_config = config.load()
    
    assert loaded_config == config_data
    assert config.get('input')['filename'] == 'test.csv'
    assert config.get('nonexistent', 'default') == 'default'

def test_config_file_not_found():
    """Testa erro quando arquivo não existe"""
    config = Config('nonexistent.yaml')
    with pytest.raises(FileNotFoundError):
        config.load()

def test_config_invalid_yaml(tmp_path):
    """Testa erro com YAML inválido"""
    config_file = tmp_path / "invalid_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write('invalid: yaml: content:')
    
    config = Config(str(config_file))
    with pytest.raises(yaml.YAMLError):
        config.load()

def test_config_validation_success(tmp_path):
    """Testa validação bem sucedida das configurações"""
    config_data = {
        'input': {
            'directory': 'data/input',
            'filename': 'test.csv',
            'date_format': '%Y-%m-%d',
            'columns': {
                'date': 'data',
                'product': 'produto',
                'quantity': 'quantidade',
                'price': 'preco'
            }
        },
        'output': {
            'directory': 'data/output'
        },
        'logging': {
            'level': 'DEBUG',
            'file': 'logs/test.log'
        }
    }
    
    config_file = tmp_path / "valid_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f)
    
    config = Config(str(config_file))
    assert config.validate() is True

def test_config_validation_missing_key(tmp_path):
    """Testa validação com chave obrigatória ausente"""
    config_data = {
        'input': {
            'filename': 'test.csv'  # Faltando 'directory'
        },
        'output': {
            'directory': 'data/output'
        },
        'logging': {
            'level': 'DEBUG',
            'file': 'logs/test.log'
        }
    }
    
    config_file = tmp_path / "invalid_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f)
    
    config = Config(str(config_file))
    with pytest.raises(ValueError) as exc_info:
        config.validate()
    assert "Configuração obrigatória ausente" in str(exc_info.value)

def test_config_validation_wrong_type(tmp_path):
    """Testa validação com tipo de dados incorreto"""
    config_data = {
        'input': {
            'directory': 123,  # Deveria ser string
            'filename': 'test.csv',
            'date_format': '%Y-%m-%d',
            'columns': {
                'date': 'data',
                'product': 'produto',
                'quantity': 'quantidade',
                'price': 'preco'
            }
        },
        'output': {
            'directory': 'data/output'
        },
        'logging': {
            'level': 'DEBUG',
            'file': 'logs/test.log'
        }
    }
    
    config_file = tmp_path / "type_error_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f)
    
    config = Config(str(config_file))
    with pytest.raises(ValueError) as exc_info:
        config.validate()
    assert "deve ser do tipo str" in str(exc_info.value)
