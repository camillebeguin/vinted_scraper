import json
import logging
import pandas as pd

import requests
from bs4 import BeautifulSoup

from src.utils import clean_text_scraped_dict

logger = logging.getLogger(__name__)


class VintedScraper:
    """Extract ads data from item pages (25 items max per page)
    Take a starting url as input
    """

    def __init__(self, scope_url, max_pages=25):
        self.scope_url = scope_url
        self.max_pages = max_pages
        self.items_df = pd.DataFrame()

    def get_pages_in_scope(self):
        urls = self.get_url_pages_in_scope()
        for url in urls:
            try:
                items_page_df = self.get_page_df_from_url(url)
                self.items_df = pd.concat([self.items_df, items_page_df])
            except:
                raise ConnectionRefusedError("Connection to Vinted.com was interrupted")

    def get_page_df_from_url(self, url):
        soup = self.request_source_data_from_url(url)
        items_dict = self.get_page_data_from_soup(soup)
        items_df = pd.DataFrame.from_dict(items_dict, orient="index")
        return items_df

    def get_page_data_from_soup(self, soup):
        page_main_script = soup.find(
            "script", {"data-js-react-on-rails-store": "MainStore"}
        )
        page_main = json.loads(page_main_script.string)
        items_dict = page_main["items"]["catalogItems"]["byId"]
        return items_dict

    def request_source_data_from_url(self, url):
        homepage = requests.get(url)
        soup = BeautifulSoup(homepage.content, "html.parser")
        return soup

    def get_url_pages_in_scope(self):
        urls = [self.scope_url]
        for page in range(1, self.max_pages):
            urls.append("{}&page={}".format(self.scope_url, page + 1))
        return urls


class VintedAdScraper:
    """Extract ads data from individual ad pages
    Take as input a list of ads urls and the corresponding list of ads ids
    """

    def __init__(self, ads_urls, ads_ids):
        self.ads_urls = ads_urls
        self.ads_ids = ads_ids
        self.ads_df = pd.DataFrame()

    def get_ads_in_scope(self):
        for url, id_ in zip(self.ads_urls, self.ads_ids):
            ad_df = self.get_ad_df_from_url(url)
            ad_df.index = [id_]
            self.ads_df = pd.concat([self.ads_df, ad_df])

    def get_ad_df_from_url(self, url):
        soup = self.request_source_data_from_url(url)
        ad_dict = self.get_ad_data_from_soup(soup)
        ad_df = pd.DataFrame.from_dict(ad_dict, orient="index").T
        return ad_df

    def get_ad_data_from_soup(self, soup):
        description = self.get_item_description_from_soup(soup)
        user_info = self.get_item_user_info_from_soup(soup)
        details = self.get_item_details_from_soup(soup)

        description = {"ad_" + k: v for k, v in description.items()}
        user_info = {"user_" + k: v for k, v in user_info.items()}
        details = {"details_" + k: v for k, v in details.items()}

        ad_dict = dict(description, **user_info, **details)
        return ad_dict

    def get_item_description_from_soup(self, soup):
        source = soup.find("script", {"data-component-name": "ItemDescription"})
        description = json.loads(source.string)["content"]
        return description

    def get_item_user_info_from_soup(self, soup):
        source = soup.find("script", {"data-component-name": "ItemUserInfo"})
        user_info = json.loads(source.string)["user"]
        return user_info

    def get_item_details_from_soup(self, soup):
        item_details = soup.find("div", {"class": "details-list details-list--details"})
        item_details_keys = item_details.findAll(
            "div", {"class": "details-list__item-title"}
        )
        item_details_values = item_details.findAll(
            "div", {"class": "details-list__item-value"}
        )

        details = {}
        for it_key, it_val in zip(item_details_keys, item_details_values):
            it_key = clean_text_scraped_dict(it_key.text)
            if it_key == "Ajouté":
                it_val = it_val.find("time")["datetime"]
            else:
                it_val = clean_text_scraped_dict(it_val.text)

            details[it_key] = it_val

        return details

    def request_source_data_from_url(self, url):
        homepage = requests.get(url)
        soup = BeautifulSoup(homepage.content, "html.parser")
        return soup
