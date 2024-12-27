"""
Script principal do ETL Pipeline
"""
import os
import logging
from etl_project.extractors.csv_extractor import CSVExtractor
from etl_project.transformers.vendas_transformer import VendasTransformer
from etl_project.loaders.excel_loader import ExcelLoader
from etl_project.utils.logger import setup_logger
from etl_project.utils.config import Config

# Configurar logger
logger = setup_logger(__name__)

def main():
    """
    Função principal que executa o pipeline ETL
    """
    try:
        logger.info("Iniciando pipeline ETL")
        
        # Carregar configurações
        config = Config()
        config.validate()
        input_config = config.get('input')
        output_config = config.get('output')
        
        # Criar diretório de saída se não existir
        os.makedirs(output_config['directory'], exist_ok=True)
        
        # Extrair dados
        logger.info("Iniciando extração dos dados")
        input_path = os.path.join(input_config['directory'], input_config['filename'])
        extractor = CSVExtractor(input_path)
        df = extractor.extract()
        
        # Transformar dados
        logger.info("Iniciando transformação dos dados")
        transformer = VendasTransformer()
        df_detalhado = transformer.transform(df)
        df_produto = transformer.group_by_product(df_detalhado)
        df_diario = transformer.group_by_date(df_detalhado)
        
        # Carregar dados
        logger.info("Iniciando carregamento dos dados")
        loader = ExcelLoader(output_config['directory'])
        
        # Salvar relatório detalhado
        loader.save(df_detalhado, output_config['files']['detailed'])
        logger.info(f"Arquivo {output_config['files']['detailed']} salvo com sucesso")
        
        # Salvar resumo por produto
        loader.save(df_produto, output_config['files']['product_summary'])
        logger.info(f"Arquivo {output_config['files']['product_summary']} salvo com sucesso")
        
        # Salvar resumo diário
        loader.save(df_diario, output_config['files']['daily_summary'])
        logger.info(f"Arquivo {output_config['files']['daily_summary']} salvo com sucesso")
        
        logger.info("Pipeline ETL concluído com sucesso")
        
    except Exception as e:
        logger.error(f"Erro durante a execução do pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()
