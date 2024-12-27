"""
Testes para o módulo de relatórios
"""
import os
import pytest
import pandas as pd
from datetime import datetime
from etl_project.reports.sales_report import SalesReport

@pytest.fixture
def sample_data():
    """
    Fixture que retorna dados de exemplo para os testes
    """
    return pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=5),
        'product': ['Produto A', 'Produto B', 'Produto A', 'Produto C', 'Produto B'],
        'quantity': [10, 5, 8, 12, 6],
        'price': [100.50, 50.25, 100.50, 75.00, 50.25],
        'total_value': [1005.00, 251.25, 804.00, 900.00, 301.50]
    })

@pytest.fixture
def report_dir(tmp_path):
    """
    Fixture que retorna um diretório temporário para os relatórios
    """
    return tmp_path / "reports"

def test_plot_daily_sales(sample_data, report_dir):
    """
    Testa a geração do gráfico de vendas diárias
    """
    report = SalesReport(str(report_dir))
    report.plot_daily_sales(sample_data, "vendas_diarias.html")
    
    assert os.path.exists(report_dir / "vendas_diarias.html")

def test_plot_product_summary(sample_data, report_dir):
    """
    Testa a geração do gráfico de resumo por produto
    """
    report = SalesReport(str(report_dir))
    report.plot_product_summary(sample_data, "resumo_produtos.html")
    
    assert os.path.exists(report_dir / "resumo_produtos.html")

def test_generate_pdf_report(sample_data, report_dir):
    """
    Testa a geração do relatório em PDF
    """
    report = SalesReport(str(report_dir))
    report.generate_pdf_report(sample_data, "relatorio.pdf")
    
    assert os.path.exists(report_dir / "relatorio.pdf")

def test_invalid_output_dir():
    """
    Testa criação do relatório com diretório inválido
    """
    # No Windows, usar um caminho que sabemos que não teremos permissão
    with pytest.raises(Exception):
        SalesReport("C:/Windows/System32/invalid")
