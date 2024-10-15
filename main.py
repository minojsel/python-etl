from etl.extract.csv_extractor import CSVExtractor
from etl.transform.holdings_transformer import HoldingsTransformer
from etl.transform.portfolio_transformer import PortfolioTransformer
from etl.load.postgresql_loader import PostgreSQLLoader
from etl.utils import load_yaml

import yaml

def main():
    pipeline = load_yaml('pipeline.yaml')
    print(pipeline)
    loader = PostgreSQLLoader()

    # Holdings ETL
    holdings_extractor = CSVExtractor(pipeline['extract']['holdings']['data'])
    holdings_extractor.extract()
    holdings_transformer = HoldingsTransformer(
        holdings_extractor.get_dataframe(),
        pipeline['transform']['holdings']['schema'][0]
    )
    holdings_transformer.transform()
    holdings_transformer.validate()
    dataframes = holdings_transformer.get_dataframe()
    for dataframe in dataframes:
        loader.load(dataframe, pipeline['load']['holdings'])

    # Portfolio ETL
    portfolio_extractor = CSVExtractor(pipeline['extract']['portfolio']['data'])
    portfolio_extractor.extract()
    portfolio_transformer = PortfolioTransformer(
        portfolio_extractor.get_dataframe(),
        pipeline['transform']['portfolio']['schema'][0]
    )
    portfolio_transformer.transform()
    portfolio_transformer.validate()
    dataframes = portfolio_transformer.get_dataframe()
    for dataframe in dataframes:
        loader.load(dataframe, pipeline['load']['portfolio'])

    for query in pipeline['load']['queries']:
        q = None
        with open(query) as fh:
            q = fh.read()
        
        loader.execute(q)

if __name__ == '__main__':
    main()