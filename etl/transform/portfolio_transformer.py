from .transformer import Transformer

class PortfolioTransformer(Transformer):
    def __init__(self, dataframes, schema_path):
        super().__init__(dataframes, schema_path)
    
    def transform(self):
        self.clean()
        self.to_numeric()
        self.to_datetime()
    
    def validate(self):
        for dataframe in self._dataframes:
            self._schema.validate(dataframe)
        
        return True