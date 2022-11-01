import pygsheets
import json
import apiRequests
import sys


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

    sheetcredentials = pygsheets.authorize(service_file=authInputFile["googlesheets"]["authorization_file"])

    sheet = sheetcredentials.open_by_key(authInputFile["googlesheets"]["authorization_key"])

    worksheet = sheet.sheet1

    myAPIScraper = apiRequests.apiScraper()

    result = myAPIScraper.scrapeUSAJobs()

    outputList = result.split(',')

    # At the moment, it crams entire result string into one cell.
    # TODO: Each comma-separated value must go into the next corresponding cell
    # worksheet.update_value('A3', result)

    # uploadMatrix = [[a, b, c, d, e] for ind, a, b, c, d, e in enumerate(outputList[ind * 5:(ind + 1) * 5])]
    uploadMatrix = [[[0] * 5] for i in range(int(len(outputList) / 5))]
    for i in range(0, int(len(outputList) / 5)):
        for j in range(0, 5):
            uploadMatrix[i][0][j] = outputList[(i * 5) + j]

    updateRanges = ['A' + str(x) + ':E' + str(x) for x in range(2, (len(uploadMatrix) + 2))]
    worksheet.update_values_batch(updateRanges, uploadMatrix, 'COLUMNS')

    for value in range(0, len(outputList)):
        currCell = str(chr(65 + (value % 5))) + str(int(value / 5) + 2)
        worksheet.update_value(currCell, outputList[value])


main(sys.argv)
