#!/usr/bin/env python

import json
import re
from datetime import datetime
from difflib import SequenceMatcher

def main():
    logData = json.loads(open("2016-MOOC-logdata.json","r").read())
    tutorialsData = json.loads(open("tutorialHelpText.json", "r").read())
    data = []
    for userData in logData["420"]:
        if findSimilar(userData, tutorialsData) != None:
            userData["exercise"] = tutorialsData[findSimilar(userData,tutorialsData)]
            data.append(userData)
    data.sort(key=lambda x: datetime.strptime(x["timestamp"],"%Y-%m-%dT%H:%M:%S.%f%z"))
    return data

def findSimilar(userInput, helpData):
    helpList = list(helpData.keys())
    userInput = re.sub("let {.*} in ", "", userInput["input"])
    maxInd = []
    for text in helpList:
        maxInd.append(SequenceMatcher(None, userInput, text).ratio())
    if max(maxInd) >= 0.6:
        return helpList[maxInd.index(max(maxInd))]

if __name__ == "__main__":
    main()
