from .transformer import Transformer
from ..utils.logger import logger

class HoldingsTransformer(Transformer):
    def __init__(self, dataframes, schema_path):
        super().__init__(dataframes, schema_path)

    @logger    
    def transform(self):
        self.clean()
        self.to_numeric()
        self.to_datetime()
    
    @logger
    def validate(self):
        for dataframe in self._dataframes:
            self._schema.validate(dataframe)
        
        return True