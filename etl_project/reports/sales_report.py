"""
Módulo para geração de relatórios e visualizações de vendas
"""
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF

from etl_project.utils.logger import setup_logger

logger = setup_logger(__name__)

class SalesReport:
    """
    Classe para geração de relatórios e visualizações de vendas
    """
    
    def __init__(self, output_dir: str):
        """
        Inicializa o gerador de relatórios
        
        Args:
            output_dir: Diretório para salvar os relatórios
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Inicializando SalesReport. Diretório de saída: {output_dir}")
        
        # Configurar estilo dos gráficos
        plt.style.use('default')
    
    def plot_daily_sales(self, df: pd.DataFrame, filename: str) -> None:
        """
        Gera gráfico de vendas diárias
        
        Args:
            df: DataFrame com os dados de vendas
            filename: Nome do arquivo para salvar o gráfico
        """
        try:
            logger.debug("Gerando gráfico de vendas diárias")
            
            # Criar figura do plotly
            fig = go.Figure()
            
            # Adicionar linha de vendas totais
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['total_value'],
                mode='lines+markers',
                name='Valor Total',
                line=dict(color='#2ecc71', width=2)
            ))
            
            # Configurar layout
            fig.update_layout(
                title='Vendas Diárias',
                xaxis_title='Data',
                yaxis_title='Valor Total (R$)',
                template='plotly_white'
            )
            
            # Salvar gráfico
            output_path = self.output_dir / filename
            fig.write_html(output_path)
            logger.info(f"Gráfico salvo em: {output_path}")
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de vendas diárias: {str(e)}")
            raise
    
    def plot_product_summary(self, df: pd.DataFrame, filename: str) -> None:
        """
        Gera gráfico de resumo por produto
        
        Args:
            df: DataFrame com os dados de vendas
            filename: Nome do arquivo para salvar o gráfico
        """
        try:
            logger.debug("Gerando gráfico de resumo por produto")
            
            # Agrupar dados por produto
            product_summary = df.groupby('product').agg({
                'quantity': 'sum',
                'total_value': 'sum'
            }).reset_index()
            
            # Criar figura do plotly
            fig = go.Figure()
            
            # Adicionar barras de quantidade
            fig.add_trace(go.Bar(
                x=product_summary['product'],
                y=product_summary['quantity'],
                name='Quantidade',
                marker_color='#3498db'
            ))
            
            # Adicionar linha de valor total
            fig.add_trace(go.Scatter(
                x=product_summary['product'],
                y=product_summary['total_value'],
                name='Valor Total',
                mode='lines+markers',
                yaxis='y2',
                line=dict(color='#e74c3c', width=2)
            ))
            
            # Configurar layout
            fig.update_layout(
                title='Resumo por Produto',
                xaxis_title='Produto',
                yaxis_title='Quantidade',
                yaxis2=dict(
                    title='Valor Total (R$)',
                    overlaying='y',
                    side='right'
                ),
                template='plotly_white'
            )
            
            # Salvar gráfico
            output_path = self.output_dir / filename
            fig.write_html(output_path)
            logger.info(f"Gráfico salvo em: {output_path}")
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de resumo por produto: {str(e)}")
            raise
    
    def generate_pdf_report(self, df: pd.DataFrame, filename: str) -> None:
        """
        Gera relatório em PDF com os principais indicadores
        
        Args:
            df: DataFrame com os dados de vendas
            filename: Nome do arquivo para salvar o relatório
        """
        try:
            logger.debug("Gerando relatório PDF")
            
            # Criar PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Configurar fonte
            pdf.set_font('Arial', 'B', 16)
            
            # Título
            pdf.cell(0, 10, 'Relatório de Vendas', 0, 1, 'C')
            pdf.ln(10)
            
            # Informações gerais
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Informações Gerais', 0, 1, 'L')
            pdf.set_font('Arial', '', 12)
            
            total_sales = df['total_value'].sum()
            total_quantity = df['quantity'].sum()
            avg_ticket = total_sales / len(df)
            
            pdf.cell(0, 10, f'Valor Total de Vendas: R$ {total_sales:,.2f}', 0, 1, 'L')
            pdf.cell(0, 10, f'Quantidade Total Vendida: {total_quantity:,}', 0, 1, 'L')
            pdf.cell(0, 10, f'Ticket Médio: R$ {avg_ticket:,.2f}', 0, 1, 'L')
            pdf.ln(10)
            
            # Top produtos
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, 'Top 5 Produtos', 0, 1, 'L')
            pdf.set_font('Arial', '', 12)
            
            top_products = df.groupby('product')['total_value'].sum().sort_values(ascending=False).head()
            
            for product, value in top_products.items():
                pdf.cell(0, 10, f'{product}: R$ {value:,.2f}', 0, 1, 'L')
            
            # Salvar PDF
            output_path = self.output_dir / filename
            pdf.output(str(output_path))
            logger.info(f"Relatório PDF salvo em: {output_path}")
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório PDF: {str(e)}")
            raise
