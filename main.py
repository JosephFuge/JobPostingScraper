import pygsheets
import json
import apiRequests
import sys

NUM_COLUMNS = 5

# jobScraperAPIAuthCredentials.json file path should be first argument passed in.
# Should contain authentication credentials on various APIs used including:
# Google Sheets and USAJobs
def main(argv):
    try:
        with open(argv[1], "r") as inputFile:
            authInputFile = json.load(inputFile)
            inputFile.close()
    except json.JSONDecodeError:
        print("File " + argv[1] + " is not a valid JSON file.")
        inputFile.close()
        exit()
    except FileNotFoundError:
        print("File " + argv[1] + " could not be found.")
        exit()

    # Authorize access to Google Sheets and enter the desired workbook.
    sheetcredentials = pygsheets.authorize(service_file=authInputFile["googlesheets"]["authorization_file"])
    sheet = sheetcredentials.open_by_key(authInputFile["googlesheets"]["authorization_key"])
    worksheet = sheet.sheet1

    myAPIScraper = apiRequests.apiScraper(argv[1])

    result = myAPIScraper.scrapeUSAJobs()

    outputList = result.split(',')

    uploadMatrix = [[[0]] * NUM_COLUMNS for i in range(int(len(outputList) / 5))]
    for i in range(0, int(len(outputList) / NUM_COLUMNS)):
        for j in range(0, NUM_COLUMNS):
            uploadMatrix[i][j] = [outputList[(i * NUM_COLUMNS) + j]]

    updateRanges = ['A' + str(x) + ':E' + str(x) for x in range(2, (len(uploadMatrix) + 2))]

    worksheet.update_values_batch(updateRanges, uploadMatrix, 'COLUMNS')

main(sys.argv)
