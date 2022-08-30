import pandas as pd
from country_names import country_names

class litData:
    def __init__(self):
        
        self.spreadsheet_id = "1yVzmSE9wdSpsH3EmrMHBY2fsu6oVJwqEAYtdE7rS-Qc"
        self.books_tab_id = "598270524"
        self.equality_scores_tab_id = "0"
        self.iso_codes_tab_id = "1833588588"
        
        self.books_df = None
        self.equality_scores_df = None
        self.iso_codes = None
    
    def get_spreadsheet(self, tab_id):
        url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/export?format=csv&id={self.spreadsheet_id}&gid={tab_id}"
        return pd.read_csv(url)
    
    def request_spreadsheet_data(self):
        self.books_df = self.get_spreadsheet(self.books_tab_id)
        self.equality_scores_df = self.get_spreadsheet(self.equality_scores_tab_id)
        self.iso_codes = self.get_spreadsheet(self.iso_codes_tab_id)
    
    def equality_scores_preprocess(self):
        self.equality_scores_df = pd.merge(self.equality_scores_df, self.iso_codes, left_on='country', right_on='country', how='left')
        
    def get_data(self):
        self.request_spreadsheet_data()
        self.equality_scores_preprocess()
        return self.books_df, self.equality_scores_df