import os

RAW_DATA_PATH = '../data/raw'
PREPROCESSED_DATA_PATH = '../data/preprocessed'

RAW_PAGES_PATH = os.path.join(RAW_DATA_PATH, 'pages_data.csv')
RAW_ADS_PATH = os.path.join(RAW_DATA_PATH, 'ads_data.csv')

PREP_PAGES_PATH = os.path.join(PREPROCESSED_DATA_PATH, 'pages_data.parquet.gz')
PREP_ADS_PATH = os.path.join(PREPROCESSED_DATA_PATH, 'ads_data.parquet.gz')