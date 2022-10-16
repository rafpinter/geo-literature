import os
import pandas as pd
from country_names import country_names
from functions import log

FILE = 'PREPROCESS'

class litData:
    def __init__(self):
        
        self.spreadsheet_id = os.environ['SPREADSHEET_ID']
        self.books_tab_id = os.environ['BOOKS_TAB_ID']
        self.equality_scores_tab_id = os.environ['EQUALITY_SCORES_TAB_ID']
        self.about_tab_id = os.environ['ABOUT_TAB_ID']
        self.iso_codes_tab_id = os.environ['ISO_CODES_TAB_ID']
        
        self.books_df = None
        self.equality_scores_df = None
        self.about_df = None
        self.iso_codes = None
    
    def _get_spreadsheet(self, tab_id):
        url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/export?format=csv&id={self.spreadsheet_id}&gid={tab_id}"
        return pd.read_csv(url)

    def _total_books_per_country(self):
        df_books_per_country = self.books_df.groupby("ISO-3").size().reset_index()
        df_books_per_country.columns = ['ISO-3', 'books_per_country']
        self.books_df = pd.merge(self.books_df, df_books_per_country, on='ISO-3', how='left')
        print(self.books_df.head())
    
    def _merge_iso_codes_to_equality_df(self):
        self.equality_scores_df = pd.merge(self.equality_scores_df, self.iso_codes, left_on='country', right_on='country', how='left')
    
    def _merge_book_count_to_equality_df(self):
        df_books_per_country = self.books_df[['ISO-3', 'books_per_country']].copy().fillna(0)
        df_books_per_country = df_books_per_country.drop_duplicates()
        self.equality_scores_df = pd.merge(self.equality_scores_df, df_books_per_country, on='ISO-3', how='left')
        
    
    def request_spreadsheet_data(self):
        self.books_df = self._get_spreadsheet(self.books_tab_id)
        self.equality_scores_df = self._get_spreadsheet(self.equality_scores_tab_id)
        self.iso_codes = self._get_spreadsheet(self.iso_codes_tab_id)
        self.about_df = self._get_spreadsheet(self.about_tab_id)
    
    def equality_scores_preprocess(self):
        self._merge_iso_codes_to_equality_df()
        self.equality_scores_df.to_csv("eq1.csv")
        self._merge_book_count_to_equality_df()
        self.equality_scores_df.to_csv("eq2.csv")

    
    def books_preprocess(self):
        self.books_df.sort_values(by='country_name', ascending=True, inplace=True)
        self._total_books_per_country()
    
    def get_data(self):
        self.request_spreadsheet_data()
        self.books_preprocess()
        self.equality_scores_preprocess()
        return self.books_df, self.equality_scores_df, self.about_df