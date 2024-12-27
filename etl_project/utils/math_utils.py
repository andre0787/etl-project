"""
Utilitários para cálculos matemáticos e estatísticos
"""
from typing import List, Union, Optional
import numpy as np
from decimal import Decimal, ROUND_HALF_UP


def calcular_media_ponderada(valores: List[float], pesos: List[float]) -> float:
    """
    Calcula a média ponderada de uma lista de valores.
    
    Args:
        valores: Lista de valores
        pesos: Lista de pesos correspondentes
        
    Returns:
        Média ponderada calculada
    """
    if len(valores) != len(pesos):
        raise ValueError("O número de valores deve ser igual ao número de pesos")
    return sum(v * p for v, p in zip(valores, pesos)) / sum(pesos)


def arredondar_decimal(valor: Union[float, str], casas: int = 2) -> Decimal:
    """
    Arredonda um valor decimal usando regras contábeis.
    
    Args:
        valor: Valor para arredondar
        casas: Número de casas decimais
        
    Returns:
        Valor arredondado como Decimal
    """
    return Decimal(str(valor)).quantize(
        Decimal('0.' + '0' * casas),
        rounding=ROUND_HALF_UP
    )


def calcular_percentual(valor: float, total: float, casas: int = 2) -> float:
    """
    Calcula o percentual de um valor em relação ao total.
    
    Args:
        valor: Valor para calcular o percentual
        total: Valor total
        casas: Número de casas decimais
        
    Returns:
        Percentual calculado
    """
    if total == 0:
        return 0.0
    return round((valor / total) * 100, casas)


def calcular_variacao_percentual(valor_inicial: float, valor_final: float, casas: int = 2) -> float:
    """
    Calcula a variação percentual entre dois valores.
    
    Args:
        valor_inicial: Valor inicial
        valor_final: Valor final
        casas: Número de casas decimais
        
    Returns:
        Variação percentual calculada
    """
    if valor_inicial == 0:
        return 0.0
    return round(((valor_final - valor_inicial) / valor_inicial) * 100, casas)


def calcular_estatisticas_basicas(valores: List[float]) -> dict:
    """
    Calcula estatísticas básicas de uma lista de valores.
    
    Args:
        valores: Lista de valores numéricos
        
    Returns:
        Dicionário com estatísticas calculadas
    """
    if not valores:
        return {
            "media": None,
            "mediana": None,
            "desvio_padrao": None,
            "minimo": None,
            "maximo": None
        }
    
    return {
        "media": np.mean(valores),
        "mediana": np.median(valores),
        "desvio_padrao": np.std(valores),
        "minimo": min(valores),
        "maximo": max(valores)
    }


def normalizar_valores(valores: List[float], 
                      min_valor: Optional[float] = None,
                      max_valor: Optional[float] = None) -> List[float]:
    """
    Normaliza uma lista de valores para o intervalo [0, 1].
    
    Args:
        valores: Lista de valores para normalizar
        min_valor: Valor mínimo para normalização (opcional)
        max_valor: Valor máximo para normalização (opcional)
        
    Returns:
        Lista com valores normalizados
    """
    if not valores:
        return []
        
    min_v = min_valor if min_valor is not None else min(valores)
    max_v = max_valor if max_valor is not None else max(valores)
    
    if min_v == max_v:
        return [0.0] * len(valores)
        
    return [(v - min_v) / (max_v - min_v) for v in valores]
