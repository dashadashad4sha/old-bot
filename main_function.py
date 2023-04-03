from functions import *


def absent_full_day(name, date_start, date_end):
    day1 = int(date_start)
    day2 = int(date_end)
    all_cells = find_cell(name, day1, day2)
    col1, row1 = all_cells[0]
    col2, row2 = all_cells[-1]

    range1 = f"first_list!{row1}{col1}"
    range2 = f"first_list!{row2}{col2}"
    values = [find_lessons_count(day1, day2)]

    body = {
        'valueInputOption': 'RAW',
        'data': [
            {'range': range1, 'values': values},
                ]
    }

    resp = sheet.values().batchUpdate(spreadsheetId=sheet_id, body=body).execute()


def absent_half_day(name, date_start, lessons_count):
    all_cells = find_cell(name, date_start, date_start)
    col, row = all_cells[0]
    range1 = f"first_list!{row}{col}"
    values = [[lessons_count]]


    resp = sheet.values().update(spreadsheetId=sheet_id,
                                 range=range1,
                                 valueInputOption='RAW',
                                 body={'values': values}).execute()


def get_names():
    ranges = ["first_list!A4:A29"]
    names = []
    results = service.spreadsheets().values().batchGet(spreadsheetId=sheet_id,
                                                       ranges=ranges,
                                                       valueRenderOption='FORMATTED_VALUE',
                                                       dateTimeRenderOption='FORMATTED_STRING').execute()
    sheet_values = results['valueRanges'][0]['values']
    for i in range(25):
        names.append(sheet_values[i][0])
    return names


