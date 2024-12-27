"""
Script para processar dados de vendas
"""
import os
from etl_project.pipeline import ETLPipeline
from etl_project.extractors.csv_extractor import CSVExtractor
from etl_project.transformers.vendas_transformer import VendasTransformer
from etl_project.loaders.excel_loader import ExcelLoader

def main():
    # Configurar caminhos
    diretorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    arquivo_entrada = os.path.join(diretorio_base, 'data', 'input', 'dados_vendas.csv')
    arquivo_saida = os.path.join(diretorio_base, 'data', 'output', 'relatorio_vendas.xlsx')
    
    # Criar componentes do pipeline
    extractor = CSVExtractor(arquivo_entrada)
    transformer = VendasTransformer()
    loader = ExcelLoader(arquivo_saida)
    
    # Criar e executar pipeline
    pipeline = ETLPipeline(extractor, transformer, loader)
    
    try:
        pipeline.run()
        print(f"Processamento concluído com sucesso!")
        print(f"Arquivo de saída: {arquivo_saida}")
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")

if __name__ == "__main__":
    main()
