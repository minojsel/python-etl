import pandas as pd
from .extractor import Extractor
from ..utils.logger import logger

class CSVExtractor(Extractor):
    def __init__(self, file_paths, delimiter=',', header=0):
        super().__init__()
        self._file_paths = file_paths
        self._delimiter = delimiter
        self._header = header
        self._dfs = []

    @logger
    def extract(self):
        for file_path in self._file_paths:
            self._dfs.append(pd.read_csv(file_path, delimiter=self._delimiter, header=self._header))

    @logger
    def get_dataframe(self):
        return self._dfs