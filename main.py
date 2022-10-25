import pygsheets

sheetCredentials = pygsheets.authorize(service_file='C:/Users/josep/Desktop/Work Projects/automaticjobscraper-9d69e1b3ecd5.json')

sheet = sheetCredentials.open_by_key('1eLcNCKAloyzM65PNzijcGr6NUpCaTRrF1j906AlIgFY')

worksheet = sheet.sheet1

worksheet.update_value('B2', 'test2 pygsheets')
