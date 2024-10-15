"""
Transformer Base Class with Schema Validation 
"""
import pandas as pd
import pandera as pa
from abc import ABC, abstractmethod
from ..utils.logger import logger

class Transformer(ABC):
    def __init__(self, dataframes, schema_path):
        self._dataframes = dataframes
        self._schema = self.load_schema(schema_path)
    
    def load_schema(self, schema_path):
        return pa.DataFrameSchema.from_yaml(schema_path)
    
    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def validate(self):
        pass
    
    @logger
    def _handle_date(self, value):
        fmts = ['%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y', '%d/%m/%Y']
        for fmt in fmts:
            try:
                return pd.to_datetime(value, format=fmt)
            except ValueError as e:
                continue
        return None
    
    @logger
    def _handle_numeric(self, value):
        value = value.replace('"', '').replace(',', '')
        if '%' in value:
            value = value.replace('%','')
            return round(pd.to_numeric(value, errors='coerce')/100, 4)
        return pd.to_numeric(value, errors='coerce')

    @logger
    @logger
    def clean(self):
        for col, dtype in self._schema.dtypes.items():
            if str(dtype) in ['date', 'datetime', 'object']:
                for idx, dataframe in enumerate(self._dataframes):
                    if col in dataframe.columns:
                        self._dataframes[idx][col] = self._dataframes[idx][col].apply(lambda x: x.strip())
    
    @logger
    def to_numeric(self):
        """
        Ensure that all floats and integers are converted to numeric to ensure that quotes, commas and percentage
        symbols are all removed from the number columnn.
        """
        for col, dtype in self._schema.dtypes.items():
            if str(dtype) in ['int64', 'float64']:
                for idx, dataframe in enumerate(self._dataframes):
                    if col in dataframe.columns and str(dataframe[col].dtypes) in 'object':
                        self._dataframes[idx][col] = self._dataframes[idx][col].apply(self._handle_numeric)
    
    @logger
    def to_datetime(self):
        """
        Handle Dates such that they are all standardized. As there are a mismatch of values in the column,
        they need to be handled row wise
        """

        for col, dtype in self._schema.dtypes.items():
            if str(dtype) in ['date']:
                for idx, dataframe in enumerate(self._dataframes):
                    try:
                        self._dataframes[idx][col] = self._dataframes[idx][col].apply(self._handle_date)
                        self._dataframes[idx][col] = self._dataframes[idx][col].dt.date
                    except Exception as e:
                        continue
    
    @logger
    def get_dataframe(self):
        return self._dataframes