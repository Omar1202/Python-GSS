import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

ITEM_SHEET = 'items'
CLIENT_SHEET = 'clients'
SPREAD_SHEET_KEY = '1GUR4bPlQeu6yTNw1ypM5-LNLtHc5LdXuieUZykWU24I'
CREDS_JSON = 'credentials-d.json'

class gsheet_helper:
    
    def __init__(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            CREDS_JSON,
            scope
        )
        
        self.client = gspread.authorize(creds)
        self.gsheet = self.client.open_by_key(SPREAD_SHEET_KEY)
        
        
    def get_items(self):
        items = self.get_sheet(ITEM_SHEET)
        return items
    
    def get_sheet(self, sheet_name):
        sheet = self.gsheet.worksheet(sheet_name)
        items = pd.DataFrame(sheet.get_all_records())
        return items
    
    def store_user(self, user_dic):
        sheet = self.gsheet.worksheet(CLIENT_SHEET)
        clients = pd.DataFrame(self.get_sheet(CLIENT_SHEET))
        
        cond = clients[clients['id'] == user_dic['id']].empty
        if cond:
            sheet.add_rows(1)
            sheet.append_row([element for element in user_dic.values()])
        else:
            print('Eso ya existe')
            
            
if __name__ == 'main':
    print(gsheet_helper().get_items)
    
        