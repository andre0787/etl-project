"""
Script principal para execução do pipeline ETL
"""
from pathlib import Path
from etl_project.extractors.csv_extractor import CSVExtractor
from etl_project.transformers.vendas_transformer import VendasTransformer
from etl_project.loaders.excel_loader import ExcelLoader
from etl_project.utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    try:
        # Configurar caminhos
        input_file = Path('data/input/vendas.csv')
        output_dir = Path('data/output')
        
        # Criar diretórios se não existirem
        input_file.parent.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Iniciando pipeline ETL")
        
        # Extração
        logger.info("Iniciando extração dos dados")
        extractor = CSVExtractor(str(input_file))
        dados_extraidos = extractor.extract()
        
        # Transformação
        logger.info("Iniciando transformação dos dados")
        transformer = VendasTransformer()
        dados_transformados = transformer.transform(dados_extraidos)
        
        # Carga
        logger.info("Iniciando carga dos dados")
        loader = ExcelLoader(output_dir)
        
        # Salvar cada DataFrame em um arquivo Excel separado
        for nome, df in dados_transformados.items():
            output_file = f"vendas_{nome}.xlsx"
            loader.save(df, output_file)
            logger.info(f"Arquivo {output_file} salvo com sucesso")
        
        logger.info("Pipeline ETL executado com sucesso")
        
    except Exception as e:
        logger.error(f"Erro durante a execução do pipeline: {str(e)}")
        raise

if __name__ == "__main__":
    main()
