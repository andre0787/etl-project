"""
Utilitários para manipulação de strings
"""
import re
from typing import List, Optional


def remover_caracteres_especiais(texto: str) -> str:
    """
    Remove caracteres especiais de uma string.
    
    Args:
        texto: String para limpar
        
    Returns:
        String limpa sem caracteres especiais
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', texto)


def normalizar_texto(texto: str) -> str:
    """
    Normaliza um texto removendo acentos e convertendo para minúsculo.
    
    Args:
        texto: String para normalizar
        
    Returns:
        String normalizada
    """
    import unicodedata
    
    # Remove acentos
    texto_sem_acentos = ''.join(c for c in unicodedata.normalize('NFKD', texto)
                               if not unicodedata.combining(c))
    
    # Converte para minúsculo
    return texto_sem_acentos.lower()


def extrair_numeros(texto: str) -> List[str]:
    """
    Extrai todos os números de uma string.
    
    Args:
        texto: String para extrair números
        
    Returns:
        Lista com todos os números encontrados
    """
    return re.findall(r'\d+', texto)


def formatar_cpf(cpf: str) -> str:
    """
    Formata um CPF adicionando pontos e traço.
    
    Args:
        cpf: String contendo apenas números do CPF
        
    Returns:
        CPF formatado (ex: 123.456.789-00)
    """
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        raise ValueError("CPF deve conter 11 dígitos")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata um CNPJ adicionando pontos, barra e traço.
    
    Args:
        cnpj: String contendo apenas números do CNPJ
        
    Returns:
        CNPJ formatado (ex: 12.345.678/0001-90)
    """
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14:
        raise ValueError("CNPJ deve conter 14 dígitos")
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def truncar_texto(texto: str, tamanho: int, sufixo: str = "...") -> str:
    """
    Trunca um texto em um determinado tamanho, adicionando um sufixo se necessário.
    
    Args:
        texto: String para truncar
        tamanho: Tamanho máximo da string
        sufixo: Sufixo a ser adicionado quando o texto for truncado
        
    Returns:
        Texto truncado
    """
    if len(texto) <= tamanho:
        return texto
    return texto[:tamanho - len(sufixo)] + sufixo
