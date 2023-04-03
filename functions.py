import os

import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from googleapiclient.discovery import build

CREDENTIALS_FILE = '/cred.json'


def get_service_sacc():
    creds_json = os.path.dirname(__file__) + CREDENTIALS_FILE
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


service = get_service_sacc()
sheet = service.spreadsheets()

sheet_id = '1oXkwc5ft6YE7e27iM_3a-UdMcMvkmus-9ogOhgRdIZI'


def find_name(name):
    ranges = ["first_list!A4:A29"]  #

    results = service.spreadsheets().values().batchGet(spreadsheetId=sheet_id,
                                                       ranges=ranges,
                                                       valueRenderOption='FORMATTED_VALUE',
                                                       dateTimeRenderOption='FORMATTED_STRING').execute()
    sheet_values = results['valueRanges'][0]['values']
    for i in range(25):
        if name == sheet_values[i][0]:
            row = i + 4
            return row


def find_date(date_start, date_end):
    dates = {1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',
             6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K',
             11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P',
             16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U',
             21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z',
             26: 'AA', 27: 'AB', 28: 'AC', 29: 'AD', 30: 'AE', 31: 'AF'}
    lst = []
    for i in range(int(date_start), int(date_end) + 1):
        lst.append(dates[i])

    return lst


def find_cell(name, date_start, date_end):
    lst = []
    col = find_name(name)
    for row in find_date(date_start, date_end):
        lst.append((col, row))
    # print(lst)
    return lst


def find_lessons_count(date_start, date_end):
    li = find_date(date_start, date_end)
    ranges = [f"first_list!{li[0]}3:{li[-1]}3"]

    results = service.spreadsheets().values().batchGet(spreadsheetId=sheet_id,
                                                       ranges=ranges,
                                                       valueRenderOption='FORMATTED_VALUE',
                                                       dateTimeRenderOption='FORMATTED_STRING').execute()
    sheet_values = results['valueRanges'][0]['values'][0]
    lst = []
    for i in range(len(sheet_values)):
        lst.append(sheet_values[i])
    return lst


