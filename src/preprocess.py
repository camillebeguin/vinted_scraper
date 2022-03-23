### Imports
import pandas as pd
import numpy as np
from datetime import datetime

import src.config.constants as cst
import src.config.constant_paths as cst_paths
from src.config.custom_logging import logger

### Pages
class VintedPagesProcessor:
    def __init__(self, pages_df, save_output=False):
        self.pages_df = pages_df.copy()
        self.save_output = save_output

    def preprocess_pages(self):
        logger.info("Preprocess raw pages")
        self._clean_price()
        self._clean_size()
        self._extract_user_data()
        self._extract_photo_data()
        self._filter_relevant_cols()
        self._rename_columns()
        self._fix_column_types()
        self._save_preprocessed_pages()

    def _clean_price(self):
        self.pages_df["discount"].fillna(0, inplace=True)

    def _clean_size(self):
        self.pages_df["size_title"] = (
            self.pages_df["size_title"].str.split("/").str[0].str.strip()
        )

    def _extract_user_data(self):
        users_df = pd.json_normalize(
            self.pages_df["user"].apply(lambda u_dict: eval(u_dict))
        ).add_prefix("user_")
        users_df.index = self.pages_df.index
        self.pages_df = self.pages_df.drop("user", axis=1)
        self.pages_df = pd.concat([self.pages_df, users_df], axis=1)

    def _extract_photo_data(self):
        photos_df = pd.json_normalize(
            self.pages_df["photo"].apply(lambda p: {} if p is np.nan else eval(p))
        )
        self.pages_df = self.pages_df.drop("photo", axis=1)
        photos_df.index = self.pages_df.index
        self.pages_df = pd.concat(
            [
                self.pages_df,
                photos_df[["url", "high_resolution.timestamp"]].rename(
                    columns={
                        "url": "photo_url",
                        "high_resolution.timestamp": "photo_timestamp",
                    }
                ),
            ],
            axis=1,
        )
        self.pages_df["photo_timestamp"] = (
            self.pages_df["photo_timestamp"]
            .fillna(0)
            .apply(
                lambda time_: np.nan if time_ == 0 else datetime.fromtimestamp(time_)
            )
        )

    def _filter_relevant_cols(self):
        self.pages_df = self.pages_df[cst.relevant_cols_pages]

    def _rename_columns(self):
        logger.info("Rename columns in pages")
        self.pages_df = self.pages_df.rename(columns=cst.colnames_pages)

    def _fix_column_types(self):
        logger.info("Fix column types in pages")
        for col, type_ in cst.coltypes_pages.items():
            if "id" in col:
                self.pages_df[col] = self.pages_df[col].astype(int).astype(type_)
            else:
                self.pages_df[col] = self.pages_df[col].astype(type_)

    def _save_preprocessed_pages(self):
        if self.save_output:
            self.pages_df.to_parquet(cst_paths.PREP_PAGES_PATH)
            logger.info("Saved preprocessed pages")


#### Ads
class VintedAdsProcessor:
    def __init__(self, ads_df, save_output=False):
        self.ads_df = ads_df.copy()
        self.save_output = save_output

    def preprocess_ads(self):
        logger.info("Preprocess raw ads")
        self._convert_time_columns()
        self._drop_erroneous_ad_id()
        self._clean_size()
        self._clean_interested_count()
        self._clean_bundle_status()
        self._clean_counts()
        self._filter_relevant_cols()
        self._rename_columns()
        self._fix_column_types()
        self._save_preprocessed_ads()

    def _convert_time_columns(self):
        for col in cst.time_cols_ads:
            self.ads_df[col] = pd.to_datetime(self.ads_df[col], utc=True)

    def _drop_erroneous_ad_id(self):
        errors = ["Je ne fais pas d&#39;échanges. "]
        self.ads_df = self.ads_df.query("ad_id not in @errors")

    def _clean_size(self):
        self.ads_df["details_Taille"] = (
            self.ads_df["details_Taille"].str.split("/").str[0].str.strip()
        )

    def _clean_interested_count(self):
        self.ads_df["details_Intéressés·ées"] = (
            self.ads_df["details_Intéressés·ées"].str.split().str[0]
        )

    def _clean_bundle_status(self):
        def extract_bundle_status(bundle):
            if bundle is np.nan:
                return False
            else:
                return eval(bundle)["enabled"]

        self.ads_df["user_bundle_discount"] = self.ads_df["user_bundle_discount"].apply(
            lambda bundle: extract_bundle_status(bundle)
        )

    def _clean_counts(self):
        check_cols = list(
            self.ads_df.columns[self.ads_df.columns.str.contains("_count")]
        )
        check_cols.append("user_feedback_reputation")
        for col in check_cols:
            self.ads_df[col] = (
                self.ads_df[col]
                .fillna("0")
                .apply(lambda count_: 0 if str(count_).lower().islower() else count_)
            )

    def _filter_relevant_cols(self):
        self.ads_df = self.ads_df[cst.relevant_cols_ads]

    def _rename_columns(self):
        logger.info("Rename columns in ads")
        self.ads_df = self.ads_df.rename(columns=cst.colnames_ads)

    def _fix_column_types(self):
        logger.info("Fix column types in ads")
        for col, type_ in cst.coltypes_ads.items():
            if "_id" in col:
                self.ads_df[col] = self.ads_df[col].astype(type_).replace(".0", "")
            else:
                self.ads_df[col] = self.ads_df[col].astype(type_)

    def _save_preprocessed_ads(self):
        if self.save_output:
            self.ads_df.to_parquet(cst_paths.PREP_ADS_PATH)
            logger.info("Saved preprocessed ads")
