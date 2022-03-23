import pandas as pd
from src.preprocess import VintedPagesProcessor, VintedAdsProcessor
import src.config.constant_paths as cst_paths
import src.config.constants as cst


def load_preprocessed_vinted_data():
    pages_df = pd.read_parquet(cst_paths.PREP_PAGES_PATH)
    ads_df = pd.read_parquet(cst_paths.PREP_ADS_PATH)
    return pages_df, ads_df


def preprocess_save_raw_vinted_data():
    pages_df = pd.read_csv(cst_paths.RAW_PAGES_PATH)
    pages_processor = VintedPagesProcessor(pages_df, save_output=True)
    pages_processor.preprocess_pages()

    ads_df = pd.read_csv(
        cst_paths.RAW_ADS_PATH, parse_dates=cst.time_cols_ads, low_memory=False
    )
    ads_processor = VintedAdsProcessor(ads_df, save_output=True)
    ads_processor.preprocess_ads()


if __name__ == "__main__":
    preprocess_save_raw_vinted_data()
