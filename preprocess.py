import os
import pandas as pd
from country_names import country_names

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
    
    def get_spreadsheet(self, tab_id):
        url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/export?format=csv&id={self.spreadsheet_id}&gid={tab_id}"
        return pd.read_csv(url)
    
    def request_spreadsheet_data(self):
        self.books_df = self.get_spreadsheet(self.books_tab_id)
        self.equality_scores_df = self.get_spreadsheet(self.equality_scores_tab_id)
        self.iso_codes = self.get_spreadsheet(self.iso_codes_tab_id)
        self.about_df = self.get_spreadsheet(self.about_tab_id)
    
    def equality_scores_preprocess(self):
        self.equality_scores_df = pd.merge(self.equality_scores_df, self.iso_codes, left_on='country', right_on='country', how='left')
    
    def books_preprocess(self):
        self.books_df.sort_values(by='country_name', ascending=True, inplace=True)
    
    def get_data(self):
        self.request_spreadsheet_data()
        self.equality_scores_preprocess()
        self.books_preprocess()
        return self.books_df, self.equality_scores_df, self.about_df