"""Main ETL pipeline implementation"""

class ETLPipeline:
    def __init__(self, extractor, transformer, loader):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader
    
    def run(self):
        """Execute the ETL pipeline"""
        # Extract
        data = self.extractor.extract()
        
        # Transform
        transformed_data = self.transformer.transform(data)
        
        # Load
        self.loader.load(transformed_data)
        
        return True
