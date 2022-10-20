import requests
from requests.auth import HTTPBasicAuth
import json

#usaJobsAuth = HTTPBasicAuth('byumpa.careerservices@gmail.com', 'I0D7oY6CmBgDyPuSTN+uTV99ELhWFbkEWS80H6oXO4I=')

usaJobsParams = {"Host":"data.usajobs.gov", "User-Agent":"byumpa.careerservices@gmail.com", "Authorization-Key":"I0D7oY6CmBgDyPuSTN+uTV99ELhWFbkEWS80H6oXO4I=", "ResultsPerPage":"1"}

# This code block currently used just to obtain and understand job categorization codes.
# It has no bearing on the output of the program.
orgCategoryResponse = requests.get("https://data.usajobs.gov/api/codelist/whomayapply")
print(orgCategoryResponse.text + "\n")
orgCategoryResponse = requests.get("https://data.usajobs.gov/api/codelist/hiringpaths")
print(orgCategoryResponse.text + "\n")

usaJobsURL = "https://data.usajobs.gov/api/search?JobCategoryCode=0340&HiringPath=PUBLIC"

response = requests.get(usaJobsURL, headers=usaJobsParams)

outputJson = json.dumps(response.json())

with open("C:\\Users\\josep\\Desktop\\SampleResult.json", "w") as outputFile:
    outputFile.write(outputJson)
# print(response.text)

# print(response.json())

usaJobsResponseDict = response.json()
usaJobsParsed = "Federal Government,"

for i in range(len(usaJobsResponseDict["SearchResult"]["SearchResultItems"])):
    usaJobsParsed += usaJobsResponseDict["SearchResult"]["SearchResultItems"][i]["MatchedObjectDescriptor"]["PositionTitle"]
    usaJobsParsed += "," + usaJobsResponseDict["SearchResult"]["SearchResultItems"][i]["MatchedObjectDescriptor"]["PositionRemuneration"][0]["MinimumRange"]
    usaJobsParsed += " - " + usaJobsResponseDict["SearchResult"]["SearchResultItems"][i]["MatchedObjectDescriptor"]["PositionRemuneration"][0]["MaximumRange"]
    usaJobsParsed += "," + usaJobsResponseDict["SearchResult"]["SearchResultItems"][i]["MatchedObjectDescriptor"]["PositionURI"]
    print(usaJobsParsed)
    usaJobsParsed += "\nFederal Government,"

with open("C:\\Users\\josep\\Desktop\\JobUpload.csv", "a") as outputFile:
    outputFile.write(usaJobsParsed)

print("\nDone!")
