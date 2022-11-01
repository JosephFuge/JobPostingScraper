import requests
from requests.auth import HTTPBasicAuth
import json

class apiScraper:
    apiAuthInput = None

    def __init__(self):
        with open("C:\\Users\\josep\\Desktop\\Work Projects\\jobScraperAPIAuthCredentials.json", "r") as inputFile:
            self.apiAuthInput = json.load(inputFile)
            inputFile.close()
    def scrapeUSAJobs(self, jobcategorycode = '0340', keywords = 'none'):
        usaJobsParams = {"Host": self.apiAuthInput["usajobs"]["host_url"],
                         "User-Agent": self.apiAuthInput["usajobs"]["usajobs_user_agent"],
                         "Authorization-Key": self.apiAuthInput["usajobs"]["usajobs_authorization_key"],
                         "ResultsPerPage": "1"}

        usaJobsURL = "https://data.usajobs.gov/api/search?JobCategoryCode=" + jobcategorycode + "&HiringPath=PUBLIC"

        if keywords != 'none':
            usaJobsURL += "&Keywords=" + keywords

        response = requests.get(usaJobsURL, headers=usaJobsParams)

        usaJobsResponseDict = response.json()
        usaJobsParsed = "Federal Government,"

        for i in range(len(usaJobsResponseDict["SearchResult"]["SearchResultItems"])):
            usaJobsPositionDict = usaJobsResponseDict["SearchResult"]["SearchResultItems"][i]["MatchedObjectDescriptor"]
            # Add job title to output string
            usaJobsParsed += usaJobsPositionDict["PositionTitle"].replace(',', '')

            # Add minimum and maximum salary range to output string
            usaJobsParsed += ",$" + usaJobsPositionDict["PositionRemuneration"][0]["MinimumRange"]

            usaJobsParsed += " - $" + usaJobsPositionDict["PositionRemuneration"][0]["MaximumRange"]

            # Add the application close date to the result string, without the time of day
            tempString = usaJobsPositionDict["ApplicationCloseDate"]
            usaJobsParsed += "," + tempString[:tempString.find('T')]
            usaJobsParsed += "," + \
                             usaJobsPositionDict["PositionURI"]
            usaJobsParsed += ",Federal Government,"

        return usaJobsParsed[0:-20]
        #outputJson = json.dumps(response.json())

        def printUSAJobsCodeLists(self):
            orgCategoryResponse = requests.get("https://data.usajobs.gov/api/codelist/whomayapply")
            print(orgCategoryResponse.text + "\n")
            orgCategoryResponse = requests.get("https://data.usajobs.gov/api/codelist/hiringpaths")
            print(orgCategoryResponse.text + "\n")
            orgCategoryResponse = requests.get("https://data.usajobs.gov/api/codelist/occupationalseries")
            print(orgCategoryResponse.text + "\n")
